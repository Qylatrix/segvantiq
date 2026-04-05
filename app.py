"""
SEGVANTIQ — app.py (Landing Page + Auth)
Entry point for the multi-tenant SaaS platform.
Built by Pretam Saha | Qylatrix Brand
"""
import streamlit as st
import base64
from pathlib import Path
from src.auth import login, register, is_authenticated

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SEGVANTIQ — AI Customer Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Redirect if already logged in ────────────────────────────────────────────
if is_authenticated():
    st.switch_page("pages/1_Dashboard.py")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800;900&display=swap');

    /* ── Reset Streamlit chrome ── */
    [data-testid="stSidebarNav"], header, footer,
    [data-testid="stToolbar"], .stDeployButton { display: none !important; }

    html, body, .stApp, .main, [data-testid="stAppViewContainer"],
    [data-testid="stMainBlockContainer"], section.main {
        background: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        color: #111827;
    }

    /* ── Layout constraint ── */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
        max-width: 1280px !important;
    }

    /* ── Navigation ── */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem 0;
        border-bottom: 1px solid #F3F4F6;
        margin-bottom: 5rem;
    }
    .nav-tag {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.8rem;
        font-weight: 500;
        color: #6B7280;
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 100px;
        padding: 6px 16px;
    }
    .nav-tag::before {
        content: '';
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #00B8C8;
        display: inline-block;
    }

    /* ── Hero text ── */
    .eyebrow {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #00B8C8;
        margin-bottom: 1.4rem;
    }
    .hero-h1 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 900;
        font-size: 3.1rem;
        line-height: 1.12;
        letter-spacing: -1.2px;
        color: #111827;
        margin-bottom: 1.4rem;
    }
    .hero-h1 .accent {
        color: #1A2640;
        background: linear-gradient(90deg, #00B8C8 0%, #6B3FAA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-p {
        font-size: 1rem;
        line-height: 1.75;
        color: #6B7280;
        max-width: 460px;
        margin-bottom: 2.5rem;
    }

    /* ── Feature tags ── */
    .tag-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 2.8rem; }
    .tag {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 6px;
        padding: 4px 12px;
        font-size: 0.78rem;
        color: #374151;
        font-weight: 500;
        transition: border-color 0.2s, color 0.2s;
    }

    /* ── Stats ── */
    .stat-row {
        display: flex;
        gap: 2.5rem;
        border-top: 1px solid #F3F4F6;
        padding-top: 1.8rem;
    }
    .stat-num {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.75rem;
        font-weight: 800;
        color: #111827;
    }
    .stat-lbl {
        font-size: 0.77rem;
        color: #9CA3AF;
        font-weight: 500;
        margin-top: 2px;
    }

    /* ── Auth card ── */
    [data-testid="column"]:last-child .stTabs {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow:
            0 1px 3px rgba(0,0,0,0.06),
            0 10px 40px rgba(0,0,0,0.07) !important;
    }

    /* ── Tab bar ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #F9FAFB !important;
        border-radius: 8px !important;
        padding: 3px !important;
        gap: 3px !important;
        border: 1px solid #E5E7EB !important;
        margin-bottom: 1.5rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px !important;
        color: #9CA3AF !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 0.4rem 1rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #111827 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }

    /* ── Auth headings ── */
    .auth-h {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.2rem;
    }
    .auth-sub { font-size: 0.83rem; color: #9CA3AF; margin-bottom: 1.5rem; }

    /* ── Inputs ── */
    .stTextInput > div > div > input {
        background: #F9FAFB !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        color: #111827 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        padding: 0.6rem 0.85rem !important;
    }
    .stTextInput > div > div > input::placeholder { color: #D1D5DB !important; }
    .stTextInput > div > div > input:focus {
        border-color: #00B8C8 !important;
        box-shadow: 0 0 0 3px rgba(0,184,200,0.1) !important;
        background: #FFFFFF !important;
        outline: none !important;
    }
    .stTextInput label {
        color: #374151 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }

    /* ── Button ── */
    .stButton > button {
        background: #1A2640 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        padding: 0.65rem 1.5rem !important;
        width: 100% !important;
        transition: all 0.2s !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.15) !important;
    }
    .stButton > button:hover {
        background: #00B8C8 !important;
        box-shadow: 0 4px 12px rgba(0,184,200,0.3) !important;
    }

    /* ── Demo hint ── */
    .demo-hint {
        background: #F0FDFE;
        border: 1px solid #A5F3FC;
        border-radius: 8px;
        padding: 9px 14px;
        font-size: 0.8rem;
        color: #0E7490;
        text-align: center;
        margin-top: 0.75rem;
    }
    .demo-hint strong { color: #0C4A6E; }

    /* ── Alert ── */
    .stAlert { border-radius: 8px !important; font-size: 0.85rem !important; }

    /* ── Footer ── */
    .page-footer {
        border-top: 1px solid #F3F4F6;
        padding: 2rem 0 1rem;
        text-align: center;
        font-size: 0.78rem;
        color: #D1D5DB;
        margin-top: 4rem;
    }
    .page-footer a { color: #9CA3AF; text-decoration: none; }
    .page-footer a:hover { color: #00B8C8; }

    /* ── Divider fix ── */
    hr { border: none; border-top: 1px solid #F3F4F6; margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Logo helper ───────────────────────────────────────────────────────────────
def _logo_b64() -> str:
    for p in ["segvantiq-removebg-preview.png", "assets/logo.png"]:
        path = Path(p)
        if path.exists():
            return base64.b64encode(path.read_bytes()).decode()
    return ""

logo_b64 = _logo_b64()

# ──────────────────────────────────────────────────────────────────────────────
# NAV BAR — logo shows perfectly on white background, no filter needed
# ──────────────────────────────────────────────────────────────────────────────
if logo_b64:
    st.markdown(f"""
    <div class="top-nav">
        <img src="data:image/png;base64,{logo_b64}" height="70"
             style="object-fit:contain; display:block;"/>
        <span class="nav-tag">AI Customer Intelligence &nbsp;·&nbsp; Qylatrix</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="top-nav">
        <span style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:900;
                     font-size:1.4rem;color:#1A2640;letter-spacing:-0.5px;">
            SEGVANTIQ
        </span>
        <span class="nav-tag">AI Customer Intelligence &nbsp;·&nbsp; Qylatrix</span>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# HERO + AUTH
# ──────────────────────────────────────────────────────────────────────────────
col_hero, col_gap, col_auth = st.columns([1.35, 0.15, 1], gap="small")

with col_hero:
    st.markdown("""
    <div class="eyebrow">AI-Powered Customer Analytics</div>

    <div class="hero-h1">
        Turn Customer Data Into<br>
        <span class="accent">Actionable Intelligence</span>
    </div>

    <p class="hero-p">
        SEGVANTIQ is an enterprise-grade AI analytics engine that automatically
        segments your customers, forecasts lifetime value, and surfaces strategic
        insights — all in one secure, isolated workspace.
    </p>

    <div class="tag-row">
        <span class="tag">K-Means Clustering</span>
        <span class="tag">CLV Forecasting</span>
        <span class="tag">Cohort Analysis</span>
        <span class="tag">Qyla AI Chat</span>
        <span class="tag">Anomaly Detection</span>
        <span class="tag">Market Basket</span>
        <span class="tag">RFM Analysis</span>
    </div>

    <div class="stat-row">
        <div>
            <div class="stat-num">12</div>
            <div class="stat-lbl">Analytics Modules</div>
        </div>
        <div>
            <div class="stat-num">4+</div>
            <div class="stat-lbl">ML Algorithms</div>
        </div>
        <div>
            <div class="stat-num">100%</div>
            <div class="stat-lbl">Tenant Isolated</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_auth:
    auth_tab_login, auth_tab_signup = st.tabs(["Sign In", "Create Account"])

    with auth_tab_login:
        st.markdown('<div class="auth-h">Welcome back</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-sub">Sign in to your intelligence workspace</div>', unsafe_allow_html=True)

        username_in = st.text_input("Username", placeholder="Enter your username", key="login_user")
        password_in = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign In", key="btn_login", use_container_width=True):
            if not username_in or not password_in:
                st.error("Please enter your credentials.")
            else:
                if login(username_in, password_in):
                    st.success("Access granted — loading dashboard...")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

        st.markdown("""
        <div class="demo-hint">
            Demo access &nbsp;·&nbsp; username: <strong>demo</strong> &nbsp;/&nbsp; password: <strong>demo</strong>
        </div>
        """, unsafe_allow_html=True)

    with auth_tab_signup:
        st.markdown('<div class="auth-h">Create workspace</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-sub">Set up your isolated business intelligence environment</div>', unsafe_allow_html=True)

        reg_business = st.text_input("Business Name", placeholder="e.g. Acme Corp", key="reg_biz")
        reg_username = st.text_input("Username", placeholder="Choose a username", key="reg_user")
        reg_email    = st.text_input("Email", placeholder="your@email.com", key="reg_email")
        reg_password = st.text_input("Password", type="password", placeholder="Min. 8 characters", key="reg_pass")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Create Account", key="btn_signup", use_container_width=True):
            if not reg_username or not reg_password or not reg_business:
                st.error("Please fill in all required fields.")
            else:
                success, msg = register(reg_username, reg_password, reg_business, reg_email)
                if success:
                    st.success("Workspace created — loading dashboard...")
                    st.rerun()
                else:
                    st.error(f"{msg}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-footer">
    <strong style="color:#9CA3AF;">SEGVANTIQ</strong> by
    <a href="https://github.com/Qylatrix">Qylatrix</a>
    &nbsp;·&nbsp; Powered by Qyla AI &nbsp;·&nbsp; &copy; 2026
</div>
""", unsafe_allow_html=True)
