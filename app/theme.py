"""Unicorn-sticker theme for the Streamlit app: navy outlines, mint / lavender / gold palette."""
from __future__ import annotations

import base64
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Russo+One&family=Noto+Sans+KR:wght@400;500;700&display=swap');
:root{--navy:#14193F;--mint:#8EF2C0;--mint-soft:#E9F8F0;--lav:#B9A2F7;--lav-deep:#6C4FD8;--gold:#FFC83D;--paper:#FBFAFF;}
html, body, [class*="css"], .stApp {font-family:'Noto Sans KR',sans-serif;}
.stApp{background-color:var(--paper);%BG%}
header[data-testid="stHeader"]{background:transparent;}
.block-container{max-width:860px;padding-top:2rem;}

/* headings: angular, slanted display type */
h1,h2,h3,.stSubheader{font-family:'Russo One','Noto Sans KR',sans-serif !important;letter-spacing:.01em;color:var(--navy);}
h2,h3{display:inline-block;transform:skewX(-6deg);padding:.15rem .7rem;margin-top:1.4rem;
  background:var(--mint);border:3px solid var(--navy);border-radius:4px;box-shadow:4px 4px 0 var(--navy);}
h3{background:var(--lav);}
h2,h3{margin-bottom:.9rem !important;}
.stButton>button p, .stDownloadButton>button p{font-family:'Russo One',sans-serif !important;}
h2 *, h3 *{transform:skewX(6deg);display:inline-block;}

/* hero */
.hero{text-align:center;margin:.2rem 0 1.2rem;}
.hero img{width:min(380px,80%);filter:drop-shadow(0 6px 0 rgba(20,25,63,.12));}
.hero .tag{font-family:'Russo One',sans-serif;color:var(--navy);margin-top:.4rem;font-size:1.05rem;letter-spacing:.02em;}
.hero .sub{color:#4B5080;font-size:.92rem;max-width:620px;margin:.3rem auto 0;}

/* cards */
div[data-testid="stFileUploader"] section, div[data-testid="stExpander"]{
  background:#fff;border:3px solid var(--navy);border-radius:12px;box-shadow:4px 4px 0 var(--navy);}
div[data-testid="stExpander"] details{border:none;}
div[data-testid="stMetric"]{background:#fff;border:3px solid var(--navy);border-radius:12px;box-shadow:4px 4px 0 var(--mint);padding:.8rem 1rem;}
div[data-testid="stMetricValue"]{font-family:'Russo One',sans-serif;color:var(--lav-deep);}
div[data-testid="stDataFrame"]{border:3px solid var(--navy);border-radius:10px;box-shadow:4px 4px 0 var(--lav);overflow:hidden;}
div[data-testid="stAlert"]{border:2px solid var(--navy);border-radius:10px;}

/* inputs */
div[data-baseweb="select"]>div, div[data-baseweb="input"]>div, div[data-baseweb="base-input"], textarea{
  border:2px solid var(--navy) !important;border-radius:8px !important;background:#fff !important;}

/* buttons: chunky sticker */
.stButton>button, .stDownloadButton>button{
  font-family:'Russo One',sans-serif;letter-spacing:.03em;border:3px solid var(--navy);border-radius:10px;
  box-shadow:4px 4px 0 var(--navy);transition:transform .08s, box-shadow .08s;}
.stButton>button:hover, .stDownloadButton>button:hover{transform:translate(-1px,-1px);box-shadow:6px 6px 0 var(--navy);}
.stButton>button:active, .stDownloadButton>button:active{transform:translate(3px,3px);box-shadow:1px 1px 0 var(--navy);}
.stButton>button[kind="primary"]{background:var(--lav-deep);color:#fff;font-size:1.1rem;padding:.65rem 1rem;}
.stButton>button[kind="primary"]:hover{background:#5B3FC4;color:#fff;border-color:var(--navy);}
.stDownloadButton>button{background:var(--gold);color:var(--navy);}

/* slider accent */
div[data-baseweb="slider"] div[role="slider"]{background:var(--lav-deep);border:3px solid var(--navy);}
hr{border-top:3px dashed var(--lav) !important;}
.footnote{color:#4B5080;font-size:.8rem;}
</style>
"""


def _data_uri(name: str, mime: str) -> str | None:
    p = ASSETS / name
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode() if p.exists() else None


def inject(st) -> None:
    bg = _data_uri("bg_pattern.jpg", "image/jpeg")
    bg_css = f"background-image:url('{bg}');background-size:520px;background-attachment:fixed;" if bg else ""
    st.markdown(CSS.replace("%BG%", bg_css), unsafe_allow_html=True)


def hero(st, tagline: str, sub: str) -> None:
    logo = _data_uri("logo_app.png", "image/png")
    if logo:
        st.markdown(f'<div class="hero"><img src="{logo}" alt="Ryoonicorn Theorem">'
                    f'<div class="tag">{tagline}</div><div class="sub">{sub}</div></div>', unsafe_allow_html=True)
    else:
        st.title("Ryoonicorn Theorem")
        st.caption(tagline)
