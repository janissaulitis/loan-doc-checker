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
  --k-go: #127a5b; --k-go-ink: #ffffff; --k-go-soft: #e7f4ee; --k-go-text: #127a5b; --k-ok: #127a5b; --k-ok-soft: #e7f4ee;
  --k-card: #127a5b; --k-card-ink: #ffffff; --k-card-muted: #cfebdd; --k-card-line: transparent; --k-tile: rgba(255,255,255,.13);
  --k-warn: #fff4db; --k-warn-ink: #8a5a00; --k-bad: #fdecec; --k-bad-ink: #b42318; --k-info: #eaf1fb; --k-info-ink: #1d4f91;
  --k-neutral: #f0f2f5; --k-neutral-ink: #475467;
  --k-hi: #8a5a00; --k-hi-bg: #fff4d6; --k-risk: #d92d20; --k-safe: #12a26f; --k-bar-2: #f5b83d;
"""
DARK = """
  --k-bg: #0f1720; --k-surface: #16212c; --k-surface-2: #1a2633; --k-line: #24313e; --k-ink: #e6edf3; --k-muted: #8b9aab;
  --k-go: #3dd39b; --k-go-ink: #0f1720; --k-go-soft: #133229; --k-go-text: #3dd39b; --k-ok: #3dd39b; --k-ok-soft: #133229;
  --k-card: #123528; --k-card-ink: #e6edf3; --k-card-muted: #9fd9bf; --k-card-line: #1e4d3b; --k-tile: rgba(255,255,255,.06);
  --k-warn: #2a2412; --k-warn-ink: #f5b83d; --k-bad: #2c1517; --k-bad-ink: #f0686c; --k-info: #16263a; --k-info-ink: #8ab4f8;
  --k-neutral: #1f2b38; --k-neutral-ink: #b4c0cc;
  --k-hi: #f5b83d; --k-hi-bg: #2a2412; --k-risk: #f0686c; --k-safe: #3dd39b; --k-bar-2: #f5b83d;
"""
SPORT_LIGHT = LIGHT.replace("--k-bg: #f5f6f8; --k-surface: #ffffff; --k-surface-2: #f9fafb; --k-line: #e4e7ec; --k-ink: #101828; --k-muted: #5b6474;",
                            "--k-bg: #f3f5f9; --k-surface: #ffffff; --k-surface-2: #f7f9fc; --k-line: #e1e6ee; --k-ink: #0b1f3a; --k-muted: #526178;") \
    .replace("--k-go: #127a5b; --k-go-ink: #ffffff; --k-go-soft: #e7f4ee; --k-go-text: #127a5b;",
             "--k-go: #e8b100; --k-go-ink: #0b1f3a; --k-go-soft: #fff4d6; --k-go-text: #8a5a00;") \
    .replace("--k-card: #127a5b; --k-card-ink: #ffffff; --k-card-muted: #cfebdd; --k-card-line: transparent; --k-tile: rgba(255,255,255,.13);",
             "--k-card: #0b1f3a; --k-card-ink: #ffffff; --k-card-muted: #f5c95c; --k-card-line: transparent; --k-tile: rgba(255,255,255,.09);")
SPORT_DARK = DARK.replace("--k-bg: #0f1720; --k-surface: #16212c; --k-surface-2: #1a2633; --k-line: #24313e; --k-ink: #e6edf3; --k-muted: #8b9aab;",
                          "--k-bg: #0a1422; --k-surface: #111e30; --k-surface-2: #15243a; --k-line: #22324a; --k-ink: #e8eef6; --k-muted: #8d9bb0;") \
    .replace("--k-go: #3dd39b; --k-go-ink: #0f1720; --k-go-soft: #133229; --k-go-text: #3dd39b;",
             "--k-go: #f5b83d; --k-go-ink: #0a1422; --k-go-soft: #2a2412; --k-go-text: #f5b83d;") \
    .replace("--k-card: #123528; --k-card-ink: #e6edf3; --k-card-muted: #9fd9bf; --k-card-line: #1e4d3b; --k-tile: rgba(255,255,255,.06);",
             "--k-card: #13243b; --k-card-ink: #ffffff; --k-card-muted: #f5c95c; --k-card-line: #22324a; --k-tile: rgba(255,255,255,.07);")
assert SPORT_LIGHT != LIGHT and SPORT_DARK != DARK


def _tokens(light, dark):
    return (":root {" + light + "}\n:root[data-k-theme='dark'] {" + dark + "}\n"
            "@media (prefers-color-scheme: dark) { :root:not([data-k-theme]) {" + dark + "} }")


# Colours follow the theme the app is actually showing (set by the sync script in page()), so a visitor who picks
# Light in Streamlit's menu on a dark computer still gets matching colours. Before the script runs, the system setting
# decides.
TOKENS = _tokens(LIGHT, DARK)

MANROPE = {"url": "family=Manrope:wght@400;500;600;700;800", "body": "'Manrope', system-ui, sans-serif",
           "display": "'Manrope', system-ui, sans-serif", "num": "'Manrope', system-ui, sans-serif",
           "mono": "ui-monospace, monospace"}


def palette(bg, surface, ink, muted, acc, acc_ink, acc_text, ok, bad, warn):
    """Full token set from a handful of base colours; the rest are mixed from them."""
    return f"""
  --k-bg: {bg}; --k-surface: {surface}; --k-ink: {ink}; --k-muted: {muted};
  --k-surface-2: color-mix(in srgb, {ink} 4%, {surface}); --k-line: color-mix(in srgb, {ink} 14%, {bg});
  --k-go: {acc}; --k-go-ink: {acc_ink}; --k-go-text: {acc_text}; --k-go-soft: color-mix(in srgb, {acc} 16%, {surface});
  --k-ok: {ok}; --k-ok-soft: color-mix(in srgb, {ok} 15%, {surface}); --k-safe: {ok};
  --k-warn: color-mix(in srgb, {warn} 17%, {surface}); --k-warn-ink: {warn}; --k-hi: {warn}; --k-hi-bg: color-mix(in srgb, {warn} 17%, {surface});
  --k-bad: color-mix(in srgb, {bad} 15%, {surface}); --k-bad-ink: {bad}; --k-risk: {bad}; --k-bar-2: {warn};
  --k-info: color-mix(in srgb, {acc_text} 13%, {surface}); --k-info-ink: {acc_text};
  --k-neutral: color-mix(in srgb, {ink} 8%, {surface}); --k-neutral-ink: {muted};
  --k-card: {surface}; --k-card-ink: {ink}; --k-card-muted: {muted}; --k-card-line: color-mix(in srgb, {ink} 14%, {bg});
  --k-tile: color-mix(in srgb, {ink} 5%, {surface});
