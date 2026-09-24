import streamlit as st

from python.ai_reasoning import ask_gemini
from python.ai_business_analyst import df


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer Product Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================
#
# DESIGN LANGUAGE — "signal console"
# ------------------------------------------------------------
# A vivid, glass-and-glow command console. Deep near-black base,
# a floating colour-coded aurora, and glassmorphic panels that
# visibly light up and lift when touched. Each feature area gets
# its own saturated signal colour so the whole console reads as
# alive rather than a single muted brand gradient.
#
# Colour
#   void       #05070d   base background
#   glass      rgba(255,255,255,0.045)   panel fill
#   glass-hi   rgba(255,255,255,0.09)    panel hover fill
#   blue       #3b82f6   Business
#   magenta    #ec4899   Risk
#   amber      #f5b23c   Profit
#   emerald    #10e0a4   Retention
#   violet     #8b5cf6   Customer 360
#   cyan       #22d3ee   Regional
#   text hi/mid/low  #f8fafc / #9aa4b2 / #5c6675
#
# Type
#   display  Space Grotesk   (bold, geometric, headline energy)
#   body     Inter           (clean UI copy)
#   mono     JetBrains Mono  (labels, stats, ticker)
#
# NOTE: every HTML string is flush-left inside its triple-quote —
# 4-space indentation makes Streamlit render raw HTML as a code
# block instead of parsing it.

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');

:root{
  --bg:#0b1220;
  --bg2:#0f1728;
  --card:#121b2c;
  --card2:#162238;
  --line:#26344d;
  --line2:#34435e;
  --text:#f4f7fb;
  --text2:#c3cede;
  --muted:#91a0b6;
  --dim:#64738b;

  --blue:#5b8cff;
  --blue-soft:#182b54;
  --violet:#9b7aff;
  --violet-soft:#281f4e;
  --green:#2bd7a0;
  --green-soft:#103b32;
  --red:#ff6b7f;
  --red-soft:#421f2a;
  --amber:#f4bd55;
  --amber-soft:#42331b;
  --cyan:#39d5ef;
}

html,body,[class*="css"]{
  font-family:'DM Sans',sans-serif;
}

.stApp{
  color:var(--text);
  background:
    radial-gradient(900px 520px at 95% -10%,rgba(91,140,255,.13),transparent 65%),
    radial-gradient(800px 500px at 0% 40%,rgba(155,122,255,.08),transparent 68%),
    linear-gradient(180deg,#0b1220 0%,#0a111d 100%);
}

.main .block-container{
  max-width:1340px;
  padding:24px 34px 105px;
}

#MainMenu,footer{visibility:hidden}

header[data-testid="stHeader"]{
  background:rgba(11,18,32,.88);
}

button:focus-visible{
  outline:2px solid var(--blue)!important;
  outline-offset:2px;
}

/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#08111f 0%,#0b1424 100%);
  border-right:1px solid #1b2940;
}

section[data-testid="stSidebar"] .block-container{
  padding:24px 17px 24px;
}

.sb-brand{
  display:flex;
  align-items:center;
  gap:11px;
}

