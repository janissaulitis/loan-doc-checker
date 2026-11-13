# Statement Check: a bank statement against the loan application

Demo for a fictional lender. An AI model (Google Gemini) reads a bank statement PDF in any language into the holder, the period and a categorised list of transactions. Fixed code (`checker.py`) then compares it with the application and gives a verdict: consistent, needs a look, or doesn't match, with the reasons.

Checks: name, how recent the statement is, typical monthly income vs stated (median month, so a bonus or a gap doesn't distort it), income that stopped, loan payments not declared, gambling, bounced payments.

- `data/make_statements.py` – 12 invented statements in Latvian, Lithuanian, Polish, Spanish and Romanian, with applications and expected answers
- `checker.py` – AI reading, the checks, scoring
- `app.py` – Streamlit app: check a statement (verdict first, details on demand), accuracy test

Set `GEMINI_API_KEY` in Streamlit secrets.
