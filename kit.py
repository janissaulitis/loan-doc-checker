"""Shared look for Jānis Saulītis' Streamlit apps: product header, answer card, fonts, colours, tabs, footer.

Usage in any app:
    import kit
    kit.page("Early Call", "Find the loans that will go late, and why", mark="📞")
    kit.answer("Worth doing", "You save about €620 a month", "Pays back in 5 months.",
               stats=[("Time freed", "60 h"), ("AI bill", "€0.47")])
    ...
    kit.footer("model.py · scikit-learn")

One design in two lighting modes, following the visitor's system setting: light is white and bank green, dark is a
deep blue-slate with a brighter green. Layout, type and spacing are identical in both; only colours change.
"""
import html

import streamlit as st

PORTFOLIO = "https://janis-saulitis-portfolio.netlify.app"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --k-bg: #f5f6f8; --k-surface: #ffffff; --k-line: #e4e7ec; --k-ink: #101828; --k-muted: #5b6474;
  --k-go: #127a5b; --k-go-ink: #ffffff; --k-go-soft: #e7f4ee;
  --k-card: #127a5b; --k-card-ink: #ffffff; --k-card-muted: #cfebdd; --k-card-line: transparent; --k-tile: rgba(255,255,255,.13);
  --k-warn: #fff4db; --k-warn-ink: #8a5a00; --k-bad: #fdecec; --k-bad-ink: #b42318;
  --k-hi: #8a5a00; --k-hi-bg: #fff4d6; --k-risk: #b42318;
}
@media (prefers-color-scheme: dark) {
  :root {
    --k-bg: #0f1720; --k-surface: #16212c; --k-line: #24313e; --k-ink: #e6edf3; --k-muted: #8b9aab;
    --k-go: #3dd39b; --k-go-ink: #0f1720; --k-go-soft: #133229;
    --k-card: #123528; --k-card-ink: #e6edf3; --k-card-muted: #9fd9bf; --k-card-line: #1e4d3b; --k-tile: rgba(255,255,255,.06);
    --k-warn: #2a2412; --k-warn-ink: #f5b83d; --k-bad: #2c1517; --k-bad-ink: #f0686c;
    --k-hi: #f5b83d; --k-hi-bg: #2a2412; --k-risk: #f0686c;
  }
}

.stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp td, .stApp th, .stApp select,
.stApp button p, .stApp [data-testid="stTab"] p, .stApp .stCaption, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
  font-family: 'Manrope', system-ui, sans-serif;
}
.stApp { font-variant-numeric: tabular-nums; }
[data-testid="stAppViewContainer"], [data-testid="stHeader"] { background: var(--k-bg); }
.block-container { max-width: 1160px; padding-top: 3.2rem; padding-bottom: 3rem; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { font-weight: 800; letter-spacing: -.01em; }

/* developer chrome off; keep the ⋮ menu (theme switch) */
[data-testid="stToolbarActions"], [data-testid="stAppDeployButton"], [data-testid="stDecoration"],
#MainMenu + div, footer, .stDeployButton { display: none !important; }

/* product header: a quiet top bar, the answer gets the attention */
.k-head { display: flex; align-items: center; justify-content: space-between; gap: 14px; flex-wrap: wrap;
  padding: 2px 0 16px; margin-bottom: 20px; border-bottom: 1px solid var(--k-line); }
.k-brand { display: flex; align-items: center; gap: 12px; min-width: 0; }
.k-mark { width: 40px; height: 40px; flex: none; display: grid; place-items: center; font-size: 19px;
  border-radius: 50%; background: var(--k-go); color: var(--k-go-ink); }
.stApp .k-name { font: 800 21px/1.15 'Manrope', sans-serif; letter-spacing: -.01em; color: var(--k-ink); margin: 0; }
.k-tag { color: var(--k-muted); font-size: 14.5px; margin-top: 2px; }
.k-meta { color: var(--k-muted); font-size: 13px; text-align: right; line-height: 1.6; }
.k-demo { display: inline-block; padding: 3px 11px; border-radius: 999px; background: var(--k-go-soft); color: var(--k-go);
  font-size: 12.5px; font-weight: 700; }

/* the answer card */
.k-ans { background: var(--k-card); color: var(--k-card-ink); border: 1px solid var(--k-card-line); border-radius: 20px;
  padding: 26px 28px; margin: 0 0 18px; }
.k-ans.warn { background: var(--k-warn); color: var(--k-ink); border-color: transparent; }
.k-ans.bad { background: var(--k-bad); color: var(--k-ink); border-color: transparent; }
.k-ans .k-kick { font-size: 14.5px; font-weight: 700; color: var(--k-card-muted); margin-bottom: 8px; }
.k-ans.warn .k-kick { color: var(--k-warn-ink); } .k-ans.bad .k-kick { color: var(--k-bad-ink); }
.stApp .k-ans .k-h { font: 800 34px/1.15 'Manrope', sans-serif; letter-spacing: -.02em; margin: 0; color: inherit; }
.k-ans .k-body { font-size: 16px; line-height: 1.6; margin-top: 10px; max-width: 62ch; opacity: .92; }
.k-ans .k-body b { font-weight: 800; }
.k-tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(92px, 1fr)); gap: 10px; margin-top: 18px; }
.k-tile { background: var(--k-tile); border-radius: 14px; padding: 12px 14px; }
.k-ans.warn .k-tile, .k-ans.bad .k-tile { background: var(--k-surface); }
.k-tile span { display: block; font-size: 12.5px; color: var(--k-card-muted); }
.k-ans.warn .k-tile span, .k-ans.bad .k-tile span { color: var(--k-muted); }
.k-tile b { display: block; font-size: 22px; font-weight: 800; margin-top: 2px; }

