"""Statement Check: a bank statement against the loan application. Run: streamlit run app.py"""
import datetime as dt
import html
import importlib
import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st

import checker as C
import kit

C = importlib.reload(C)  # Streamlit Cloud keeps old copies of imported files after an update; always use the latest
kit = importlib.reload(kit)

kit.page("Statement Check", "Reads a bank statement and checks it against the loan application", mark="doc-check", icon="🧾",
         meta="For a lender's underwriting team · runs on Google Gemini")

HERE = Path(__file__).parent
CASES = json.loads((HERE / "data" / "cases.json").read_text(encoding="utf-8"))
SAVED = HERE / "data" / "verified" / "test.json"
LOOK = {"consistent": ("✅", "Consistent with the application", "success"),
        "review": ("🟠", "Needs a look", "warning"),
        "mismatch": ("⛔", "Doesn't match the application", "error")}
FLAG = {"lv": "🇱🇻", "lt": "🇱🇹", "pl": "🇵🇱", "es": "🇪🇸", "ro": "🇷🇴"}
COUNTRY = {"lv": "Latvia", "lt": "Lithuania", "pl": "Poland", "es": "Spain", "ro": "Romania"}
CHECKS = [("name_mismatch", "Name matches the applicant"), ("statement_old", "Statement is recent"),
          ("income_lower", "Income matches what was stated"), ("income_stopped", "Income still coming in"),
          ("undeclared_loan", "All loans declared"), ("gambling", "No regular gambling"),
          ("bounced_payments", "No bounced payments")]
VERDICT = {"consistent": ("good", "Consistent"), "review": ("warn", "Needs a look"), "mismatch": ("bad", "Doesn't match")}


def secret(name, default=""):
    try:
        return st.secrets.get(name) or os.environ.get(name, default)
    except Exception:
        return os.environ.get(name, default)


API_KEY = secret("GEMINI_API_KEY")


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def models():
    return C.pick_models(API_KEY, secret("GEMINI_MODEL"))


@st.cache_data(show_spinner=False, max_entries=100, ttl=60 * 60 * 24 * 7)
def read_pdf(pdf: bytes, version: str):
    """Cached for everyone: the same PDF is only sent to the AI once a week."""
    try:
        ms = models()
    except C.AIError:
        raise
    except Exception as e:
        raise C.AIError(str(e)) from e
    note = st.empty()
    out = C.read_statement(pdf, API_KEY, ms,
                           on_wait=lambda why, k, w: note.caption(f"Waiting {w:.0f} s ({why}), attempt {k} of 6…"))
    note.empty()
    return out


def saved():
    try:
        return json.loads(SAVED.read_text(encoding="utf-8"))
    except Exception:
        return None


def error_text(e):
    msg = str(e)
    if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
        return "Today's free AI requests are used up. They reset every morning."
    return f"The AI service did not answer: {msg[:300]}"


