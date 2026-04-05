import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64
import io
from pathlib import Path
from typing import Dict, Tuple, Any, Optional, Union
from sklearn.base import ClusterMixin, TransformerMixin

from src.auth import require_auth, logout, get_current_user
from src.preprocess import preprocess_pipeline, calculate_rfm
from src.model import (
    build_clustering_model, apply_pca, get_recommendations,
    calculate_wcss, calculate_clv, calculate_model_metrics,
    get_cohort_data, detect_anomalies, get_market_basket,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SEGVANTIQ Dashboard",
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
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;900&family=Inter:wght@300;400;700&display=swap');

    /* Hide default Streamlit page nav — we build our own */
    [data-testid="stSidebarNav"] { display: none !important; }

    .stApp {
        background-color: #FFFFFF;
        background-image:
            radial-gradient(ellipse at 0% 0%, rgba(123,47,190,0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 100% 100%, rgba(0,123,255,0.05) 0%, transparent 50%);
        background-attachment: fixed;
        color: #212529;
        font-family: 'Inter', sans-serif;
    }
    .glass-card {
        background: #FFFFFF;
        backdrop-filter: blur(20px);
        border: 1px solid #E9ECEF;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.04);
        transition: all 0.4s ease;
        margin-bottom: 1.5rem;
        position: relative; overflow: hidden;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F8F9FA;
        border-radius: 12px;
        padding: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        color: #4A4A6A;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7B2FBE !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(123,47,190,0.2);
    }
    .elite-header {
        text-align: center; padding: 3rem 2rem;
        background: rgba(255,255,255,0.02);
        border-radius: 24px; margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .elite-header h1 {
        font-family: 'Outfit', sans-serif; font-weight: 900;
        font-size: 3.5rem;
        background: linear-gradient(135deg, #1A1A1A 0%, #7B2FBE 45%, #007BFF 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -2px; line-height: 1.1; margin-bottom: 0.5rem;
    }
    .badge-active {
        background: rgba(123,47,190,0.05);
        color: #007BFF; padding: 6px 16px; border-radius: 4px;
        font-size: 0.7rem; font-weight: 700; border: 1px solid rgba(0,123,255,0.2);
        letter-spacing: 1px; text-transform: uppercase;
        display: inline-block; margin-bottom: 1.2rem;
    }
    [data-testid="metric-container"] {
        background: rgba(123,47,190,0.1) !important;
        border: 1px solid rgba(123,47,190,0.25) !important;
        border-radius: 8px !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-thumb { background: rgba(123,47,190,0.4); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ── Logo helper ──────────────────────────────────────────────────────────────
def _logo_b64() -> str:
    p = Path("assets/logo.png")
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""


# ════════════════════════════════════════════════════════════════════════════
# CACHED PIPELINE
# ════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_and_model_data(
    n_clusters: int,
    file_bytes: Optional[bytes],
    username: str,
) -> Tuple[pd.DataFrame, pd.DataFrame, Any, Any, Dict, pd.DataFrame, pd.DataFrame]:
    if file_bytes is not None:
        df_clean = pd.read_csv(io.BytesIO(file_bytes), encoding="ISO-8859-1")
        df_clean["InvoiceDate"] = pd.to_datetime(df_clean["InvoiceDate"])
        df_rfm = calculate_rfm(df_clean)
    else:
        df_clean, df_rfm = preprocess_pipeline()

    df_rfm, scaler, kmeans = build_clustering_model(df_rfm, n_clusters=n_clusters)
    df_rfm = apply_pca(df_rfm, scaler)
    metrics_results = calculate_model_metrics(df_rfm, kmeans)
    cohort_retention = get_cohort_data(df_clean)
    df_rfm = detect_anomalies(df_rfm)
    market_basket_rules = get_market_basket(df_clean)
    return df_clean, df_rfm, scaler, kmeans, metrics_results, cohort_retention, market_basket_rules


def map_clusters(df_rfm: pd.DataFrame) -> Tuple[pd.DataFrame, Dict, pd.DataFrame]:
    aggs = df_rfm.groupby("Cluster")[["Recency", "Frequency", "Monetary"]].mean()
    n = len(aggs)
    whale_id   = aggs["Monetary"].idxmax()
    at_risk_id = aggs["Recency"].idxmax()
    remaining  = [c for c in aggs.index if c not in (whale_id, at_risk_id)]
    mapping    = {whale_id: "Whales (High Spend)", at_risk_id: "At-Risk / Churned"}
    if n == 4:
        if aggs.loc[remaining[0], "Frequency"] > aggs.loc[remaining[1], "Frequency"]:
            mapping[remaining[0]] = "The Loyalists"
            mapping[remaining[1]] = "Occasional Buyers"
        else:
            mapping[remaining[1]] = "The Loyalists"
            mapping[remaining[0]] = "Occasional Buyers"
    else:
        for i, c in enumerate(remaining):
            mapping[c] = f"Segment {i+1} (Growth)"
    df_rfm["Persona"] = df_rfm["Cluster"].map(mapping)
    return df_rfm, mapping, aggs


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    logo_b64 = _logo_b64()
    if logo_b64:
        st.markdown(
            f'<img src="data:image/png;base64,{logo_b64}" width="200" style="margin-bottom:0.8rem;display:block;background:white;border-radius:6px;padding:8px;"/>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown("## SEGVANTIQ")

    st.markdown(f"**Workspace:** `{business}`")
    st.caption(f"Plan: {user.get('plan', 'Free')} · System Active")
    st.markdown("---")

    # Nav links
    st.page_link("pages/1_Dashboard.py", label="Dashboard", use_container_width=True)
    st.page_link("pages/2_Qyla_AI.py",   label="Qyla Intelligence", use_container_width=True)
    st.markdown("---")

    st.subheader("Model Configuration")
    k_value = st.slider("Clustering Parameters (k)", 2, 8, value=4)

    st.markdown("---")
    st.subheader("Data Environment")
    uploaded_file = st.file_uploader(
        "Upload Analytical CSV",
        type=["csv"],
        help="Required schema: InvoiceNo, Description, Quantity, InvoiceDate, UnitPrice, CustomerID",
    )
    if uploaded_file is None:
        st.info("System running in Demo Mode. Initialize CSV upload for live analysis.")
    else:
        st.success(f"Analytical source identified: {uploaded_file.name}")

    st.markdown("---")
    if st.button("Sign Out", use_container_width=True):
        logout()
        st.switch_page("app.py")


# ════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ════════════════════════════════════════════════════════════════════════════
file_bytes = uploaded_file.read() if uploaded_file else None

try:
    with st.spinner("Processing intelligence environment..."):
        (df_clean, df_rfm_raw, scaler, kmeans,
         model_metrics, cohort_retention, basket_rules) = load_and_model_data(
            k_value, file_bytes, username
        )
        df_rfm, cluster_mapping, cluster_aggs_raw = map_clusters(df_rfm_raw.copy())
except Exception as e:
    st.error(f"Engine failure: {e}")
    st.info("Please verify CSV formatting and refresh.")
    st.stop()


# ── Sidebar export (after data loads) ───────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.subheader("Analytical Export")

    @st.cache_data
    def _to_csv(df: pd.DataFrame) -> bytes:
        return df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Dataset",
        data=_to_csv(df_rfm),
        file_name="segvantiq_data.csv",
        mime="text/csv",
        use_container_width=True,
    )
    
    selected_personas = st.multiselect(
        "Segment Filter",
        options=list(cluster_mapping.values()),
        default=list(cluster_mapping.values()),
    )

filtered_rfm = df_rfm[df_rfm["Persona"].isin(selected_personas)]


# ════════════════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="elite-header">
    <div class="badge-active">
        Qyla Intelligence Environment · {business} Workspace
    </div>
    <h1>Customer Intelligence</h1>
    <p style="color:#4A4A6A;font-size:1.1rem;max-width:700px;margin:8px auto 0;">
        Machine learning segmentation and predictive behavioral analytics.
    </p>
</div>
""", unsafe_allow_html=True)

# ── KPI strip ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Customers",     f"{len(df_rfm):,}")
c2.metric("Total Transactions",  f"{len(df_clean):,}")
c3.metric("Total Revenue",       f"${df_rfm['Monetary'].sum():,.0f}")
c4.metric("Avg Order Value",     f"${(df_rfm['Monetary'].sum() / df_rfm['Frequency'].sum()):,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# ── AI Brief ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card" style="border-left:4px solid #7B2FBE; padding: 1rem; background: #F8F9FA; border-radius: 8px;">
    <h3 style="color:#4B0082;margin-top:0;font-weight:900;">Qyla Executive Brief</h3>
    <p style="color:#2D2D44;line-height:1.7;font-weight:500;">
        <b style="color:#7B2FBE;">Core Insight:</b> High-value <b>Whales</b> represent the priority tier for revenue stability.<br>
        <b style="color:#0056b3;">Strategic Action:</b> Automated win-back protocols recommended for <b>At-Risk</b> segments to mitigate projected churn.<br>
        <b style="color:#155724;">Opportunity:</b> Market Basket analysis indicates significant cross-sell potential within top-tier product categories.
    </p>
</div>
""", unsafe_allow_html=True)

(tab1, tab2, tab3, tab4, tab5,
 tab6, tab7, tab8, tab9, tab10, tab11, tab12) = st.tabs([
    "Segment Analytics", "Cluster Profiles", "AI Recommendations",
    "Model Tuning", "CLV Prediction", "Marketing Plan",
    "Cohort Analysis", "Customer 360", "Anomaly Detection",
    "Market Basket", "Roadmap", "Platform Guide",
])

COLORS = px.colors.qualitative.Set2

# ─── Tab 1: Segment Analytics ────────────────────────────────────────────────
with tab1:
    st.markdown("### Clustering Projection (2D PCA)")
    fig = px.scatter(filtered_rfm, x="PCA1", y="PCA2", color="Persona",
                     hover_data=["CustomerID", "Monetary", "Recency", "Frequency"],
                     color_discrete_sequence=COLORS, template="plotly_white")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=20,r=20,t=20,b=20), font=dict(color="#2D2D44"))
    st.plotly_chart(fig, use_container_width=True)

    ca, cb = st.columns(2)
    with ca:
        st.markdown("### Segment Distribution")
        fig2 = px.pie(filtered_rfm, names="Persona", hole=0.6,
                      color_discrete_sequence=COLORS, template="plotly_white")
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#2D2D44"))
        st.plotly_chart(fig2, use_container_width=True)
    with cb:
        st.markdown("### Revenue Contribution")
        fig3 = px.bar(filtered_rfm.groupby("Persona")["Monetary"].sum().reset_index(),
                      x="Persona", y="Monetary", color="Persona",
                      color_discrete_sequence=COLORS, template="plotly_white")
        fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           showlegend=False, font=dict(color="#2D2D44"))
        st.plotly_chart(fig3, use_container_width=True)

# ─── Tab 2: Cluster Profiles ─────────────────────────────────────────────────
with tab2:
    st.markdown("### Behavioral DNA Matrix")
    radar_data = df_rfm.groupby("Persona")[["Recency", "Frequency", "Monetary"]].mean().reset_index()
    for col in ["Recency", "Frequency", "Monetary"]:
        mx = radar_data[col].max()
        if mx > 0:
            radar_data[col] = radar_data[col] / mx
    radar_data["Recency_Score"] = 1.0 - radar_data["Recency"]
    categories = ["Recency (Score)", "Frequency (Relative)", "Monetary (Relative)"]
    fig_r = go.Figure()
    colors = ["#C77DFF", "#00E5FF", "#92FE9D", "#fc8d62"]
    for i, row in radar_data.iterrows():
        fig_r.add_trace(go.Scatterpolar(
            r=[row["Recency_Score"], row["Frequency"], row["Monetary"]],
            theta=categories, fill="toself", name=row["Persona"],
            line_color=colors[i % len(colors)],
        ))
    fig_r.update_layout(
        polar={"radialaxis": {"visible": True, "range": [0,1], "showticklabels": False},
               "bgcolor": "rgba(255,255,255,0.04)"},
        showlegend=True, template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#2D2D44"}, height=550,
    )
    st.plotly_chart(fig_r, use_container_width=True)
    st.markdown("### Cluster Statistical Breakdown")
    st.dataframe(cluster_aggs_raw.style.background_gradient(cmap="Purples"), use_container_width=True)

# ─── Tab 3: Recommendations ──────────────────────────────────────────────────
with tab3:
    st.markdown("### Predictive Product Engine")
    col_sel, col_res = st.columns([1, 2])
    with col_sel:
        user_list = df_rfm["CustomerID"].astype(int).sort_values().unique().tolist()
        default_user = (
            df_rfm[df_rfm["Persona"].str.contains("Loyal", case=False)]["CustomerID"].iloc[0]
            if len(df_rfm[df_rfm["Persona"].str.contains("Loyal", case=False)]) > 0
            else user_list[0]
        )
        selected_user = float(st.selectbox("Identifier:", user_list, index=user_list.index(int(default_user))))
        ud = df_rfm[df_rfm["CustomerID"] == selected_user].iloc[0]
        st.info(f"**Persona Classification:** {ud['Persona']}")
        st.write(f"- Recency: {ud['Recency']} days")
        st.write(f"- Frequency: {ud['Frequency']} orders")
        st.write(f"- Spend: ${ud['Monetary']:,.2f}")
    with col_res:
        recs = get_recommendations(selected_user, df_clean, df_rfm, top_n=5)
        if len(recs) > 0:
            st.dataframe(recs, use_container_width=True, hide_index=True,
                column_config={"Popularity_Score": st.column_config.ProgressColumn(
                    "Cluster Popularity", format="%d", min_value=0,
                    max_value=int(recs["Popularity_Score"].max() * 1.2))})
            st.success("Analysis complete. Recommendations generated.")
        else:
            st.warning("No new recommendations identified.")

# ─── Tab 4: Model Tuning ─────────────────────────────────────────────────────
with tab4:
    st.markdown("### Algorithm Optimization (Elbow Method)")
    with st.spinner("Processing WCSS iterations..."):
        wcss = calculate_wcss(df_rfm_raw.copy())
        fig_e = px.line(x=list(wcss.keys()), y=list(wcss.values()), markers=True,
                        labels={"x": "k (Clusters)", "y": "WCSS (Error)"}, template="plotly_white")
        fig_e.update_traces(line={"color": "#C77DFF", "width": 3}, marker={"size": 8, "color": "#00E5FF"})
        fig_e.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font={"color": "#2D2D44"})
        st.plotly_chart(fig_e, use_container_width=True)
    m1, m2 = st.columns(2)
    m1.metric("Silhouette Score", f"{model_metrics['Silhouette Score']:.4f}")
    m2.metric("Calinski-Harabasz Index", f"{model_metrics['Calinski-Harabasz Index']:.1f}")
    st.info("Mathematical verification confirmed choice of segments.")

