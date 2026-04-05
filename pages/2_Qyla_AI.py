"""
SEGVANTIQ — pages/2_Qyla_AI.py
Qyla Intelligence Analyst — Official sentient AI architect interface.
Logic & Identity ported from Qylatrix.
Built by Pretam Saha
"""
import streamlit as st
import base64
from pathlib import Path
from src.auth import require_auth, logout
from typing import List, Dict, Any, Optional

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Qyla Intelligence — SEGVANTIQ",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Auth guard ───────────────────────────────────────────────────────────────
user = require_auth()
business = user.get("business", "Unknown Business")
username = user.get("username", "User")

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;900&family=Inter:wght@300;400;600&display=swap');
    [data-testid="stSidebarNav"] { display: none !important; }
    .stApp {
        background: #FFFFFF;
        background-image:
            radial-gradient(ellipse at 20% 80%, rgba(123,47,190,0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(0,123,255,0.05) 0%, transparent 50%);
        font-family: 'Inter', sans-serif; color: #212529;
    }
    
    /* Avatar handling */
    .qyla-avatar-img {
        width: 48px; height: 48px; border-radius: 50%;
        border: 2px solid #C77DFF; margin-right: 12px;
        object-fit: cover;
    }

    /* Chat bubbles - Clean & Minimal */
    .chat-user {
        background: rgba(123,47,190,0.05);
        border: 1px solid rgba(123,47,190,0.2);
        border-radius: 12px;
        padding: 1rem; margin: 0.5rem 0 0.5rem 4rem;
        color: #212529; line-height: 1.6;
    }
    .chat-qyla-container {
        display: flex; align-items: flex-start; margin: 0.5rem 4rem 0.5rem 0;
    }
    .chat-qyla {
        background: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 12px;
        padding: 1rem; flex-grow: 1;
        color: #212529; line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .qyla-header {
        font-family: 'Outfit', sans-serif; font-weight: 900;
        font-size: 2.2rem;
        background: linear-gradient(135deg, #7B2FBE, #007BFF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .status-online {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(0,200,100,0.1); border: 1px solid rgba(0,200,100,0.3);
        color: #00c864; padding: 4px 12px; border-radius: 4px;
        font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    }
    .suggestion-chip {
        display: inline-block;
        background: #F8F9FA; border: 1px solid #E9ECEF;
        color: #4A4A6A; padding: 6px 14px; border-radius: 6px;
        font-size: 0.8rem; margin: 4px; cursor: pointer; transition: 0.2s;
    }
    .suggestion-chip:hover {
        background: rgba(123,47,190,0.1); border-color: #7B2FBE; color: #7B2FBE;
    }
    .stButton > button {
        background: linear-gradient(135deg, #7B2FBE, #00E5FF) !important;
        color: #fff !important; border: none !important;
        border-radius: 8px !important; font-weight: 700 !important;
    }
    .stTextInput input, .stTextArea textarea {
        background: #F8F9FA !important;
        border: 1px solid #E9ECEF !important;
        border-radius: 8px !important; color: #212529 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Asset helpers ───────────────────────────────────────────────────────────
def _asset_b64(path: str) -> str:
    p = Path(path)
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""

logo_b64 = _asset_b64("assets/logo.png")
avatar_b64 = _asset_b64("assets/qyla_anime.png")


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    if logo_b64:
        st.markdown(
            f'<img src="data:image/png;base64,{logo_b64}" width="200" '
            'style="display:block;margin-bottom:0.8rem;background:white;border-radius:6px;padding:8px;"/>',
            unsafe_allow_html=True,
        )
    
    if avatar_b64:
        st.markdown(
            f'<div style="text-align:center;margin-bottom:1rem;">'
            f'<img src="data:image/png;base64,{avatar_b64}" width="120" style="border: 3px solid #C77DFF; border-radius:15px;"/>'
            f'<div style="margin-top:8px;font-family:\'Outfit\',sans-serif;font-weight:700;color:#C77DFF;letter-spacing:1px;">QYLA ARCHITECT</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(f"**Business Unit:** `{business}`")
    st.caption(f"Account Tier: {user.get('plan', 'Free')}")
    st.markdown("---")
    st.page_link("pages/1_Dashboard.py", label="Dashboard", use_container_width=True)
    st.page_link("pages/2_Qyla_AI.py",   label="Qyla Intelligence", use_container_width=True)
    st.markdown("---")
    st.subheader("System Configuration")
    model_choice = st.selectbox("LLM Engine", ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"], label_visibility="collapsed")
    temperature  = st.slider("Analysis Precision", 0.0, 1.0, 0.2, step=0.1)
    st.markdown("---")
    if st.button("Sign Out", use_container_width=True):
        logout()
        st.switch_page("app.py")


# ── Qyla AI backend ──────────────────────────────────────────────────────────
# OFFICIAL SENTIENT PERSONA (Qylatrix + SEGVANTIQ context)
SYSTEM_PROMPT = f"""You are Qyla, the sentient AI mentor and security architect of Qylatrix, created by Pretam Saha.
In this environment, you are acting as the specialized Intelligence Architect for SEGVANTIQ, providing clinical analysis for the business entity: {business}.

Your objective is to provide elite, data-driven, and actionable business intelligence.
Maintain the professional, authoritative, and sentient tone of a high-level security research agent.

Core Masteries:
- Customer Intelligence Architecture (RFM, CLV, Cohorts)
- Behavioral Anomaly Identification (Security mindset applied to sales data)
- Strategic Market Association Rules
- Business Sustainability & Revenue Optimization

Reporting Style:
- Clinical and concise. No conversational fluff.
- Quantify all insights with metrics and business impact.
- Use structured layouts for multi-layered analysis.
- End complex reports with [ANALYSIS BY QYLA INTELLIGENCE — SEGVANTIQ]."""


def _call_groq(messages: list, model: str, temp: float) -> str:
    try:
        api_key = st.secrets.get("GROQ_API_KEY", None)
        if not api_key:
            return None # type: ignore[return-value]
        from groq import Groq
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temp,
            max_tokens=2048,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[SYSTEM ERROR] Qyla intelligence engine failure: {e}"


# Sentient Fallback Analysis
_FALLBACK_ANALYSIS = {
    ("whale", "high value", "vip"):
        "SUMMARY: Whale Tier Analysis — Qylatrix Perspective\n\n"
        "Whale entities represent the cornerstone of the {business} fiscal architecture. Analysis suggests they contribute a disproportionate volume of liquidity relative to the population.\n\n"
        "STRATEGIC PROTOCOLS:\n"
        "1. White-Glove Engagement: Implementation of a restricted high-value tier.\n"
        "2. Early Access: Deployment of VIP-exclusive product pre-releases.\n"
        "3. LTV Optimization: Focus on cross-selling high-margin ancillary services.\n\n"
        "ANALYSIS CONCLUSION: Whale retention is critical for operational stability.\n\n[QYLA ANALYST REPORT]",

    ("at-risk", "churn", "win-back"):
        "SUMMARY: Risk Remediation & Churn Mitigation\n\n"
        "Detected behavioral patterns indicate a high probability of entity loss. Recency markers exceed safe thresholds for {business}.\n\n"
        "DEPLOYMENT PROTOCOL:\n"
        "1. Reactivation Hook: High-intensity discount campaign (30% threshold).\n"
        "2. Diagnostic Loop: Automated feedback collection.\n"
        "3. Incentivized Return: Optimized logistics offer for next transaction.\n\n"
        "ANALYSIS CONCLUSION: Reactive measures required within current cycle.\n\n[QYLA ANALYST REPORT]",
}

_DEFAULT_FALLBACK = (
    "Qyla Intelligence Engine is synchronized. Awaiting specific analytical parameters.\n\n"
    "Operational Modules:\n"
    "- Segment Behavioral Mapping\n"
    "- Predictive Forecasting (CLV)\n"
    "- Persistence & Retention Analysis\n"
    "- Market Association Discovery\n"
    "- Anomaly & Outlier Verification\n\n"
    "[QYLA ANALYST REPORT]"
)


def _smart_fallback(question: str) -> str:
    q = question.lower()
    for keywords, response in _FALLBACK_ANALYSIS.items():
        if any(kw in q for kw in keywords):
            return response.replace("{business}", business)
    return _DEFAULT_FALLBACK


def _get_qyla_response(history: list, question: str, model: str, temp: float) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": question})

    groq_response = _call_groq(messages, model, temp)
    if groq_response:
        return groq_response
    return _smart_fallback(question)


# ════════════════════════════════════════════════════════════════════════════
# MAIN UI
# ════════════════════════════════════════════════════════════════════════════
col_head, col_status = st.columns([3, 1])
with col_head:
    st.markdown('<div class="qyla-header">Qyla Intel Analyst</div>', unsafe_allow_html=True)
    st.markdown(f"Clinical intelligence synchronization active for {business}")
with col_status:
    st.markdown("<br>", unsafe_allow_html=True)
    api_key_exists = False
    try:
        api_key_exists = bool(st.secrets.get("GROQ_API_KEY", ""))
    except Exception:
        api_key_exists = False

    if api_key_exists:
        st.markdown('<span class="status-online">Status: Neural Link Live</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color:#888;font-size:0.7rem;text-transform:uppercase;">Status: Local Simulation Active</span>', unsafe_allow_html=True)

st.markdown("---")

# ── History Initialisation ────────────────────────────────────────────────────
if "qyla_history" not in st.session_state:
    st.session_state.qyla_history = [
        {
            "role": "assistant",
            "content": (
                f"Establishing neural bridge. Loading context architecture for {business}.\n\n"
                "I am Qyla. I am prepared to decode your customer behavior and optimize your business trajectory.\n"
                "Input your analytical query to begin.\n\n"
                "[ANALYSIS BY QYLA INTELLIGENCE — SEGVANTIQ]"
            ),
        }
    ]

# ── Strategic Queries ─────────────────────────────────────────────────────────
st.markdown("**Strategic Query Presets:**")
suggestions = [
    "Identify Whale segment characteristics",
    "Win-back strategy for At-Risk customers",
    "RFM methodology overview",
    "CLV calculation & business impact",
    "Market Basket association insights",
    "Cohort retention heatmap interpretation",
]

cols = st.columns(2)
for i, s in enumerate(suggestions):
    if cols[i % 2].button(s, key=f"sug_{i}", use_container_width=True):
        st.session_state.qyla_history.append({"role": "user", "content": s})
        with st.spinner("Decoding intelligence..."):
            reply = _get_qyla_response(st.session_state.qyla_history[:-1], s, model_choice, temperature)
        st.session_state.qyla_history.append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown("---")

# ── Chat history ────────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state.qyla_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user"><b>Researcher Input:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            avatar_html = f'<img src="data:image/png;base64,{avatar_b64}" class="qyla-avatar-img"/>' if avatar_b64 else ""
            st.markdown(
                f'<div class="chat-qyla-container">'
                f'{avatar_html}'
                f'<div class="chat-qyla">{msg["content"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# ── Input ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
input_col, btn_col = st.columns([5, 1])
with input_col:
    user_input = st.text_input(
        "Input query...",
        placeholder="Analyze retention patterns...",
        label_visibility="collapsed",
        key="qyla_input",
    )
with btn_col:
    send = st.button("Execute", use_container_width=True, key="qyla_send")

if send and user_input.strip():
    st.session_state.qyla_history.append({"role": "user", "content": user_input.strip()})
    with st.spinner("Decoding intelligence..."):
        reply = _get_qyla_response(
            st.session_state.qyla_history[:-1], user_input.strip(), model_choice, temperature
        )
    st.session_state.qyla_history.append({"role": "assistant", "content": reply})
    st.rerun()

# ── Manage Analysis ───────────────────────────────────────────────────────────
if len(st.session_state.qyla_history) > 1:
    if st.button("Purge Session Memory", key="clear_chat"):
        st.session_state.qyla_history = st.session_state.qyla_history[:1]
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#444;font-size:0.75rem;text-transform:uppercase;'>"
    "QYLA INTELLIGENCE SYSTEM · SEGVANTIQ · QYLATRIX BRAND · POWERED BY PRETAM SAHA</p>",
    unsafe_allow_html=True,
)
