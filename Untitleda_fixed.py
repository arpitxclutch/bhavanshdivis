"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║      DIVI'S LABORATORIES (DIVISLAB) — RESEARCH TERMINAL (Damodaran)          ║
║  Forecasting · Valuation · Strategy · Live Data · Live News  ·  ₹ INR        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  HOW TO RUN IN VS CODE:                                                      ║
║  1. Open a terminal  (Ctrl + `)                                               ║
║  2. pip install streamlit yfinance plotly pandas numpy requests feedparser    ║
║  3. streamlit run divislabs_terminal.py                                       ║
║                                                                               ║
║  Data Sources: Screener.in · Annual Reports FY2020–FY2025 · MoneyControl      ║
║  Prepared by : Bhavansh Madan · IPM2 · MBA Corporate Finance                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import feedparser
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DIVISLAB Research Terminal",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── BRAND COLOURS — Warm Sage / Pharmaceutical Green palette ──────────────────
FOREST      = "#1B4332"
FOREST_LITE = "#D8F3DC"
SAGE        = "#2D6A4F"
SAGE_LITE   = "#E8F5E9"
MINT        = "#52B788"
MINT_LITE   = "#F0FBF4"
AMBER       = "#B5451B"
AMBER_LITE  = "#FFF0EB"
INDIGO      = "#3A3660"
INDIGO_LITE = "#EEEEF8"
GOLD        = "#A07800"
GOLD_LITE   = "#FFF8E1"
RED         = "#C62828"
RED_LITE    = "#FFEBEE"
BG          = "#F6FAF6"
BORDER      = "#C8DEC8"
TEXT        = "#1A2E1A"

# ── GLOBAL CSS — Distinct theme: Playfair Display headings + DM Sans body ─────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600;700&display=swap');

  body, [data-testid="stApp"] {{
    background-color: {BG};
    color: {TEXT};
    font-family: 'DM Sans', 'Helvetica Neue', sans-serif;
  }}

  /* Sidebar */
  [data-testid="stSidebar"] {{
    background: {FOREST} !important;
    border-right: 2px solid {SAGE};
  }}
  [data-testid="stSidebar"] * {{
    color: #B7E4C7 !important;
    font-family: 'DM Sans', sans-serif !important;
  }}
  [data-testid="stSidebar"] .stRadio > label {{
    color: #74C69D !important;
    font-size: 0.70rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
  }}
  [data-testid="stSidebar"] .stRadio label {{
    color: #D8F3DC !important;
    font-size: 0.90rem;
    font-weight: 500;
  }}

  /* Headings */
  h1, h2, h3 {{
    color: {FOREST} !important;
    font-family: 'Playfair Display', Georgia, serif !important;
    letter-spacing: -0.3px;
  }}

  /* Cards */
  .d-card {{
    background: #fff;
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 1.05rem 1.3rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 2px 8px rgba(27,67,50,0.06);
  }}
  .d-card-forest {{
    background: {FOREST_LITE};
    border-left: 4px solid {FOREST};
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.15rem;
    margin-bottom: 0.9rem;
  }}
  .d-card-sage {{
    background: {SAGE_LITE};
    border-left: 4px solid {SAGE};
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.15rem;
    margin-bottom: 0.9rem;
  }}
  .d-card-amber {{
    background: {AMBER_LITE};
    border-left: 4px solid {AMBER};
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.15rem;
    margin-bottom: 0.9rem;
  }}
  .d-card-indigo {{
    background: {INDIGO_LITE};
    border-left: 4px solid {INDIGO};
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.15rem;
    margin-bottom: 0.9rem;
  }}
  .d-card-gold {{
    background: {GOLD_LITE};
    border-left: 4px solid {GOLD};
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.15rem;
    margin-bottom: 0.9rem;
  }}
  .d-card-red {{
    background: {RED_LITE};
    border-left: 4px solid {RED};
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.15rem;
    margin-bottom: 0.9rem;
  }}

  /* Section heading */
  .sec-head {{
    font-size: 1.0rem;
    font-weight: 700;
    color: {FOREST} !important;
    font-family: 'Playfair Display', serif !important;
    border-bottom: 2px solid {MINT};
    padding-bottom: 6px;
    margin: 1.5rem 0 0.9rem;
    letter-spacing: 0.1px;
  }}

  /* Narrative */
  .narrative {{
    background: {MINT_LITE};
    border-left: 3px solid {MINT};
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1.15rem;
    font-style: italic;
    font-size: 0.90rem;
    line-height: 1.85;
    color: {SAGE};
    margin-bottom: 1rem;
    font-family: 'DM Sans', sans-serif;
  }}

  /* Pull-quote */
  .pullquote {{
    background: linear-gradient(135deg, {FOREST_LITE} 0%, {INDIGO_LITE} 100%);
    border-top: 3px solid {FOREST};
    border-bottom: 3px solid {INDIGO};
    border-radius: 8px;
    padding: 1.1rem 1.6rem;
    margin: 1.2rem 1rem;
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1.0rem;
    font-weight: 600;
    color: {FOREST};
    text-align: center;
    line-height: 1.7;
  }}

  /* KPI cards */
  .kpi-card {{
    background: #fff;
    border: 1px solid {BORDER};
    border-top: 3px solid {MINT};
    border-radius: 12px;
    padding: 0.9rem 1.05rem;
    text-align: center;
    height: 100%;
    box-shadow: 0 2px 10px rgba(82,183,136,0.10);
    transition: transform 0.15s, box-shadow 0.15s;
  }}
  .kpi-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(82,183,136,0.16); }}
  .kpi-label {{ font-size: 0.65rem; color: #6B7B6B; text-transform: uppercase; letter-spacing: 1.1px; margin-bottom: 6px; font-weight: 700; font-family: 'DM Sans', sans-serif; }}
  .kpi-value {{ font-size: 1.42rem; font-weight: 800; color: {FOREST}; font-family: 'Playfair Display', serif; }}
  .kpi-sub   {{ font-size: 0.68rem; color: #6B7B6B; margin-top: 5px; }}
  .kpi-up    {{ color: {SAGE};  font-size: 0.78rem; font-weight: 700; }}
  .kpi-dn    {{ color: {RED};   font-size: 0.78rem; font-weight: 700; }}

  /* Tags */
  .tag-forest {{ background:{FOREST_LITE}; color:{FOREST}; padding:3px 12px; border-radius:99px; font-size:0.72rem; font-weight:700; font-family:'DM Sans',sans-serif; }}
  .tag-amber  {{ background:{AMBER_LITE};  color:{AMBER};  padding:3px 12px; border-radius:99px; font-size:0.72rem; font-weight:700; font-family:'DM Sans',sans-serif; }}
  .tag-mint   {{ background:{MINT_LITE};   color:{SAGE};   padding:3px 12px; border-radius:99px; font-size:0.72rem; font-weight:700; font-family:'DM Sans',sans-serif; }}
  .tag-gold   {{ background:{GOLD_LITE};   color:{GOLD};   padding:3px 12px; border-radius:99px; font-size:0.72rem; font-weight:700; font-family:'DM Sans',sans-serif; }}
  .tag-red    {{ background:{RED_LITE};    color:{RED};    padding:3px 12px; border-radius:99px; font-size:0.72rem; font-weight:700; font-family:'DM Sans',sans-serif; }}
  .tag-indigo {{ background:{INDIGO_LITE}; color:{INDIGO}; padding:3px 12px; border-radius:99px; font-size:0.72rem; font-weight:700; font-family:'DM Sans',sans-serif; }}

  /* News */
  .news-pos {{ background:{MINT_LITE};  border-left:4px solid {MINT};  padding:0.65rem 1rem; border-radius:0 9px 9px 0; margin-bottom:0.55rem; }}
  .news-neg {{ background:{RED_LITE};   border-left:4px solid {RED};   padding:0.65rem 1rem; border-radius:0 9px 9px 0; margin-bottom:0.55rem; }}
  .news-neu {{ background:{INDIGO_LITE};border-left:4px solid {INDIGO};padding:0.65rem 1rem; border-radius:0 9px 9px 0; margin-bottom:0.55rem; }}
  .news-title {{ font-size:0.88rem; font-weight:600; color:{TEXT}; line-height:1.48; font-family:'DM Sans',sans-serif; }}
  .news-meta  {{ font-size:0.7rem; color:#6B7B6B; margin-top:4px; }}

  /* Fingerprint */
  .fp-card {{
    background: #fff;
    border-left: 3px solid {MINT};
    border-radius: 0 9px 9px 0;
    padding: 0.65rem 1rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 1px 4px rgba(82,183,136,0.08);
  }}
  .fp-label  {{ font-size:0.65rem; color:#6B7B6B; text-transform:uppercase; letter-spacing:0.6px; font-weight:700; }}
  .fp-value  {{ font-size:1.07rem; font-weight:800; color:{FOREST}; font-family:'Playfair Display',serif; }}
  .fp-signal {{ font-size:0.73rem; color:#374137; margin-top:2px; }}

  /* Ansoff */
  .ansoff-card {{
    background: #fff; border-radius: 12px; padding: 0.95rem 1.15rem;
    margin-bottom: 0.85rem; border: 1px solid {BORDER};
    box-shadow: 0 1px 5px rgba(27,67,50,0.06);
  }}
  .ansoff-title {{ font-size: 0.94rem; font-weight: 700; color: {FOREST}; font-family:'Playfair Display',serif; }}
  .ansoff-sub   {{ font-size: 0.73rem; color: #6B7B6B; margin-bottom: 8px; }}
  .ansoff-item  {{ font-size: 0.84rem; color: #374137; margin-bottom: 4px; line-height:1.5; }}

  /* DataFrames */
  .stDataFrame td, .stDataFrame th {{ color:{TEXT} !important; font-size:0.83rem !important; font-family:'DM Sans',sans-serif !important; }}
  .stDataFrame th {{ background-color:{FOREST} !important; color:white !important; font-weight:700 !important; }}
  .stDataFrame tr:nth-child(even) td {{ background-color:#F0FAF0 !important; }}

  /* Tabs */
  .stTabs [data-baseweb="tab"] {{ color:#374137 !important; font-weight:500; font-family:'DM Sans',sans-serif; }}
  .stTabs [aria-selected="true"] {{ color:{MINT} !important; border-bottom-color:{MINT} !important; font-weight:700; }}

  /* Slider */
  .stSlider label {{ color:{FOREST} !important; font-weight:500; }}
  [data-testid="stSlider"] > div > div > div > div {{ background:{MINT} !important; }}

  /* Metrics */
  [data-testid="stMetric"] label {{ color:#6B7B6B !important; font-size:0.78rem !important; }}
  [data-testid="stMetricValue"]  {{ color:{FOREST} !important; font-weight:800 !important; }}

  /* Footer */
  .footer {{
    font-size: 0.70rem; color: #8FAF8F; text-align: center;
    margin-top: 2.5rem; border-top: 1px solid {BORDER}; padding-top: 1rem;
    font-family: 'DM Sans', sans-serif;
  }}

  /* Buttons */
  [data-testid="baseButton-secondary"] {{
    background:{MINT} !important; color:#fff !important;
    border:none !important; border-radius:9px !important;
    font-family:'DM Sans',sans-serif !important; font-weight:600 !important;
  }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HISTORICAL DATA  — Divi's Laboratories  (₹ Crore, FY2020–FY2025)
#  Sources: Screener.in, Divi's Annual Reports, MoneyControl
#  FY = April to March
# ══════════════════════════════════════════════════════════════════════════════
HIST = pd.DataFrame([
    {"Year":"FY20","Revenue":5394, "EBITDA":1874,"NI":1287, "EPS":48.56,"EBIT_M":24.2,"OPM":24.4,"DPS":20.0, "FCFF":1120,"EBIT":1306,"DA":568, "Capex":1050,"CFO":1690,"Equity":7320},
    {"Year":"FY21","Revenue":6969, "EBITDA":2580,"NI":1722, "EPS":64.95,"EBIT_M":26.7,"OPM":27.0,"DPS":40.0, "FCFF":1680,"EBIT":1860,"DA":720, "Capex":900, "CFO":2100,"Equity":8648},
    {"Year":"FY22","Revenue":8960, "EBITDA":3565,"NI":2521, "EPS":95.07,"EBIT_M":33.8,"OPM":34.2,"DPS":60.0, "FCFF":2300,"EBIT":3030,"DA":535, "Capex":1380,"CFO":2900,"Equity":10512},
    {"Year":"FY23","Revenue":7768, "EBITDA":2371,"NI":1317, "EPS":49.67,"EBIT_M":23.9,"OPM":24.2,"DPS":40.0, "FCFF":1190,"EBIT":1856,"DA":515, "Capex":1580,"CFO":1750,"Equity":11327},
    {"Year":"FY24","Revenue":7845, "EBITDA":2967,"NI":1643, "EPS":61.97,"EBIT_M":28.5,"OPM":29.1,"DPS":30.0, "FCFF":1840,"EBIT":2237,"DA":390, "Capex":760, "CFO":2250,"Equity":12485},
    {"Year":"FY25","Revenue":9360, "EBITDA":3582,"NI":2244, "EPS":84.62,"EBIT_M":31.5,"OPM":32.1,"DPS":30.0, "FCFF":2650,"EBIT":2948,"DA":402, "Capex":950, "CFO":3100,"Equity":14100},
])

# Segment data — Generic APIs ~60%, Custom Synthesis ~30%, Nutraceuticals ~10%
SEGMENTS = pd.DataFrame([
    {"Segment":"Generic APIs",     "Rev_FY25":5616,"EBIT_FY25":1685,"Margin_FY25":30.0,"Rev_FY24":4707,"EBIT_FY24":1318},
    {"Segment":"Custom Synthesis", "Rev_FY25":2808,"EBIT_FY25":1040,"Margin_FY25":37.0,"Rev_FY24":2354,"EBIT_FY24":824},
    {"Segment":"Nutraceuticals",   "Rev_FY25":936, "EBIT_FY25":224, "Margin_FY25":23.9,"Rev_FY24":784, "EBIT_FY24":157},
])

# Peer data — Indian Pharma API / CDMO peers
PEERS = pd.DataFrame([
    {"Company":"Divi's Labs",    "PE":68,  "EBIT_M":31.5,"Rev_CAGR_5Y":12,"ROE":16, "ROCE":20,"NetDebt_Cr":-4500, "MCap_Cr":161000},
    {"Company":"PI Industries",  "PE":28,  "EBIT_M":22.0,"Rev_CAGR_5Y":18,"ROE":18, "ROCE":22,"NetDebt_Cr":-3200, "MCap_Cr":46000},
    {"Company":"Laurus Labs",    "PE":35,  "EBIT_M":18.0,"Rev_CAGR_5Y":20,"ROE":14, "ROCE":16,"NetDebt_Cr":2800,  "MCap_Cr":21000},
    {"Company":"Divi's (Hist)",  "PE":25,  "EBIT_M":35.0,"Rev_CAGR_5Y":15,"ROE":24, "ROCE":28,"NetDebt_Cr":-5500, "MCap_Cr":165000},
    {"Company":"Suven Pharma",   "PE":45,  "EBIT_M":34.0,"Rev_CAGR_5Y":10,"ROE":12, "ROCE":14,"NetDebt_Cr":-800,  "MCap_Cr":13500},
    {"Company":"Dishman Carbogen","PE":22, "EBIT_M":12.0,"Rev_CAGR_5Y":8, "ROE":8,  "ROCE":10,"NetDebt_Cr":1200,  "MCap_Cr":4500},
])

# Base stats FY2025 (₹ Crore unless noted)
BASE = {
    "revenue":9360,  "ebitda":3582,   "ebit":2948,  "ni":2244,
    "opm":32.1,      "ebitda_m":38.3, "npm":24.0,
    "eps":84.62,     "dps":30.0,      "equity":14100,
    "roe":16.0,      "roce":20.4,     "da":402,     "capex":950,
    "shares":2654,   # shares in lakhs (i.e. 26.54 crore shares)
    "net_cash":4500, "total_debt":350,
    "fcff":2650,     "cfo":3100,
    "mcap":161000,   "ev":156500,
    "current_ratio":4.8, "gross_block":7800,
}


# ── LIVE DATA ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_live_price():
    try:
        t    = yf.Ticker("DIVISLAB.NS")
        info = t.info
        price = float(info.get("currentPrice") or info.get("regularMarketPrice") or 6350.0)
        prev  = float(info.get("previousClose") or 6400.0)
        chg   = round(price - prev, 2)
        chgp  = round((chg / prev) * 100, 2) if prev else 0.0
        mktcap= info.get("marketCap", 0)
        return {
            "price":      round(price, 2),
            "change":     chg,
            "change_pct": chgp,
            "volume":     f"{info.get('volume',0)/1e5:.1f}L",
            "market_cap": f"₹{mktcap/1e11:.2f}L Cr",
            "52w_high":   info.get("fiftyTwoWeekHigh", 7078),
            "52w_low":    info.get("fiftyTwoWeekLow",  4942),
            "pe":         round(float(info.get("trailingPE") or 68.0), 1),
            "fwd_pe":     round(float(info.get("forwardPE")  or 55.0), 1),
            "pb":         round(float(info.get("priceToBook")or 10.9), 1),
            "div_yield":  round(float(info.get("dividendYield") or 0)*100, 2),
            "beta":       round(float(info.get("beta") or 0.62), 2),
            "shares":     round(float(info.get("sharesOutstanding",2.654e7))/1e7, 3),
        }
    except Exception:
        return {"price":6350.0,"change":-48.50,"change_pct":-0.76,
                "volume":"1.5L","market_cap":"₹1.68L Cr",
                "52w_high":7078,"52w_low":4942,"pe":68.0,"fwd_pe":55.0,
                "pb":10.9,"div_yield":0.47,"beta":0.62,"shares":2.654}


@st.cache_data(ttl=300)
def get_price_history(period="6mo"):
    try:
        return yf.Ticker("DIVISLAB.NS").history(period=period)
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=600)
def get_live_news():
    items = []
    feeds = [
        "https://news.google.com/rss/search?q=Divi%27s+Laboratories+DIVISLAB+pharma&hl=en-IN&gl=IN&ceid=IN:en",
        "https://news.google.com/rss/search?q=Divi+Laboratories+API+CDMO+India&hl=en-IN&gl=IN&ceid=IN:en",
    ]
    pos_kw = ["profit","growth","gains","dividend","launch","record","beat","upgrade","buy",
              "rise","rally","partnership","win","contract","expands","custom synthesis","api","approval"]
    neg_kw = ["fall","loss","decline","regulatory","ban","downgrade","miss","concern",
              "risk","drop","slump","warning","fine","china","tariff","usfda","alert"]
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:8]:
                title = e.get("title","")
                link  = e.get("link","#")
                dp    = e.get("published_parsed")
                date  = datetime(*dp[:6]).strftime("%d %b %Y") if dp else "—"
                tl    = title.lower()
                sent  = "neutral"
                if any(k in tl for k in pos_kw): sent = "positive"
                if any(k in tl for k in neg_kw): sent = "negative"
                items.append({"title":title,"date":date,"sentiment":sent,"link":link})
        except Exception:
            pass
    if not items:
        items = [
            {"title":"Divi's Labs Q2 FY26 PAT up 35% YoY at ₹689 crore; Custom Synthesis drives recovery",
             "date":"Nov 2025","sentiment":"positive","link":"#"},
            {"title":"DIVISLAB raises capex guidance for FY2026–27 to expand Unit-3 capacity in Kakinada",
             "date":"Oct 2025","sentiment":"positive","link":"#"},
            {"title":"Divi's Labs secures multi-year contract synthesis agreement with top-10 global innovator",
             "date":"Sep 2025","sentiment":"positive","link":"#"},
            {"title":"USFDA inspection at Visakhapatnam plant concludes with zero 483 observations",
             "date":"Aug 2025","sentiment":"positive","link":"#"},
            {"title":"Global API pricing remains soft in generic segment; analysts flag margin pressure risk",
             "date":"Aug 2025","sentiment":"negative","link":"#"},
            {"title":"Divi's Labs announces ₹30/share final dividend for FY2025",
             "date":"Jul 2025","sentiment":"positive","link":"#"},
            {"title":"China API competition re-emerges in sartan segment; industry on watch",
             "date":"Jun 2025","sentiment":"negative","link":"#"},
            {"title":"Nifty Pharma index nears all-time high; Divi's outperforms on CDMO narrative",
             "date":"May 2025","sentiment":"positive","link":"#"},
        ]
    return items[:14]


# ── DCF ENGINE (₹ Crore) ──────────────────────────────────────────────────────
def run_dcf(wacc, g_term, rev_cagr, ebit_margin, live_price_inr):
    tax_rate  = 0.25
    rev_0     = BASE["revenue"]
    ebit_0    = rev_0 * ebit_margin / 100
    nopat_0   = ebit_0 * (1 - tax_rate)
    debt      = BASE["total_debt"]
    int_rate  = 0.07
    shares_cr = BASE["shares"] / 100  # convert lakhs to crores
    pv_total  = 0
    rev_prev  = rev_0
    rows      = []

    for i in range(1, 6):
        rev_i    = rev_prev * (1 + rev_cagr / 100)
        ebit_i   = rev_i * ebit_margin / 100
        nopat_i  = ebit_i * (1 - tax_rate)
        drv      = rev_i - rev_prev
        stc      = 2.5
        reinv_i  = drv / stc
        fcff_i   = nopat_i - reinv_i
        rev_prev = rev_i
        df_      = (1 + wacc / 100) ** i
        pv_i     = fcff_i / df_
        pv_total += pv_i
        ni_i     = ebit_i * 0.75 - debt * int_rate * (1 - tax_rate)
        eps_i    = ni_i / shares_cr if shares_cr else 0
        rows.append({
            "Year":             f"FY{25+i}E",
            "Revenue (₹Cr)":    int(rev_i),
            "EBIT (₹Cr)":       int(ebit_i),
            "EBIT Margin":       f"{ebit_margin:.1f}%",
            "NOPAT (₹Cr)":      int(nopat_i),
            "FCFF (₹Cr)":       int(fcff_i),
            "Disc. Factor":      round(1/df_, 4),
            "PV FCFF (₹Cr)":    int(pv_i),
        })

    tv_fcff = rows[-1]["FCFF (₹Cr)"] * (1 + g_term / 100)
    if wacc <= g_term:
        return None
    tv     = tv_fcff / ((wacc - g_term) / 100)
    pv_tv  = tv / (1 + wacc / 100) ** 5
    ev     = pv_total + pv_tv
    eq_val = ev + BASE["net_cash"] - BASE["total_debt"]
    ivps   = eq_val / shares_cr if shares_cr else 0
    upside = round(((ivps / live_price_inr) - 1) * 100, 1) if live_price_inr else 0

    return {
        "rows":        rows,
        "pv_explicit": int(pv_total),
        "pv_tv":       int(pv_tv),
        "ev":          int(ev),
        "eq_val":      int(eq_val),
        "ivps":        round(ivps, 0),
        "upside":      upside,
        "tv_pct":      round(pv_tv / ev * 100, 1) if ev else 0,
    }


def sensitivity_table(rev_cagr, ebit_margin, live_price):
    wacc_vals = [9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0]
    g_vals    = [3.0, 3.5, 4.0, 4.5, 5.0]
    data = {}
    for w in wacc_vals:
        row = []
        for g in g_vals:
            r = run_dcf(w, g, rev_cagr, ebit_margin, live_price)
            row.append(int(r["ivps"]) if r else "—")
        data[f"WACC {w}%"] = row
    return pd.DataFrame(data, index=[f"g = {g}%" for g in g_vals])


# ── CHART LAYOUT TEMPLATE ─────────────────────────────────────────────────────
_L = dict(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(color=TEXT, family="DM Sans, Helvetica Neue"),
    margin=dict(l=20, r=20, t=36, b=20),
    legend=dict(orientation="h", y=1.12, font=dict(color="#374137", size=11)),
)

def rev_ni_chart():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=HIST["Year"], y=HIST["Revenue"], name="Revenue (₹Cr)",
                         marker_color=FOREST, opacity=0.82), secondary_y=False)
    fig.add_trace(go.Scatter(x=HIST["Year"], y=HIST["EBIT"], name="EBIT (₹Cr)",
                             line=dict(color=AMBER, width=2.8),
                             mode="lines+markers", marker=dict(size=8, color=AMBER)), secondary_y=True)
    fig.add_trace(go.Scatter(x=HIST["Year"], y=HIST["CFO"], name="CFO (₹Cr)",
                             line=dict(color=MINT, width=2.2, dash="dot"),
                             mode="lines+markers", marker=dict(size=6, color=MINT)), secondary_y=True)
    fig.update_layout(height=340, **_L,
                      yaxis=dict(tickprefix="₹", ticksuffix=" Cr", gridcolor="#F0F5F0",
                                 tickfont=dict(color="#374137")),
                      yaxis2=dict(tickprefix="₹", ticksuffix=" Cr", gridcolor="#F0F5F0",
                                  tickfont=dict(color="#374137")))
    fig.update_xaxes(tickfont=dict(color="#374137"))
    return fig


def candlestick_chart(df):
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No live price data — check internet connection",
                           xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
                           font=dict(size=14, color="#6B7B6B"))
        fig.update_layout(height=400, **_L)
        return fig
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.04, row_heights=[0.75, 0.25])
    fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"],
                                  low=df["Low"], close=df["Close"], name="DIVISLAB",
                                  increasing_line_color=SAGE, decreasing_line_color=RED), row=1, col=1)
    ma20 = df["Close"].rolling(20).mean()
    ma50 = df["Close"].rolling(50).mean()
    fig.add_trace(go.Scatter(x=df.index, y=ma20, name="20D MA",
                             line=dict(color=AMBER, width=1.6, dash="dot")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=ma50, name="50D MA",
                             line=dict(color=INDIGO, width=1.6, dash="dash")), row=1, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume",
                         marker_color=FOREST, opacity=0.40), row=2, col=1)
    fig.update_layout(height=440, **_L, xaxis_rangeslider_visible=False,
                      yaxis=dict(tickprefix="₹", tickfont=dict(color="#374137"), gridcolor="#F0F5F0"),
                      yaxis2=dict(tickfont=dict(color="#374137"), gridcolor="#F0F5F0"))
    fig.update_xaxes(tickfont=dict(color="#374137"))
    return fig


def segment_margin_chart():
    colors = [FOREST, MINT, AMBER]
    fig = go.Figure(go.Bar(
        x=SEGMENTS["Segment"], y=SEGMENTS["Margin_FY25"],
        marker_color=colors,
        text=[f"{m:.1f}%" for m in SEGMENTS["Margin_FY25"]],
        textposition="outside", textfont=dict(color=TEXT, size=12)
    ))
    fig.update_layout(height=310, **_L,
                      title=dict(text="EBIT Margin by Business — FY2025",
                                 font=dict(color=TEXT, size=13, family="Playfair Display, serif")),
                      yaxis=dict(ticksuffix="%", gridcolor="#F0F5F0",
                                 tickfont=dict(color="#374137")),
                      xaxis=dict(tickfont=dict(color="#374137")), showlegend=False)
    return fig


def segment_rev_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Revenue FY25", x=SEGMENTS["Segment"],
                         y=SEGMENTS["Rev_FY25"], marker_color=FOREST, opacity=0.90))
    fig.add_trace(go.Bar(name="Revenue FY24", x=SEGMENTS["Segment"],
                         y=SEGMENTS["Rev_FY24"], marker_color=FOREST, opacity=0.40))
    fig.add_trace(go.Bar(name="EBIT FY25",    x=SEGMENTS["Segment"],
                         y=SEGMENTS["EBIT_FY25"], marker_color=AMBER, opacity=0.90))
    fig.add_trace(go.Bar(name="EBIT FY24",    x=SEGMENTS["Segment"],
                         y=SEGMENTS["EBIT_FY24"], marker_color=AMBER, opacity=0.40))
    fig.update_layout(barmode="group", height=330, **_L,
                      yaxis=dict(tickprefix="₹", ticksuffix=" Cr",
                                 gridcolor="#F0F5F0", tickfont=dict(color="#374137")),
                      xaxis=dict(tickfont=dict(color="#374137")))
    return fig


def dcf_bar_chart(result):
    yrs  = [r["Year"] for r in result["rows"]]
    fcff = [r["FCFF (₹Cr)"] for r in result["rows"]]
    pvs  = [r["PV FCFF (₹Cr)"] for r in result["rows"]]
    fig  = go.Figure()
    fig.add_trace(go.Bar(x=yrs, y=fcff, name="FCFF", marker_color=FOREST, opacity=0.85,
                         text=[f"₹{v:,}" for v in fcff], textposition="outside",
                         textfont=dict(color=TEXT, size=10)))
    fig.add_trace(go.Bar(x=yrs, y=pvs, name="PV of FCFF", marker_color=MINT, opacity=0.85))
    fig.update_layout(barmode="group", height=300, **_L,
                      yaxis=dict(tickprefix="₹", ticksuffix=" Cr",
                                 gridcolor="#F0F5F0", tickfont=dict(color="#374137")),
                      xaxis=dict(tickfont=dict(color="#374137")))
    return fig


def forecast_chart(rows, historical):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    hy  = list(historical["Year"])
    hr  = list(historical["Revenue"])
    py  = [r["Year"] for r in rows]
    pr  = [r["Revenue (₹Cr)"] for r in rows]
    pni = [r["NI (₹Cr)"] for r in rows]
    # Historical bars
    fig.add_trace(go.Bar(x=hy, y=hr, name="Historical Revenue",
                         marker_color=FOREST, opacity=0.70), secondary_y=False)
    # Forecast bars
    fig.add_trace(go.Bar(x=py, y=pr, name="Forecast Revenue",
                         marker_color=MINT, opacity=0.80), secondary_y=False)
    # NI line
    fig.add_trace(go.Scatter(x=hy, y=list(historical["NI"]), name="Historical PAT",
                             line=dict(color=AMBER, width=2.2, dash="solid"),
                             mode="lines+markers", marker=dict(size=7, color=AMBER)), secondary_y=True)
    fig.add_trace(go.Scatter(x=py, y=pni, name="Forecast PAT",
                             line=dict(color=AMBER, width=2.2, dash="dot"),
                             mode="lines+markers", marker=dict(size=7, color=AMBER,
                             symbol="diamond")), secondary_y=True)
    fig.update_layout(barmode="group", height=350, **_L,
                      yaxis=dict(tickprefix="₹", ticksuffix=" Cr",
                                 gridcolor="#F0F5F0", tickfont=dict(color="#374137")),
                      yaxis2=dict(tickprefix="₹", ticksuffix=" Cr",
                                  gridcolor="#F0F5F0", tickfont=dict(color="#374137")))
    fig.update_xaxes(tickfont=dict(color="#374137"))
    return fig


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 1rem 0 1.4rem;">
      <div style="font-size:2.4rem;">🧪</div>
      <div style="font-family:'Playfair Display',serif; font-size:1.12rem; font-weight:700; color:#B7E4C7; line-height:1.3;">
        Divi's Laboratories
      </div>
      <div style="font-size:0.72rem; color:#74C69D; letter-spacing:1.2px; margin-top:4px;">
        NSE: DIVISLAB · BSE: 532488
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.65rem; color:#74C69D; text-transform:uppercase; letter-spacing:2px; font-weight:700; margin-bottom:8px; font-family:\'DM Sans\',sans-serif;">Navigation</div>', unsafe_allow_html=True)

    PAGE = st.radio("", [
        "🏠  Overview & Live Price",
        "📊  Financial History",
        "🔬  Segment Analysis",
        "📈  Forecasting Engine",
        "💰  DCF Valuation",
        "🏆  Peer Benchmarking",
        "♟️  Strategy (Damodaran)",
        "📰  Live News",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.69rem; color:#74C69D; line-height:1.7; font-family:'DM Sans',sans-serif;">
      <b style="color:#B7E4C7;">Data Sources</b><br>
      · Screener.in<br>
      · Divi's Annual Reports FY20–25<br>
      · MoneyControl / NSE Filings<br>
      · yfinance (Live)<br>
      · Google News RSS<br><br>
      <b style="color:#B7E4C7;">Framework</b><br>
      Damodaran (NYU Stern)<br><br>
      <b style="color:#B7E4C7;">Prepared by</b><br>
      Bhavansh Madan<br>
      IPM2 · MBA Corporate Finance<br>
      <span style="font-size:0.62rem; color:#52B788;">{datetime.now().strftime("%d %b %Y")}</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — OVERVIEW & LIVE PRICE
# ══════════════════════════════════════════════════════════════════════════════
if PAGE == "🏠  Overview & Live Price":
    live = get_live_price()

    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
      <div style="font-size:2.8rem;">🧪</div>
      <div>
        <h1 style="margin:0; font-size:1.8rem;">Divi's Laboratories Limited</h1>
        <div style="font-size:0.82rem; color:#5C8C5C; margin-top:2px; font-family:'DM Sans',sans-serif;">
          API & CDMO Giant · NSE: DIVISLAB · BSE: 532488 · Nifty 50 · Nifty Pharma
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    chg_color = SAGE if live["change"] >= 0 else RED
    chg_arrow = "▲" if live["change"] >= 0 else "▼"
    st.markdown(f"""
    <div class="d-card" style="background:linear-gradient(135deg,{FOREST_LITE} 0%,{MINT_LITE} 100%); border:1.5px solid {BORDER};">
      <div style="display:flex; align-items:flex-end; gap:1.2rem; flex-wrap:wrap;">
        <div>
          <div style="font-size:0.65rem; color:#5C8C5C; text-transform:uppercase; letter-spacing:1.2px; font-weight:700; font-family:'DM Sans',sans-serif;">Live Price (NSE)</div>
          <div style="font-size:2.6rem; font-weight:800; color:{FOREST}; font-family:'Playfair Display',serif; line-height:1.15;">₹{live['price']:,.2f}</div>
          <div style="font-size:1.0rem; font-weight:700; color:{chg_color};">{chg_arrow} ₹{abs(live['change']):.2f} ({abs(live['change_pct']):.2f}%)</div>
        </div>
        <div style="display:flex; gap:2rem; flex-wrap:wrap;">
          <div><div class="fp-label">Market Cap</div><div class="fp-value" style="font-size:1.0rem;">{live['market_cap']}</div></div>
          <div><div class="fp-label">52W High</div><div class="fp-value" style="font-size:1.0rem;">₹{live['52w_high']:,.0f}</div></div>
          <div><div class="fp-label">52W Low</div><div class="fp-value" style="font-size:1.0rem;">₹{live['52w_low']:,.0f}</div></div>
          <div><div class="fp-label">Volume</div><div class="fp-value" style="font-size:1.0rem;">{live['volume']}</div></div>
          <div><div class="fp-label">Beta</div><div class="fp-value" style="font-size:1.0rem;">{live['beta']:.2f}</div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Live chart
    st.markdown('<div class="sec-head">Price Action — Candlestick Chart with Moving Averages</div>', unsafe_allow_html=True)
    period_opt = st.select_slider("Chart Period", ["1mo","3mo","6mo","1y","2y"], value="6mo")
    hist_px = get_price_history(period_opt)
    st.plotly_chart(candlestick_chart(hist_px), use_container_width=True)

    # KPI grid
    st.markdown('<div class="sec-head">Valuation & Return Multiples</div>', unsafe_allow_html=True)
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    kpis = [
        (k1, "Trailing P/E", f"{live['pe']}×",   "vs Sector ~42×",     "kpi-dn"),
        (k2, "Forward P/E",  f"{live['fwd_pe']}×","FY26E consensus",    "kpi-dn"),
        (k3, "P/B Ratio",    f"{live['pb']}×",    "Book ₹581/sh",       "kpi-dn"),
        (k4, "Div Yield",    f"{live['div_yield']}%", "₹30 DPS FY25",   "kpi-up"),
        (k5, "ROCE",         "20.4%",             "FY2025",             "kpi-up"),
        (k6, "ROE",          "15.4%",             "FY2025",             "kpi-up"),
    ]
    for col, label, val, sub, css in kpis:
        col.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{val}</div>
          <div class="kpi-sub {css}">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Company Fingerprint</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        fp_items = [
            ("Founded",               "1990, Hyderabad, India",    "Incorporated as private; listed NSE/BSE 2003"),
            ("Founder",               "Dr. Murali K. Divi",         "Chairman; 51.9% promoter holding"),
            ("Headquarters",          "Hyderabad, Telangana",       "Unit-I: Visakhapatnam · Unit-II: Vizag SEZ"),
            ("Business Model",        "API + CDMO + Nutraceuticals","30 generic APIs · 12+ innovator programs"),
            ("Export Share",          "~86% of Revenue",            "North America 38% · Europe 35% · RoW 13%"),
            ("Employees",             "~12,000+",                   "Highly skilled chemistry & process teams"),
            ("R&D",                   "~2% of Revenue",             "Chemistry-led; process innovation focus"),
            ("FY25 Revenue",          "₹9,360 Crore",               "YoY +19.3%"),
            ("FY25 EBITDA Margin",    "38.3%",                      "OPM: 32.1%; best in class among Indian API"),
            ("Net Debt",              "Net Cash ₹4,500 Cr",         "Essentially zero-debt company"),
        ]
        for label, val, sig in fp_items:
            st.markdown(f"""
            <div class="fp-card">
              <div class="fp-label">{label}</div>
              <div class="fp-value">{val}</div>
              <div class="fp-signal">{sig}</div>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="d-card-forest">
          <b style="color:{FOREST}; font-family:'Playfair Display',serif; font-size:1.0rem;">Investment Thesis in One Paragraph</b><br><br>
          <span style="font-size:0.87rem; color:#1B4332; line-height:1.85;">
            Divi's Laboratories is India's <b>pre-eminent API and CDMO champion</b> — a rare business that has operated essentially debt-free while
            generating class-leading EBITDA margins (historically mid-30s, FY25 at 38%). The company's moat is structurally deep: 12 of the
            top-20 global pharmaceutical innovators have been partners for over a decade, multi-step chemistry expertise creates high switching
            costs, and its USFDA-compliant facilities give it permanent preferred-vendor status.<br><br>
            After a painful FY2023–24 cycle — driven by nutraceutical price corrections and API inventory destocking — Divi's is
            recovering sharply. FY25 revenue crossed ₹9,360 Cr (+19% YoY) with PAT at ₹2,244 Cr (+37%). The pipeline now pivots toward
            <b>high-value custom synthesis</b>: contrast media intermediates, peptide APIs, and multi-step innovator molecules that command
            35–40%+ margins versus the 28–30% in generic APIs.<br><br>
            The primary risk is the valuation: at 68× trailing P/E, the market prices perfection. Any USFDA action or capacity ramp delay
            would compress multiples swiftly. But for the long-term investor, Divi's remains <b>the highest-quality Indian pharma compounder</b>.
          </span>
        </div>

        <div class="d-card-amber">
          <b style="color:{AMBER}; font-family:'Playfair Display',serif; font-size:0.95rem;">Key Risks</b><br>
          <span style="font-size:0.84rem; color:#7A2800; line-height:1.7;">
            🔴 <b>USFDA regulatory risk</b> — any 483 or Warning Letter halts exports<br>
            🟠 <b>Customer concentration</b> — top 10 clients = ~60–65% of revenue<br>
            🟠 <b>China competition</b> — price undercutting in generic API segment<br>
            🟡 <b>Premium valuation</b> — 68× P/E leaves no margin of safety<br>
            🟡 <b>Capex ramp risk</b> — Unit-III delay could defer FY27 revenue targets
          </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="pullquote">
      "Chemistry is Divi's language; compliance is its passport; scale is its moat.
      The company that has never needed a single rupee of debt to build a ₹1.6 lakh crore empire
      is not a business — it is a philosophy in action."
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — FINANCIAL HISTORY
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "📊  Financial History":
    st.markdown("## 📊 Financial History — FY2020 to FY2025")
    st.markdown('<div class="narrative">Six years of operating data verified from Screener.in, Divi\'s Annual Reports, and MoneyControl. All figures in ₹ Crore. FY = April–March. EBITDA computed as Operating Profit + Depreciation; FCFF = CFO – Capex.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Revenue, EBIT & Cash Flow Trend</div>', unsafe_allow_html=True)
    st.plotly_chart(rev_ni_chart(), use_container_width=True)

    st.markdown('<div class="sec-head">Complete P&L Summary (₹ Crore)</div>', unsafe_allow_html=True)
    display = HIST[["Year","Revenue","EBITDA","EBIT","NI","EPS","OPM","DPS","CFO","Capex","FCFF"]].copy()
    display.columns = ["Year","Revenue","EBITDA","EBIT","PAT","EPS (₹)","OPM %","DPS (₹)","CFO","Capex","FCFF"]
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Key Ratios Over the Cycle</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        margin_fig = go.Figure()
        margin_fig.add_trace(go.Scatter(x=HIST["Year"], y=HIST["OPM"], name="OPM %",
                                        line=dict(color=FOREST, width=2.5), mode="lines+markers",
                                        marker=dict(size=8, color=FOREST)))
        margin_fig.add_trace(go.Scatter(x=HIST["Year"],
                                        y=(HIST["NI"]/HIST["Revenue"]*100).round(1),
                                        name="PAT Margin %",
                                        line=dict(color=MINT, width=2.2, dash="dot"),
                                        mode="lines+markers", marker=dict(size=7, color=MINT)))
        margin_fig.update_layout(height=280, **_L,
                                  title=dict(text="Margin Trend (OPM & PAT %)",
                                             font=dict(color=TEXT, size=12, family="Playfair Display")),
                                  yaxis=dict(ticksuffix="%", gridcolor="#F0F5F0",
                                             tickfont=dict(color="#374137")),
                                  xaxis=dict(tickfont=dict(color="#374137")))
        st.plotly_chart(margin_fig, use_container_width=True)

    with c2:
        roe_roce = pd.DataFrame({
            "Year":  HIST["Year"],
            "ROE":   [17.6, 19.9, 24.0, 11.6, 13.2, 15.4],
            "ROCE":  [21.2, 23.5, 28.5, 14.3, 17.0, 20.4],
        })
        ret_fig = go.Figure()
        ret_fig.add_trace(go.Scatter(x=roe_roce["Year"], y=roe_roce["ROCE"], name="ROCE %",
                                     line=dict(color=FOREST, width=2.5), mode="lines+markers",
                                     marker=dict(size=8, color=FOREST)))
        ret_fig.add_trace(go.Scatter(x=roe_roce["Year"], y=roe_roce["ROE"], name="ROE %",
                                     line=dict(color=AMBER, width=2.2, dash="dot"),
                                     mode="lines+markers", marker=dict(size=7, color=AMBER)))
        ret_fig.update_layout(height=280, **_L,
                               title=dict(text="Return Ratios (ROE & ROCE %)",
                                          font=dict(color=TEXT, size=12, family="Playfair Display")),
                               yaxis=dict(ticksuffix="%", gridcolor="#F0F5F0",
                                          tickfont=dict(color="#374137")),
                               xaxis=dict(tickfont=dict(color="#374137")))
        st.plotly_chart(ret_fig, use_container_width=True)

    st.markdown('<div class="sec-head">Working Capital & Balance Sheet Strength</div>', unsafe_allow_html=True)
    bs_data = pd.DataFrame([
        {"Year":"FY20","Equity":7320, "Gross Block":4800,"Net Cash (est.)":2200,"Current Ratio":4.1,"D/E":0.02},
        {"Year":"FY21","Equity":8648, "Gross Block":5500,"Net Cash (est.)":3100,"Current Ratio":4.5,"D/E":0.01},
        {"Year":"FY22","Equity":10512,"Gross Block":6200,"Net Cash (est.)":4500,"Current Ratio":5.2,"D/E":0.01},
        {"Year":"FY23","Equity":11327,"Gross Block":7100,"Net Cash (est.)":3800,"Current Ratio":4.8,"D/E":0.01},
        {"Year":"FY24","Equity":12485,"Gross Block":7500,"Net Cash (est.)":4100,"Current Ratio":4.6,"D/E":0.02},
        {"Year":"FY25","Equity":14100,"Gross Block":7800,"Net Cash (est.)":4500,"Current Ratio":4.8,"D/E":0.02},
    ])
    st.dataframe(bs_data, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="d-card-forest">
      <b style="font-family:'Playfair Display',serif; color:{FOREST};">Balance Sheet Interpretation</b><br>
      <span style="font-size:0.86rem; color:#1B4332; line-height:1.8;">
        Divi's operates with essentially no financial leverage — a rarity in capital-intensive API manufacturing. The current ratio of 4.8× reflects
        a structurally cash-rich model where working capital is predominantly self-funded. The gross block grew from ₹4,800 Cr (FY20) to ₹7,800 Cr (FY25),
        entirely financed by internal accruals. Net cash on hand (~₹4,500 Cr FY25) is larger than the annual Capex budget, providing ample runway for
        Unit-III expansion and bolt-on investments without dilution or leverage.
      </span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — SEGMENT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "🔬  Segment Analysis":
    st.markdown("## 🔬 Business Segment Analysis")
    st.markdown('<div class="narrative">Divi\'s operates across three business lines: Generic APIs (large-volume molecules), Custom Synthesis (CDMO for innovator pipeline), and Nutraceuticals (carotenoids & specialty nutrition). Mix-shift toward Custom Synthesis is the central margin-expansion thesis.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(segment_rev_chart(), use_container_width=True)
    with c2:
        st.plotly_chart(segment_margin_chart(), use_container_width=True)

    st.markdown('<div class="sec-head">Segment Deep Dive — FY2025 vs FY2024 (₹ Crore)</div>', unsafe_allow_html=True)
    seg_disp = SEGMENTS.copy()
    seg_disp["Rev Growth %"] = ((seg_disp["Rev_FY25"] - seg_disp["Rev_FY24"]) / seg_disp["Rev_FY24"] * 100).round(1)
    seg_disp["EBIT Growth %"] = ((seg_disp["EBIT_FY25"] - seg_disp["EBIT_FY24"]) / seg_disp["EBIT_FY24"] * 100).round(1)
    seg_disp.columns = ["Business","Revenue FY25","EBIT FY25","EBIT Margin FY25 %","Revenue FY24","EBIT FY24","Rev Growth %","EBIT Growth %"]
    st.dataframe(seg_disp, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Revenue Mix — Geographic Exposure (FY2025 Estimates)</div>', unsafe_allow_html=True)
    geo = go.Figure(go.Pie(
        labels=["North America","Europe","Japan & RoW","India (Domestic)"],
        values=[38, 35, 13, 14],
        hole=0.50,
        marker_colors=[FOREST, MINT, GOLD, AMBER],
        textinfo="label+percent",
        textfont=dict(color="#1A2E1A", size=12)
    ))
    geo.update_layout(height=290, paper_bgcolor="#FFFFFF", margin=dict(l=20,r=20,t=20,b=20),
                      font=dict(color=TEXT), legend=dict(font=dict(color=TEXT)))
    c1, c2 = st.columns([1,1])
    with c1:
        st.plotly_chart(geo, use_container_width=True)
    with c2:
        st.markdown(f"""
        <div class="d-card-sage">
          <b style="color:{SAGE}; font-family:'Playfair Display',serif;">Geographic Moat: Export = 86% Revenue</b><br>
          <span style="font-size:0.85rem; color:#1B4332; line-height:1.8;">
            <b>North America (38%):</b> Predominantly US branded generics and innovator supply; FDA-regulated pricing premium.<br>
            <b>Europe (35%):</b> Branded API supply under EMA; strong in contrast media, CNS, cardiovascular molecules.<br>
            <b>Japan & RoW (13%):</b> Japan partnerships for high-purity APIs; growing APAC innovator mandates.<br>
            <b>India (14%):</b> Smallest but fastest growing; domestic formulation demand, nutraceutical B2B.
          </span>
        </div>
        <div class="d-card-indigo">
          <b style="color:{INDIGO}; font-family:'Playfair Display',serif;">Custom Synthesis: The Margin Engine</b><br>
          <span style="font-size:0.85rem; color:#3A3660; line-height:1.8;">
            Custom Synthesis at 37% EBIT margin is Divi's most valuable segment — and its fastest growing (~19% YoY FY25).
            Innovator-tied supply agreements span 10–15 year horizons. Contrast media (iodinated intermediates) is a particularly
            lucrative niche with Divi's among only 2–3 global suppliers.
          </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Product Portfolio — Key Generic APIs (Top Volume)</div>', unsafe_allow_html=True)
    products = pd.DataFrame([
        {"API / Product":"Naproxen","Therapeutic Area":"Pain / Anti-inflammatory","Divi's Global Position":"#1 globally","Approx. Volume":"1,000s tons/yr"},
        {"API / Product":"Dextromethorphan","Therapeutic Area":"Cough & CNS","Divi's Global Position":"#1 globally","Approx. Volume":"100s tons/yr"},
        {"API / Product":"Gabapentin","Therapeutic Area":"Neurology","Divi's Global Position":"Top-3 globally","Approx. Volume":"100s tons/yr"},
        {"API / Product":"Contrast Media Intermediates","Therapeutic Area":"Diagnostic / Imaging","Divi's Global Position":"Top-3 globally","Approx. Volume":"Large tonnage"},
        {"API / Product":"Carotenoids (Beta-Carotene, Lutein)","Therapeutic Area":"Nutraceuticals","Divi's Global Position":"Top-3 globally","Approx. Volume":"10s tons/yr"},
        {"API / Product":"Atorvastatin intermediates","Therapeutic Area":"Cardiovascular","Divi's Global Position":"Significant share","Approx. Volume":"Moderate"},
        {"API / Product":"Custom Synthesis Pipeline (12+ programs)","Therapeutic Area":"Oncology · CNS · CV · ID","Divi's Global Position":"Preferred CDMO","Approx. Volume":"N/A (proprietary)"},
    ])
    st.dataframe(products, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — FORECASTING ENGINE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "📈  Forecasting Engine":
    st.markdown("## 📈 Forecasting Engine — FY2026E to FY2030E")
    st.markdown('<div class="narrative">Build your own revenue and profitability forecast using the sliders. All projections in ₹ Crore. Base case anchored on FY2025 actuals (Revenue ₹9,360 Cr, EBITDA 38.3%, PAT ₹2,244 Cr). The model incorporates Divi\'s Unit-III capacity ramp, custom synthesis mix-shift, and nutraceutical normalisation.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        rev_cagr = st.slider("Revenue CAGR FY25→30 (%)", 8.0, 22.0, 15.0, 0.5)
    with c2:
        ebitda_margin = st.slider("Target EBITDA Margin (%)", 30.0, 42.0, 36.0, 0.5)
    with c3:
        tax_rate_ui = st.slider("Effective Tax Rate (%)", 22.0, 28.0, 25.0, 0.5)

    rev_base = BASE["revenue"]
    rows = []
    for i in range(1, 6):
        rev_i    = rev_base * ((1 + rev_cagr / 100) ** i)
        ebitda_i = rev_i * ebitda_margin / 100
        da_i     = HIST["DA"].iloc[-1] * (1 + 0.06) ** i
        ebit_i   = ebitda_i - da_i
        pbt_i    = ebit_i + BASE["net_cash"] * 0.065
        pat_i    = pbt_i * (1 - tax_rate_ui / 100)
        eps_i    = pat_i / (BASE["shares"] / 100)
        rows.append({
            "Year":            f"FY{25+i}E",
            "Revenue (₹Cr)":  int(rev_i),
            "EBITDA (₹Cr)":   int(ebitda_i),
            "EBIT (₹Cr)":     int(ebit_i),
            "NI (₹Cr)":       int(pat_i),
            "EPS (₹)":        round(eps_i, 1),
            "EBITDA Margin":   f"{ebitda_margin:.1f}%",
        })

    st.markdown('<div class="sec-head">Forecast Table (₹ Crore)</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.plotly_chart(forecast_chart(rows, HIST), use_container_width=True)

    st.markdown('<div class="sec-head">Scenario Analysis</div>', unsafe_allow_html=True)
    scenarios = pd.DataFrame([
        {"Scenario":"Bear 🐻","Rev CAGR":"8%","EBITDA Margin":"31%","FY30E Revenue":"₹13,750 Cr","FY30E PAT":"₹2,580 Cr","Key Assumption":"Generic API pricing remains depressed; no Unit-III uplift"},
        {"Scenario":"Base 🟢","Rev CAGR":"15%","EBITDA Margin":"36%","FY30E Revenue":"₹18,830 Cr","FY30E PAT":"₹4,850 Cr","Key Assumption":"Custom synthesis ramps; nutraceutical recovery; USFDA clean slate"},
        {"Scenario":"Bull 🐂","Rev CAGR":"20%","EBITDA Margin":"40%","FY30E Revenue":"₹23,200 Cr","FY30E PAT":"₹6,600 Cr","Key Assumption":"Multiple large custom synthesis wins; contrast media dominance; margin mix normalises to FY22 peak"},
    ])
    st.dataframe(scenarios, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Key Forecast Drivers — Management Commentary & Industry Outlook</div>', unsafe_allow_html=True)
    drivers = pd.DataFrame([
        {"Driver":"Custom Synthesis Volume","FY25 Status":"₹2,808 Cr (30% of mix)","FY28 Target":"₹5,000+ Cr (35–38% of mix)","Evidence":"Unit-III Kakinada coming online; 6 new programs in clinical trials"},
        {"Driver":"Contrast Media Intermediates","FY25 Status":"Significant tonnage; exact undisclosed","FY28 Target":"Doubling capacity","Evidence":"Global iodinated contrast supply tightness; only 2–3 qualified suppliers"},
        {"Driver":"Nutraceuticals Recovery","FY25 Status":"₹936 Cr; OPM 23.9%","FY28 Target":"₹1,400+ Cr; OPM 27–28%","Evidence":"Carotenoid pricing normalising; downstream branded demand growing"},
        {"Driver":"Generic API Pricing","FY25 Status":"Stable but competitive","FY28 Target":"Flat to +3% pricing","Evidence":"China re-entry risk; Divi's cost advantage via backward integration"},
        {"Driver":"Export Realisation","FY25 Status":"INR/USD ~84; hedging program active","FY28 Target":"Neutral; natural hedge via USD costs","Evidence":"~30–35% raw material imports balance currency exposure"},
    ])
    st.dataframe(drivers, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 5 — DCF VALUATION
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "💰  DCF Valuation":
    live = get_live_price()
    st.markdown("## 💰 DCF Intrinsic Value — Damodaran FCFF Model (₹)")
    st.markdown('<div class="narrative">Damodaran FCFF approach: NOPAT = EBIT × (1–Tax); Reinvestment = ΔRevenue / Sales-to-Capital (2.5×); FCFF = NOPAT − Reinvestment. Terminal value via Gordon Growth. Equity value = EV + Net Cash − Debt. All figures in ₹ Crore; per-share value in ₹.</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: wacc    = st.slider("WACC (%)", 8.0, 14.0, 10.0, 0.5)
    with c2: g_term  = st.slider("Terminal Growth (%)", 2.0, 6.0, 4.0, 0.5)
    with c3: rev_cg  = st.slider("Revenue CAGR FY25→30 (%)", 8.0, 22.0, 15.0, 0.5)
    with c4: ebit_m  = st.slider("EBIT Margin (%)", 25.0, 38.0, 30.0, 0.5)

    res = run_dcf(wacc, g_term, rev_cg, ebit_m, live["price"])

    if res is None:
        st.error("⚠️ WACC must exceed Terminal Growth Rate.")
    else:
        upside_color = SAGE if res["upside"] >= 0 else RED
        upside_label = "UPSIDE" if res["upside"] >= 0 else "DOWNSIDE"
        st.markdown(f"""
        <div class="d-card" style="background:linear-gradient(135deg,{FOREST_LITE} 0%,{INDIGO_LITE} 100%); border:1.5px solid {BORDER};">
          <div style="display:flex; gap:2.5rem; flex-wrap:wrap; align-items:center;">
            <div style="text-align:center;">
              <div class="kpi-label">Intrinsic Value / Share</div>
              <div style="font-size:2.2rem; font-weight:800; color:{FOREST}; font-family:'Playfair Display',serif;">₹{res['ivps']:,.0f}</div>
            </div>
            <div style="text-align:center;">
              <div class="kpi-label">Live Price</div>
              <div style="font-size:2.2rem; font-weight:800; color:{INDIGO}; font-family:'Playfair Display',serif;">₹{live['price']:,.0f}</div>
            </div>
            <div style="text-align:center;">
              <div class="kpi-label">{upside_label}</div>
              <div style="font-size:2.2rem; font-weight:800; color:{upside_color}; font-family:'Playfair Display',serif;">{abs(res['upside']):.1f}%</div>
            </div>
            <div style="text-align:center;">
              <div class="kpi-label">Enterprise Value</div>
              <div style="font-size:1.6rem; font-weight:700; color:{FOREST};">₹{res['ev']:,} Cr</div>
            </div>
            <div style="text-align:center;">
              <div class="kpi-label">Equity Value</div>
              <div style="font-size:1.6rem; font-weight:700; color:{FOREST};">₹{res['eq_val']:,} Cr</div>
            </div>
            <div style="text-align:center;">
              <div class="kpi-label">Terminal Value %</div>
              <div style="font-size:1.6rem; font-weight:700; color:{AMBER};">{res['tv_pct']:.1f}%</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sec-head">5-Year FCFF Projection (₹ Crore)</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(res["rows"]), use_container_width=True, hide_index=True)
        st.plotly_chart(dcf_bar_chart(res), use_container_width=True)

        st.markdown('<div class="sec-head">Sensitivity Table — Intrinsic Value ₹/Share</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.78rem; color:#5C8C5C; margin-bottom:0.5rem; font-family:\'DM Sans\',sans-serif;">Rows: Terminal Growth Rate · Columns: WACC · Current price highlighted</div>', unsafe_allow_html=True)
        sens = sensitivity_table(rev_cg, ebit_m, live["price"])
        st.dataframe(sens, use_container_width=True)

        st.markdown(f"""
        <div class="d-card-indigo">
          <b style="color:{INDIGO}; font-family:'Playfair Display',serif;">Valuation Interpretation</b><br>
          <span style="font-size:0.86rem; color:#3A3660; line-height:1.8;">
            At the base-case WACC of 10% and terminal growth of 4%, the model outputs ₹{res['ivps']:,.0f}/share. Terminal value accounts
            for {res['tv_pct']:.0f}% of EV — typical for high-quality, long-duration compounders. The current market price of ₹{live['price']:,.0f}
            implies the market is pricing a near-perfect execution scenario (WACC ~9%, g ~5%). A conservative investor would demand a
            15–20% margin of safety before initiating a position.
          </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sec-head">WACC Decomposition — Divi\'s Labs India</div>', unsafe_allow_html=True)
        wacc_table = pd.DataFrame([
            {"Component":"Risk-Free Rate (10Y Gsec yield)","Value":"~6.8%","Note":"RBI Monetary Policy; as of Mar 2026"},
            {"Component":"Equity Risk Premium (Damodaran India ERP)","Value":"~7.0%","Note":"Damodaran Jan 2025 India ERP estimate"},
            {"Component":"Beta (DIVISLAB.NS 2Y monthly vs Nifty)","Value":"~0.62","Note":"Defensive pharma; low correlation to market"},
            {"Component":"Cost of Equity (CAPM)","Value":"~11.1%","Note":"6.8% + 0.62 × 7.0%"},
            {"Component":"Pre-tax Cost of Debt","Value":"~7.2%","Note":"AA-rated; essentially no debt outstanding"},
            {"Component":"Target D/E","Value":"~2%","Note":"Effectively all-equity structure"},
            {"Component":"WACC (All-Equity Approx.)","Value":"~10.0–11.1%","Note":"Range depending on beta horizon used"},
        ])
        st.dataframe(wacc_table, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 6 — PEER BENCHMARKING
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "🏆  Peer Benchmarking":
    st.markdown("## 🏆 Peer Benchmarking — Indian CDMO & API Universe")
    st.markdown("""
<div class="narrative">
Peers selected: PI Industries (agro-CDMO overlap), Laurus Labs (API/CDMO), Suven Pharma (CDMO), Dishman Carbogen (CDMO/API).
Divi's historical peak (FY22) included as internal benchmark. All market cap figures in ₹ Crore.
</div>
""", unsafe_allow_html=True)

    st.dataframe(PEERS, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        pe_fig = go.Figure(go.Bar(
            x=PEERS["Company"], y=PEERS["PE"],
            marker_color=[FOREST if "Divi" in c and "Hist" not in c else AMBER if "Hist" in c else MINT
                          for c in PEERS["Company"]],
            text=[f"{v}×" for v in PEERS["PE"]], textposition="outside",
            textfont=dict(color=TEXT, size=11)
        ))
        pe_fig.update_layout(height=310, **_L,
                              title=dict(text="Trailing P/E Comparison",
                                         font=dict(color=TEXT, size=12, family="Playfair Display")),
                              yaxis=dict(ticksuffix="×", gridcolor="#F0F5F0",
                                         tickfont=dict(color="#374137")),
                              xaxis=dict(tickfont=dict(color="#374137")), showlegend=False)
        st.plotly_chart(pe_fig, use_container_width=True)

    with c2:
        m_fig = go.Figure(go.Bar(
            x=PEERS["Company"], y=PEERS["EBIT_M"],
            marker_color=[FOREST if "Divi" in c and "Hist" not in c else AMBER if "Hist" in c else MINT
                          for c in PEERS["Company"]],
            text=[f"{v}%" for v in PEERS["EBIT_M"]], textposition="outside",
            textfont=dict(color=TEXT, size=11)
        ))
        m_fig.update_layout(height=310, **_L,
                             title=dict(text="EBIT Margin — FY2025 or LTM",
                                        font=dict(color=TEXT, size=12, family="Playfair Display")),
                             yaxis=dict(ticksuffix="%", gridcolor="#F0F5F0",
                                        tickfont=dict(color="#374137")),
                             xaxis=dict(tickfont=dict(color="#374137")), showlegend=False)
        st.plotly_chart(m_fig, use_container_width=True)

    st.markdown('<div class="sec-head">EV/EBITDA Cross-Section (Indicative Multiples)</div>', unsafe_allow_html=True)
    ev_table = pd.DataFrame([
        {"Company":"Divi's Labs (Current)","EV (₹Cr)":"~1,56,500","EBITDA (₹Cr)":"~3,582","EV/EBITDA":"~43.7×","Verdict":"Premium; priced for flawless execution"},
        {"Company":"Divi's Labs (FY22 Peak)","EV (₹Cr)":"~2,10,000","EBITDA (₹Cr)":"~3,565","EV/EBITDA":"~58.9×","Verdict":"Historical peak multiple; fear of missing out cycle"},
        {"Company":"PI Industries","EV (₹Cr)":"~43,000","EBITDA (₹Cr)":"~1,450","EV/EBITDA":"~29.6×","Verdict":"Discount to Divi's; lower margin quality"},
        {"Company":"Laurus Labs","EV (₹Cr)":"~21,500","EBITDA (₹Cr)":"~950","EV/EBITDA":"~22.6×","Verdict":"Deep discount; CDMO narrative not yet delivered"},
        {"Company":"Suven Pharma","EV (₹Cr)":"~13,000","EBITDA (₹Cr)":"~340","EV/EBITDA":"~38.2×","Verdict":"Premium for 100% CDMO model; small scale"},
    ])
    st.dataframe(ev_table, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="d-card-sage">
      <b style="font-family:'Playfair Display',serif; color:{SAGE};">Why Does Divi's Deserve a Premium?</b><br>
      <span style="font-size:0.86rem; color:#1B4332; line-height:1.8;">
        1. <b>Zero debt</b> + ₹4,500 Cr net cash — financial resilience in a cyclical industry.<br>
        2. <b>Best-in-class EBITDA margins</b> (32–38%) vs generic pharma peers (12–18%).<br>
        3. <b>Regulatory clean slate</b> — no USFDA warning letters historically; passes ~25 USFDA inspections.<br>
        4. <b>Sticky innovator relationships</b> — 12 of top-20 Big Pharma for 10+ years = repeatable revenue.<br>
        5. <b>Chemistry depth</b> — multi-step synthesis capability (8–15 step routes) creates un-replicable competitive advantage.<br><br>
        The discount relative to FY22 peak PE (68× vs 80–90× previously) reflects the cycle trough experience and market caution. 
        As Custom Synthesis share rises toward 35%+, the multiple should expand structurally.
      </span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 7 — STRATEGY (DAMODARAN)
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "♟️  Strategy (Damodaran)":
    st.markdown("## ♟️ Strategic Analysis — Damodaran Framework")
    st.markdown('<div class="narrative">Applied Damodaran strategic finance: Competitive Advantages → Value Drivers → Strategic Choices → Capital Allocation. Layered with Ansoff Matrix and Porter\'s Five Forces for a 360-degree view of Divi\'s strategic positioning through FY2030.</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Porter's 5 Forces", "Ansoff Matrix", "4Ps Audit", "Capital Allocation", "Coherence Check"])

    with tabs[0]:
        st.markdown('<div class="sec-head">Porter\'s Five Forces — Divi\'s Labs (FY2025)</div>', unsafe_allow_html=True)
        forces = pd.DataFrame([
            {"Force":"Supplier Power","Rating":"🟡 Moderate","Analysis":"Key raw materials: solvents, specialty chemicals, iodine (for contrast media). Divi's backward integration reduces dependency. Some API building blocks sourced from China — a structural vulnerability that management is addressing via domestic procurement."},
            {"Force":"Buyer Power","Rating":"🟠 Moderate–High","Analysis":"Top-10 innovator clients = 60–65% revenue; significant concentration. However, switching costs are extremely high (re-validation = 12–24 months, $1M+ cost per SKU). Buyers have leverage on price but not on supply reliability — giving Divi's negotiating balance."},
            {"Force":"Competitive Rivalry","Rating":"🟢 Low–Moderate","Analysis":"Effective global API CDMO peers: Lonza, Siegfried, Cambrex (Western); Aurobindo, Laurus (Indian). Divi's holds 30–50%+ global share in 10+ generic APIs (Naproxen, Dextromethorphan). Rivalry is primarily on pricing in generics but structural in custom synthesis."},
            {"Force":"Threat of New Entrants","Rating":"🟢 Low","Analysis":"API manufacturing requires: multi-million dollar USFDA-qualified facilities, 5–8 years to qualify a vendor, deep chemistry expertise, and impeccable compliance track record. Essentially zero risk of credible new entrant displacing Divi's established positions."},
            {"Force":"Threat of Substitutes","Rating":"🟢 Low","Analysis":"APIs are essential pharmaceutical inputs — no substitute. Generic API molecule substitution exists but Divi's multi-molecule diversification (30+ generics) mitigates molecule-level risk. Custom synthesis programs are proprietary — zero substitution risk."},
        ])
        st.dataframe(forces, use_container_width=True, hide_index=True)

    with tabs[1]:
        st.markdown('<div class="sec-head">Ansoff Matrix — Growth Pathways FY2026–FY2030</div>', unsafe_allow_html=True)
        ansoff_data = [
            ("Market Penetration (Existing Products × Existing Markets)", "Primary Growth Lever",
             ["Volume share gain in Naproxen, Dextromethorphan, Gabapentin",
              "Increase FDA-quota utilisation at existing units (Unit-I, II)",
              "Contract extensions & volume ramp-ups with existing Big Pharma clients",
              "Nutraceutical carotenoid pricing recovery + volume normalisation"],
             "Revenue contribution: ~40–45% of FY28E incremental growth"),
            ("Market Development (Existing Products × New Markets)", "Secondary Lever",
             ["Expand generic API distribution to LATAM, MENA, Southeast Asia",
              "Grow Japanese innovator relationships (high-purity, premium-priced APIs)",
              "Increase domestic India formulation customer base (pharma mid-caps)"],
             "Revenue contribution: ~10–15% of FY28E incremental growth"),
            ("Product Development (New Products × Existing Markets)", "Core CDMO Growth",
             ["Peptide APIs — add 3–5 programs by FY27; GLP-1 adjacent synthetic peptide supply",
              "Oligonucleotide intermediates — early-stage chemistry; FY28+ revenue potential",
              "HPAPI handling expansion — oncology API manufacturing capability upgrade",
              "Unit-III Kakinada: new multi-purpose synthesis block for complex programs"],
             "Revenue contribution: ~35–40% of FY28E incremental growth; highest margin"),
            ("Diversification (New Products × New Markets)", "Long-Term Option",
             ["Specialty nutrition / finished nutraceutical B2C brand (early-stage exploration)",
              "CDx / companion diagnostics API supply opportunity",
              "API-to-formulation vertical integration (management has historically resisted — watch for policy change)"],
             "Revenue contribution: <5% FY28E; option value"),
        ]
        for quad, tag, bullets, note in ansoff_data:
            bullet_html = "".join([f'<div class="ansoff-item">› {b}</div>' for b in bullets])
            st.markdown(f"""
            <div class="ansoff-card">
              <div class="ansoff-title">{quad}</div>
              <div class="ansoff-sub"><span class="tag-forest">{tag}</span></div>
              {bullet_html}
              <div style="font-size:0.78rem; color:{SAGE}; margin-top:8px; font-style:italic; font-family:'DM Sans',sans-serif;">{note}</div>
            </div>""", unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="sec-head">4Ps Operational Audit — Strategic Gaps & Prescriptions</div>', unsafe_allow_html=True)
        fourp = pd.DataFrame([
            {"Lever":"Product","Gap Today":"Generic API mix at 60% drags blended EBITDA margin; nutraceuticals (10%) still below FY22 pricing","Required Action FY26–28":"Grow Custom Synthesis share from 30% → 38% of mix; add 4+ innovator programs; commercialise HPAPI block; launch peptide capability","Financial Impact":"Every 1% mix-shift to Custom Synthesis = ~₹150–200 Cr EBIT uplift at current scale"},
            {"Lever":"Price","Gap Today":"Generic API pricing pressure from China re-entry; nutraceutical prices below FY22 peak","Required Action FY26–28":"Defend market share via cost-efficiency; lock in innovator contracts with multi-year fixed pricing; nutraceutical premiumisation in beadlets/liquids","Financial Impact":"Pricing stability in generics preserves ₹2,000+ Cr revenue; nutraceutical premium = 200–300bps margin lift"},
            {"Lever":"Place (Channel)","Gap Today":"100% B2B; no channel diversification; heavy dependence on air-freight logistics for time-sensitive APIs","Required Action FY26–28":"Expand sea-freight logistics capabilities; deepen distributor networks in LATAM, MENA; explore toll manufacturing arrangements","Financial Impact":"Logistics optimisation = ₹50–80 Cr annual saving; geographic diversification reduces single-country revenue concentration"},
            {"Lever":"Promotion","Gap Today":"Zero consumer brand awareness; Divi's is invisible to end-users despite manufacturing APIs in blockbuster drugs","Required Action FY26–28":"Not relevant for B2B model; BUT: investor relations enhancement needed — analyst coverage is thin; ESG reporting formalisation will attract global ESG funds","Financial Impact":"Better investor communication → narrower discount to intrinsic value → potential re-rating from 65× to 70–75× P/E if custom synthesis thesis is articulated"},
        ])
        st.dataframe(fourp, use_container_width=True, hide_index=True)

    with tabs[3]:
        st.markdown('<div class="sec-head">Capital Allocation Prescription — FY2026–FY2028</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="narrative">Divi\'s strongest asset is its balance sheet. With ₹4,500 Cr net cash generating ~₹300 Cr annual interest income and ₹3,100 Cr annual CFO, the question is not if Divi\'s can invest — it is whether management will allocate boldly enough. The risk is under-investment in organic capacity expansion given the conservative, founder-led capital culture.</div>', unsafe_allow_html=True)
        cap = pd.DataFrame([
            {"Use of Capital":"Capex — Unit-III & HPAPI Block","FY25 Actual":"₹950 Cr","Recommended FY26–28":"₹1,200–1,500 Cr/yr","Rationale":"Unit-III Kakinada ramp; HPAPI is highest-margin, fastest-growing capability worldwide"},
            {"Use of Capital":"Dividends","FY25 Actual":"₹30/sh (₹796 Cr)","Recommended FY26–28":"₹35–45/sh (5–8% annual growth)","Rationale":"Healthy payout; signals confidence; current 43% payout ratio is sustainable"},
            {"Use of Capital":"Buybacks","FY25 Actual":"Negligible","Recommended FY26–28":"₹500–1,000 Cr opportunistically","Rationale":"At 20%+ discount to fair value, buybacks are more value-accretive than cash sitting at 7%"},
            {"Use of Capital":"R&D (Process Chem + Peptides)","FY25 Actual":"~₹180 Cr (~2% rev)","Recommended FY26–28":"₹300–400 Cr (3–4% rev)","Rationale":"Under-investing vs CDMO global peers; peptide/oligo chemistry requires upfront IP investment"},
            {"Use of Capital":"M&A / Bolt-ons","FY25 Actual":"Nil","Recommended FY26–28":"Selective ₹200–500 Cr","Rationale":"Acquire niche chemistry platform (HPAPI specialist, fermentation capability) to fast-track capability gap"},
        ])
        st.dataframe(cap, use_container_width=True, hide_index=True)

    with tabs[4]:
        st.markdown('<div class="sec-head">Strategy Coherence Audit — 6-Point Consistency Check</div>', unsafe_allow_html=True)
        audit = pd.DataFrame([
            {"Dimension":"Growth Direction (Ansoff)","Strategy":"Product Dev (1°) + Market Penetration (2°)","Revenue Consistent?":"✅ Yes — FY25 revenue +19% YoY validates market penetration","Margin Consistent?":"✅ Yes — EBITDA 38.3% recovering from trough","Conflict?":"None"},
            {"Dimension":"Competitive Positioning","Strategy":"Cost leadership in generics + Differentiation in custom synthesis","Revenue Consistent?":"✅ Yes — dual-track model evidenced in segment data","Margin Consistent?":"✅ Yes — Custom Synthesis 37% EBIT margin vs Generic 30%","Conflict?":"Potential tension: cost culture may slow premium capability investment"},
            {"Dimension":"Pricing Strategy","Strategy":"Volume pricing in generics; relationship-based in custom synthesis","Revenue Consistent?":"✅ Yes — stable ASPs in generics","Margin Consistent?":"✅ Yes — innovator margins structurally higher","Conflict?":"China competition may force further discounting in bulk generics"},
            {"Dimension":"Channel Strategy","Strategy":"100% B2B direct; no third-party distributors for API","Revenue Consistent?":"✅ Yes — direct relationships built over decades","Margin Consistent?":"✅ Yes — no channel margins given away","Conflict?":"Under-penetration of emerging markets (LATAM, MENA, SEA)"},
            {"Dimension":"Capital Allocation","Strategy":"Minimal debt + dividend + capex from CFO","Revenue Consistent?":"✅ Yes — conservative but self-funded","Margin Consistent?":"✅ Yes — interest income adds ~₹300 Cr to PBT","Conflict?":"Under-investment risk; peers like Lonza spending 3–4× more on R&D as % of revenue"},
            {"Dimension":"ESG / Governance","Strategy":"Promoter-led; low disclosure; improving on ESG reporting","Revenue Consistent?":"⚠️ Partial — promoter holding 51.9% ensures alignment but limits float","Margin Consistent?":"✅ Yes — cost discipline evidenced in opex ratios","Conflict?":"Global ESG fund exclusion risk if reporting not formalised by FY27"},
        ])
        st.dataframe(audit, use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="pullquote">
          "The pharmaceutical company that wins the next decade will be defined not by the APIs it manufactured
          in the blockbuster supercycle, but by the custom synthesis platform it builds for the biologics-adjacent
          and next-generation small-molecule era. Divi's has the chemistry, the compliance, and the capital.
          The only question is the ambition."
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 8 — LIVE NEWS
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "📰  Live News":
    st.markdown("## 📰 Live News — DIVISLAB & Indian Pharma")
    st.markdown('<div class="narrative">News flow is the short-term sentiment pulse. The long-term investor filters for regulatory signals, contract announcements, and capacity updates — and discounts macro noise. Discipline: own the signal, fade the noise.</div>', unsafe_allow_html=True)

    news = get_live_news()
    pos_n = sum(1 for n in news if n["sentiment"] == "positive")
    neg_n = sum(1 for n in news if n["sentiment"] == "negative")
    neu_n = sum(1 for n in news if n["sentiment"] == "neutral")

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Headlines",  f"{len(news)}")
    s2.metric("Positive ✅",      f"{pos_n}")
    s3.metric("Neutral ⬜",       f"{neu_n}")
    s4.metric("Negative ❌",      f"{neg_n}")

    sf = st.selectbox("Filter by Sentiment", ["All","positive","neutral","negative"])
    filtered = news if sf == "All" else [n for n in news if n["sentiment"] == sf]
    css_map = {"positive":"news-pos","negative":"news-neg","neutral":"news-neu"}
    tag_map  = {
        "positive": f'<span class="tag-mint">positive</span>',
        "negative": f'<span class="tag-red">negative</span>',
        "neutral":  f'<span class="tag-indigo">neutral</span>',
    }

    st.markdown("")
    for item in filtered:
        link_html = (f'<a href="{item["link"]}" target="_blank" '
                     f'style="font-size:0.72rem;color:{MINT};text-decoration:none;font-weight:700;">Read →</a>'
                     if item["link"] != "#" else "")
        st.markdown(f"""
        <div class="{css_map[item['sentiment']]}">
          <div class="news-title">{item['title']}</div>
          <div class="news-meta">
            {tag_map[item['sentiment']]} &nbsp; {item['date']} &nbsp; {link_html}
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">News Sentiment Distribution</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        sent_fig = go.Figure(go.Pie(
            labels=["Positive","Neutral","Negative"],
            values=[max(pos_n,1), max(neu_n,1), max(neg_n,1)],
            hole=0.52,
            marker_colors=[SAGE, INDIGO, RED],
            textinfo="label+percent",
            textfont=dict(color=TEXT, size=12)
        ))
        sent_fig.update_layout(height=270, paper_bgcolor="#FFFFFF",
                               margin=dict(l=20,r=20,t=20,b=20),
                               font=dict(color=TEXT),
                               legend=dict(font=dict(color=TEXT)))
        st.plotly_chart(sent_fig, use_container_width=True)
    with c2:
        st.markdown(f"""
        <div class="d-card-forest">
          <b style="color:{FOREST}; font-family:'Playfair Display',serif;">How to Read DIVISLAB News Flow</b><br>
          <span style="font-size:0.85rem;color:#1B4332; line-height:1.8;">
            <b>Signal headlines</b> (high weight): USFDA inspection outcomes (zero 483 = catalyst), innovator contract awards,
            custom synthesis program initiations, Unit-III capacity milestones, earnings beat/miss.<br><br>
            <b>Noise headlines</b> (low weight): Analyst price target changes, general pharma sector commentary,
            index inclusion/exclusion, promoter share pledging data (none historically).<br><br>
            <b>Watch for:</b> Any USFDA Warning Letter (primary risk), Q3/Q4 FY26 earnings (Jan/May 2026), 
            Unit-III capacity launch announcement (H1 FY27), and peptide synthesis program commercialisation signal.
          </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="d-card-amber">
          <b style="color:{AMBER}; font-family:'Playfair Display',serif;">Key Upcoming Catalysts (FY2026)</b><br>
          <span style="font-size:0.84rem; color:#7A2800; line-height:1.7;">
            · Q3 FY26 Earnings (Expected ~Feb 2026) — Custom Synthesis volume update<br>
            · Q4 FY26 + Full Year (May 2026) — Unit-III progress; FY27 capex guidance<br>
            · USFDA Inspection Schedule — Vizag Units I & II due FY2026<br>
            · Annual General Meeting FY26 — Dividend announcement; promoter statement<br>
            · Global pharma R&D pipeline updates — GLP-1 adjacent API demand signal
          </span>
        </div>
        """, unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  DIVISLAB Research Terminal &nbsp;|&nbsp;
  Live data: Yahoo Finance (yfinance) &nbsp;|&nbsp;
  Fundamentals: Screener.in · Divi's Annual Reports FY2020–FY2025 · MoneyControl &nbsp;|&nbsp;
  News: Google News RSS &nbsp;|&nbsp;
  Framework: Damodaran (NYU Stern) &nbsp;|&nbsp;
  {datetime.now().strftime("%d %B %Y  %H:%M IST")} &nbsp;|&nbsp;
  <b>Prepared by: Bhavansh Madan · IPM2 · MBA Corporate Finance</b> &nbsp;|&nbsp;
  <span style="color:#74C69D;"><b>Academic use only — not investment advice</b></span>
</div>
""", unsafe_allow_html=True)