def show_result(result: dict, statement: dict, application: dict, pdf: bytes | None, source: str):
    icon, title, kind = LOOK[result["verdict"]]
    n = result["numbers"]
    tone = {"consistent": "good", "review": "warn", "mismatch": "bad"}[result["verdict"]]
    if result["findings"]:
        body = "<br>".join(f"<b>{html.escape(f['title'])}.</b> {html.escape(f['detail'])}" for f in result["findings"])
    else:
        body = (f"Income of about <b>{n['typical_monthly_income']:,.0f} {n['currency']}</b> a month matches the "
                f"{n['stated_income']:,.0f} stated. Name, date and payments raise no questions.")
    kit.answer({"good": "Looks right", "warn": "Check before deciding", "bad": "Stop here"}[tone], title,
               body + "<br><br>A person makes the decision. This check tells them where to look.",
               [("Typical monthly income", f"{n['typical_monthly_income']:,.0f} {n['currency']}"),
                ("Loan payments a month", f"{n['loan_payments_monthly']:,.0f} {n['currency']}"),
                ("Transactions read", str(n["transactions"]))], tone=tone)
    found = {f["code"]: f for f in result["findings"]}
    st.markdown("#### The 7 checks")
    kit.table([{"c": label, "r": {"mismatch": "Fails", "review": "Look at this"}.get(found[code]["severity"]) if code in found
                else "Passed", "d": found[code]["detail"] if code in found else "Nothing to flag"} for code, label in CHECKS],
              [kit.col("Check", "c", "strong"), kit.col("Result", "r", "chip", {"Passed": "good", "Look at this": "warn", "Fails": "bad"}),
               kit.col("What it found", "d", "muted")])
    with st.expander("Show what the AI read"):
        st.markdown("**Income by month**")
        kit.columns_chart([(dt.date.fromisoformat(k + "-01").strftime("%b %Y"), v, f"{v:,.0f}")
                           for k, v in n["income_by_month"].items()])
        st.markdown(f"<p class='k-row-sub' style='margin-top:14px'>{html.escape(str(statement.get('holder')))} · "
                    f"{html.escape(str(statement.get('bank')))} · {statement.get('period_start')} – {statement.get('period_end')}</p>",
                    unsafe_allow_html=True)
        txs = statement.get("transactions", [])
        if txs:
            kit.table([{"d": t.get("date", ""), "t": t.get("description", ""), "c": t.get("category", ""),
                        "a": f"{float(t.get('amount') or 0):,.2f}"} for t in txs],
                      [kit.col("Date", "d", "muted"), kit.col("Description", "t", "wrap"), kit.col("Category", "c", "chip", {}),
                       kit.col(f"Amount {n['currency']}", "a", "num")], max_height=340)
        if pdf:
            st.download_button("Open the statement (PDF)", pdf, file_name="statement.pdf", mime="application/pdf")


tab_check, tab_test = st.tabs(["Check a statement", "Accuracy test (12 statements)"])

# ---------------------------------------------------------------- check one statement
with tab_check:
    labels = {f"{c['application']['name']} ({COUNTRY[c['language']]}) · states {c['application']['monthly_net_income']:,} "
              f"{c['currency']} a month": c for c in CASES}
    mode = st.segmented_control("Statement", ["Sample applications", "Upload your own"], default="Sample applications",
                                label_visibility="collapsed")
    if mode == "Upload your own":
        up = st.file_uploader("Bank statement (PDF)", type="pdf")
        a, b = st.columns(2)
        app = {"name": a.text_input("Applicant's name"),
               "monthly_net_income": a.number_input("Stated monthly net income", 0, 100_000, 1500, 50),
               "declared_loan_payments": b.number_input("Declared loan payments a month", 0, 10_000, 0, 10),
               "applied_on": dt.date.today().isoformat()}
        pdf = up.getvalue() if up else None
        st.caption("Your file is sent to Google Gemini to be read and is not stored by this app. Use invented or "
                   "anonymised statements only.")
        case = None
    else:
        pick = st.selectbox("Application", list(labels), label_visibility="collapsed")
        case = labels[pick]
        app = case["application"]
        pdf = (HERE / "data" / case["file"]).read_bytes()
    key = case["id"] if case else "upload"
    b1, b2 = st.columns([1, 3])
    if b1.button("▶  Check the statement", type="primary", disabled=not pdf or not app["name"]):
        st.session_state.go = (key, "saved" if case else "live")
    if case and API_KEY and b2.button("Read it live with AI (about 20 s)"):
        st.session_state.go = (key, "live")
    go = st.session_state.get("go") or (None, None)
    if go[0] == key:
        statement, source = None, ""
        if go[1] == "live" and API_KEY:
            try:
                import time as _t
                t0 = _t.time()
                with st.spinner("The AI is reading the statement…"):
                    statement, used = read_pdf(pdf, C.PROMPT_VERSION)
                source = f"Read live by {used} in {_t.time() - t0:.0f} s. The checks are fixed rules (checker.py), not AI."
            except C.AIError as e:
                st.warning(error_text(e) + " Showing the saved reading instead.")
        if statement is None and case:
            sv = saved()
            if sv and case["id"] in sv["statements"]:
                statement = sv["statements"][case["id"]]
                source = (f"Instant result from the AI's verified reading on {sv['date']} ({sv['model']}). "
                          "The checks are fixed rules (checker.py), not AI.")
            else:
                statement = C.from_truth(case)
                source = "Uses the statement's known contents. The checks are fixed rules (checker.py), not AI."
        if statement:
            show_result(C.check(statement, app), statement, app, pdf, source)
            st.caption(source)
        elif not case:
            st.info("Uploads need the AI to read them. Try again when the AI is available.")

