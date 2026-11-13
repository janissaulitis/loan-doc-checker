"""Checks a bank statement against a loan application.

The AI model only READS the statement: it turns the PDF into the holder's name, the period and a list of
transactions, each with a category. Every DECISION is made by fixed code below, so the same statement always gets
the same verdict, and every finding can be traced to the transactions behind it.
"""
from __future__ import annotations

import json
import re
import statistics
import time
import unicodedata
from collections import defaultdict
from datetime import date, timedelta

CATEGORIES = {
    "salary": "Salary or wages from an employer",
    "other_income": "Other regular income: client payments for the self-employed, pension, benefits",
    "loan_repayment": "Payment to a lender: loan, credit, instalment",
    "gambling_out": "Payment to a casino, betting or gambling site",
    "gambling_in": "Winnings paid out by a casino or betting site",
    "returned_payment": "Direct debit or payment returned / refused for lack of funds",
    "bank_fee": "Bank fee or penalty",
    "rent": "Rent or mortgage", "utilities": "Electricity, gas, water, phone, internet",
    "groceries": "Food and everyday shopping", "transport": "Transport and fuel", "cash": "Cash withdrawal",
    "transfer": "Transfer between own accounts or to a person", "other": "Anything else",
}

SYSTEM = f"""You read bank statements for a lender's underwriting team. The statement can be in any language.
Return JSON only, following the schema. Read every page and every transaction row; do not skip or merge rows.
- holder: the account holder's full name exactly as printed.
- bank, currency (ISO code), period_start and period_end (YYYY-MM-DD) as printed on the statement.
- transactions: every row except the opening balance, with date (YYYY-MM-DD), description as printed, amount as a
  number (negative for money out, positive for money in, 0 if the row shows no amount) and one category:
{chr(10).join(f"  - {k}: {v}" for k, v in CATEGORIES.items())}
A payment that went to a lender is loan_repayment even if the lender's name is unfamiliar. A row saying a payment was
returned or refused for lack of funds is returned_payment. Do not judge or summarise the customer; just read."""

SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "holder": {"type": "STRING"}, "bank": {"type": "STRING"}, "currency": {"type": "STRING"},
        "period_start": {"type": "STRING"}, "period_end": {"type": "STRING"},
        "transactions": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {
            "date": {"type": "STRING"}, "description": {"type": "STRING"}, "amount": {"type": "NUMBER"},
            "category": {"type": "STRING", "enum": list(CATEGORIES)}},
            "required": ["date", "description", "amount", "category"]}},
    },
    "required": ["holder", "bank", "currency", "period_start", "period_end", "transactions"],
}
PROMPT_VERSION = "v1"


class AIError(RuntimeError):
    pass


# ---------------------------------------------------------------- AI reading (Google Gemini)

def pick_models(api_key: str, preferred: str = "") -> list[str]:
    from google import genai
    names = [m.name.removeprefix("models/") for m in genai.Client(api_key=api_key).models.list()
             if "generateContent" in (getattr(m, "supported_actions", None) or [])]
    skip = ("lite", "image", "tts", "audio", "live", "embedding", "thinking", "exp", "learnlm", "8b")
    flash = [n for n in names if "flash" in n and not any(x in n for x in skip)]
    if not flash:
        raise AIError(f"No Flash model available for this key. Models found: {', '.join(names[:15])}")

    def rank(n):
        ver = re.findall(r"gemini-(\d+(?:\.\d+)?)", n)
        return ("preview" not in n, float(ver[0]) if ver else 0, n.endswith("latest"), -len(n))

    ranked = sorted(flash, key=rank, reverse=True)[:4]
    if preferred and preferred in names:
        ranked = [preferred] + [m for m in ranked if m != preferred]
    return ranked


