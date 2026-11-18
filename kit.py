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

LIGHT = """
  --k-bg: #f5f6f8; --k-surface: #ffffff; --k-surface-2: #f9fafb; --k-line: #e4e7ec; --k-ink: #101828; --k-muted: #5b6474;
  --k-go: #127a5b; --k-go-ink: #ffffff; --k-go-soft: #e7f4ee;
  --k-card: #127a5b; --k-card-ink: #ffffff; --k-card-muted: #cfebdd; --k-card-line: transparent; --k-tile: rgba(255,255,255,.13);
  --k-warn: #fff4db; --k-warn-ink: #8a5a00; --k-bad: #fdecec; --k-bad-ink: #b42318; --k-info: #eaf1fb; --k-info-ink: #1d4f91;
  --k-neutral: #f0f2f5; --k-neutral-ink: #475467;
  --k-hi: #8a5a00; --k-hi-bg: #fff4d6; --k-risk: #d92d20; --k-safe: #12a26f; --k-bar-2: #f5b83d;
"""
DARK = """
  --k-bg: #0f1720; --k-surface: #16212c; --k-surface-2: #1a2633; --k-line: #24313e; --k-ink: #e6edf3; --k-muted: #8b9aab;
  --k-go: #3dd39b; --k-go-ink: #0f1720; --k-go-soft: #133229;
  --k-card: #123528; --k-card-ink: #e6edf3; --k-card-muted: #9fd9bf; --k-card-line: #1e4d3b; --k-tile: rgba(255,255,255,.06);
  --k-warn: #2a2412; --k-warn-ink: #f5b83d; --k-bad: #2c1517; --k-bad-ink: #f0686c; --k-info: #16263a; --k-info-ink: #8ab4f8;
  --k-neutral: #1f2b38; --k-neutral-ink: #b4c0cc;
  --k-hi: #f5b83d; --k-hi-bg: #2a2412; --k-risk: #f0686c; --k-safe: #3dd39b; --k-bar-2: #f5b83d;
"""
# Colours follow the theme the app is actually showing (set by the sync script in page()), so a visitor who picks
# Light in Streamlit's menu on a dark computer still gets matching colours. Before the script runs, the system setting
# decides.
TOKENS = (":root {" + LIGHT + "}\n:root[data-k-theme='dark'] {" + DARK + "}\n"
          "@media (prefers-color-scheme: dark) { :root:not([data-k-theme]) {" + DARK + "} }")

THEME_SYNC = """<script>
const d = window.parent.document;
function sync() {
  const app = d.querySelector('.stApp'); if (!app) return;
  const c = (getComputedStyle(app).color.match(/\\d+/g) || []).map(Number); if (c.length < 3) return;
  const t = (c[0] * 299 + c[1] * 587 + c[2] * 114) / 1000 > 128 ? 'dark' : 'light';
  if (d.documentElement.dataset.kTheme !== t) d.documentElement.dataset.kTheme = t;
}
sync(); setInterval(sync, 300);
</script>"""