# ─── Tab 5: CLV ──────────────────────────────────────────────────────────────
with tab5:
    st.markdown("### Customer Lifetime Value (CLV) Predictions")
    df_clv = calculate_clv(df_rfm.copy())
    c1, c2 = st.columns(2)
    with c1:
        clv_aggs = df_clv.groupby("Persona")["CLV"].mean().reset_index()
        fig_c = px.bar(clv_aggs, x="Persona", y="CLV", color="Persona",
                       color_discrete_sequence=COLORS, template="plotly_white", text_auto=".2s")
        fig_c.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            showlegend=False, font=dict(color="#2D2D44"))
        st.plotly_chart(fig_c, use_container_width=True)
    with c2:
        st.dataframe(df_clv.nlargest(5, "CLV")[["CustomerID", "Persona", "CLV", "Tenure"]],
                     use_container_width=True, hide_index=True)
        if len(clv_aggs) > 0:
            top_p = clv_aggs.loc[clv_aggs["CLV"].idxmax(), "Persona"]
            st.success(f"**Insight:** '{top_p}' have the highest projected Lifetime Value.")

# ─── Tab 6: Marketing Plan ───────────────────────────────────────────────────
with tab6:
    st.markdown("### Strategic Strategic Marketing Deployment")
    persona = st.selectbox("Target Classification:", list(cluster_mapping.values()))
    if "Whales" in persona:
        st.markdown("#### Strategic Objective: VIP Retention")
        st.write("- Tier 1 early-access protocols\n- Physical milestone recognition")
        st.info('**Communication Header:** "Priority Service Initialization — Qylatrix Restricted Tier"')
    elif "Loyalist" in persona:
        st.markdown("#### Strategic Objective: Expansion & Advocacy")
        st.write("- Referral incentive structures\n- Bundle optimization")
        st.info('**Communication Header:** "Strategic Expansion Opportunity for Integrated Partners"')
    elif "Occasional" in persona:
        st.markdown("#### Strategic Objective: Habituation")
        st.write("- Temporal discount windows\n- Progression-based rewards")
        st.info('**Communication Header:** "Limited Analysis Timeframe — Exclusive Offer Inside"')
    else:
        st.markdown("#### Strategic Objective: Churn Mitigation")
        st.write("- Aggressive reactivation discounts\n- Service feedback protocols")
        st.info('**Communication Header:** "System Alert: Win-Back Protocol Active"')

