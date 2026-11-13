"""Generates invented bank statements (PDF) plus the matching loan applications and the answer a careful
underwriter would give. Banks, people, employers, lenders and casinos are all fictional.

Each case tests one thing an underwriter checks when reading a statement against an application:
income, identity, how recent the statement is, undeclared loans, gambling, bounced payments, income that stopped.
Some are deliberately tricky: salary paid in two parts, a one-off bonus, irregular self-employed income.
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

HERE = Path(__file__).parent
OUT = HERE / "statements"
OUT.mkdir(exist_ok=True)

for name, file in [("DV", "DejaVuSans.ttf"), ("DVB", "DejaVuSans-Bold.ttf")]:
    for d in ["/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/dejavu/"]:
        if Path(d + file).exists():
            pdfmetrics.registerFont(TTFont(name, d + file))
            break

APPLIED = date(2026, 10, 20)  # date of every application in the test set

# Language packs for the statement layout
L = {
    "lv": dict(title="Konta izraksts", holder="Konta turētājs", period="Periods", date="Datums", desc="Apraksts",
               amount="Summa", balance="Atlikums", opening="Sākuma atlikums", salary="Alga", rent="Īre",
               groceries=["Rimi", "Maxima", "Lidl"], transport="Rīgas Satiksme e-talons", utilities="Elektrum rēķins",
               cash="Skaidras naudas izņemšana"),
    "lt": dict(title="Sąskaitos išrašas", holder="Sąskaitos savininkas", period="Laikotarpis", date="Data",
               desc="Aprašymas", amount="Suma", balance="Likutis", opening="Pradinis likutis", salary="Darbo užmokestis",
               rent="Nuoma", groceries=["Iki", "Maxima", "Norfa"], transport="Vilniaus viešasis transportas",
               utilities="Ignitis sąskaita", cash="Grynųjų išėmimas"),
    "pl": dict(title="Wyciąg z rachunku", holder="Właściciel rachunku", period="Okres", date="Data", desc="Opis",
               amount="Kwota", balance="Saldo", opening="Saldo początkowe", salary="Wynagrodzenie", rent="Czynsz",
               groceries=["Biedronka", "Lidl", "Żabka"], transport="Bilet miesięczny ZTM", utilities="Tauron rachunek",
               cash="Wypłata z bankomatu"),
    "es": dict(title="Extracto de cuenta", holder="Titular", period="Periodo", date="Fecha", desc="Concepto",
               amount="Importe", balance="Saldo", opening="Saldo inicial", salary="Nómina", rent="Alquiler",
               groceries=["Mercadona", "Carrefour", "Dia"], transport="Abono transporte", utilities="Iberdrola recibo",
               cash="Retirada cajero"),
    "ro": dict(title="Extras de cont", holder="Titular cont", period="Perioada", date="Data", desc="Descriere",
               amount="Suma", balance="Sold", opening="Sold inițial", salary="Salariu", rent="Chirie",
               groceries=["Kaufland", "Lidl", "Mega Image"], transport="Abonament STB", utilities="Enel factură",
               cash="Retragere numerar"),
}

CASES = [
    dict(id="S01", lang="lv", bank="Daugava Bank", cur="EUR", holder="Līga Bērziņa", applicant="Līga Bērziņa",
         stated=1300, declared_loans=0, employer="SIA Baltic Logistics", salary=[1320, 1320, 1320],
         verdict="consistent", issues=[], note="clean case"),
    dict(id="S02", lang="pl", bank="Vistula Bank", cur="PLN", holder="Marek Nowicki", applicant="Marek Nowicki",
         stated=6500, declared_loans=0, employer="TransPol Sp. z o.o.", salary=[4200, 4200, 4250],
         verdict="mismatch", issues=["income_lower"], note="stated income about 55% higher than the salary"),
    dict(id="S03", lang="es", bank="Banco Meseta", cur="EUR", holder="Lucía Romero García", applicant="Lucía Romero García",
         stated=1450, declared_loans=0, employer="Hostelería Sur SL", salary=[(1000, 450), (1000, 450), (1000, 450)],
         verdict="consistent", issues=[], note="salary paid in two parts each month"),
    dict(id="S04", lang="lt", bank="Nemunas Bank", cur="EUR", holder="Tomas Petraitis", applicant="Tomas Petrauskas",
         stated=1500, declared_loans=0, employer="UAB Kauno Statyba", salary=[1510, 1510, 1510],
         verdict="mismatch", issues=["name_mismatch"], note="statement belongs to a different person (similar name)"),
    dict(id="S05", lang="ro", bank="Banca Carpați", cur="RON", holder="Andrei Popescu", applicant="Andrei Popescu",
         stated=5200, declared_loans=0, employer="SC Delta Distribuție SRL", salary=[5200, 5200, 5200], months_back=8,
         verdict="mismatch", issues=["statement_old"], note="statement ended about five months before the application"),
    dict(id="S06", lang="lv", bank="Daugava Bank", cur="EUR", holder="Kristaps Ozols", applicant="Kristaps Ozols",
         stated=1600, declared_loans=0, employer="SIA Vidzemes Mežs", salary=[1610, 1610, 1610],
         loans=[("ZibensKredīts SIA aizdevuma maksājums", 145)],
         verdict="review", issues=["undeclared_loan"], note="pays another lender every month, declared no loans"),
    dict(id="S07", lang="lv", bank="Daugava Bank", cur="EUR", holder="Edgars Kalniņš", applicant="Edgars Kalniņš",
         stated=1400, declared_loans=0, employer="SIA Rīgas Auto", salary=[1400, 1400, 1400], gambling=True,
         verdict="review", issues=["gambling"], note="frequent payments to an online casino"),
    dict(id="S08", lang="pl", bank="Vistula Bank", cur="PLN", holder="Anna Wiśniewska", applicant="Anna Wiśniewska",
         stated=5100, declared_loans=0, employer="Medicus Kraków Sp. z o.o.", salary=[5100, 5100, 5100], bounced=True,
         verdict="review", issues=["bounced_payments"], note="direct debits returned for lack of funds, with fees"),
    dict(id="S09", lang="es", bank="Banco Meseta", cur="EUR", holder="Javier Ortega Ruiz", applicant="Javier Ortega Ruiz",
         stated=1800, declared_loans=0, employer=None, freelance=[[1100, 520, 310], [640, 1290], [900, 700, 280]],
         verdict="consistent", issues=[], note="self-employed: irregular client payments, average close to stated"),
    dict(id="S10", lang="lt", bank="Nemunas Bank", cur="EUR", holder="Rūta Jankauskienė", applicant="Rūta Jankauskienė",
         stated=1700, declared_loans=0, employer="UAB Vilniaus Duomenys", salary=[1700, 1700, 1700], bonus=(1, 2400),
         verdict="consistent", issues=[], note="one-off bonus in one month should not lift the income"),
    dict(id="S11", lang="ro", bank="Banca Carpați", cur="RON", holder="Elena Ionescu", applicant="Elena Ionescu",
         stated=4800, declared_loans=0, employer="SC Textil Nord SA", salary=[4800, 4800, 0],
         verdict="review", issues=["income_stopped"], note="no salary in the most recent month"),
    dict(id="S12", lang="lv", bank="Daugava Bank", cur="EUR", holder="Jānis Liepa", applicant="Jānis Liepa",
         stated=1250, declared_loans=90, employer="SIA Liepājas Osta", salary=[1250, 1250, 1250],
         loans=[("ZibensKredīts SIA aizdevuma maksājums", 90), ("NaudaTūlīt SIA kredīta atmaksa", 120),
                ("Kredītu Ātrums SIA maksājums", 75)],
         verdict="review", issues=["undeclared_loan"], note="three lenders, only one declared (90)"),
]


def month_starts(end_month: date, n: int = 3):
    y, m = end_month.year, end_month.month
    out = []
    for _ in range(n):
        out.append(date(y, m, 1))
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return list(reversed(out))


def build_transactions(c, rnd):
    lp = L[c["lang"]]
    months_back = c.get("months_back", 1)
    end = date(APPLIED.year, APPLIED.month, 1) - timedelta(days=1)  # end of the month before the application
    for _ in range(months_back - 1):
        end = date(end.year, end.month, 1) - timedelta(days=1)
    starts = month_starts(date(end.year, end.month, 1))
    tx = []
    scale = {"EUR": 1, "PLN": 4.3, "RON": 5}[c["cur"]]
    for i, ms in enumerate(starts):
        def d(day):
            return ms.replace(day=min(day, 28))
        if c.get("employer"):
            s = c["salary"][i]
            parts = s if isinstance(s, tuple) else ((s,) if s else ())
            for k, amt in enumerate(parts):
                tx.append((d(10 if k == 0 else 25), f"{lp['salary']} {c['employer']}", amt))
            if c.get("bonus") and c["bonus"][0] == i:
                tx.append((d(15), f"{lp['salary']} bonus {c['employer']}", c["bonus"][1]))
        for k, amt in enumerate(c.get("freelance", [[]] * 3)[i]):
            tx.append((d(5 + 9 * k), f"Transferencia cliente {['Estudio Nébula SL', 'Grupo Faro', 'Ana Molina'][k % 3]} factura",
                       amt))
        tx.append((d(2), f"{lp['rent']}", -round(rnd.choice([380, 420, 450]) * scale)))
        tx.append((d(4), lp["utilities"], -round(rnd.uniform(35, 70) * scale, 2)))
        tx.append((d(6), lp["transport"], -round(30 * scale, 2)))
        for _ in range(9):
            tx.append((d(rnd.randint(1, 28)), rnd.choice(lp["groceries"]), -round(rnd.uniform(8, 65) * scale, 2)))
        tx.append((d(rnd.randint(12, 20)), lp["cash"], -round(rnd.choice([50, 100]) * scale)))
        for name, amt in c.get("loans", []):
            tx.append((d(15), name, -amt))
        if c.get("gambling"):
            for _ in range(7):
                tx.append((d(rnd.randint(1, 28)), "LuckySpin Casino Ltd online", -rnd.choice([20, 25, 40, 50, 100])))
            tx.append((d(rnd.randint(1, 28)), "LuckySpin Casino Ltd izmaksa", rnd.choice([60, 90])))
        if c.get("bounced") and i > 0:
            tx.append((d(12), "Polecenie zapłaty Orange zwrócone – brak środków", 0.0))
            tx.append((d(12), "Opłata za brak środków na rachunku", -15.0))
    tx.sort(key=lambda t: t[0])
    return starts[0], date(end.year, end.month, end.day), tx


def write_pdf(c, start, end, tx, opening):
    lp = L[c["lang"]]
    doc = SimpleDocTemplate(str(OUT / f"{c['id']}.pdf"), pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm,
                            topMargin=14 * mm, bottomMargin=14 * mm,
                            title=f"{c['bank']} {lp['title']}", author=c["bank"])
    st = lambda size, bold=False, col=colors.black: ParagraphStyle("x", fontName="DVB" if bold else "DV",
                                                                   fontSize=size, leading=size * 1.3, textColor=col)
    iban = f"{c['lang'].upper()}00 DEMO {random.Random(c['id']).randint(1000, 9999)} {random.Random(c['id'] + 'x').randint(1000, 9999)} 0000"
    els = [Paragraph(c["bank"], st(16, True, colors.HexColor("#1d3557"))), Paragraph(f"{lp['title']} · DEMO", st(10)),
           Spacer(1, 6 * mm),
           Paragraph(f"<b>{lp['holder']}:</b> {c['holder']}", st(10)),
           Paragraph(f"<b>IBAN:</b> {iban}", st(10)),
           Paragraph(f"<b>{lp['period']}:</b> {start:%d.%m.%Y} – {end:%d.%m.%Y} · {c['cur']}", st(10)),
           Spacer(1, 5 * mm)]
    rows = [[lp["date"], lp["desc"], lp["amount"], lp["balance"]], ["", lp["opening"], "", f"{opening:,.2f}"]]
    bal = opening
    for dt, desc, amt in tx:
        bal += amt
        rows.append([f"{dt:%d.%m.%Y}", desc, f"{amt:+,.2f}", f"{bal:,.2f}"])
    t = Table(rows, colWidths=[24 * mm, 98 * mm, 28 * mm, 28 * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "DV", 8.5), ("FONT", (0, 0), (-1, 0), "DVB", 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")), ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#cfd6de")), ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    els.append(t)
    doc.build(els)
    return bal


def main():
    answers = []
    for c in CASES:
        rnd = random.Random(c["id"])
        start, end, tx = build_transactions(c, rnd)
        opening = round(rnd.uniform(900, 1600) * {"EUR": 1, "PLN": 4.3, "RON": 5}[c["cur"]], 2)
        write_pdf(c, start, end, tx, opening)
        answers.append({
            "id": c["id"], "file": f"statements/{c['id']}.pdf", "language": c["lang"], "currency": c["cur"],
            "application": {"name": c["applicant"], "monthly_net_income": c["stated"], "employer": c.get("employer") or "self-employed",
                            "declared_loan_payments": c["declared_loans"], "applied_on": APPLIED.isoformat()},
            "expected": {"verdict": c["verdict"], "issues": c["issues"]}, "note": c["note"],
            "truth": {"holder": c["holder"], "period_end": end.isoformat(),
                      "transactions": [{"date": d.isoformat(), "description": s, "amount": a} for d, s, a in tx]},
        })
    (HERE / "cases.json").write_text(json.dumps(answers, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(answers)} statements -> {OUT}")


if __name__ == "__main__":
    main()