"""


SKINS = {
    "bank": {"light": LIGHT, "dark": DARK, "fonts": MANROPE, "css": ""},
    "sport": {"light": SPORT_LIGHT, "dark": SPORT_DARK, "fonts": MANROPE, "css": ""},
}


def skin(name, light, dark, fonts, css=""):
    SKINS[name] = {"light": light, "dark": dark, "fonts": fonts, "css": css}


# ---------------------------------------------------------------- per-app skins (design directions, 19 Nov 2026)
def _fonts(families, body, display=None, num=None, mono="ui-monospace, monospace"):
    return {"url": families, "body": body, "display": display or body, "num": num or body, "mono": mono}


SQUARE = """
.stApp [data-baseweb="input"], .stApp [data-baseweb="select"] > div, .stApp [data-baseweb="textarea"], .stButton button,
.stDownloadButton button, [data-testid="stPopover"] button, .k-tw, .k-msgs, .k-tl, .k-mail, .k-tile, .k-ans,
[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stExpander"] details, .stTabs [role="tablist"],
.stTabs [data-testid="stTab"], [data-testid="stMultiSelectTagsContainer"] > span > span { border-radius: 0 !important; }
"""

skin("amber",  # Early Call: a risk desk like a trader's terminal
     palette("#FBF8F2", "#FFFFFF", "#141210", "#6E5F48", "#B85F00", "#FFFFFF", "#9A4F00", "#2F7D4E", "#C8322B", "#9A5A00"),
     palette("#0A0A0A", "#161412", "#F2E8D8", "#B39F80", "#FFA028", "#0A0A0A", "#FFA028", "#7FC99A", "#FF5C5C", "#FFA028"),
     _fonts("family=IBM+Plex+Sans+Condensed:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600",
            "'IBM Plex Sans Condensed', sans-serif", num="'IBM Plex Mono', monospace", mono="'IBM Plex Mono', monospace"),
     SQUARE + """
.k-mark { display: none; }
.stApp .k-name { font-family: var(--k-font-mono) !important; color: var(--k-go-text); text-transform: uppercase; letter-spacing: .04em; font-size: 24px; }
.k-demo { background: transparent; border: 1px solid var(--k-line); color: var(--k-muted); font-family: var(--k-font-mono); text-transform: uppercase; font-weight: 500; letter-spacing: .04em; }
.k-ans { background: var(--k-surface); border: 0; border-left: 3px solid var(--k-go); }
.k-ans .k-kick { color: var(--k-go-text); font-family: var(--k-font-mono); text-transform: uppercase; letter-spacing: .1em; font-size: 12px; }
.stApp .k-ans .k-h { font-weight: 600; letter-spacing: 0; }
.k-ans .k-body { color: var(--k-muted); opacity: 1; }
.k-tiles { gap: 2px; } .k-tile { background: var(--k-bg); padding: 12px 14px; }
.k-tile span { text-transform: uppercase; letter-spacing: .1em; font-size: 11px; color: var(--k-muted); }
.k-tile b { font-size: 32px; font-weight: 400; } .k-tile:first-child b { color: var(--k-go-text); }
.stTabs [role="tablist"] { background: transparent; border: 0 !important; padding: 0; gap: 2px; }
.stTabs [data-testid="stTab"] { background: var(--k-surface); padding: 7px 14px; }
.stTabs [data-testid="stTab"] p { color: var(--k-go-text) !important; text-transform: uppercase; letter-spacing: .06em; font-weight: 600; font-size: 13px; }
.k-chip { border-radius: 0; background: transparent !important; border: 1px solid currentColor; font-family: var(--k-font-mono); text-transform: uppercase; font-weight: 500; font-size: 11.5px; }
.k-t th { font-family: var(--k-font-mono); text-transform: uppercase; letter-spacing: .08em; font-size: 11px; font-weight: 500; }
.k-t tbody tr:nth-child(even) td { background: var(--k-surface-2); }
.k-t td.mut:first-child { font-family: var(--k-font-mono); color: var(--k-go-text); }
.k-why-bar, .k-meter div, .k-meter i, .k-why-bar i { border-radius: 0; }
""")

skin("broadsheet",  # Statement Check: audit paper
     palette("#ECE6D9", "#FFFDF8", "#1B1A17", "#6B655A", "#1F3A93", "#FFFFFF", "#1F3A93", "#1D6B52", "#A3243B", "#8A5F00"),
     palette("#141311", "#1E1C19", "#EDE6D8", "#A69E8F", "#8FA8FF", "#141311", "#8FA8FF", "#6BC6A0", "#E2738A", "#E0B45C"),
     _fonts("family=Instrument+Serif:ital@0;1&family=Instrument+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500",
            "'Instrument Sans', sans-serif", "'Instrument Serif', serif", "'DM Mono', monospace", "'DM Mono', monospace"),
     """
.k-mark { border-radius: 4px; }
.stApp .k-name { font-weight: 400; font-size: 26px; }
.k-ans, .k-ans.warn, .k-ans.bad { background: transparent; border: 0; padding: 4px 0 6px; color: var(--k-ink); }
.k-ans .k-kick { font-family: var(--k-font-mono); text-transform: uppercase; letter-spacing: .12em; font-size: 12px; color: var(--k-muted) !important; }
.stApp .k-ans .k-h { font-weight: 400; font-size: 52px; line-height: 1.02; letter-spacing: -.01em; max-width: 20ch; }
.k-ans .k-body { color: var(--k-muted); }
.k-tile, .k-ans.warn .k-tile, .k-ans.bad .k-tile { background: var(--k-surface); border: 1px solid var(--k-line); border-radius: 6px; }
.k-tile span { color: var(--k-muted) !important; } .k-tile b { font-weight: 500; }
.k-paper { background: #FFFDF8; color: #1B1A17; box-shadow: 0 18px 40px rgba(0,0,0,.22); transform: rotate(-.7deg); padding: 22px 22px 18px;
  border-radius: 2px; margin: 8px 6px 18px; }
.k-paper-h { display: flex; justify-content: space-between; font-family: var(--k-font-mono); font-size: 11.5px; letter-spacing: .1em;
  text-transform: uppercase; color: #6B655A; border-bottom: 1px solid #1B1A17; padding-bottom: 8px; margin-bottom: 8px; }
.k-paper-r { display: grid; grid-template-columns: 64px 1fr auto; gap: 10px; padding: 7px 8px; font-size: 14px; border-radius: 2px; }
.k-paper-r span:first-child, .k-paper-r b { font-family: var(--k-font-mono); font-weight: 400; }
.k-paper-r.good { background: #E3EFE7; } .k-paper-r.bad { background: #F6DEE3; } .k-paper-r.warn { background: #F5EBD3; }
.k-paper-f { font-size: 12px; color: #6B655A; margin-top: 16px; font-style: italic; }
.k-note { border: 1px solid var(--k-line); background: var(--k-surface); padding: 14px 16px; border-radius: 4px; margin-bottom: 12px; }
.k-note h5 { margin: 0 0 8px; font-family: var(--k-font-mono) !important; font-size: 11.5px; letter-spacing: .12em; text-transform: uppercase; color: var(--k-muted); font-weight: 400; }
.k-note .m { font-family: var(--k-font-mono); font-size: 14.5px; line-height: 1.7; }
.k-find { display: grid; grid-template-columns: 22px 1fr; gap: 6px; padding: 5px 0; font-size: 14.5px; }
.k-find i { font-style: normal; font-weight: 700; } .k-find.ok i { color: var(--k-ok); } .k-find.bad i { color: var(--k-bad-ink); } .k-find.warn i { color: var(--k-warn-ink); }
""")

skin("glass",  # Inbox Router: quiet layered dark, keyboard-first
     palette("#FBFBFC", "#FFFFFF", "#0F1012", "#62666D", "#5E6AD2", "#FFFFFF", "#4C57C4", "#0E8F7A", "#D1435B", "#A86A00"),
     palette("#08090A", "#111214", "#F7F8F8", "#8A8F98", "#7C83FF", "#08090A", "#A3A8FF", "#34D3B4", "#F7768E", "#E8B464"),
     _fonts("family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500;600", "'Geist', sans-serif",
            num="'Geist Mono', monospace", mono="'Geist Mono', monospace"),
     """
.k-mark { border-radius: 10px; }
.k-ans { background: var(--k-surface); border: 1px solid var(--k-line); border-radius: 14px; color: var(--k-ink); }
.k-ans .k-kick { color: var(--k-muted); font-weight: 500; }
.k-ans .k-body { color: var(--k-muted); opacity: 1; }
.k-tile { background: var(--k-surface-2); border: 1px solid var(--k-line); border-radius: 10px; }
.k-tile span { color: var(--k-muted); } .k-tile b { font-size: 26px; font-weight: 500; }
.k-tile:nth-child(2) b { color: var(--k-bad-ink); } .k-tile:nth-child(3) b { color: var(--k-ok); }
.k-ans:has(.k-body:empty) .k-body { display: none; }
.k-chip { border-radius: 6px; }
.k-st { font-family: var(--k-font-mono); font-size: 11.5px; letter-spacing: .04em; font-weight: 500; }
.k-st.p { color: var(--k-bad-ink); } .k-st.d { color: var(--k-ok); }
.k-ib { border: 1px solid var(--k-line); border-radius: 14px; background: var(--k-surface); overflow: hidden; }
.k-ib-r { display: grid; grid-template-columns: 34px 1fr 110px 108px; gap: 12px; align-items: center; padding: 11px 14px;
  border-bottom: 1px solid var(--k-line); font-size: 14.5px; }
.k-ib-r:last-child { border-bottom: 0; } .k-ib-r.sel { background: color-mix(in srgb, var(--k-go) 10%, var(--k-surface)); }
.k-ib-r .t { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--k-ink); }
.k-ib-r .c { color: var(--k-muted); font-size: 13.5px; }
.k-detail-p { border: 1px solid var(--k-line); border-radius: 14px; background: var(--k-surface); padding: 16px 18px; }
.k-detail-p blockquote { margin: 12px 0 6px; padding: 0; border: 0; font-size: 18px; line-height: 1.45; color: var(--k-ink); }
.k-detail-p .en { color: var(--k-muted); font-size: 14px; line-height: 1.5; }
.k-detail-p .rule { border-top: 1px solid var(--k-line); margin-top: 14px; padding-top: 12px; font-size: 14px; line-height: 1.5; }
@media (max-width: 640px) { .k-ib-r { grid-template-columns: 34px 1fr; } .k-ib-r .c, .k-ib-r .k-st { display: none; } }
""")

skin("brutal",  # Auto Books: loud, friendly, chunky
     palette("#FFF8E7", "#FFFFFF", "#0A0A0A", "#4A4A4A", "#FFD23F", "#0A0A0A", "#7A5A00", "#16857A", "#D93A3F", "#7A5A00"),
     palette("#111111", "#1C1C1C", "#FAFAFA", "#B5B5B5", "#FFD23F", "#111111", "#FFD23F", "#3DDBC6", "#FF7A7A", "#FFD23F"),
     _fonts("family=Archivo+Black&family=Archivo:wght@400;500;600;700;800&family=Space+Mono:wght@400;700",
            "'Archivo', sans-serif", "'Archivo Black', sans-serif", "'Archivo', sans-serif", "'Space Mono', monospace"),
     SQUARE + """
.k-mark { display: none; }
.stApp .k-name { font-weight: 400; text-transform: uppercase; font-size: 30px; letter-spacing: 0; }
.k-demo { background: var(--k-ok); color: #0A0A0A; border: 2px solid var(--k-ink); transform: rotate(-3deg); text-transform: uppercase;
  font-family: var(--k-font-mono); padding: 4px 12px; }
.k-ans { background: transparent; border: 0; padding: 0; color: var(--k-ink); }
.k-ans .k-kick { color: var(--k-muted); font-family: var(--k-font-mono); text-transform: uppercase; }
.stApp .k-ans .k-h { font-weight: 400; font-size: 46px; line-height: 1.08; letter-spacing: -.01em; }
.k-ans mark { background: var(--k-go); color: #0A0A0A; padding: 0 .18em; }
.k-ans .k-body { color: var(--k-muted); opacity: 1; }
.k-tile { background: var(--k-surface); border: 2px solid var(--k-ink); box-shadow: 4px 4px 0 var(--k-ink); padding: 12px 14px; }
.k-tile:last-child { background: var(--k-go); } .k-tile:last-child span, .k-tile:last-child b { color: #0A0A0A !important; }
.k-tile span { font-family: var(--k-font-mono); text-transform: uppercase; font-weight: 700; font-size: 11.5px; color: var(--k-ink) !important; }
.k-tile b { font-size: 30px; font-weight: 500; }
.k-tiles { gap: 14px; margin-top: 22px; }
[data-testid="stVerticalBlockBorderWrapper"] { border: 2px solid var(--k-ink) !important; box-shadow: 4px 4px 0 var(--k-ink); }
.stButton button[kind="primary"], .stDownloadButton button[kind="primary"] { background: var(--k-ink); border: 2px solid var(--k-ink);
  box-shadow: 4px 4px 0 var(--k-ok); }
.stButton button[kind="primary"] p, .stDownloadButton button[kind="primary"] p { color: var(--k-bg) !important; text-transform: uppercase; }
.stTabs [role="tablist"] { border: 2px solid var(--k-ink) !important; }
.k-tw, .k-tl { border: 2px solid var(--k-ink); }
.k-bar i, .k-meter i { background: var(--k-ink); } .k-bar div, .k-meter div { border: 1px solid var(--k-ink); background: transparent; }
""")

skin("space",  # Where AI Pays: one money number, cinema dark
     palette("#F7F9FC", "#FFFFFF", "#0A1A33", "#55627A", "#1257E6", "#FFFFFF", "#1257E6", "#0B8C6E", "#D4462E", "#9A6A00"),
     palette("#000814", "#071A33", "#EAF0FA", "#8EA0BD", "#1C6CFF", "#FFFFFF", "#7FA8FF", "#22D3A6", "#FF7A59", "#F5B83D"),
     _fonts("family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700", "'Inter', sans-serif", "'Sora', sans-serif",
            "'Sora', sans-serif"),
     """
:root[data-k-theme='dark'] [data-testid="stAppViewContainer"] { background: radial-gradient(1100px 560px at 75% -8%, #0c2b63 0%, #000814 62%); }
.k-mark { border-radius: 12px; }
.k-ans { background: transparent; border: 0; padding: 0 0 6px; color: var(--k-ink); }
.k-ans .k-kick { color: var(--k-muted); text-transform: uppercase; letter-spacing: .12em; font-size: 12.5px; }
.stApp .k-ans .k-h { font-size: 92px; line-height: .95; letter-spacing: -.045em; }
.k-ans .k-h small { font-size: .38em; letter-spacing: -.02em; color: var(--k-muted); font-weight: 700; }
.k-ans .k-body { color: var(--k-muted); font-size: 17px; opacity: 1; } .k-ans .k-body b { color: var(--k-ok); }
.k-tile { background: color-mix(in srgb, var(--k-surface) 80%, transparent); border: 1px solid var(--k-line); border-radius: 14px; }
.k-tile span { color: var(--k-muted); }
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) { background: color-mix(in srgb, var(--k-surface) 85%, transparent); border-radius: 16px; }
.k-chip { background: transparent !important; border: 1.5px solid currentColor; }
.k-rank { font-family: var(--k-font-display); font-weight: 800; font-size: 22px; color: var(--k-muted); }
@media (max-width: 640px) { .stApp .k-ans .k-h { font-size: 64px; } }
""")

skin("field",  # AI Cost Check: a gadget with an LCD
     palette("#E6E6E3", "#F5F5F2", "#111111", "#56564F", "#C24400", "#FFFFFF", "#A33A00", "#257A55", "#C42A5E", "#8A5A00"),
     palette("#121212", "#1D1D1C", "#ECECE8", "#9A9A94", "#FF6A13", "#121212", "#FF8A3D", "#3DDC97", "#FF5C8A", "#F5B83D"),
     _fonts("family=Martian+Mono:wght@400;500;700&family=Archivo:wght@400;500;600;700;800", "'Archivo', sans-serif",
            "'Archivo', sans-serif", "'Martian Mono', monospace", "'Martian Mono', monospace"),
     """
.k-mark { border-radius: 8px; }
.stApp .k-name { font-size: 26px; }
.k-ans, .k-ans.warn { background: #0D1A11; border: 2px solid #050505; border-radius: 12px; color: #4DFF94;
  box-shadow: inset 0 0 0 1px #1E3A27, inset 0 0 40px rgba(77,255,148,.06); }
.k-ans.warn { color: #FFB86B; }
.k-ans .k-kick { font-family: var(--k-font-mono); text-transform: uppercase; letter-spacing: .14em; font-size: 11px; color: inherit !important; opacity: .7; }
.stApp .k-ans .k-h { font-family: var(--k-font-mono) !important; font-weight: 700; font-size: 54px; text-shadow: 0 0 14px currentColor; letter-spacing: -.02em; }
.k-ans .k-body { font-family: var(--k-font-mono); font-size: 13.5px; line-height: 1.7; opacity: .85; color: inherit; }
.k-ans .k-body b { color: inherit; }
.k-tiles { gap: 0; border: 1.5px solid #1E3A27; }
.k-tile, .k-ans.warn .k-tile { background: transparent; border-radius: 0; border-right: 1.5px solid #1E3A27; }
.k-tile:last-child { border-right: 0; } .k-tile span { color: inherit !important; opacity: .65; font-family: var(--k-font-mono); text-transform: uppercase; font-size: 10.5px; letter-spacing: .1em; }
.k-tile b { color: inherit; font-size: 20px; }
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) { border: 2px solid var(--k-ink) !important; border-radius: 12px; }
.k-knobs { display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; margin: 4px 0 6px; }
.k-knob { text-align: center; flex: 1 1 70px; } .k-knob svg { width: 64px; height: 64px; }
.k-knob span { display: block; font-family: var(--k-font-mono); font-size: 10px; letter-spacing: .1em; text-transform: uppercase; color: var(--k-muted); margin-top: 4px; }
.k-knob b { display: block; font-family: var(--k-font-mono); font-size: 14px; color: var(--k-ink); }
.k-bar i { background: var(--k-ink); border-radius: 0; } .k-bar.pick i { background: var(--k-go); } .k-bar div { border-radius: 0; }
.k-bar span { font-family: var(--k-font-mono); font-size: 12.5px; }
""")

skin("ledger",  # AI Cost Check: a calm cost sheet; the waterfall shows where the money goes
     palette("#F4F6F8", "#FFFFFF", "#0E1A2B", "#566273", "#0F766E", "#FFFFFF", "#0F766E", "#0F766E", "#C2410C", "#A16207"),
     palette("#0B1220", "#121B2B", "#E6ECF3", "#93A0B2", "#2DD4BF", "#0B1220", "#5EEAD4", "#2DD4BF", "#FB923C", "#FACC15"),
     _fonts("family=Inter+Tight:wght@400;500;600;700;800", "'Inter Tight', sans-serif"),
     """
.k-mark { border-radius: 10px; }
.k-ans { background: var(--k-surface); color: var(--k-ink); border: 1px solid var(--k-line); border-radius: 16px; }
.k-ans.warn { background: var(--k-surface); border-color: var(--k-warn-ink); }
.k-ans .k-kick { color: var(--k-go-text) !important; text-transform: uppercase; letter-spacing: .1em; font-size: 12px; }
.k-ans.warn .k-kick { color: var(--k-warn-ink) !important; }
.stApp .k-ans .k-h { font-size: 40px; letter-spacing: -.02em; }
.k-ans .k-body { color: var(--k-muted); opacity: 1; } .k-ans .k-body b { color: var(--k-ink); }
.k-ans .k-h em { font-style: normal; color: var(--k-ok); }
.k-ans.warn .k-h em { color: var(--k-warn-ink); }
.k-split { margin-top: 20px; }
.k-split-h { display: flex; justify-content: space-between; font-size: 13px; color: var(--k-muted); margin-bottom: 8px; }
.k-split-bar { display: flex; height: 16px; border-radius: 8px; overflow: hidden; gap: 2px; background: var(--k-surface-2); }
.k-split-bar i { display: block; height: 100%; min-width: 4px; }
.k-split-bar .keep { background: var(--k-ok); } .k-split-bar .check { background: var(--k-risk); }
.k-split-bar .tools { background: var(--k-muted); } .k-split-bar .ai { background: var(--k-warn-ink); }
.k-split-l { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 14px; }
.k-split-l div { border-left: 3px solid; padding-left: 10px; }
.k-split-l span { display: block; font-size: 12.5px; color: var(--k-muted); }
.k-split-l b { display: block; font-size: 20px; font-weight: 800; color: var(--k-ink); }
.k-split-l .keep { border-color: var(--k-ok); } .k-split-l .keep b { color: var(--k-ok); }
.k-split-l .check { border-color: var(--k-risk); } .k-split-l .tools { border-color: var(--k-muted); } .k-split-l .ai { border-color: var(--k-warn-ink); }
@media (max-width: 640px) { .k-split-l { grid-template-columns: repeat(2, minmax(0, 1fr)); } .stApp .k-ans .k-h { font-size: 30px; } }
""")

skin("flap",  # Court Finish: departures board
     palette("#ECE7DC", "#FFFFFF", "#1A1A1A", "#615B50", "#B86A00", "#FFFFFF", "#8F5200", "#2E7D3E", "#C0391B", "#8F5200"),
     palette("#111111", "#1C1C1C", "#EDE6D6", "#A8A295", "#FFB000", "#111111", "#FFB000", "#7FD18B", "#FF6B4A", "#FFB000"),
     _fonts("family=Space+Mono:wght@400;700&family=Oswald:wght@400;500;600", "'Space Mono', monospace", "'Oswald', sans-serif",
            "'Space Mono', monospace", "'Space Mono', monospace"),
     """
.k-mark { border-radius: 6px; }
.stApp .k-name { text-transform: uppercase; letter-spacing: .06em; font-weight: 500; }
.k-tag, .k-meta { font-size: 13px; }
.k-demo { border-radius: 4px; text-transform: uppercase; font-family: var(--k-font-mono); }
.k-board { background: #141414; color: #EDE6D6; border-radius: 10px; padding: 20px 22px; margin: 0 0 18px; border: 1px solid #000; }
.k-board-top { display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; font-family: 'Oswald', sans-serif;
  letter-spacing: .14em; text-transform: uppercase; font-size: 17px; color: #BDB5A3; margin-bottom: 14px; }
.k-board-top span:last-child { color: #FFB000; font-size: 14px; }
.k-board-hero { display: flex; gap: 26px; align-items: center; flex-wrap: wrap; }
.k-flap { display: inline-flex; gap: 5px; }
.k-flap span { position: relative; display: grid; place-items: center; background: #232323; color: #F3EAD6; font-family: 'Space Mono', monospace;
  font-weight: 700; border-radius: 5px; box-shadow: inset 0 -2px 0 rgba(0,0,0,.45); }
.k-flap span::after { content: ""; position: absolute; left: 0; right: 0; top: 50%; height: 2px; background: #0b0b0b; }
.k-flap.big span { width: 62px; height: 92px; font-size: 64px; } .k-flap.big span.c { width: 30px; background: transparent; box-shadow: none; }
.k-flap.big span.c::after, .k-flap.sm span.c::after { display: none; }
.k-flap.sm span { width: 21px; height: 30px; font-size: 18px; line-height: 1; background: linear-gradient(#272727 0 50%, #1d1d1d 50% 100%); }
.k-flap.sm span::after { display: none; } .k-flap.sm span.c { width: 10px; background: transparent; box-shadow: none; }
.k-flap.amber span { color: #FFB000; }
.k-board-sub { font-family: 'Space Mono', monospace; font-size: 15px; line-height: 1.75; }
.k-board-sub .o { color: #FF6B4A; } .k-board-sub .m { color: #A8A295; }
.k-dep { display: grid; grid-template-columns: 70px 1fr 1fr 1fr 110px; gap: 10px; align-items: center; padding: 8px 0; }
.k-dep.h { font-family: 'Oswald', sans-serif; letter-spacing: .14em; font-size: 12px; color: #A8A295; padding-bottom: 2px; }
.k-dep .st { font-family: 'Oswald', sans-serif; letter-spacing: .1em; font-size: 15px; text-transform: uppercase; }
.k-dep .st.ok { color: #7FD18B; } .k-dep .st.w { color: #FFB000; } .k-dep .st.o { color: #FF6B4A; } .k-dep .st.n { color: #EDE6D6; }
.k-dep .blank span { color: transparent; }
.k-board-f { display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; border-top: 1px solid #2a2a2a; margin-top: 14px; padding-top: 12px;
  font-size: 12.5px; color: #A8A295; letter-spacing: .04em; text-transform: uppercase; }
@media (max-width: 760px) { .k-dep { grid-template-columns: 52px auto auto; justify-content: space-between; gap: 14px; padding: 9px 0; } .k-dep .nb, .k-dep.h .nb, .k-dep .st { display: none; } .k-flap.sm { gap: 2px; } .k-flap.sm span { width: 19px; height: 28px; font-size: 16px; } .k-flap.sm span.c { width: 8px; }
  .k-flap.big span { width: 44px; height: 64px; font-size: 44px; } }
""")

skin("stub",  # Tournament Report: event paper and rubber stamps
     palette("#F5EEDF", "#FFFDF7", "#1E1A16", "#6E6457", "#C2412A", "#FFFFFF", "#A9361F", "#23685B", "#B23A24", "#8A5F00"),
     palette("#14110F", "#201B17", "#F2E8D5", "#9A8F7E", "#D94F30", "#FFFFFF", "#F08066", "#5FBFA8", "#F08066", "#E0B45C"),
     _fonts("family=Alfa+Slab+One&family=Roboto+Slab:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500",
            "'Roboto Slab', serif", "'Alfa Slab One', serif", "'IBM Plex Mono', monospace", "'IBM Plex Mono', monospace"),
     """
.k-mark { border-radius: 4px; }
.stApp .k-name { font-weight: 400; letter-spacing: .01em; }
.stApp h4 { font-weight: 400 !important; }
.k-ans { background: var(--k-surface); color: var(--k-ink); border: 2px dashed var(--k-line); border-radius: 6px; }
.k-ans .k-kick { color: var(--k-go-text); font-family: var(--k-font-mono); text-transform: uppercase; letter-spacing: .12em; font-size: 12px; }
.stApp .k-ans .k-h { font-weight: 400; }
.k-ans .k-body { color: var(--k-muted); opacity: 1; }
.k-tile { background: var(--k-bg); border: 1px solid var(--k-line); border-radius: 4px; } .k-tile span { color: var(--k-muted); }
.k-paper { background: #F2E8D5; color: #1E1A16; border-radius: 4px; padding: 22px 22px 14px; box-shadow: 0 14px 34px rgba(0,0,0,.25); }
.k-paper .eyebrow { font-family: var(--k-font-mono); font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase; color: #6E6457; }
.k-paper h3 { font-family: 'Roboto Slab', serif !important; font-weight: 400 !important; font-size: 30px !important; line-height: 1.08; margin: 4px 0 16px; color: #1E1A16; }
.k-fix { display: grid; grid-template-columns: 1fr 1fr 118px; gap: 12px; align-items: center; padding: 11px 0; border-bottom: 1px dashed #b9ad97; }
.k-fix.h { font-family: var(--k-font-mono); font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: #6E6457; border-bottom: 1px solid #1E1A16; padding-top: 0; }
.k-fix s { font-family: var(--k-font-mono); color: #857a68; font-size: 13.5px; }
.k-fix b { font-family: 'Roboto Slab', serif; font-weight: 700; font-size: 14.5px; }
.k-stamp { justify-self: end; display: inline-block; border: 2px solid currentColor; padding: 3px 12px; transform: rotate(-5deg);
  font-family: 'Alfa Slab One', serif; text-transform: uppercase; letter-spacing: .05em; font-size: 12.5px; border-radius: 3px;
  box-shadow: inset 0 0 0 1px currentColor; opacity: .92; }
.k-stamp.fixed { color: #23685B; } .k-stamp.held { color: #9A6A00; } .k-stamp.flag { color: #B23A24; }
.k-tilt img { transform: rotate(1.4deg); box-shadow: 0 14px 30px rgba(0,0,0,.28); border-radius: 3px; }
""")

skin("booth",  # Caption Checker: looks like the TV graphics it feeds
     palette("#F3F4F7", "#FFFFFF", "#0B0E14", "#5B6476", "#E0281E", "#FFFFFF", "#C4221A", "#1E8E3E", "#D42A1F", "#7A5E00"),
     palette("#0B0E14", "#151A24", "#F4F6FA", "#8A93A6", "#FF3B30", "#FFFFFF", "#FF6A61", "#4CD07D", "#FF3B30", "#FFD60A"),
     _fonts("family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700", "'Barlow', sans-serif",
            "'Barlow Condensed', sans-serif", "'Barlow Condensed', sans-serif"),
     SQUARE + """
.k-head { display: none; }
.k-bug { display: flex; align-items: stretch; background: var(--k-surface); border: 1px solid var(--k-line); margin: 0 0 16px; min-height: 58px; }
.k-bug .tag { background: #E0281E; color: #fff; font: 800 20px/1 'Barlow Condensed', sans-serif; letter-spacing: .04em; padding: 0 22px 0 18px;
  display: flex; align-items: center; clip-path: polygon(0 0, 100% 0, 88% 100%, 0 100%); text-transform: uppercase; }
.k-bug .t { flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 6px 18px; min-width: 0; }
.k-bug .t b { font: 800 22px/1.05 'Barlow Condensed', sans-serif; text-transform: uppercase; letter-spacing: .02em; color: var(--k-ink); }
.k-bug .t small { color: var(--k-muted); font-size: 13px; }
.k-bug .n { background: #FFD60A; color: #0B0E14; font: 800 22px/1 'Barlow Condensed', sans-serif; padding: 0 18px; display: flex; align-items: center; text-transform: uppercase; white-space: nowrap; }
.k-bug .n.held { background: #E0281E; color: #fff; }
@media (max-width: 640px) { .k-bug { flex-wrap: wrap; } .k-bug .tag { min-height: 44px; } .k-bug .n { margin-left: auto; min-height: 44px; }
  .k-bug .t { order: 3; flex-basis: 100%; border-top: 1px solid var(--k-line); padding: 10px 14px; } .k-bug .t b { font-size: 20px; } }
.k-ans { background: transparent; border: 0; padding: 0; color: var(--k-ink); }
.k-ans .k-kick, .k-ans .k-h { display: none; }
.k-ans .k-body { color: var(--k-muted); opacity: 1; font-size: 15px; margin: 0 0 4px; }
.k-tiles { gap: 2px; margin-top: 12px; } .k-tile { background: var(--k-surface); border: 1px solid var(--k-line); padding: 12px 16px; }
.k-tile span { text-transform: uppercase; letter-spacing: .1em; font-size: 12px; color: var(--k-muted) !important; font-weight: 600; }
.k-tile b { font-size: 46px; font-weight: 800; line-height: 1; }
.k-tile:nth-child(2) b { color: #E8B800; } .k-tile:nth-child(3) b { color: var(--k-bad-ink); }
.k-chip { border-radius: 2px; font-family: 'Barlow Condensed', sans-serif; font-weight: 800; letter-spacing: .05em; text-transform: uppercase; font-size: 13.5px; }
.k-chip.warn { background: #FFD60A; color: #0B0E14; } .k-chip.bad { background: #E0281E; color: #fff; }
.k-chip.good { background: var(--k-neutral); color: var(--k-ink); } .k-chip.info { background: #2B6DE8; color: #fff; }
.k-t td.strong { font-family: 'Barlow Condensed', sans-serif; font-weight: 800; text-transform: uppercase; font-size: 16px; letter-spacing: .02em; }
.k-stage { background: linear-gradient(135deg, #1a2433, #0b0e14); display: grid !important; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); }
.k-stage .lt { width: 100%; margin: 0 !important; } .k-stage .lt .nm { flex: 1; min-width: 0; } .k-stage .lt .co { width: 118px; flex: none; justify-content: center; } .k-stage .lt .nm b { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
@media (max-width: 640px) { .k-stage { grid-template-columns: 1fr; padding: 16px 12px; } .k-stage .lt .nm { padding: 8px 12px 6px; } .k-stage .lt .nm b, .k-stage .lt .co { font-size: 22px; } .k-stage .lt .co { width: 96px; padding: 0 8px; } .k-stage .lt .co svg { width: 24px; height: 16px; margin-right: 7px; } }
.lt { display: inline-flex; align-items: stretch; box-shadow: 0 8px 22px rgba(0,0,0,.4); }
.lt .edge { width: 14px; background: #E0281E; clip-path: polygon(40% 0, 100% 0, 100% 100%, 0 100%); }
.lt .nm { background: #F4F6FA; color: #0B0E14; padding: 8px 18px 6px; min-width: 210px; }
.lt .nm b { display: block; font: 800 28px/1 'Barlow Condensed', sans-serif; text-transform: uppercase; letter-spacing: .01em; }
.lt .nm small { font: 500 14px/1.3 'Barlow', sans-serif; color: #5B6476; }
.lt .co svg { width: 30px; height: 20px; margin-right: 10px; flex: none; box-shadow: 0 0 0 1px rgba(255,255,255,.35); }
.lt .co { gap: 0; background: #0B0E14; color: #F4F6FA; font: 800 28px/1 'Barlow Condensed', sans-serif; padding: 0 16px; display: flex; align-items: center; border: 2px solid #F4F6FA; }
""")


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
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "captions": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 15h4M13 15h4M7 11h10"/>',
    "report": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 17v-3M12 17v-6M15 17v-2"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
}

CSS = """
@@FONTS@@

@@TOKENS@@


.stApp, .k-head, .k-ans, .k-t, .k-bars, .k-why, .k-msgs, .k-pairs, .k-cols, .k-cols-x, .k-foot, .k-mail, .k-tl { font-family: var(--k-font); }
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp .k-name, .stApp .k-ans .k-h { font-family: var(--k-font-display) !important; }
.k-tile b, .k-t .num, .k-meter b, .k-bar b, .k-cols b, [data-testid='stMetricValue'] * { font-family: var(--k-font-num) !important; }
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
.stApp .k-name { font-size: 21px; line-height: 1.15; font-weight: 800; letter-spacing: -.01em; color: var(--k-ink); margin: 0; }
.k-tag { color: var(--k-muted); font-size: 14.5px; margin-top: 2px; }
.k-meta { color: var(--k-muted); font-size: 13px; text-align: right; line-height: 1.6; }
.k-demo { display: inline-block; padding: 3px 11px; border-radius: 999px; background: var(--k-go-soft); color: var(--k-go-text);
  font-size: 12.5px; font-weight: 700; }

/* the answer card */
.k-ans { background: var(--k-card); color: var(--k-card-ink); border: 1px solid var(--k-card-line); border-radius: 20px;
  padding: 26px 28px; margin: 0 0 18px; }
.k-ans.warn { background: var(--k-warn); color: var(--k-ink); border-color: transparent; }
.k-ans.bad { background: var(--k-bad); color: var(--k-ink); border-color: transparent; }
.k-ans .k-kick { font-size: 14.5px; font-weight: 700; color: var(--k-card-muted); margin-bottom: 8px; }
.k-ans.warn .k-kick { color: var(--k-warn-ink); } .k-ans.bad .k-kick { color: var(--k-bad-ink); }
.stApp .k-ans .k-h { font-size: 34px; line-height: 1.15; font-weight: 800; letter-spacing: -.02em; margin: 0; color: inherit; }
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
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * { font-size: 28px !important; font-weight: 800 !important; }
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
.stButton button, .stDownloadButton button, [data-testid="stPopover"] > div > button, [data-testid="stPopoverButton"] {
  border-radius: 12px; min-height: 44px; padding: 0 18px; transition: background .15s, border-color .15s, color .15s; }
.stButton button p, .stDownloadButton button p, [data-testid="stPopover"] button p { font-weight: 700 !important; font-size: 15px; }
.stButton button[kind="primary"], .stDownloadButton button[kind="primary"] {
  background: var(--k-go); border: 1px solid var(--k-go); color: var(--k-go-ink); box-shadow: 0 1px 2px rgba(16,24,40,.12); }
.stButton button[kind="primary"] p, .stDownloadButton button[kind="primary"] p { color: var(--k-go-ink) !important; }
.stButton button[kind="primary"]:hover, .stDownloadButton button[kind="primary"]:hover { filter: brightness(1.08); }
.stButton button[kind="secondary"], .stDownloadButton button[kind="secondary"], [data-testid="stPopover"] button {
  background: var(--k-surface) !important; border: 1px solid var(--k-line) !important; color: var(--k-ink) !important; }
.stButton button[kind="secondary"] p, .stDownloadButton button[kind="secondary"] p, [data-testid="stPopover"] button p,
[data-testid="stPopover"] button svg, [data-testid="stPopover"] button span { color: var(--k-ink) !important; }
.stButton button[kind="secondary"]:hover, .stDownloadButton button[kind="secondary"]:hover, [data-testid="stPopover"] button:hover {
  border-color: var(--k-go) !important; }
.stButton button[kind="secondary"]:hover p, [data-testid="stPopover"] button:hover p { color: var(--k-go-text) !important; }
.stApp [data-baseweb="input"], .stApp [data-baseweb="select"] > div, .stApp [data-baseweb="textarea"] { border-radius: 10px; }
/* chosen items in a multi-select: soft green, readable in both modes */
[data-testid="stMultiSelectTagsContainer"] > span > span { background: var(--k-go-soft) !important; color: var(--k-go-text) !important; }
[data-testid="stMultiSelectTagsContainer"] > span > span * { color: var(--k-go-text) !important; fill: var(--k-go-text) !important; font-weight: 700; }
/* tabs: no leftover underline under the selected pill */
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"], .stTabs .react-aria-SelectionIndicator { display: none !important; }
/* segmented control */
[data-testid="stButtonGroup"] button p { font-weight: 600; }

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
.k-foot a { color: var(--k-go-text); text-decoration: none; font-weight: 700; }


.k-mark svg { width: 21px; height: 21px; fill: none; stroke: currentColor; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }

/* designed tables: kit.table() */
.k-tw { border: 1px solid var(--k-line); border-radius: 14px; overflow: auto; background: var(--k-surface); margin: 6px 0 14px; }
.k-t { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 14px; }
.k-t th { position: sticky; top: 0; z-index: 1; background: var(--k-surface-2); color: var(--k-muted); font-size: 12.5px;
  font-weight: 700; text-align: left; padding: 10px 14px; border-bottom: 1px solid var(--k-line); white-space: nowrap; }
.k-t th, .k-t td { border-left: 0 !important; border-right: 0 !important; border-top: 0 !important; }
.k-t td { padding: 11px 14px; border-bottom: 1px solid var(--k-line); color: var(--k-ink); vertical-align: middle; }
.k-t tr:last-child td { border-bottom: 0; }
.k-t tbody tr:hover td { background: var(--k-surface-2); }
.k-t .num { text-align: right; white-space: nowrap; font-weight: 600; }
.k-t th.num { text-align: right; }
.k-t .mut { color: var(--k-muted); }
.k-t .strong { font-weight: 700; }
.k-t .wrap { min-width: 180px; line-height: 1.45; }
.k-t code { white-space: normal; line-height: 1.9; }
.k-chip { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12.5px; font-weight: 700; white-space: nowrap;
  background: var(--k-neutral); color: var(--k-neutral-ink); }
.k-chip.good { background: var(--k-ok-soft); color: var(--k-ok); }
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
.k-why { display: grid; gap: 14px; margin: 4px 0 6px; }
.k-why-top { display: flex; justify-content: space-between; gap: 12px; align-items: baseline; margin-bottom: 6px; }
.k-why-top b { font-size: 14.5px; font-weight: 700; color: var(--k-ink); }
.k-why-top span { font-size: 12.5px; font-weight: 700; white-space: nowrap; }
.k-why-row.up .k-why-top span { color: var(--k-bad-ink); } .k-why-row.down .k-why-top span { color: var(--k-ok); }
.k-why-bar { height: 8px; border-radius: 4px; background: var(--k-line); overflow: hidden; }
.k-why-bar i { display: block; height: 100%; border-radius: 4px; }
.k-why-row.up i { background: var(--k-risk); } .k-why-row.down i { background: var(--k-safe); }
.k-detail { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 14px; }
.k-detail b { font-size: 18px; font-weight: 800; color: var(--k-ink); }
.k-detail span.m { color: var(--k-muted); font-size: 14px; }

/* message list: kit.messages() */
.k-msgs { border: 1px solid var(--k-line); border-radius: 14px; background: var(--k-surface); overflow: hidden; margin: 6px 0 14px; }
.k-msg { display: grid; grid-template-columns: 44px 1fr; gap: 12px; align-items: start; padding: 13px 16px; border-bottom: 1px solid var(--k-line); }
.k-msg:last-child { border-bottom: 0; }
.k-msg:hover { background: var(--k-surface-2); }
.k-msg .k-lang { margin-top: 1px; }
.k-msg p { margin: 0; font-size: 14.5px; line-height: 1.5; color: var(--k-ink); }
.k-msg small { display: block; color: var(--k-muted); font-size: 12.5px; margin-top: 2px; }

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
.k-mail.reply { background: var(--k-go-soft); color: var(--k-ink); border-color: transparent; }
.k-mail-h { font-size: 12.5px; font-weight: 700; color: var(--k-muted); margin: 0 0 6px; }

/* timeline: kit.timeline() */
.k-tl { border: 1px solid var(--k-line); border-radius: 14px; background: var(--k-surface); padding: 14px 16px 10px; margin: 6px 0 12px; }
.k-tl-row { display: grid; grid-template-columns: minmax(110px, 22%) 1fr; gap: 14px; align-items: center; padding: 9px 0; border-bottom: 1px solid var(--k-line); }
.k-tl-row:last-of-type { border-bottom: 0; }
.k-tl-row > div:first-child b { display: block; font-size: 14.5px; font-weight: 700; color: var(--k-ink); }
.k-tl-row > div:first-child small { font-size: 12.5px; color: var(--k-muted); }
.k-tl-track { position: relative; height: 26px; }
.k-tl-band { position: absolute; top: 4px; height: 18px; border-radius: 9px; background: var(--k-go-soft); }
.k-tl-mid { position: absolute; top: 8px; height: 10px; border-radius: 5px; background: var(--k-go); }
.k-tl-mid.late { background: var(--k-risk); }
.k-tl-lab { position: absolute; top: -1px; font-size: 11.5px; font-weight: 700; color: var(--k-muted); white-space: nowrap; transform: translateX(6px); }
.k-tl-grid { position: absolute; top: -4px; bottom: -4px; width: 1px; background: var(--k-line); }
.k-tl-shift { position: absolute; top: -6px; bottom: -6px; width: 2px; background: var(--k-risk); opacity: .7; }
.k-tl-axis { display: grid; grid-template-columns: minmax(110px, 22%) 1fr; gap: 14px; margin-top: 6px; }
.k-tl-axis > div:last-child { position: relative; height: 30px; }
.k-tl-axis > div:last-child span { position: absolute; transform: translateX(-50%); font-size: 11.5px; color: var(--k-muted); white-space: nowrap; }
.k-tl-axis > div:last-child span.shift { color: var(--k-bad-ink); font-weight: 700; }
.k-tl-legend { display: flex; gap: 18px; flex-wrap: wrap; font-size: 12.5px; color: var(--k-muted); margin-top: 6px; }
.k-tl-legend i { display: inline-block; width: 18px; height: 9px; border-radius: 5px; margin-right: 6px; vertical-align: 0; }

/* broadcast stage for on-screen previews */
.k-stage { border-radius: 16px; padding: 26px 24px; background: linear-gradient(135deg, #0b1f3a 0%, #13314f 55%, #0f2a2a 100%);
  border: 1px solid var(--k-line); display: flex; flex-wrap: wrap; gap: 14px 18px; align-items: flex-start; margin: 6px 0 10px; }

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
         badge: str = "Demo · invented data", theme: str = "bank"):
    """Page setup + product header. Call first, before any other st.* call."""
    st.set_page_config(page_title=f"{name} · {tagline}", page_icon=icon or mark, layout="wide" if wide else "centered")
    sk = SKINS[theme]
    f = sk["fonts"]
    fonts = (f"@import url('https://fonts.googleapis.com/css2?{f['url']}&display=swap');\n"
             f":root {{ --k-font: {f['body']}; --k-font-display: {f['display']}; --k-font-num: {f['num']}; --k-font-mono: {f['mono']}; }}")
    css = CSS.replace("@@FONTS@@", fonts).replace("@@TOKENS@@", _tokens(sk["light"], sk["dark"])) + sk["css"]
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(f'<div class="k-skin-{theme}" style="display:none"></div>', unsafe_allow_html=True)
    with st.container(key="k_sync"):
        st.iframe(THEME_SYNC, height=1)
    glyph = (f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[mark]}</svg>' if mark in ICONS else mark)
    st.markdown(
        f'<div class="k-head"><div class="k-brand"><div class="k-mark" aria-hidden="true">{glyph}</div>'
        f'<div><p class="k-name">{name}</p><div class="k-tag">{tagline}</div></div></div>'
        f'<div class="k-meta"><span class="k-demo">{badge}</span>{"<br>" + meta if meta else ""}</div></div>',
        unsafe_allow_html=True)


def answer(kicker: str, headline: str, body: str = "", stats: list[tuple[str, str]] | None = None, tone: str = "good",
           raw: bool = False):
    """The answer card. tone: good (green) | warn (amber) | bad (red). body may hold <b> tags; the rest is escaped."""
    tiles = "".join(f'<div class="k-tile"><span>{html.escape(a)}</span><b>{html.escape(b)}</b></div>'
                    for a, b in (stats or []))
    st.markdown(
        f'<div class="k-ans {"" if tone == "good" else tone}"><div class="k-kick">{html.escape(kicker)}</div>'
        f'<p class="k-h">{headline if raw else html.escape(headline)}</p>'
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
    if c["fmt"] and c["kind"] not in ("meter", "tags"):
        v = c["fmt"](v)
    k = c["kind"]
    e = "" if k == "tags" else html.escape(str(v))
    if k in ("chip", "lang") and e == "":
        return "<td></td>"
    if k == "chip":
        return f'<td><span class="k-chip {c["tones"].get(v, "")}">{e}</span></td>'
    if k == "lang":
        return f'<td><span class="k-lang">{e.upper()}</span></td>'
    if k == "code":
        return f'<td><code>{e}</code></td>'
    if k == "tags":  # v: list of (text, tone)
        return "<td>" + "".join(f'<span class="k-chip {t}" style="margin:2px 4px 2px 0">{html.escape(x)}</span>' for x, t in v) + "</td>"
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


def contrib(rows: list[tuple[str, float]], up: str = "raises risk", down: str = "lowers risk"):
    """Why-bars: one row per reason, red when it pushes the risk up, green when it pulls it down."""
    top = max((abs(v) for _, v in rows), default=0) or 1
    out = []
    for n, v in rows:
        rel = abs(v) / top
        size = "strongly" if rel >= 0.6 else "somewhat" if rel >= 0.3 else "slightly"
        out.append(f'<div class="k-why-row {"up" if v > 0 else "down"}"><div class="k-why-top"><b>{html.escape(n)}</b>'
                   f'<span>{size} {up if v > 0 else down}</span></div>'
                   f'<div class="k-why-bar"><i style="width:{max(rel, .04) * 100:.0f}%"></i></div></div>')
    st.markdown('<div class="k-why">' + "".join(out) + "</div>", unsafe_allow_html=True)


def messages(rows: list[dict]):
    """A clean message list (like an inbox): {lang, text, sub?}."""
    st.markdown('<div class="k-msgs">' + "".join(
        f'<div class="k-msg"><span class="k-lang">{html.escape(r["lang"].upper())}</span><div><p>{html.escape(r["text"])}</p>'
        + (f'<small>{html.escape(r["sub"])}</small>' if r.get("sub") else "") + "</div></div>" for r in rows) + "</div>",
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


def timeline(rows: list[dict], start: int, end: int, marker: tuple[int, str] | None = None, fmt=None):
    """Gantt-style timeline in minutes from midnight. rows: {label, sub, lo, hi, mid0, mid1, late?, text}."""
    span = max(end - start, 1)
    pos = lambda m: (m - start) / span * 100
    fmt = fmt or (lambda m: f"{int(m // 60) % 24:02d}:{int(m % 60):02d}")
    grid = "".join(f'<div class="k-tl-grid" style="left:{pos(t):.2f}%"></div>' for t in range(start, end + 1, 60))
    mark = f'<div class="k-tl-shift" style="left:{pos(marker[0]):.2f}%"></div>' if marker and start <= marker[0] <= end else ""
    body = "".join(
        f'<div class="k-tl-row"><div><b>{html.escape(r["label"])}</b><small>{html.escape(r.get("sub", ""))}</small></div>'
        f'<div class="k-tl-track">{grid}{mark}<div class="k-tl-band" style="left:{pos(r["lo"]):.2f}%;width:{pos(r["hi"]) - pos(r["lo"]):.2f}%"></div>'
        f'<div class="k-tl-mid{" late" if r.get("late") else ""}" style="left:{pos(r["mid0"]):.2f}%;width:{max(pos(r["mid1"]) - pos(r["mid0"]), .8):.2f}%"></div>'
        f'</div></div>' for r in rows)
    ticks = "".join(f'<span style="left:{pos(t):.2f}%">{fmt(t)}</span>' for t in range(start, end + 1, 60))
    if marker and start <= marker[0] <= end:
        ticks += f'<span class="shift" style="left:{pos(marker[0]):.2f}%;top:14px">{html.escape(marker[1])}</span>'
    st.markdown(f'<div class="k-tl">{body}<div class="k-tl-axis"><div></div><div>{ticks}</div></div></div>',
                unsafe_allow_html=True)


def demo(video: str, title: str, steps: str, extra=None):
    """The '1-min demo' + 'How it works' pair shown under the header on every app."""
    @st.dialog(title, width="large")
    def _show():
        st.video(video, autoplay=True)
    bar = st.container(horizontal=True, key="k_demo")
    if extra:
        extra(bar)
    if bar.button("▶  1-min demo", type="primary", key="demo_btn"):
        _show()
    with bar.popover("How it works"):
        st.markdown(steps)
    return bar


def footer(engine: str = ""):
    st.markdown(
        f'<div class="k-foot"><span>Built by Jānis Saulītis with AI{(" · " + engine) if engine else ""}</span>'
        f'<a href="{PORTFOLIO}" target="_blank" rel="noopener">See more tools</a></div>',
        unsafe_allow_html=True)