# ─── Tab 7: Cohort ───────────────────────────────────────────────────────────
with tab7:
    st.markdown("### Monthly Retention Heatmaps")
    import matplotlib.pyplot as plt
    import seaborn as sns
    fig_ch, ax = plt.subplots(figsize=(12, 7))
    sns.heatmap(cohort_retention, annot=True, fmt=".0%", cmap="Purples",
                cbar_kws={"label": "Retention Rate"}, ax=ax,
                linewidths=0.5, linecolor="#eee")
    plt.title("Customer Persistence by Cohort", pad=12)
    plt.xlabel("Months Elapsed"); plt.ylabel("Cohort Initiation Month")
    st.pyplot(fig_ch)
    plt.close(fig_ch)

# ─── Tab 8: Customer 360 ─────────────────────────────────────────────────────
with tab8:
    st.markdown("### CRM Entity Analysis (360 Degree View)")
    sid = st.number_input("Entity ID", min_value=int(df_rfm["CustomerID"].min()),
                          max_value=int(df_rfm["CustomerID"].max()), value=int(df_rfm["CustomerID"].iloc[0]))
    if sid in df_rfm["CustomerID"].astype(int).values:
        cp = df_rfm[df_rfm["CustomerID"] == sid].iloc[0]
        x1, x2, x3 = st.columns(3)
        x1.metric("Classification", cp["Persona"])
        x2.metric("Aggregate Spend", f"${cp['Monetary']:,.2f}")
        x3.metric("System Tenure", f"{cp['Tenure']} days")
        st.markdown("---")
        st.subheader("Strategic Deployment")
        if "Whale" in cp["Persona"]:
            st.success("- Managed account protocols\n- Priority engagement\n- Optimized logistics")
        elif "Loyalist" in cp["Persona"]:
            st.info("- Upsell to enterprise tier\n- Partner expansion program\n- Early platform access")
        elif "At-Risk" in cp["Persona"]:
            st.warning("- Immediate win-back trigger\n- High-intensity re-engagement\n- Direct outreach")
        else:
            st.write("- Automated habituation sequences\n- Event-based notification triggers")
    else:
        st.error("Entity ID not found in current namespace.")