def read_statement(pdf: bytes, api_key: str, models: list[str], on_wait=None) -> tuple[dict, str]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    models = list(models)
    think_off = True
    for attempt in range(6):
        model = models[0]
        try:
            cfg = dict(system_instruction=SYSTEM, response_mime_type="application/json", response_schema=SCHEMA,
                       temperature=0)
            if think_off:
                cfg["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
            resp = client.models.generate_content(
                model=model,
                contents=[types.Part.from_bytes(data=pdf, mime_type="application/pdf"), "Read this bank statement."],
                config=types.GenerateContentConfig(**cfg))
            return json.loads(resp.text), getattr(resp, "model_version", None) or model
        except Exception as e:
            msg = str(e)
            if think_off and "thinking" in msg.lower():
                think_off = False
                continue
            busy = "503" in msg or "UNAVAILABLE" in msg or "overloaded" in msg
            limited = "429" in msg or "RESOURCE_EXHAUSTED" in msg
            if (busy or (limited and (attempt >= 1 or "PerDay" in msg))) and len(models) > 1:
                models.pop(0)
                if on_wait:
                    on_wait(f"model busy, switching to {models[0]}", attempt + 1, 0)
                continue
            if attempt == 5 or "PerDay" in msg or "404" in msg or "API_KEY" in msg or "PERMISSION" in msg:
                raise AIError(msg[:600]) from e
            wait = (20 if limited else 3) * (attempt + 1) / 2
            if on_wait:
                on_wait("rate limit" if limited else msg[:100], attempt + 1, wait)
            time.sleep(wait)
    raise AIError("The AI did not answer after several tries.")


# ---------------------------------------------------------------- the checks (fixed code, no AI)

def _fold(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c))
    return " ".join(sorted(re.sub(r"[^a-z ]", " ", s.lower()).split()))


def _d(s: str) -> date | None:
    try:
        return date.fromisoformat(str(s)[:10])
    except ValueError:
        return None


def _lender(desc: str) -> str:
    """Short lender name from a payment description, so several payments to one lender count once."""
    words = re.sub(r"[^\w\s]", " ", desc).split()
    keep = []
    for w in words:
        keep.append(w)
        if w.upper() in ("SIA", "UAB", "SL", "SA", "SRL", "LTD", "OY", "AS") or len(keep) == 2:
            break
    return " ".join(keep)


def check(statement: dict, application: dict) -> dict:
    """statement: what the AI read. application: what the customer wrote. Returns verdict, findings and the numbers."""
    tx = [t for t in statement.get("transactions", []) if _d(t.get("date"))]
    cur = statement.get("currency", "")
    applied = _d(application.get("applied_on")) or date.today()
    findings = []  # (severity, code, title, detail)

    # identity
    if _fold(statement.get("holder", "")) != _fold(application["name"]):
        findings.append(("mismatch", "name_mismatch", "Name doesn't match",
                         f"Statement is for {statement.get('holder', '?')}, the application is from {application['name']}."))

    # recency
    end = _d(statement.get("period_end")) or max((_d(t["date"]) for t in tx), default=None)
    if end and (applied - end).days > 45:
        findings.append(("mismatch", "statement_old", "Statement is too old",
                         f"It ends on {end:%d.%m.%Y}, {(applied - end).days} days before the application. "
                         "Ask for one from the last month."))

    # income: the typical month (median), so a one-off bonus or a missing month doesn't distort it
    monthly = defaultdict(float)
    months = sorted({(_d(t["date"]).year, _d(t["date"]).month) for t in tx})
    for t in tx:
        if t["category"] in ("salary", "other_income") and t["amount"] > 0:
            dt = _d(t["date"])
            monthly[(dt.year, dt.month)] += t["amount"]
    per_month = [monthly.get(m, 0.0) for m in months]
    typical = statistics.median(per_month) if per_month else 0.0
    stated = float(application["monthly_net_income"])
    if stated > 0 and typical >= 0:
        gap = (typical - stated) / stated
        if gap < -0.20:
            findings.append(("mismatch", "income_lower", "Income is lower than stated",
                             f"Statement shows about {typical:,.0f} {cur} a month; the application says {stated:,.0f} {cur} "
                             f"({gap:+.0%})."))
        elif gap < -0.10:
            findings.append(("review", "income_lower", "Income a little lower than stated",
                             f"About {typical:,.0f} {cur} a month against {stated:,.0f} {cur} stated ({gap:+.0%})."))
    if len(per_month) >= 2 and per_month[-1] == 0 and max(per_month[:-1]) > 0:
        findings.append(("review", "income_stopped", "No income in the latest month",
                         "Salary arrived in earlier months but not in the most recent one. Ask whether the job continues."))

    # loans the customer didn't declare
    loans = defaultdict(float)
    for t in tx:
        if t["category"] == "loan_repayment" and t["amount"] < 0:
            loans[_lender(t["description"])] += -t["amount"]
    n_months = max(1, len(months))
    loan_monthly = sum(loans.values()) / n_months
    declared = float(application.get("declared_loan_payments") or 0)
    if loan_monthly - declared > 20:
        names = ", ".join(sorted(loans))
        findings.append(("review", "undeclared_loan", "Loan payments not declared",
                         f"Pays about {loan_monthly:,.0f} {cur} a month to {len(loans)} lender(s) ({names}); "
                         f"declared {declared:,.0f} {cur}."))

    # gambling
    gamb = [t for t in tx if t["category"] == "gambling_out" and t["amount"] < 0]
    gamb_monthly = -sum(t["amount"] for t in gamb) / n_months
    if len(gamb) >= 3 or (typical and gamb_monthly > 0.05 * typical):
        findings.append(("review", "gambling", "Regular gambling payments",
                         f"{len(gamb)} payments to gambling sites, about {gamb_monthly:,.0f} {cur} a month."))

    # bounced payments
    bounced = [t for t in tx if t["category"] == "returned_payment"]
    if bounced:
        findings.append(("review", "bounced_payments", "Payments bounced",
                         f"{len(bounced)} payment(s) returned for lack of funds."))

    verdict = ("mismatch" if any(f[0] == "mismatch" for f in findings)
               else "review" if findings else "consistent")
    return {
        "verdict": verdict,
        "findings": [{"severity": s, "code": c, "title": t, "detail": d} for s, c, t, d in findings],
        "numbers": {"currency": cur, "typical_monthly_income": typical, "stated_income": stated,
                    "income_by_month": {f"{y}-{m:02d}": round(monthly.get((y, m), 0.0), 2) for y, m in months},
                    "loan_payments_monthly": loan_monthly, "lenders": sorted(loans),
                    "gambling_monthly": gamb_monthly, "bounced": len(bounced),
                    "transactions": len(tx), "period_end": str(end) if end else ""},
    }