# ---------------------------------------------------------------- accuracy test
with tab_test:
    st.markdown("**12 invented statements in 5 languages, each with the answer a careful underwriter would give.** "
                "They include the cases that catch people out: salary paid in two parts, a one-off bonus, "
                "irregular self-employed income, a similar but different name, three small lenders.")
    with st.expander("See the 12 cases and the expected answers"):
        kit.table([{"id": c["id"], "l": c["language"], "a": c["application"]["name"], "e": VERDICT[c["expected"]["verdict"]][1],
                    "w": c["note"]} for c in CASES],
                  [kit.col("Case", "id", "muted"), kit.col("", "l", "lang"), kit.col("Applicant", "a", "strong"),
                   kit.col("Expected", "e", "chip", {v[1]: v[0] for v in VERDICT.values()}), kit.col("Why it's tricky", "w", "wrap")])
    sv = saved()
    run = st.button("▶  Run it live" if sv else "▶  Run the test", type="primary", disabled=not API_KEY)
    readings, label = None, ""
    if run:
        readings, used = {}, ""
        bar = st.progress(0.0, "Reading statements…")
        try:
            for i, c in enumerate(CASES):
                readings[c["id"]], used = read_pdf((HERE / "data" / c["file"]).read_bytes(), C.PROMPT_VERSION)
                bar.progress((i + 1) / len(CASES), f"Read {i + 1} of {len(CASES)}")
            label = f"Live run · {used} · prompt {C.PROMPT_VERSION}"
            st.download_button("Download this run (JSON)", json.dumps(
                {"date": dt.date.today().isoformat(), "model": used, "prompt": C.PROMPT_VERSION, "statements": readings},
                ensure_ascii=False), file_name="test.json", mime="application/json")
        except C.AIError as e:
            st.error(error_text(e))
            readings = None
    if readings is None and sv:
        readings, label = sv["statements"], f"Saved verified run from {sv['date']} · {sv['model']} · prompt {sv['prompt']}"
    if readings:
        results = {c["id"]: C.check(readings[c["id"]], c["application"]) for c in CASES if c["id"] in readings}
        s = C.score(CASES, results)
        ok = sum(r["verdict_ok"] and r["issues_ok"] for r in s["rows"])
        kit.answer("Accuracy test", f"{ok} of {len(s['rows'])} statements got the right verdict and the right reasons",
                   f"Problems missed: <b>{s['missed_problems']}</b>. " + ("No problem statement passed as consistent."
                   if s["missed_problems"] == 0 else "Some problem statements would have passed as consistent."),
                   [("Right verdict", f"{s['verdict']:.0%}"), ("Right reasons", f"{s['issues']:.0%}"),
                    ("Problems missed", str(s["missed_problems"]))], tone="good" if s["missed_problems"] == 0 else "bad")
        kit.table([{"id": r["id"], "l": r["language"], "e": VERDICT[r["expected"]][1], "g": VERDICT[r["got"]][1],
                    "ok": "Right" if r["verdict_ok"] and r["issues_ok"] else "Differs",
                    "n": r["note"] + (f" · missed {', '.join(r['missed'])}" if r["missed"] else "")
                    + (f" · extra {', '.join(r['extra'])}" if r["extra"] else "")} for r in s["rows"]],
                  [kit.col("Case", "id", "muted"), kit.col("", "l", "lang"),
                   kit.col("Expected", "e", "chip", {v[1]: v[0] for v in VERDICT.values()}),
                   kit.col("Got", "g", "chip", {v[1]: v[0] for v in VERDICT.values()}),
                   kit.col("", "ok", "chip", {"Right": "good", "Differs": "warn"}), kit.col("Case notes", "n", "wrap")])
        st.caption(label)
    elif not API_KEY:
        st.info("No AI key set on this copy, so the live test can't run.")

kit.footer("Google Gemini reads · checker.py decides")