# ─── Tab 9: Anomaly Detection ─────────────────────────────────────────────────
with tab9:
    st.markdown("### Outlier Identification (Isolation Forest)")
    fig_a = px.scatter(df_rfm, x="PCA1", y="PCA2", color="Is_Anomaly", symbol="Is_Anomaly",
                       color_discrete_map={"Normal": "#00E5FF", "Outlier": "#FF4B4B"},
                       hover_data=["CustomerID", "Monetary", "Frequency"], template="plotly_white")
    fig_a.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_a, use_container_width=True)
    outlier_count = len(df_rfm[df_rfm["Is_Anomaly"] == "Outlier"])
    st.info(f"System identified {outlier_count} non-conformant entities (Top 5% variance).")

# ─── Tab 10: Market Basket ────────────────────────────────────────────────────
with tab10:
    st.markdown("### Association Rules (Market Basket Analysis)")
    st.dataframe(basket_rules.sort_values("Lift", ascending=False),
                 use_container_width=True, hide_index=True,
                 column_config={
                     "Confidence": st.column_config.ProgressColumn(format="%.2f", min_value=0, max_value=1),
                     "Lift": st.column_config.NumberColumn(format="%.2f"),
                 })
    st.markdown("Strategic Application: Product bundling and cross-channel optimization.")