# ---------------------------------------------------------------- scoring against the labelled cases

def score(cases: list[dict], results: dict[str, dict]) -> dict:
    rows = []
    for c in cases:
        r = results.get(c["id"])
        if not r:
            continue
        got = {f["code"] for f in r["findings"]}
        exp = set(c["expected"]["issues"])
        rows.append({"id": c["id"], "language": c["language"], "note": c["note"],
                     "expected": c["expected"]["verdict"], "got": r["verdict"],
                     "verdict_ok": r["verdict"] == c["expected"]["verdict"],
                     "issues_ok": got == exp, "missed": sorted(exp - got), "extra": sorted(got - exp),
                     # the costly error: a problem statement that would have passed as "consistent"
                     "missed_problem": c["expected"]["verdict"] != "consistent" and r["verdict"] == "consistent"})
    n = len(rows) or 1
    return {"n": len(rows), "verdict": sum(r["verdict_ok"] for r in rows) / n,
            "issues": sum(r["issues_ok"] for r in rows) / n,
            "missed_problems": sum(r["missed_problem"] for r in rows), "rows": rows}


def from_truth(case: dict) -> dict:
    """Builds what a perfect reader would extract, using simple keyword rules on the known transactions.
    Used to test the checks themselves without the AI, and as an offline fallback."""
    rules = [("loan_repayment", r"kred|aizdev|credit|loan|pożycz"), ("gambling_in", r"casino.*(izmaksa|payout|win)"),
             ("gambling_out", r"casino|bet|spin"), ("returned_payment", r"zwrócon|returned|brak środków"),
             ("bank_fee", r"opłata|fee|komisija"), ("salary", r"alga|užmokest|wynagrodz|nómina|salariu|salary"),
             ("other_income", r"cliente|factura"), ("rent", r"īre|nuoma|czynsz|alquiler|chirie|rent"),
             ("cash", r"skaidr|grynųjų|bankomat|cajero|numerar")]
    tx = []
    for t in case["truth"]["transactions"]:
        cat = next((c for c, rx in rules if re.search(rx, t["description"], re.I)), "other")
        tx.append({**t, "category": cat})
    return {"holder": case["truth"]["holder"], "bank": "", "currency": case["currency"],
            "period_start": tx[0]["date"] if tx else "", "period_end": case["truth"]["period_end"], "transactions": tx}
