"""Statement Check: a bank statement against the loan application. Run: streamlit run app.py"""
import datetime as dt
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

kit.page("Statement Check", "Reads a bank statement and checks it against the loan application", mark="🧾",
         meta="For a lender's underwriting team · runs on Google Gemini")

HERE = Path(__file__).parent
CASES = json.loads((HERE / "data" / "cases.json").read_text(encoding="utf-8"))
SAVED = HERE / "data" / "verified" / "test.json"
LOOK = {"consistent": ("✅", "Consistent with the application", "success"),
        "review": ("🟠", "Needs a look", "warning"),
        "mismatch": ("⛔", "Doesn't match the application", "error")}
FLAG = {"lv": "🇱🇻", "lt": "🇱🇹", "pl": "🇵🇱", "es": "🇪🇸", "ro": "🇷🇴"}


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
    with st.container(border=True):
        st.markdown(f"### {icon} {title}")
        if result["findings"]:
            for f in result["findings"]:
                st.markdown(f"**{f['title']}.** {f['detail']}")
        else:
            st.markdown(f"Income of about **{n['typical_monthly_income']:,.0f} {n['currency']}** a month matches the "
                        f"{n['stated_income']:,.0f} stated. Name, date and payments raise no questions.")
        st.caption("A person makes the decision. This check tells them where to look.")
    with st.expander("Show the details"):
        a, b, c = st.columns(3)
        a.metric("Typical monthly income", f"{n['typical_monthly_income']:,.0f} {n['currency']}",
                 help="The middle month, so a one-off bonus or a missing month doesn't distort it.")
        b.metric("Loan payments a month", f"{n['loan_payments_monthly']:,.0f} {n['currency']}",
                 help=", ".join(n["lenders"]) or "none found")
        c.metric("Transactions read", n["transactions"])
        st.markdown("**Income by month**")
        st.bar_chart(pd.Series(n["income_by_month"], name=n["currency"]), color="#2fb985", height=200)
        st.markdown(f"**What the AI read:** {statement.get('holder')} · {statement.get('bank')} · "
                    f"{statement.get('period_start')} – {statement.get('period_end')}")
        tx = pd.DataFrame(statement.get("transactions", []))
        if not tx.empty:
            st.dataframe(tx, hide_index=True, width="stretch", height=280,
                         column_config={"amount": st.column_config.NumberColumn(format="%.2f")})
        if pdf:
            st.download_button("Open the statement (PDF)", pdf, file_name="statement.pdf", mime="application/pdf")
        st.caption(source)


tab_check, tab_test = st.tabs(["Check a statement", "Accuracy test (12 statements)"])

# ---------------------------------------------------------------- check one statement
with tab_check:
    labels = {f"{FLAG[c['language']]}  {c['application']['name']} · states {c['application']['monthly_net_income']:,} "
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
    if st.button("▶  Check the statement", type="primary", disabled=not pdf or not app["name"]):
        st.session_state.go = (case["id"] if case else "upload")
    if st.session_state.get("go") in ((case["id"] if case else "upload"),):
        statement, source = None, ""
        if API_KEY:
            try:
                with st.spinner("The AI is reading the statement…"):
                    statement, used = read_pdf(pdf, C.PROMPT_VERSION)
                source = f"Read by {used} · checks are fixed code (checker.py), not AI."
            except C.AIError as e:
                st.warning(error_text(e))
        if statement is None and case:
            sv = saved()
            if sv and case["id"] in sv["statements"]:
                statement = sv["statements"][case["id"]]
                source = f"Saved reading from {sv['date']} by {sv['model']}, because the AI isn't available right now."
            elif not API_KEY:
                statement = C.from_truth(case)
                source = "No AI key set: this copy uses the statement's known contents instead of an AI reading."
        if statement:
            show_result(C.check(statement, app), statement, app, pdf, source)
        elif not case:
            st.info("Uploads need the AI to read them. Try again when the AI is available.")

# ---------------------------------------------------------------- accuracy test
with tab_test:
    st.markdown("**12 invented statements in 5 languages, each with the answer a careful underwriter would give.** "
                "They include the cases that catch people out: salary paid in two parts, a one-off bonus, "
                "irregular self-employed income, a similar but different name, three small lenders.")
    with st.expander("See the 12 cases and the expected answers"):
        st.dataframe(pd.DataFrame([{"Case": c["id"], "": FLAG[c["language"]], "Applicant": c["application"]["name"],
                                    "Expected": c["expected"]["verdict"], "Why": c["note"]} for c in CASES]),
                     hide_index=True, width="stretch")
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
        m = st.columns(3)
        m[0].metric("Right verdict", f"{s['verdict']:.0%}")
        m[1].metric("Right reasons", f"{s['issues']:.0%}", help="Exactly the expected findings, no more, no fewer.")
        m[2].metric("Problems missed", s["missed_problems"], help="A problem statement marked consistent. Target: 0.")
        st.table(pd.DataFrame([{"Case": r["id"], "": FLAG[r["language"]], "Expected": r["expected"], "Got": r["got"],
                                "": "✅" if r["verdict_ok"] and r["issues_ok"] else "⚠️",
                                "Note": r["note"] + (f" · missed {r['missed']}" if r["missed"] else "")
                                + (f" · extra {r['extra']}" if r["extra"] else "")} for r in s["rows"]]).set_index("Case"))
        st.caption(label)
    elif not API_KEY:
        st.info("No AI key set on this copy, so the live test can't run.")

kit.footer("Google Gemini reads · checker.py decides")