# ─── Tab 11: Roadmap ──────────────────────────────────────────────────────────
with tab11:
    st.markdown("### Platform Roadmap")
    phases = [
        ("#C77DFF", "Phase 1 — Core Intelligence (Finalized)",
         "K-Means architecture, RFM infrastructure, 12-page analysis environment."),
        ("#00E5FF", "Phase 2 — Multi-Tenant SaaS (Active)",
         "Business entity registration, per-user data isolation, Qyla engine deployment."),
        ("#92FE9D", "Phase 3 — Persistent Middleware",
         "Supabase database integration for global account persistence."),
        ("#FF8C00", "Phase 4 — Distribution & Scale",
         "Real-time transaction streaming pipelines and distributed ML modeling."),
        ("#FF4B4B", "Phase 5 — Ecosystem Expansion",
         "Enterprise API development and omnichannel service connectors."),
    ]
    for color, title, desc in phases:
        st.markdown(f"""
        <div class="glass-card" style="border-left:4px solid {color};">
            <h4 style="color:{color};margin:0 0 0.5rem;">{title}</h4>
            <p style="color:#999;margin:0;">{desc}</p>
        </div>""", unsafe_allow_html=True)

# ─── Tab 12: Platform Guide (README) ──────────────────────────────────────────
with tab12:
    logo_b64_guide = _logo_b64()
    if logo_b64_guide:
        st.markdown(
            f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64_guide}" width="300" style="margin-bottom:2rem;"/></div>',
            unsafe_allow_html=True,
        )
    readme_path = Path("README.md")
    if readme_path.exists():
        st.markdown(readme_path.read_text(encoding="utf-8"))
    else:
        st.info("System documentation not identified.")

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#444;font-size:0.75rem;text-transform:uppercase;'>"
    "SEGVANTIQ INTELLIGENCE · QYLATRIX SYSTEMS · 2026</p>",
    unsafe_allow_html=True,
)

