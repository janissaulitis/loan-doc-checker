"""Shared look for Jānis Saulītis' Streamlit apps: product header, fonts, colours, cards, tabs, footer.

Usage in any app:
    import kit
    kit.page("Early Call", "Find the loans that will go late, and why", mark="📞", icon="📞")
    ...
    kit.footer("model.py · scikit-learn")

Colours follow the portfolio (janis-saulitis-portfolio.netlify.app), in light and dark, and follow the visitor's
system setting. Streamlit's own developer chrome (Deploy, GitHub, Fork) is hidden; the ⋮ menu stays for the theme switch.
"""
import streamlit as st

PORTFOLIO = "https://janis-saulitis-portfolio.netlify.app"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');

:root {
  --k-bg: #f6f8f7; --k-surface: #ffffff; --k-line: #dbe3df; --k-ink: #14201b; --k-muted: #56645d;
  --k-go: #1f9d6f; --k-go-ink: #ffffff; --k-hi: #8a5a00; --k-hi-bg: #fff4d6; --k-risk: #c93d41;
}
@media (prefers-color-scheme: dark) {
  :root {
    --k-bg: #0e1211; --k-surface: #151b19; --k-line: #26302c; --k-ink: #e8eeeb; --k-muted: #9aa7a1;
    --k-go: #2fb985; --k-go-ink: #0e1211; --k-hi: #f2c230; --k-hi-bg: #2a2410; --k-risk: #f0686c;
  }
}

.stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp td, .stApp th,
.stApp button p, .stApp [data-testid="stTab"] p, .stApp .stCaption {
  font-family: 'IBM Plex Sans', system-ui, sans-serif;
}
[data-testid="stAppViewContainer"], [data-testid="stHeader"] { background: var(--k-bg); }
.block-container { max-width: 1180px; padding-top: 3.6rem; padding-bottom: 3rem; }

/* developer chrome off; keep the ⋮ menu (theme switch) */
[data-testid="stToolbarActions"], [data-testid="stAppDeployButton"], [data-testid="stDecoration"],
#MainMenu + div, footer, .stDeployButton { display: none !important; }

/* product header */
.k-head { display: flex; align-items: flex-end; justify-content: space-between; gap: 18px; flex-wrap: wrap;
  padding: 6px 0 18px; margin-bottom: 18px; border-bottom: 1px solid var(--k-line); }
.k-brand { display: flex; align-items: center; gap: 14px; min-width: 0; }
.k-mark { width: 46px; height: 46px; flex: none; display: grid; place-items: center; font-size: 24px;
  border-radius: 12px; background: var(--k-go); color: var(--k-go-ink); }
.stApp .k-name { font: 700 40px/0.95 'Barlow Condensed', sans-serif; letter-spacing: .01em; color: var(--k-ink); margin: 0; }
.k-tag { color: var(--k-muted); font-size: 15.5px; margin-top: 4px; }
.k-meta { color: var(--k-muted); font-size: 13px; text-align: right; }
.k-meta b { color: var(--k-ink); font-weight: 600; }
.k-demo { display: inline-block; padding: 3px 10px; border-radius: 999px; background: var(--k-hi-bg); color: var(--k-hi);
  font-size: 12.5px; font-weight: 600; margin-bottom: 6px; }

/* headings and numbers */
h1, h2, h3 { font-family: 'Barlow Condensed', sans-serif !important; letter-spacing: .01em; }
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * { font: 700 38px/1.05 'Barlow Condensed', sans-serif !important; font-variant-numeric: tabular-nums; }
[data-testid="stMetricLabel"] p { color: var(--k-muted); font-size: 13.5px; }
[data-testid="stMetric"] { border-left: 3px solid var(--k-go); padding: 2px 0 2px 14px; }

/* cards */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) { border-radius: 12px; }
div[data-testid="stExpander"] details { border-radius: 10px; border-color: var(--k-line); }

/* tabs as a segmented control */
.stTabs [role="tablist"] { gap: 4px; background: var(--k-surface); border: 1px solid var(--k-line) !important;
  border-radius: 12px; padding: 4px; width: fit-content; max-width: 100%; overflow-x: auto; box-shadow: none; }
.stTabs [role="tablist"]::after, .stTabs [role="tablist"]::before { display: none !important; }
.stTabs [data-testid="stTab"] { border-radius: 9px; padding: 7px 14px; white-space: nowrap; border: 0 !important; }
.stTabs [data-testid="stTab"] p { font-weight: 500; }
.stTabs [data-testid="stTab"][aria-selected="true"] { background: var(--k-go); }
.stTabs [data-testid="stTab"][aria-selected="true"] p { color: var(--k-go-ink) !important; font-weight: 600; }
.stTabs [data-testid="stTab"]:focus-visible { outline: 2px solid var(--k-hi); outline-offset: 2px; }

/* buttons */
.stButton button, .stDownloadButton button, [data-testid="stPopover"] button { border-radius: 10px; font-weight: 600; }
.stButton button[kind="primary"] { color: var(--k-go-ink); }

/* inline code = highlighted example values */
code { color: var(--k-hi) !important; background: var(--k-hi-bg) !important; border-radius: 6px; padding: 1px 6px; }

/* tables */
[data-testid="stDataFrame"], [data-testid="stTable"] { border-radius: 10px; overflow: hidden; }

/* footer */
.k-foot { margin-top: 42px; padding-top: 16px; border-top: 1px solid var(--k-line); color: var(--k-muted);
  font-size: 13px; display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.k-foot a { color: var(--k-go); text-decoration: none; font-weight: 600; }

@media (max-width: 640px) {
  .stApp .k-name { font-size: 32px; }
  .k-mark { width: 40px; height: 40px; font-size: 20px; }
  .k-meta { text-align: left; }
  [data-testid="stMetricValue"], [data-testid="stMetricValue"] * { font-size: 30px !important; }
  /* number rows: two per line on phones instead of one long column */
  [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stMetric"]) { flex-wrap: wrap; flex-direction: row; gap: 14px 12px; }
  [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stMetric"]) > [data-testid="stColumn"] { width: calc(50% - 6px) !important; flex: 0 0 calc(50% - 6px) !important; min-width: 0 !important; }
}
"""


def page(name: str, tagline: str, mark: str = "●", icon: str | None = None, meta: str = "", wide: bool = True):
    """Page setup + product header. Call first, before any other st.* call."""
    st.set_page_config(page_title=f"{name} · {tagline}", page_icon=icon or mark, layout="wide" if wide else "centered")
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
    st.markdown(
        f'<div class="k-head"><div class="k-brand"><div class="k-mark" aria-hidden="true">{mark}</div>'
        f'<div><p class="k-name">{name}</p><div class="k-tag">{tagline}</div></div></div>'
        f'<div class="k-meta"><span class="k-demo">Demo · invented data</span><br>{meta}</div></div>',
        unsafe_allow_html=True)


def footer(engine: str = ""):
    st.markdown(
        f'<div class="k-foot"><span>Built by Jānis Saulītis with AI{(" · " + engine) if engine else ""}</span>'
        f'<a href="{PORTFOLIO}" target="_blank" rel="noopener">See more tools</a></div>',
        unsafe_allow_html=True)