/* numbers outside the card */
[data-testid="stMetric"] { background: var(--k-surface); border: 1px solid var(--k-line); border-radius: 14px; padding: 12px 14px; }
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * { font: 800 28px/1.1 'Manrope', sans-serif !important; }
[data-testid="stMetricLabel"] p { color: var(--k-muted); font-size: 13px; }

/* cards and panels */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) { border-radius: 18px; background: var(--k-surface); border-color: var(--k-line) !important; }
div[data-testid="stExpander"] details { border-radius: 14px; border-color: var(--k-line); background: var(--k-surface); }

/* tabs as a segmented control */
.stTabs [role="tablist"] { gap: 4px; background: var(--k-surface); border: 1px solid var(--k-line) !important;
  border-radius: 12px; padding: 4px; width: fit-content; max-width: 100%; overflow-x: auto; box-shadow: none; }
.stTabs [role="tablist"]::after, .stTabs [role="tablist"]::before { display: none !important; }
.stTabs [data-testid="stTab"] { border-radius: 9px; padding: 7px 14px; white-space: nowrap; border: 0 !important; }
.stTabs [data-testid="stTab"] p { font-weight: 600; }
.stTabs [data-testid="stTab"][aria-selected="true"] { background: var(--k-go); }
.stTabs [data-testid="stTab"][aria-selected="true"] p { color: var(--k-go-ink) !important; font-weight: 700; }
.stTabs [data-testid="stTab"]:focus-visible { outline: 2px solid var(--k-go); outline-offset: 2px; }

/* buttons and inputs */
.stButton button, .stDownloadButton button, [data-testid="stPopover"] button { border-radius: 12px; font-weight: 700; min-height: 44px; }
.stButton button[kind="primary"], .stDownloadButton button[kind="primary"] { color: var(--k-go-ink); }
.stApp [data-baseweb="input"], .stApp [data-baseweb="select"] > div, .stApp [data-baseweb="textarea"] { border-radius: 10px; }

/* inline code = highlighted example values */
code { color: var(--k-hi) !important; background: var(--k-hi-bg) !important; border-radius: 6px; padding: 1px 6px; }

/* tables */
[data-testid="stDataFrame"], [data-testid="stTable"] { border-radius: 12px; overflow: hidden; }

