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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');

:root {
--void: #05070d;
--glass: rgba(255,255,255,0.045);
--glass-hi: rgba(255,255,255,0.09);
--border: rgba(255,255,255,0.09);
--border-hi: rgba(255,255,255,0.22);
--blue: #3b82f6;
--magenta: #ec4899;
--amber: #f5b23c;
--emerald: #10e0a4;
--violet: #8b5cf6;
--cyan: #22d3ee;
--text-hi: #f8fafc;
--text-mid: #9aa4b2;
--text-low: #5c6675;
}

html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; }
::selection { background: rgba(139,92,246,0.4); color: #fff; }

@keyframes bgshift { 0% { background-position: 0% 0%, 100% 0%, 0% 100%, 100% 100%; } 100% { background-position: 6% 4%, 94% 6%, 4% 94%, 96% 96%; } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes blink { 0%,100% {opacity:1;} 50% {opacity:0.35;} }
@keyframes shimmer { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }

/* aurora lives on the background property itself (not a positioned
   overlay element) so it can never stack on top of real content */
.stApp {
background-color: var(--void);
background-image:
radial-gradient(600px 420px at 8% 5%, rgba(59,130,246,0.20), transparent 60%),
radial-gradient(560px 420px at 92% 15%, rgba(236,72,153,0.16), transparent 60%),
radial-gradient(620px 460px at 25% 95%, rgba(16,224,164,0.13), transparent 60%),
radial-gradient(500px 400px at 80% 90%, rgba(139,92,246,0.15), transparent 60%);
background-repeat: no-repeat;
background-size: 120% 120%;
animation: bgshift 24s ease-in-out infinite alternate;
}
@media (prefers-reduced-motion: reduce) { .stApp, .ring::before, .ticker-dot { animation: none !important; } }

.main .block-container { max-width: 1180px; padding-top: 20px; padding-bottom: 110px; }
#MainMenu, footer {visibility: hidden;}

button:focus-visible { outline: 2px solid var(--violet) !important; outline-offset: 2px; }

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
background: linear-gradient(180deg, #07090f 0%, #05070c 100%);
border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 22px; }

.sb-brand { display:flex; align-items:center; gap:11px; margin-bottom:3px; }
.sb-brand-mark {
width:36px; height:36px; border-radius:11px; flex-shrink:0;
background: linear-gradient(135deg, var(--blue), var(--violet) 50%, var(--magenta));
display:flex; align-items:center; justify-content:center;
font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:15px; color:#fff;
box-shadow: 0 0 18px rgba(139,92,246,0.55);
}
.sb-brand-name { font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:15px; color:var(--text-hi); line-height:1.15; }
.sb-brand-sub { font-family:'JetBrains Mono',monospace; font-size:9.5px; letter-spacing:1px; color:var(--text-low); margin-left:47px; margin-bottom:20px; text-transform:uppercase; }

section[data-testid="stSidebar"] .stButton button {
width:100%; border-radius:10px; border:1px solid transparent; background-color: var(--glass);
color:#d7dce3; min-height:40px; font-family:'Inter',sans-serif; font-size:13.5px; font-weight:500;
text-align:left; justify-content:flex-start; padding-left:12px;
transition: all .18s cubic-bezier(.2,.8,.3,1.2);
}
section[data-testid="stSidebar"] .stButton button:hover { transform: translateX(3px) scale(1.015); background-color: var(--glass-hi); color:var(--text-hi); }
section[data-testid="stSidebar"] .stButton button:active { transform: scale(0.98); }

section[data-testid="stSidebar"] .stButton button[kind="primary"] {
background: linear-gradient(90deg, var(--blue), var(--violet), var(--magenta), var(--blue));
background-size: 300% 100%;
animation: shimmer 6s linear infinite;
color:#fff; font-weight:600; border:none;
box-shadow: 0 6px 22px -4px rgba(139,92,246,0.65);
}
section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover { transform: translateY(-1px) scale(1.02); box-shadow: 0 10px 30px -4px rgba(139,92,246,0.85); }

.st-key-side_business button { border:1px solid rgba(59,130,246,0.35) !important; }
.st-key-side_business button:hover { box-shadow: 0 6px 20px -6px rgba(59,130,246,0.55); border-color: var(--blue) !important; }
.st-key-side_risk button { border:1px solid rgba(236,72,153,0.35) !important; }
.st-key-side_risk button:hover { box-shadow: 0 6px 20px -6px rgba(236,72,153,0.55); border-color: var(--magenta) !important; }
.st-key-side_profit button { border:1px solid rgba(245,178,60,0.35) !important; }
.st-key-side_profit button:hover { box-shadow: 0 6px 20px -6px rgba(245,178,60,0.5); border-color: var(--amber) !important; }
.st-key-side_retention button { border:1px solid rgba(16,224,164,0.35) !important; }
.st-key-side_retention button:hover { box-shadow: 0 6px 20px -6px rgba(16,224,164,0.5); border-color: var(--emerald) !important; }
.st-key-side_customer button { border:1px solid rgba(139,92,246,0.35) !important; }
.st-key-side_customer button:hover { box-shadow: 0 6px 20px -6px rgba(139,92,246,0.55); border-color: var(--violet) !important; }
.st-key-side_region button { border:1px solid rgba(34,211,238,0.35) !important; }
.st-key-side_region button:hover { box-shadow: 0 6px 20px -6px rgba(34,211,238,0.5); border-color: var(--cyan) !important; }
.st-key-side_subscription button { border:1px solid rgba(59,130,246,0.35) !important; }
.st-key-side_subscription button:hover { box-shadow: 0 6px 20px -6px rgba(59,130,246,0.55); border-color: var(--blue) !important; }

.sb-rule { height:1px; background: linear-gradient(90deg, transparent, var(--border-hi), transparent); margin:18px 0 16px 0; border:none; }

.sb-label {
color:var(--text-low); font-family:'JetBrains Mono',monospace; font-size:9.5px; font-weight:600;
letter-spacing:1.6px; margin:14px 0 9px 2px; text-transform:uppercase;
}

.sb-stat {
text-align:center; padding: 16px 10px; border-radius:14px; margin-top:4px;
background: linear-gradient(160deg, rgba(59,130,246,0.14), rgba(236,72,153,0.08));
border: 1px solid var(--border);
}
.sb-stat-num {
font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:32px; line-height:1;
background: linear-gradient(90deg, #fff, var(--cyan)); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
}
.sb-stat-label { font-family:'JetBrains Mono',monospace; font-size:9.5px; letter-spacing:1.4px; color:var(--text-low); text-transform:uppercase; margin-top:6px; }

.verified-chip {
display:flex; align-items:center; gap:7px; margin-top:12px; padding:10px 12px; border-radius:10px;
background: rgba(16,224,164,0.1); border:1px solid rgba(16,224,164,0.35);
font-family:'JetBrains Mono',monospace; font-size:10.5px; color:#5eead4; font-weight:500; letter-spacing:0.3px;
box-shadow: 0 0 16px rgba(16,224,164,0.15);
}

/* ---------- HEADER ---------- */

.app-header {
display:flex; align-items:center; justify-content:space-between;
padding:6px 4px 20px 4px; margin-bottom:8px; border-bottom:1px solid var(--border);
}
.app-header-left { display:flex; align-items:center; gap:14px; }
.app-header-mark {
width:44px; height:44px; border-radius:13px;
background: linear-gradient(135deg, var(--blue), var(--violet) 50%, var(--magenta));
display:flex; align-items:center; justify-content:center;
font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:19px; color:#fff;
box-shadow: 0 0 24px rgba(139,92,246,0.5);
}
.app-header-title { font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:600; color:var(--text-hi); line-height:1.2; }
.app-header-subtitle { font-family:'Inter',sans-serif; font-size:12.5px; color:var(--text-mid); margin-top:2px; }

.ticker {
display:flex; align-items:center; gap:8px; padding:8px 15px; border-radius:100px;
border:1px solid rgba(16,224,164,0.4); background: rgba(16,224,164,0.09);
font-family:'JetBrains Mono',monospace; font-size:11.5px; letter-spacing:0.4px; color:#5eead4; font-weight:500;
box-shadow: 0 0 20px rgba(16,224,164,0.18);
}
.ticker-dot { width:7px; height:7px; border-radius:50%; background:var(--emerald); box-shadow:0 0 0 4px rgba(16,224,164,0.22); animation: blink 2s ease-in-out infinite; }

/* ---------- HERO ---------- */

.hero-wrap { position:relative; text-align:center; padding:44px 10px 6px 10px; }
.ring { position:relative; width:68px; height:68px; margin:0 auto 20px auto; }
.ring::before {
content:""; position:absolute; inset:-6px; border-radius:50%;
background: conic-gradient(from 0deg, var(--blue), var(--violet), var(--magenta), var(--amber), var(--emerald), var(--blue));
animation: spin 6s linear infinite; opacity: 0.85;
}
.ring-core {
position:absolute; inset:0; border-radius:50%; background: var(--void);
display:flex; align-items:center; justify-content:center; font-size:26px;
}
.hero-title {
font-family:'Space Grotesk',sans-serif; font-size:32px; font-weight:700; margin-bottom:10px; line-height:1.2;
background: linear-gradient(90deg, #fff 20%, var(--cyan) 50%, var(--violet) 80%);
-webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
}
.hero-subtitle { font-family:'Inter',sans-serif; font-size:14.5px; color:var(--text-mid); max-width:520px; margin:0 auto 34px auto; line-height:1.65; }

/* ---------- QUICK CARDS ---------- */

.qcard {
position:relative; border-radius:16px; border:1px solid var(--border); background: var(--glass);
backdrop-filter: blur(14px); padding:20px 17px 18px 17px; height:100%; overflow:hidden;
transition: all .2s cubic-bezier(.2,.8,.3,1.2);
}
.qcard:hover { transform: translateY(-5px) scale(1.015); background: var(--glass-hi); }
.qcard::after { content:""; position:absolute; top:0; left:0; right:0; height:3px; }
.qc-blue::after { background: linear-gradient(90deg,var(--blue),#60a5fa); }
.qc-blue:hover { border-color: rgba(59,130,246,0.6); box-shadow: 0 14px 34px -10px rgba(59,130,246,0.4); }
.qc-magenta::after { background: linear-gradient(90deg,var(--magenta),#f9a8d4); }
.qc-magenta:hover { border-color: rgba(236,72,153,0.6); box-shadow: 0 14px 34px -10px rgba(236,72,153,0.4); }
.qc-violet::after { background: linear-gradient(90deg,var(--violet),#c4b5fd); }
.qc-violet:hover { border-color: rgba(139,92,246,0.6); box-shadow: 0 14px 34px -10px rgba(139,92,246,0.4); }
.qc-emerald::after { background: linear-gradient(90deg,var(--emerald),#6ee7b7); }
.qc-emerald:hover { border-color: rgba(16,224,164,0.6); box-shadow: 0 14px 34px -10px rgba(16,224,164,0.4); }

.qcard-icon {
width:38px; height:38px; border-radius:11px; display:flex; align-items:center; justify-content:center; font-size:17px; margin-bottom:13px;
}
.qi-blue { background: linear-gradient(135deg, rgba(59,130,246,0.35), rgba(59,130,246,0.1)); box-shadow: 0 0 16px rgba(59,130,246,0.3); }
.qi-magenta { background: linear-gradient(135deg, rgba(236,72,153,0.35), rgba(236,72,153,0.1)); box-shadow: 0 0 16px rgba(236,72,153,0.3); }
.qi-violet { background: linear-gradient(135deg, rgba(139,92,246,0.35), rgba(139,92,246,0.1)); box-shadow: 0 0 16px rgba(139,92,246,0.3); }
.qi-emerald { background: linear-gradient(135deg, rgba(16,224,164,0.35), rgba(16,224,164,0.1)); box-shadow: 0 0 16px rgba(16,224,164,0.3); }

.qcard-title { font-family:'Space Grotesk',sans-serif; font-size:15px; font-weight:600; color:var(--text-hi); margin-bottom:4px; }
.qcard-text { font-family:'Inter',sans-serif; font-size:12px; color:var(--text-mid); line-height:1.5; }

/* ---------- SUGGESTED QUESTIONS ---------- */

.suggest-label { margin-top:36px; }

div[data-testid="column"] .stButton button {
border-radius:14px; border:1px solid var(--border); background: var(--glass);
color:#d7dce3; font-family:'Inter',sans-serif; font-size:13.5px; font-weight:500;
text-align:left; justify-content:flex-start; padding:14px 16px; min-height:48px;
white-space:normal; line-height:1.4;
transition: all .18s cubic-bezier(.2,.8,.3,1.2);
}
div[data-testid="column"] .stButton button:hover { transform: translateY(-3px) scale(1.015); background: var(--glass-hi); color:var(--text-hi); }
div[data-testid="column"] .stButton button:active { transform: scale(0.98); }

.st-key-suggestion_0 button { border-left:3px solid var(--blue) !important; }
.st-key-suggestion_0 button:hover { box-shadow: 0 10px 26px -8px rgba(59,130,246,0.5); border-color: var(--blue) !important; }
.st-key-suggestion_1 button { border-left:3px solid var(--magenta) !important; }
.st-key-suggestion_1 button:hover { box-shadow: 0 10px 26px -8px rgba(236,72,153,0.5); border-color: var(--magenta) !important; }
.st-key-suggestion_2 button { border-left:3px solid var(--amber) !important; }
.st-key-suggestion_2 button:hover { box-shadow: 0 10px 26px -8px rgba(245,178,60,0.45); border-color: var(--amber) !important; }
.st-key-suggestion_3 button { border-left:3px solid var(--emerald) !important; }
.st-key-suggestion_3 button:hover { box-shadow: 0 10px 26px -8px rgba(16,224,164,0.45); border-color: var(--emerald) !important; }

/* ---------- CHAT ---------- */

div[data-testid="stChatMessage"] {
border-radius:16px; border:1px solid var(--border); background: var(--glass); backdrop-filter: blur(10px); padding:4px 6px;
}
div[data-testid="stChatMessageAvatarUser"] { background: linear-gradient(135deg, var(--cyan), var(--blue)) !important; }
div[data-testid="stChatMessageAvatarAssistant"] {
background: linear-gradient(135deg, var(--blue), var(--violet), var(--magenta)) !important;
box-shadow: 0 0 14px rgba(139,92,246,0.5);
}
div[data-testid="stChatInput"] textarea { font-family:'Inter',sans-serif; font-size:14px; }
div[data-testid="stChatInput"] { border-radius:16px; border:1px solid var(--border-hi); background: var(--glass); }

/* ---------- FOOTER ---------- */

.footer-text {
text-align:center; color:var(--text-low); font-family:'JetBrains Mono',monospace; font-size:10px;
letter-spacing:0.8px; margin-top:32px; text-transform:uppercase;
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

    st.markdown("""
<div class="hero-wrap">
<div class="ring"><div class="ring-core">✨</div></div>
<div class="hero-title">Your AI Business Analyst</div>
<div class="hero-subtitle">Ask about churn, profit, retention or any customer by name — powered by verified Python analytics and explained in plain language.</div>
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------
    # QUICK ANALYSIS CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
<div class="qcard qc-blue">
<div class="qcard-icon qi-blue">📊</div>
<div class="qcard-title">Business Overview</div>
<div class="qcard-text">KPIs, churn and profitability</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="qcard qc-magenta">
<div class="qcard-icon qi-magenta">🔴</div>
<div class="qcard-title">Risk Analysis</div>
<div class="qcard-text">Find customers at risk</div>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown("""
<div class="qcard qc-violet">
<div class="qcard-icon qi-violet">👤</div>
<div class="qcard-title">Customer 360</div>
<div class="qcard-text">Analyze any customer</div>
</div>
""", unsafe_allow_html=True)

    with col4:
        st.markdown("""
<div class="qcard qc-emerald">
<div class="qcard-icon qi-emerald">🎯</div>
<div class="qcard-title">Retention</div>
<div class="qcard-text">Prioritize customer actions</div>
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------
    # SUGGESTED QUESTIONS
    # --------------------------------------------------------

    st.markdown(
        '<div class="suggest-label sb-label">Try asking</div>',
        unsafe_allow_html=True,
    )

    sq_col1, sq_col2 = st.columns(2)

    with sq_col1:

        if st.button(
            "💬  Tell me everything about C04291",
            key="suggestion_0",
            use_container_width=True,
        ):
            queue_question("Tell me everything about C04291")

        if st.button(
            "💬  Which region has the highest profit?",
            key="suggestion_2",
            use_container_width=True,
        ):
            queue_question("Which region has the highest profit?")

    with sq_col2:

        if st.button(
            "💬  How many high-risk customers are there?",
            key="suggestion_1",
            use_container_width=True,
        ):
            queue_question("How many high-risk customers are there?")

        if st.button(
            "💬  Compare Free and Premium customers.",
            key="suggestion_3",
            use_container_width=True,
        ):
            queue_question("Compare Free and Premium customers.")


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