ICONS = {  # simple stroke icons for the product mark
    "calculator": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15v3M8 18h4"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
    "book": '<path d="M5 4h10a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h10M9 8h5"/>',
    "inbox": '<path d="M3 13h5l1.5 3h5L16 13h5"/><path d="M5.5 5h13L21 13v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5z"/>',
    "doc-check": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 14l2 2 4-4"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

@@TOKENS@@


.stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp td, .stApp th, .stApp select,
.stApp button p, .stApp [data-testid="stTab"] p, .stApp .stCaption, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
  font-family: 'Manrope', system-ui, sans-serif;
}
.stApp { font-variant-numeric: tabular-nums; }
[data-testid="stAppViewContainer"], [data-testid="stHeader"] { background: var(--k-bg); }
.block-container { max-width: 1160px; padding-top: 3.2rem; padding-bottom: 3rem; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { font-weight: 800; letter-spacing: -.01em; }
.stApp h3 { font-size: 23px !important; } .stApp h4 { font-size: 18px !important; padding-top: .4rem; }

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


.k-mark svg { width: 21px; height: 21px; fill: none; stroke: currentColor; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }

/* designed tables: kit.table() */
.k-tw { border: 1px solid var(--k-line); border-radius: 14px; overflow: auto; background: var(--k-surface); margin: 6px 0 14px; }
.k-t { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 14px; }
.k-t th { position: sticky; top: 0; z-index: 1; background: var(--k-surface-2); color: var(--k-muted); font-size: 12.5px;
  font-weight: 700; text-align: left; padding: 10px 14px; border-bottom: 1px solid var(--k-line); white-space: nowrap; }
.k-t td { padding: 11px 14px; border-bottom: 1px solid var(--k-line); color: var(--k-ink); vertical-align: middle; }
.k-t tr:last-child td { border-bottom: 0; }
.k-t tbody tr:hover td { background: var(--k-surface-2); }
.k-t .num { text-align: right; white-space: nowrap; font-weight: 600; }
.k-t th.num { text-align: right; }
.k-t .mut { color: var(--k-muted); }
.k-t .strong { font-weight: 700; }
.k-t .wrap { min-width: 240px; line-height: 1.45; }
.k-chip { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12.5px; font-weight: 700; white-space: nowrap;
  background: var(--k-neutral); color: var(--k-neutral-ink); }
.k-chip.good { background: var(--k-go-soft); color: var(--k-go); }
.k-chip.warn { background: var(--k-warn); color: var(--k-warn-ink); }
.k-chip.bad { background: var(--k-bad); color: var(--k-bad-ink); }
.k-chip.info { background: var(--k-info); color: var(--k-info-ink); }
.k-lang { display: inline-block; min-width: 26px; text-align: center; padding: 2px 6px; border-radius: 6px; font-size: 11.5px;
  font-weight: 800; letter-spacing: .04em; background: var(--k-neutral); color: var(--k-neutral-ink); }
.k-meter { display: flex; align-items: center; gap: 10px; min-width: 130px; }
.k-meter div { flex: 1; height: 8px; border-radius: 4px; background: var(--k-line); overflow: hidden; }
.k-meter i { display: block; height: 100%; border-radius: 4px; background: var(--k-go); }
.k-meter i.warn { background: var(--k-bar-2); } .k-meter i.bad { background: var(--k-risk); }
.k-meter b { width: 40px; text-align: right; font-weight: 700; font-size: 13.5px; }

/* why-bars: kit.contrib() */
.k-contrib { display: grid; gap: 9px; margin: 6px 0 10px; }
.k-crow { display: grid; grid-template-columns: minmax(130px, 34%) 1fr 1fr; align-items: center; gap: 0; font-size: 14px; }
.k-crow > span { padding-right: 12px; color: var(--k-ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.k-crow .l, .k-crow .r { height: 14px; display: flex; }
.k-crow .l { justify-content: flex-end; border-right: 2px solid var(--k-line); }
.k-crow .l i { background: var(--k-safe); border-radius: 4px 0 0 4px; } .k-crow .r i { background: var(--k-risk); border-radius: 0 4px 4px 0; }
.k-crow i { display: block; height: 100%; }
.k-clegend { display: flex; gap: 18px; font-size: 12.5px; color: var(--k-muted); margin-top: 2px; }
.k-clegend span::before { content: ""; display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }
.k-clegend .lo::before { background: var(--k-safe); } .k-clegend .hi::before { background: var(--k-risk); }

/* paired bars: kit.pairs() */
.k-pairs { display: grid; gap: 10px; margin: 6px 0 10px; }
.k-prow { display: grid; grid-template-columns: 90px 1fr; gap: 12px; align-items: center; font-size: 13.5px; }
.k-prow > span { color: var(--k-muted); }
.k-prow .two { display: grid; gap: 4px; }
.k-prow .two div { display: flex; align-items: center; gap: 8px; }
.k-prow .two i { display: block; height: 9px; border-radius: 5px; min-width: 3px; }
.k-prow .two .a i { background: var(--k-go); } .k-prow .two .b i { background: var(--k-bar-2); }
.k-prow .two b { font-size: 12.5px; font-weight: 700; color: var(--k-ink); }
.k-plegend { display: flex; gap: 18px; font-size: 12.5px; color: var(--k-muted); }
.k-plegend span::before { content: ""; display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }
.k-plegend .a::before { background: var(--k-go); } .k-plegend .b::before { background: var(--k-bar-2); }

/* column chart: kit.columns_chart() */
.k-cols { display: flex; align-items: flex-end; gap: 10px; height: 170px; padding: 8px 4px 0; border-bottom: 1px solid var(--k-line); margin-top: 6px; }
.k-cols div { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 100%; gap: 6px; min-width: 0; }
.k-cols i { display: block; width: 100%; max-width: 56px; background: var(--k-go); border-radius: 6px 6px 0 0; min-height: 3px; }
.k-cols b { font-size: 12px; font-weight: 700; color: var(--k-ink); white-space: nowrap; }
.k-cols-x { display: flex; gap: 10px; padding: 6px 4px 0; }
.k-cols-x span { flex: 1; text-align: center; font-size: 12px; color: var(--k-muted); min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* message boxes: customer email and draft reply */
.k-mail { border: 1px solid var(--k-line); border-radius: 12px; padding: 12px 14px; background: var(--k-surface-2); font-size: 14.5px; line-height: 1.55; color: var(--k-ink); }
.k-mail.reply { background: var(--k-go-soft); border-color: transparent; }
.k-mail-h { font-size: 12.5px; font-weight: 700; color: var(--k-muted); margin: 0 0 6px; }

/* list rows that replace editable tables */
.k-row-desc { font-weight: 700; color: var(--k-ink); } .k-row-sub { font-size: 13px; color: var(--k-muted); }
.st-key-k_sync { position: absolute !important; width: 1px; height: 0 !important; overflow: hidden; opacity: 0; pointer-events: none; }

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
    st.markdown(f"<style>{CSS.replace('@@TOKENS@@', TOKENS)}</style>", unsafe_allow_html=True)
    with st.container(key="k_sync"):
        st.iframe(THEME_SYNC, height=1)
    glyph = (f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[mark]}</svg>' if mark in ICONS else mark)
    st.markdown(
        f'<div class="k-head"><div class="k-brand"><div class="k-mark" aria-hidden="true">{glyph}</div>'
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


def col(label: str, key: str, kind: str = "text", tones: dict | None = None, fmt=None):
    """A table column. kind: text | strong | muted | wrap | num | chip | lang | meter (0–1, tones by value)."""
    return {"label": label, "key": key, "kind": kind, "tones": tones or {}, "fmt": fmt}


def _cell(c, v):
    if c["fmt"] and c["kind"] != "meter":
        v = c["fmt"](v)
    e = html.escape(str(v))
    k = c["kind"]
    if k in ("chip", "lang") and e == "":
        return "<td></td>"
    if k == "chip":
        return f'<td><span class="k-chip {c["tones"].get(v, "")}">{e}</span></td>'
    if k == "lang":
        return f'<td><span class="k-lang">{e.upper()}</span></td>'
    if k == "meter":
        x = float(v)
        tone = "bad" if x >= c["tones"].get("bad", 2) else "warn" if x >= c["tones"].get("warn", 2) else ""
        return (f'<td><div class="k-meter"><div><i class="{tone}" style="width:{max(0, min(1, x)) * 100:.0f}%"></i></div>'
                f'<b>{x:.0%}</b></div></td>')
    cls = {"num": "num", "muted": "mut", "strong": "strong", "wrap": "wrap"}.get(k, "")
    return f'<td class="{cls}">{e}</td>'


def table(rows: list[dict], cols: list[dict], max_height: int | None = None):
    """A designed, read-only table: chips for statuses, language tags, risk meters, right-aligned numbers."""
    head = "".join(f'<th class="{"num" if c["kind"] == "num" else ""}">{html.escape(c["label"])}</th>' for c in cols)
    body = "".join("<tr>" + "".join(_cell(c, r.get(c["key"], "")) for c in cols) + "</tr>" for r in rows)
    style = f' style="max-height:{max_height}px"' if max_height else ""
    st.markdown(f'<div class="k-tw"{style}><table class="k-t"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>',
                unsafe_allow_html=True)


def contrib(rows: list[tuple[str, float]], low: str = "lowers risk", high: str = "raises risk"):
    """Why-bars: each reason pushes left (good) or right (bad) from the middle line."""
    top = max((abs(v) for _, v in rows), default=0) or 1
    st.markdown('<div class="k-contrib">' + "".join(
        f'<div class="k-crow"><span title="{html.escape(n)}">{html.escape(n)}</span>'
        f'<div class="l"><i style="width:{max(-v, 0) / top * 100:.0f}%"></i></div>'
        f'<div class="r"><i style="width:{max(v, 0) / top * 100:.0f}%"></i></div></div>' for n, v in rows)
        + f'</div><div class="k-clegend"><span class="lo">{html.escape(low)}</span><span class="hi">{html.escape(high)}</span></div>',
        unsafe_allow_html=True)


def pairs(rows: list[tuple[str, float, float]], names: tuple[str, str], fmt=lambda x: f"{x:.0%}"):
    """Two bars per row, e.g. predicted vs actual."""
    top = max((max(a, b) for _, a, b in rows), default=0) or 1
    st.markdown(f'<div class="k-plegend"><span class="a">{html.escape(names[0])}</span><span class="b">{html.escape(names[1])}</span></div>'
                '<div class="k-pairs">' + "".join(
        f'<div class="k-prow"><span>{html.escape(n)}</span><div class="two">'
        f'<div class="a"><i style="width:{a / top * 100:.0f}%"></i><b>{fmt(a)}</b></div>'
        f'<div class="b"><i style="width:{b / top * 100:.0f}%"></i><b>{fmt(b)}</b></div></div></div>' for n, a, b in rows)
        + "</div>", unsafe_allow_html=True)


def columns_chart(rows: list[tuple[str, float, str]]):
    """Vertical bars with the value on top: (label, value, text)."""
    top = max((v for _, v, _ in rows), default=0) or 1
    st.markdown('<div class="k-cols">' + "".join(
        f'<div><b>{html.escape(t)}</b><i style="height:{v / top * 82:.0f}%"></i></div>' for _, v, t in rows)
        + '</div><div class="k-cols-x">' + "".join(f"<span>{html.escape(n)}</span>" for n, _, _ in rows) + "</div>",
        unsafe_allow_html=True)


def footer(engine: str = ""):
    st.markdown(
        f'<div class="k-foot"><span>Built by Jānis Saulītis with AI{(" · " + engine) if engine else ""}</span>'
        f'<a href="{PORTFOLIO}" target="_blank" rel="noopener">See more tools</a></div>',
        unsafe_allow_html=True)