/* simple ranked bars: kit.bars() */
.k-bars { display: grid; gap: 8px; margin: 4px 0 8px; }
.k-bar { display: grid; grid-template-columns: minmax(120px, 36%) 1fr 84px; align-items: center; gap: 10px; font-size: 14px; }
.k-bar span { color: var(--k-ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.k-bar span small { color: var(--k-muted); }
.k-bar div { height: 10px; background: var(--k-line); border-radius: 5px; overflow: hidden; }
.k-bar i { display: block; height: 100%; min-width: 3px; background: var(--k-go); border-radius: 5px; }
.k-bar b { text-align: right; font-weight: 700; color: var(--k-ink); }
.k-bar.dim span, .k-bar.dim b { color: var(--k-muted); font-weight: 500; }
.k-bar.dim i { background: var(--k-muted); opacity: .45; }
.k-bar.pick span { font-weight: 700; }

/* footer */
.k-foot { margin-top: 42px; padding-top: 16px; border-top: 1px solid var(--k-line); color: var(--k-muted);
  font-size: 13px; display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.k-foot a { color: var(--k-go); text-decoration: none; font-weight: 700; }

@media (max-width: 640px) {
  .block-container { padding-top: 2.6rem; }
  .k-meta { text-align: left; }
  .k-ans { padding: 20px; border-radius: 18px; }
  .stApp .k-ans .k-h { font-size: 27px; }
  .k-tiles { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  /* answer-first layouts: the right-hand answer column comes before the questions on phones */
  .st-key-answer_first [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] .k-ans) { flex-direction: column-reverse; }
  /* number rows: two per line on phones instead of one long column */
  [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stMetric"]):not(:has([data-testid="stHorizontalBlock"])) { flex-wrap: wrap; flex-direction: row; gap: 10px; }
  [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stMetric"]):not(:has([data-testid="stHorizontalBlock"])) > [data-testid="stColumn"] { width: calc(50% - 5px) !important; flex: 0 0 calc(50% - 5px) !important; min-width: 0 !important; }
}
"""


def page(name: str, tagline: str, mark: str = "●", icon: str | None = None, meta: str = "", wide: bool = True,
         badge: str = "Demo · invented data"):
    """Page setup + product header. Call first, before any other st.* call."""
    st.set_page_config(page_title=f"{name} · {tagline}", page_icon=icon or mark, layout="wide" if wide else "centered")
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
    st.markdown(
        f'<div class="k-head"><div class="k-brand"><div class="k-mark" aria-hidden="true">{mark}</div>'
        f'<div><p class="k-name">{name}</p><div class="k-tag">{tagline}</div></div></div>'
        f'<div class="k-meta"><span class="k-demo">{badge}</span>{"<br>" + meta if meta else ""}</div></div>',
        unsafe_allow_html=True)


def answer(kicker: str, headline: str, body: str = "", stats: list[tuple[str, str]] | None = None, tone: str = "good"):
    """The answer card. tone: good (green) | warn (amber) | bad (red). body may hold <b> tags; the rest is escaped."""
    tiles = "".join(f'<div class="k-tile"><span>{html.escape(a)}</span><b>{html.escape(b)}</b></div>'
                    for a, b in (stats or []))
    st.markdown(
        f'<div class="k-ans {"" if tone == "good" else tone}"><div class="k-kick">{html.escape(kicker)}</div>'
        f'<p class="k-h">{html.escape(headline)}</p>'
        + (f'<div class="k-body">{body}</div>' if body else "")
        + (f'<div class="k-tiles">{tiles}</div>' if tiles else "") + "</div>",
        unsafe_allow_html=True)


def bars(rows: list[dict]):
    """Ranked bar list. rows: {label, value (number), text (shown), note?, dim?, pick?}."""
    top = max((r["value"] for r in rows), default=0) or 1
    st.markdown("<div class='k-bars'>" + "".join(
        f"<div class='k-bar{' pick' if r.get('pick') else ''}{' dim' if r.get('dim') else ''}'>"
        f"<span>{html.escape(r['label'])}{' <small>· ' + html.escape(r['note']) + '</small>' if r.get('note') else ''}</span>"
        f"<div><i style='width:{r['value'] / top * 100:.1f}%'></i></div><b>{html.escape(r['text'])}</b></div>"
        for r in rows) + "</div>", unsafe_allow_html=True)


def footer(engine: str = ""):
    st.markdown(
        f'<div class="k-foot"><span>Built by Jānis Saulītis with AI{(" · " + engine) if engine else ""}</span>'
        f'<a href="{PORTFOLIO}" target="_blank" rel="noopener">See more tools</a></div>',
        unsafe_allow_html=True)