.sb-brand-mark{
  width:38px;
  height:38px;
  border-radius:11px;
  display:flex;
  align-items:center;
  justify-content:center;
  background:linear-gradient(135deg,#4f7cff,#805cff);
  color:#fff;
  font:700 15px 'Space Grotesk';
  box-shadow:0 9px 24px rgba(79,124,255,.25);
}

.sb-brand-name{
  font:600 14px 'Space Grotesk';
  color:#fff!important;
}

.sb-brand-sub{
  margin:7px 0 22px 49px;
  color:#70809b!important;
  font:500 7.5px 'JetBrains Mono';
  letter-spacing:1.45px;
  text-transform:uppercase;
}

.sb-rule{
  height:1px;
  border:0;
  background:#233149;
  margin:18px 0;
}

.sb-label{
  color:#71829e!important;
  font:600 8px 'JetBrains Mono';
  letter-spacing:1.5px;
  text-transform:uppercase;
  margin:17px 0 8px 3px;
}

section[data-testid="stSidebar"] .stButton button{
  width:100%;
  min-height:39px;
  border:1px solid transparent;
  border-radius:9px;
  background:transparent;
  color:#b9c5d8!important;
  font-size:11.5px;
  font-weight:500;
  text-align:left;
  justify-content:flex-start;
  padding-left:11px;
  transition:.16s ease;
}

section[data-testid="stSidebar"] .stButton button:hover{
  background:#142137;
  color:#fff!important;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"]{
  background:linear-gradient(100deg,#3868f5,#7658ed);
  color:#fff!important;
  border:0;
  box-shadow:0 9px 24px rgba(62,92,230,.25);
}

.sb-stat{
  padding:15px 12px;
  border-radius:12px;
  margin-top:4px;
  background:#111c2e;
  border:1px solid #25344d;
}

.sb-stat-num{
  font:700 27px 'Space Grotesk';
  color:#fff!important;
}

.sb-stat-label{
  margin-top:3px;
  color:#71829e!important;
  font:500 7.5px 'JetBrains Mono';
  letter-spacing:1px;
  text-transform:uppercase;
}

.verified-chip{
  display:flex;
  align-items:center;
  gap:6px;
  margin-top:9px;
  padding:8px 10px;
  border:1px solid rgba(43,215,160,.28);
  border-radius:9px;
  background:#0d2a26;
  color:#65e1bd!important;
  font:500 8.5px 'JetBrains Mono';
}

/* =========================================================
   HEADER
   ========================================================= */

.app-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 0 17px;
  border-bottom:1px solid var(--line);
}

.app-header-left{
  display:flex;
  align-items:center;
  gap:12px;
}

.app-header-mark{
  width:40px;
  height:40px;
  border-radius:11px;
  display:flex;
  align-items:center;
  justify-content:center;
  background:linear-gradient(135deg,#3c6ff6,#7659e9);
  color:#fff!important;
  font:700 17px 'Space Grotesk';
  box-shadow:0 8px 20px rgba(64,94,236,.22);
}

.app-header-title{
  font:700 19px 'Space Grotesk';
  color:#f7f9fc!important;
  letter-spacing:-.35px;
}

.app-header-subtitle{
  font-size:10.5px;
  color:#91a0b6!important;
  margin-top:3px;
}

.ticker{
  padding:7px 11px;
  border:1px solid #29415c;
  border-radius:8px;
  background:#0e1a2c;
  color:#b9c8dd!important;
  font:600 8px 'JetBrains Mono';
}

.ticker-dot{
  display:inline-block;
  width:6px;
  height:6px;
  border-radius:50%;
  background:#2bd7a0;
  margin-right:6px;
  box-shadow:0 0 10px rgba(43,215,160,.5);
}

/* =========================================================
   HERO
   ========================================================= */

.hero{
  position:relative;
  overflow:hidden;
  margin-top:18px;
  padding:30px 31px;
  border:1px solid #29436a;
  border-radius:17px;
  background:
    radial-gradient(500px 220px at 90% 50%,rgba(91,140,255,.18),transparent 70%),
    linear-gradient(115deg,#111e33 0%,#14243e 55%,#182848 100%);
  box-shadow:0 18px 45px rgba(0,0,0,.22);
}

.hero:after{
  content:"";
  position:absolute;
  right:22px;
  top:-75px;
  width:230px;
  height:230px;
  border-radius:50%;
  border:1px solid rgba(125,157,220,.16);
  box-shadow:
    0 0 0 30px rgba(91,140,255,.045),
    0 0 0 62px rgba(91,140,255,.025);
  pointer-events:none;
}

.hero-kicker{
  font:600 8px 'JetBrains Mono';
  letter-spacing:1.5px;
  color:#8da6d0!important;
  text-transform:uppercase;
}

.hero h1{
  margin:9px 0 7px;
  color:#f7faff!important;
  font:700 30px/1.12 'Space Grotesk';
  letter-spacing:-.8px;
}

.hero p{
  margin:0;
  max-width:700px;
  color:#b7c5d9!important;
  font-size:12px;
  line-height:1.65;
}

.hero-status{
  display:inline-flex;
  margin-top:15px;
  padding:7px 10px;
  border-radius:7px;
  background:#0e1b2e;
  border:1px solid #2b4264;
  color:#a9bad4!important;
  font:500 7.5px 'JetBrains Mono';
}

/* =========================================================
   KPI
   ========================================================= */

.kpi-grid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:11px;
  margin-top:13px;
}

.kpi{
  position:relative;
  overflow:hidden;
  padding:16px 17px;
  background:#111a2a;
  border:1px solid #26364f;
  border-radius:14px;
  box-shadow:0 8px 25px rgba(0,0,0,.15);
}

.kpi:after{
  content:"";
  position:absolute;
  left:0;
  bottom:0;
  height:2px;
  width:100%;
  background:linear-gradient(90deg,#4f7cff,transparent);
  opacity:.75;
}

.kpi-top{
  display:flex;
  justify-content:space-between;
  align-items:center;
}

.kpi-label{
  font:600 8px 'JetBrains Mono';
  letter-spacing:1.05px;
  color:#91a0b6!important;
  text-transform:uppercase;
}

.kpi-icon{
  width:28px;
  height:28px;
  border-radius:8px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:13px;
}

.icon-blue{background:#172d59;color:#6f9aff!important}
.icon-amber{background:#3d3019;color:#f5c969!important}
.icon-violet{background:#2c2253;color:#a88aff!important}
.icon-red{background:#40202a;color:#ff7b8d!important}

.kpi-value{
  margin-top:7px;
  color:#f5f8fd!important;
  font:700 24px 'Space Grotesk';
  letter-spacing:-.4px;
}

.kpi-note{
  font-size:9px;
  color:#7888a1!important;
  margin-top:2px;
}

/* =========================================================
   ANALYSIS WORKSPACE
   ========================================================= */

.section-head{
  display:flex;
  align-items:end;
  justify-content:space-between;
  margin:26px 0 11px;
}

.section-title{
  color:#f2f6fc!important;
  font:700 18px 'Space Grotesk';
}

.section-sub{
  margin-top:3px;
  color:#8291a8!important;
  font-size:9.5px;
}

.section-pill{
  padding:5px 8px;
  border:1px solid #2a3a54;
  border-radius:7px;
  background:#111b2b;
  color:#8295b2!important;
  font:500 7.5px 'JetBrains Mono';
}

.module-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:11px;
}

.module{
  display:grid;
  grid-template-columns:43px 1fr 20px;
  align-items:center;
  gap:13px;
  min-height:78px;
  padding:14px 17px;
  background:#111a2a;
  border:1px solid #26364f;
  border-radius:14px;
  box-shadow:0 7px 23px rgba(0,0,0,.14);
  transition:.18s ease;
}

.module:hover{
  transform:translateY(-2px);
  background:#152239;
  border-color:#385071;
  box-shadow:0 13px 30px rgba(0,0,0,.2);
}

.module-icon{
  width:43px;
  height:43px;
  border-radius:11px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:16px;
}

.mi-blue{background:#172d59;color:#6f9aff!important}
.mi-red{background:#40202a;color:#ff7b8d!important}
.mi-violet{background:#2c2253;color:#a88aff!important}
.mi-green{background:#10382f;color:#51dfb3!important}

.module h3{
  margin:0;
  color:#f0f4fa!important;
  font:600 13px 'Space Grotesk';
}

.module p{
  margin:4px 0 0;
  color:#8392aa!important;
  font-size:9.5px;
}

.module-arrow{
  color:#7286a4!important;
  font-size:17px;
}

/* =========================================================
   ASK PANEL + BUTTONS
   ========================================================= */

.ask-wrap{
  margin-top:16px;
  padding:18px;
  background:#111a2a;
  border:1px solid #26364f;
  border-radius:15px;
  box-shadow:0 7px 24px rgba(0,0,0,.14);
}

.ask-title{
  color:#f1f5fb!important;
  font:700 13px 'Space Grotesk';
}

.ask-sub{
  margin:3px 0 11px;
  color:#8291a8!important;
  font-size:9.5px;
}

div[data-testid="column"] .stButton button{
  width:100%;
  min-height:42px;
  padding:10px 13px;
  border:1px solid #2b3a53;
  border-radius:9px;
  background:#172235!important;
  color:#dbe4f1!important;
  font-size:10.5px;
  font-weight:500;
  text-align:left;
  justify-content:flex-start;
  transition:.16s ease;
}

div[data-testid="column"] .stButton button *,
div[data-testid="column"] .stButton button p,
div[data-testid="column"] .stButton button span{
  color:#dbe4f1!important;
}

div[data-testid="column"] .stButton button:hover{
  background:#1c2b43!important;
  color:#ffffff!important;
  border-color:#425a7b;
  transform:translateY(-1px);
  box-shadow:0 6px 18px rgba(0,0,0,.18);
}

div[data-testid="column"] .stButton button:hover *,
div[data-testid="column"] .stButton button:hover p,
div[data-testid="column"] .stButton button:hover span{
  color:#ffffff!important;
}

.st-key-suggestion_0 button{border-left:2px solid #5b8cff!important}
.st-key-suggestion_1 button{border-left:2px solid #ff6b7f!important}
.st-key-suggestion_2 button{border-left:2px solid #f4bd55!important}
.st-key-suggestion_3 button{border-left:2px solid #2bd7a0!important}

/* =========================================================
   CHAT / STREAMLIT NATIVE COMPONENTS
   ========================================================= */

div[data-testid="stChatMessage"]{
  background:#111a2a!important;
  border:1px solid #26364f;
  border-radius:13px;
  padding:5px 8px;
  margin:8px 0;
  box-shadow:0 5px 18px rgba(0,0,0,.14);
}

div[data-testid="stChatMessage"],
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] div{
  color:#dce5f1!important;
}

div[data-testid="stChatMessageAvatarUser"]{
  background:#386bf4!important;
}

div[data-testid="stChatMessageAvatarAssistant"]{
  background:#7658e8!important;
}

div[data-testid="stChatInput"]{
  border:1px solid #33445f!important;
  border-radius:14px;
  background:#111a2a!important;
  box-shadow:0 12px 32px rgba(0,0,0,.22);
}

div[data-testid="stChatInput"] textarea{
  font-size:12px;
  color:#e6edf7!important;
  -webkit-text-fill-color:#e6edf7!important;
}

div[data-testid="stChatInput"] textarea::placeholder{
  color:#71829b!important;
  opacity:1!important;
}

[data-testid="stMetric"]{
  padding:14px;
  border:1px solid #26364f;
  border-radius:12px;
  background:#111a2a!important;
}

[data-testid="stMetricLabel"]{
  color:#91a0b6!important;
}

[data-testid="stMetricValue"]{
  font-family:'Space Grotesk',sans-serif!important;
  color:#f4f7fb!important;
}

[data-testid="stDataFrame"]{
  background:#111a2a!important;
}

.footer-text{
  text-align:center;
  margin-top:27px;
  color:#596b86!important;
  font:500 7.5px 'JetBrains Mono';
  letter-spacing:1px;
  text-transform:uppercase;
}

/* Generic markdown text */
.main .stMarkdown,
.main .stMarkdown p,
.main .stMarkdown span{
  color:inherit;
}

/* Error/success/info blocks stay readable */
[data-testid="stAlert"]{
  color:#e8eef7!important;
}

@media(max-width:900px){
  .main .block-container{padding:18px}
  .kpi-grid{grid-template-columns:1fr 1fr}
}

@media(max-width:650px){
  .kpi-grid,.module-grid{grid-template-columns:1fr}
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============================================================
# HELPERS
# ============================================================

def queue_question(question):
    """Queue a question so it is processed on the next Streamlit rerun."""
    st.session_state.pending_question = question
    st.rerun()


def clear_conversation():
    """Completely reset the current conversation."""
    st.session_state.messages = []
    st.session_state.pending_question = None
    st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
<div class="sb-brand">
<div class="sb-brand-mark">◈</div>
<div class="sb-brand-name">AI Business Analyst</div>
</div>
<div class="sb-brand-sub">Customer Product Intelligence</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------
    # NEW CONVERSATION
    # --------------------------------------------------------

    if st.button(
        "＋  New conversation",
        use_container_width=True,
        key="new_chat_button",
        type="primary",
    ):
        clear_conversation()

    st.markdown('<hr class="sb-rule" />', unsafe_allow_html=True)

    # --------------------------------------------------------
    # QUICK ANALYSIS
    # --------------------------------------------------------

    st.markdown('<div class="sb-label">Quick analysis</div>', unsafe_allow_html=True)

    if st.button("📊  Business Overview", use_container_width=True, key="side_business"):
        queue_question("Give me a complete business overview.")

    if st.button("🔴  Risk Analysis", use_container_width=True, key="side_risk"):
        queue_question("Give me the complete customer risk analysis.")

    if st.button("💰  Profit Analysis", use_container_width=True, key="side_profit"):
        queue_question(
            "Analyze customer profitability and "
            "identify the most important profit segments."
        )

    if st.button("🎯  Retention Priorities", use_container_width=True, key="side_retention"):
        queue_question("Which customers should we prioritize for retention?")

    # --------------------------------------------------------
    # CUSTOMER INTELLIGENCE
    # --------------------------------------------------------

    st.markdown('<div class="sb-label">Customer intelligence</div>', unsafe_allow_html=True)

    if st.button("👤  Customer 360", use_container_width=True, key="side_customer"):
        queue_question(
            "Explain how I can analyze the complete "
            "profile of a specific customer."
        )

    if st.button("📍  Regional Analysis", use_container_width=True, key="side_region"):
        queue_question("Compare customer performance across regions.")

    if st.button("💳  Subscription Analysis", use_container_width=True, key="side_subscription"):
        queue_question("Compare customers by subscription type.")

    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    st.markdown('<div class="sb-label">Dataset</div>', unsafe_allow_html=True)

    total_customers = len(df)

    st.markdown(f"""
<div class="sb-stat">
<div class="sb-stat-num">{total_customers:,}</div>
<div class="sb-stat-label">Customers tracked</div>
</div>
<div class="verified-chip">🔒 Verified Python Analytics</div>
""", unsafe_allow_html=True)


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown("""
<div class="app-header">
<div class="app-header-left">
<div class="app-header-mark">◈</div>
<div>
<div class="app-header-title">Customer Product Intelligence</div>
<div class="app-header-subtitle">AI-powered customer analytics &amp; business intelligence</div>
</div>
</div>
<div class="ticker">
<span class="ticker-dot"></span>
AI Analyst Online
</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    # --------------------------------------------------------
    # PREMIUM LIGHT EXECUTIVE DASHBOARD
    # --------------------------------------------------------

    total_customers = len(df)

    def _sum_value(column):
        try:
            if column in df.columns:
                return f"{df[column].sum():,.0f}"
        except Exception:
            pass
        return "—"

    revenue = _sum_value("total_revenue")
    profit = _sum_value("total_profit")

    churn = "—"
    try:
        if "actual_churn" in df.columns:
            churn = f"{df['actual_churn'].mean()*100:.1f}%"
        elif "churn_probability" in df.columns:
            churn = f"{df['churn_probability'].mean()*100:.1f}%"
    except Exception:
        pass

    st.markdown(f"""
    <div class="hero">
      <div class="hero-kicker">EXECUTIVE INSIGHTS</div>
      <h1>Understand your customers. Drive growth.</h1>
      <p>Explore customer behavior, predict risks, identify opportunities and make data-driven decisions with AI-powered analytics.</p>
      <div class="hero-status">● PYTHON ANALYTICS VERIFIED &nbsp; · &nbsp; {total_customers:,} CUSTOMER RECORDS</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi">
        <div class="kpi-top"><div class="kpi-label">Customers</div><div class="kpi-icon icon-blue">♙</div></div>
        <div class="kpi-value">{total_customers:,}</div><div class="kpi-note">Records tracked</div>
      </div>
      <div class="kpi">
        <div class="kpi-top"><div class="kpi-label">Revenue</div><div class="kpi-icon icon-amber">◉</div></div>
        <div class="kpi-value">{revenue}</div><div class="kpi-note">Customer-level total</div>
      </div>
      <div class="kpi">
        <div class="kpi-top"><div class="kpi-label">Profit</div><div class="kpi-icon icon-violet">▥</div></div>
        <div class="kpi-value">{profit}</div><div class="kpi-note">Customer-level total</div>
      </div>
      <div class="kpi">
        <div class="kpi-top"><div class="kpi-label">Churn indicator</div><div class="kpi-icon icon-red">◔</div></div>
        <div class="kpi-value">{churn}</div><div class="kpi-note">Current dataset signal</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-head">
      <div>
        <div class="section-title">Analysis workspace</div>
        <div class="section-sub">Focused modules for the questions that matter most.</div>
      </div>
      <div class="section-pill">7 INTELLIGENCE MODULES</div>
    </div>

    <div class="module-grid">
      <div class="module">
        <div class="module-icon mi-blue">▥</div>
        <div><h3>Business Overview</h3><p>Revenue, profit, churn and customer KPIs.</p></div>
        <div class="module-arrow">›</div>
      </div>
      <div class="module">
        <div class="module-icon mi-red">◉</div>
        <div><h3>Risk Analysis</h3><p>Churn probability, risk segments and exposure.</p></div>
        <div class="module-arrow">›</div>
      </div>
      <div class="module">
        <div class="module-icon mi-violet">♙</div>
        <div><h3>Customer 360</h3><p>Investigate an individual customer profile.</p></div>
        <div class="module-arrow">›</div>
      </div>
      <div class="module">
        <div class="module-icon mi-green">◎</div>
        <div><h3>Retention Priorities</h3><p>Identify customers requiring attention.</p></div>
        <div class="module-arrow">›</div>
      </div>
    </div>

    <div class="ask-wrap">
      <div class="ask-title">Ask the intelligence layer</div>
      <div class="ask-sub">Use a shortcut below, or type your own business question in the analyst input.</div>
    """, unsafe_allow_html=True)

    sq_col1, sq_col2 = st.columns(2)

    with sq_col1:
        if st.button("💬  Tell me everything about C04291", key="suggestion_0", use_container_width=True):
            queue_question("Tell me everything about C04291")
        if st.button("💬  Which region has the highest profit?", key="suggestion_2", use_container_width=True):
            queue_question("Which region has the highest profit?")

    with sq_col2:
        if st.button("💬  How many high-risk customers are there?", key="suggestion_1", use_container_width=True):
            queue_question("How many high-risk customers are there?")
        if st.button("💬  Compare Free and Premium customers.", key="suggestion_3", use_container_width=True):
            queue_question("Compare Free and Premium customers.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar="✨"):
            st.markdown(message["content"])
    else:
        with st.chat_message("user"):
            st.markdown(message["content"])


# ============================================================
# PENDING QUESTION
# ============================================================

pending_question = st.session_state.pending_question
st.session_state.pending_question = None


# ============================================================
# CHAT INPUT
# ============================================================

typed_question = st.chat_input("Ask anything about your business...")


# ============================================================
# DETERMINE QUESTION
# ============================================================

question = None

if pending_question:
    question = pending_question
elif typed_question:
    question = typed_question


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    # --------------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant", avatar="✨"):

        with st.spinner("Analyzing verified customer data..."):

            try:
                answer = ask_gemini(question)

            except Exception as error:

                error_text = str(error).lower()

                if (
                    "429" in error_text
                    or "quota" in error_text
                    or "too_many_requests" in error_text
                    or "rate limit" in error_text
                ):
                    answer = (
                        "### ⏳ AI temporarily rate-limited\n\n"
                        "Gemini's current request limit has been "
                        "reached.\n\n"
                        "Please wait for the quota window to reset "
                        "and try again.\n\n"
                        "Your customer data and verified Python "
                        "analytics are unaffected."
                    )
                else:
                    answer = (
                        "### ⚠️ Something went wrong\n\n"
                        "The analysis could not be completed "
                        "right now. Please try again."
                    )

        st.markdown(answer)

    # --------------------------------------------------------
    # SAVE AI RESPONSE
    # --------------------------------------------------------

    st.session_state.messages.append({"role": "assistant", "content": answer})


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer-text">Customer Product Intelligence · Verified Python Analytics · AI Business Analyst</div>
""", unsafe_allow_html=True)