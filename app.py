
"""
app.py  –  Lean In Mission Dashboard
=====================================
Multi-layer Streamlit dashboard surfacing the signals that matter most for
Lean In's mission: community growth, circle health, member advancement, and
geographic impact.

Run:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_generator import load_all

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lean In | Mission Dashboard",
    page_icon="https://leanin.org/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
# BRAND PALETTE  –  Lean In red + Morandian professional accents
# ─────────────────────────────────────────────────────────────────
LEAN_RED    = "#CC1428"   # Lean In signature red
LEAN_DARK   = "#1A1A1A"   # near-black for headlines
LEAN_GRAY   = "#5C5C5C"   # body text
LEAN_BG     = "#F7F5F2"   # warm off-white background
LEAN_MAUVE  = "#7A4F56"   # muted rose  (Morandian accent 1)
LEAN_SAGE   = "#5A7A63"   # sage green  (Morandian accent 2)
LEAN_SAND   = "#B8A090"   # warm sand   (Morandian accent 3)
LEAN_SLATE  = "#5C6B7A"   # slate blue  (Morandian accent 4)
LEAN_WHITE  = "#FFFFFF"

# Status colours – clear semantic signal
STATUS_ACTIVE   = "#2D6A4F"   # forest green  → positive
STATUS_AT_RISK  = "#D4870A"   # amber          → warning
STATUS_INACTIVE = "#CC1428"   # Lean In red    → alert

COLOR_SEQ = [LEAN_RED, LEAN_MAUVE, LEAN_SAGE, LEAN_SLATE,
             LEAN_SAND, "#8C6B55", "#A07070"]

# ─────────────────────────────────────────────────────────────────
# GLOBAL CSS  –  professional / career-women aesthetic
# ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    /* Google Font ------------------------------------------------ */
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;800&family=Barlow+Condensed:wght@600;700&display=swap');

    /* Global ----------------------------------------------------- */
    html, body, [class*="css"] {{
        font-family: "Barlow", sans-serif;
    }}
    [data-testid="stAppViewContainer"] {{
        background: {LEAN_BG};
    }}

    /* Sidebar ---------------------------------------------------- */
    [data-testid="stSidebar"] {{
        background: {LEAN_WHITE};
        border-right: 1px solid #E8E4DF;
    }}
    [data-testid="stSidebar"] * {{
        color: {LEAN_DARK} !important;
    }}
    .sidebar-brand {{
        border-left: 4px solid {LEAN_RED};
        padding: 6px 0 6px 14px;
        margin-bottom: 20px;
    }}
    .sidebar-brand-name {{
        font-size: 1.1rem;
        font-weight: 800;
        color: {LEAN_RED} !important;
        letter-spacing: 0.5px;
    }}
    .sidebar-brand-sub {{
        font-size: 0.78rem;
        color: {LEAN_GRAY} !important;
        font-weight: 500;
    }}
    .sidebar-section {{
        font-size: 0.7rem;
        font-weight: 700;
        color: {LEAN_GRAY} !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 20px 0 6px 0;
    }}

    /* Headlines -------------------------------------------------- */
    h1, h2, h3 {{
        font-family: "Barlow", sans-serif;
        color: {LEAN_DARK};
    }}

    /* KPI cards -------------------------------------------------- */
    .kpi-card {{
        background: {LEAN_WHITE};
        border-radius: 8px;
        padding: 18px 20px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.07);
        border-left: 4px solid {LEAN_RED};
        margin-bottom: 10px;
        height: 115px;
    }}
    .kpi-card.mauve  {{ border-left-color: {LEAN_MAUVE}; }}
    .kpi-card.sage   {{ border-left-color: {LEAN_SAGE}; }}
    .kpi-card.sand   {{ border-left-color: {LEAN_SAND}; }}
    .kpi-card.slate  {{ border-left-color: {LEAN_SLATE}; }}
    .kpi-label {{
        font-size: 0.68rem;
        color: {LEAN_GRAY};
        font-weight: 700;
        letter-spacing: .8px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }}
    .kpi-value {{
        font-size: 2rem;
        font-weight: 800;
        color: {LEAN_DARK};
        line-height: 1.1;
    }}
    .kpi-delta         {{ font-size: 0.75rem; color: #2D7A4F; font-weight: 600; margin-top: 4px; }}
    .kpi-delta.neg     {{ color: #C0392B; }}
    .kpi-delta.neutral {{ color: {LEAN_GRAY}; }}

    /* Section divider -------------------------------------------- */
    .section-header {{
        margin: 28px 0 14px 0;
        padding-bottom: 7px;
        border-bottom: 2px solid {LEAN_RED};
        color: {LEAN_DARK};
        font-weight: 700;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: "Barlow Condensed", sans-serif;
    }}

    /* Insight box ------------------------------------------------ */
    .insight-box {{
        background: #FDF9F7;
        border-radius: 6px;
        padding: 12px 16px;
        border-left: 3px solid {LEAN_MAUVE};
        font-size: 0.86rem;
        color: {LEAN_DARK};
        margin: 10px 0;
        line-height: 1.55;
    }}

    /* Tab styling ------------------------------------------------ */
    button[data-baseweb="tab"] {{
        font-family: "Barlow", sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.2px;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {LEAN_RED} !important;
        border-bottom: 3px solid {LEAN_RED} !important;
    }}

    /* Sidebar inputs – always-on red border ---------------------- */
    [data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {{
        border: 1.5px solid {LEAN_RED} !important;
        border-radius: 4px !important;
        background: white !important;
    }}
    [data-testid="stSidebar"] [data-testid="stDateInputPrimitive"] > div,
    [data-testid="stSidebar"] [data-testid="stDateInput"] > div > div {{
        border: 1.5px solid {LEAN_RED} !important;
        border-radius: 4px !important;
        background: white !important;
    }}

    /* Divider ---------------------------------------------------- */
    hr {{ border-color: #E8E4DF; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# DATA LOAD (cached)
# ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading data...")
def get_data():
    return load_all()

circles, members, kpis, events = get_data()

members_rich = members.merge(
    circles[["circle_id", "circle_type", "has_facilitator_training",
             "uses_curriculum", "status", "avg_attendance_pct"]],
    on="circle_id", how="left"
)


# ─────────────────────────────────────────────────────────────────
# SIDEBAR  –  GLOBAL FILTERS
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-name">Lean In</div>
        <div class="sidebar-brand-sub">Mission Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Date Range</div>', unsafe_allow_html=True)
    date_min = kpis["month"].min().date()
    date_max = kpis["month"].max().date()
    date_range = st.date_input(
        "Select range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-section">Geography</div>', unsafe_allow_html=True)
    countries_available = ["All"] + sorted(circles["country"].unique().tolist())
    selected_country = st.selectbox("Country", countries_available)

    st.markdown('<div class="sidebar-section">Circle Type</div>', unsafe_allow_html=True)
    types_available = ["All"] + sorted(circles["circle_type"].unique().tolist())
    selected_type = st.selectbox("Type", types_available)

    st.markdown('<div class="sidebar-section">Industry</div>', unsafe_allow_html=True)
    industries_available = ["All"] + sorted(members["industry"].unique().tolist())
    selected_industry = st.selectbox("Industry", industries_available)

    st.markdown("---")
    st.caption(
        "Built on synthetic data reflecting Lean In's community footprint. "
        "All figures are illustrative. Data period: Jan 2022 – Mar 2025."
    )


# ─────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────
if len(date_range) == 2:
    d_start, d_end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    d_start, d_end = pd.Timestamp(date_min), pd.Timestamp(date_max)

kpis_f = kpis[(kpis["month"] >= d_start) & (kpis["month"] <= d_end)].copy()

circles_f = circles.copy()
if selected_country != "All":
    circles_f = circles_f[circles_f["country"] == selected_country]
if selected_type != "All":
    circles_f = circles_f[circles_f["circle_type"] == selected_type]

members_f = members_rich.copy()
if selected_country != "All":
    members_f = members_f[members_f["country"] == selected_country]
if selected_industry != "All":
    members_f = members_f[members_f["industry"] == selected_industry]
if selected_type != "All":
    members_f = members_f[members_f["circle_type"] == selected_type]


# ─────────────────────────────────────────────────────────────────
# COMPUTE HEADLINE KPIs
# ─────────────────────────────────────────────────────────────────
total_circles   = len(circles_f)
active_circles  = (circles_f["status"] == "Active").sum()
total_members   = len(members_f)
promotion_rate  = members_f["promoted"].mean() * 100
nps_latest      = kpis_f["nps"].iloc[-1] if not kpis_f.empty else 0

if len(kpis_f) >= 2:
    delta_circles = int(kpis_f["total_circles"].iloc[-1] - kpis_f["total_circles"].iloc[-2])
    delta_members = int(kpis_f["total_members"].iloc[-1] - kpis_f["total_members"].iloc[-2])
    delta_nps     = kpis_f["nps"].iloc[-1] - kpis_f["nps"].iloc[-2]
else:
    delta_circles = delta_members = delta_nps = 0


# ─────────────────────────────────────────────────────────────────
# HEADER BANNER
# ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background: {LEAN_RED};
            border-radius: 10px;
            padding: 26px 36px;
            margin-bottom: 26px;
            color: white;">
    <div style="font-family:'Barlow Condensed',sans-serif;
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                opacity: 0.85;
                margin-bottom: 8px;">
        Lean In &nbsp;·&nbsp; Mission Overview
    </div>
    <div style="font-family:'Barlow',sans-serif;
                font-size: 1.7rem;
                font-weight: 800;
                line-height: 1.25;
                margin-bottom: 8px;">
        Tracking how Lean In Circles advance women's careers
    </div>
    <div style="font-size: 0.88rem; opacity: 0.85; font-weight: 400;">
        Community growth · Circle health · Career outcomes &nbsp;·&nbsp;
        Data period: <strong>{d_start.strftime('%b %Y')} – {d_end.strftime('%b %Y')}</strong>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# KPI STRIP
# ─────────────────────────────────────────────────────────────────
def kpi_card(label, value, delta, delta_label="vs last month",
             color_class="", delta_suffix="", fmt="{:.0f}", delta_neutral=False):
    if delta_neutral:
        delta_class = "neutral"
        delta_sign  = ""
    elif delta < 0:
        delta_class = "neg"
        delta_sign  = ""
    else:
        delta_class = ""
        delta_sign  = "+"
    val_str = fmt.format(value) if isinstance(value, (int, float)) else str(value)
    return f"""
<div class="kpi-card {color_class}">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{val_str}</div>
    <div class="kpi-delta {delta_class}">{delta_sign}{delta:.1f}{delta_suffix} {delta_label}</div>
</div>"""

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(kpi_card("Total Circles", total_circles, delta_circles, fmt="{:,.0f}"),
                unsafe_allow_html=True)
with c2:
    active_pct_vs_target = active_circles / max(total_circles, 1) * 100 - 78
    st.markdown(kpi_card("Active Circles", active_circles,
                          active_pct_vs_target,
                          delta_label="vs 78% target", delta_suffix="%",
                          color_class="mauve", fmt="{:,.0f}"),
                unsafe_allow_html=True)
with c3:
    st.markdown(kpi_card("Total Members", total_members, delta_members,
                          color_class="sage", fmt="{:,.0f}"),
                unsafe_allow_html=True)
with c4:
    promo_lift = promotion_rate - 12
    st.markdown(kpi_card("Promotion Rate", promotion_rate,
                          promo_lift,
                          delta_label="vs non-Circle",
                          delta_suffix="%", color_class="slate",
                          fmt="{:.1f}%"),
                unsafe_allow_html=True)
with c5:
    st.markdown(kpi_card("Circle NPS", nps_latest, delta_nps,
                          color_class="sand", fmt="{:.0f}"),
                unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Growth & Reach",
    "Circle Health",
    "Member Advancement",
    "Geographic Expansion",
    "Signal Strategy",
])

PLOTLY_LAYOUT = dict(template="plotly_white", margin=dict(l=0, r=0, t=40, b=0),
                      font=dict(family="Barlow, sans-serif", color=LEAN_DARK))


# ══════════════════════════════════════════════════════════════════
# TAB 1  –  GROWTH & REACH
# ══════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Community Growth Over Time</div>',
                unsafe_allow_html=True)

    col_l, col_r = st.columns([2, 1])
    with col_l:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x=kpis_f["month"], y=kpis_f["total_circles"],
            name="Total Circles", mode="lines",
            line=dict(color=LEAN_RED, width=2.5),
            fill="tozeroy", fillcolor="rgba(204,20,40,0.07)"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=kpis_f["month"], y=kpis_f["total_members"],
            name="Total Members", mode="lines",
            line=dict(color=LEAN_SAGE, width=2.5, dash="dot"),
        ), secondary_y=True)
        fig.add_trace(go.Bar(
            x=kpis_f["month"], y=kpis_f["new_circles"],
            name="New Circles (MoM)", marker_color=LEAN_SAND, opacity=0.55,
        ), secondary_y=False)
        fig.update_layout(height=340, legend=dict(orientation="h", y=1.14),
                           hovermode="x unified", **PLOTLY_LAYOUT)
        fig.update_yaxes(title_text="Circles", secondary_y=False)
        fig.update_yaxes(title_text="Members", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig2 = go.Figure(go.Scatter(
            x=kpis_f["month"], y=kpis_f["corporate_partners"],
            fill="tozeroy", mode="lines",
            line=dict(color=LEAN_MAUVE, width=2),
            fillcolor="rgba(122,79,86,0.08)",
        ))
        fig2.update_layout(
            height=340, showlegend=False,
            title=dict(text="CORPORATE PARTNERSHIPS",
                       font=dict(size=11, color=LEAN_DARK, family="Barlow Condensed, sans-serif"),
                       x=0, xanchor="left"),
            xaxis=dict(showgrid=False),
            **{**PLOTLY_LAYOUT, "margin": dict(l=0, r=0, t=36, b=0)},
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Growth summary insight
    if len(kpis_f) >= 2:
        circle_start = int(kpis_f["total_circles"].iloc[0])
        circle_end   = int(kpis_f["total_circles"].iloc[-1])
        member_start = int(kpis_f["total_members"].iloc[0])
        member_end   = int(kpis_f["total_members"].iloc[-1])
        circle_growth_pct = (circle_end - circle_start) / circle_start * 100
        member_growth_pct = (member_end - member_start) / member_start * 100
        partner_end = int(kpis_f["corporate_partners"].iloc[-1])
        partner_start = int(kpis_f["corporate_partners"].iloc[0])
        partner_growth_pct = (partner_end - partner_start) / partner_start * 100
        st.markdown(f"""
        <div class="insight-box">
            Circles grew <strong>{circle_growth_pct:.0f}%</strong> over the period
            ({circle_start:,} → {circle_end:,}), with membership tracking closely at
            <strong>{member_growth_pct:.0f}%</strong> growth ({member_start:,} → {member_end:,}) —
            indicating circles are maintaining consistent average size rather than growing hollow.
            Corporate partnerships expanded <strong>{partner_growth_pct:.0f}%</strong>
            ({partner_start:,} → {partner_end:,}), and the acceleration visible from mid-2023 onward
            coincides with stronger institutional partner uptake.
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Engagement Rate & Circle Churn</div>',
                unsafe_allow_html=True)

    fig3 = make_subplots(rows=1, cols=2,
                          subplot_titles=(
                              "Circle Engagement Rate (% circles meeting monthly)",
                              "Circle Churn Rate (% going inactive)"
                          ))
    fig3.add_trace(go.Scatter(
        x=kpis_f["month"], y=kpis_f["engagement_rate"] * 100,
        mode="lines", line=dict(color=STATUS_ACTIVE, width=2.5),
        fill="tozeroy", fillcolor="rgba(45,106,79,0.10)", name="Engagement %",
    ), row=1, col=1)
    fig3.add_hline(y=75, line_dash="dash", line_color=LEAN_DARK, line_width=1.5,
                    annotation_text="75% target",
                    annotation_font=dict(color=LEAN_DARK, size=11),
                    row=1, col=1)
    fig3.add_trace(go.Scatter(
        x=kpis_f["month"], y=kpis_f["circle_churn_rate"] * 100,
        mode="lines", line=dict(color=STATUS_INACTIVE, width=2.5),
        fill="tozeroy", fillcolor="rgba(204,20,40,0.10)", name="Churn %",
    ), row=1, col=2)
    fig3.add_hline(y=10, line_dash="dash", line_color=LEAN_DARK, line_width=1.5,
                    annotation_text="10% threshold",
                    annotation_font=dict(color=LEAN_DARK, size=11),
                    row=1, col=2)
    fig3.update_layout(height=280, showlegend=False, hovermode="x unified",
                        **PLOTLY_LAYOUT)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-header">Community NPS (Net Promoter Score)</div>',
                unsafe_allow_html=True)
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=kpis_f["month"], y=kpis_f["nps"],
        mode="lines", line=dict(color=LEAN_RED, width=3),
        fill="tozeroy", fillcolor="rgba(204,20,40,0.06)", name="NPS",
    ))
    fig4.add_hrect(y0=50, y1=100, fillcolor="rgba(90,122,99,0.06)", line_width=0,
                    annotation_text="Excellent (>50)", annotation_position="top left")
    fig4.add_hrect(y0=0,  y1=50,  fillcolor="rgba(184,160,144,0.06)", line_width=0,
                    annotation_text="Good (0–50)", annotation_position="top left")
    fig4.update_layout(height=220, yaxis=dict(range=[0, 100]), showlegend=False,
                        **{**PLOTLY_LAYOUT, "margin": dict(l=0, r=0, t=20, b=0)})
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# TAB 2  –  CIRCLE HEALTH
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Circle Status Breakdown</div>', unsafe_allow_html=True)

    col_a, col_c = st.columns(2)

    STATUS_MAP = {"Active": STATUS_ACTIVE, "At Risk": STATUS_AT_RISK, "Inactive": STATUS_INACTIVE}

    with col_a:
        status_counts = circles_f["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig5 = px.pie(status_counts, names="Status", values="Count", hole=0.55,
                       color="Status", color_discrete_map=STATUS_MAP)
        fig5.update_traces(textposition="outside", textinfo="percent+label",
                            textfont=dict(size=13))
        fig5.update_layout(height=300, showlegend=True,
                            legend=dict(orientation="h", y=-0.15),
                            title="Circle Status Distribution",
                            **{**PLOTLY_LAYOUT, "margin": dict(l=20, r=20, t=40, b=40)})
        st.plotly_chart(fig5, use_container_width=True)

    with col_c:
        train_impact = circles_f.groupby(["has_facilitator_training", "status"]).size().reset_index(name="n")
        train_impact["has_facilitator_training"] = train_impact["has_facilitator_training"].map(
            {True: "Trained", False: "Untrained"})
        fig7 = px.bar(train_impact, x="has_facilitator_training", y="n", color="status",
                       barmode="group", color_discrete_map=STATUS_MAP,
                       title="Facilitator Training vs Circle Status",
                       labels={"has_facilitator_training": "", "n": "Circles",
                               "status": ""})
        fig7.update_layout(height=320,
                            legend=dict(orientation="h", y=-0.22,
                                        xanchor="center", x=0.5, title_text=""),
                            **{**PLOTLY_LAYOUT, "margin": dict(l=0, r=0, t=40, b=60)})
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown('<div class="section-header">Circle Lifecycle Funnel</div>', unsafe_allow_html=True)
    st.markdown(
        "How many circles survive each milestone? This is the most important leading indicator of long-term impact.",
    )

    funnel_stages = ["Founded", "First Meeting", "3rd Meeting", "6th Meeting", "Annual Milestone"]
    funnel_counts = [events[events["event"] == s]["circle_id"].nunique() for s in funnel_stages]

    fig8 = go.Figure(go.Funnel(
        y=funnel_stages, x=funnel_counts,
        textinfo="value+percent initial",
        marker=dict(color=[LEAN_RED, LEAN_MAUVE, LEAN_SAND, LEAN_SAGE, LEAN_SLATE]),
        connector=dict(line=dict(color="#E8E4DF", width=2)),
    ))
    fig8.update_layout(height=380, **{**PLOTLY_LAYOUT, "margin": dict(l=80, r=20, t=20, b=20)})
    st.plotly_chart(fig8, use_container_width=True)

    survival_to_6m = funnel_counts[3] / max(funnel_counts[2], 1) * 100
    st.markdown(f"""
    <div class="insight-box">
        <strong>Key insight:</strong> The largest drop-off is between <em>Founded</em> and
        <em>First Meeting</em>. Circles that reach their 3rd meeting have a
        <strong>{survival_to_6m:.0f}% probability</strong> of reaching the 6-month mark.
        Early check-ins at day 14 and day 45 could materially move this funnel.
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Meeting Cadence vs. Member Satisfaction</div>',
                unsafe_allow_html=True)
    fig9 = px.scatter(
        circles_f.sample(min(500, len(circles_f))),
        x="meetings_held", y="nps_score",
        color="status", size="size",
        color_discrete_map={"Active": STATUS_ACTIVE, "At Risk": STATUS_AT_RISK,
                            "Inactive": STATUS_INACTIVE},
        hover_data=["circle_type", "country"],
        labels={"meetings_held": "Meetings Held", "nps_score": "Circle NPS", "size": "Members"},
        title="Circles that meet more often report higher satisfaction",
        opacity=0.7,
    )
    fig9.update_layout(height=350, **PLOTLY_LAYOUT)
    st.plotly_chart(fig9, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# TAB 3  –  MEMBER ADVANCEMENT
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Career Advancement — The Mission Proof Point</div>',
                unsafe_allow_html=True)
    st.caption(
        "Lean In's core claim: women in Circles are nearly 2× as likely to be promoted. "
        "These charts stress-test that claim across segments."
    )

    col_x, col_y = st.columns(2)

    with col_x:
        promo_seniority = members_f.groupby("seniority_at_join")["promoted"].mean().reset_index()
        promo_seniority.columns = ["Seniority at Join", "Promotion Rate"]
        promo_seniority["Promotion Rate %"] = (promo_seniority["Promotion Rate"] * 100).round(1)
        order = ["Individual Contributor", "Manager", "Senior Manager",
                 "Director", "VP / SVP", "C-Suite / Exec"]
        promo_seniority["Seniority at Join"] = pd.Categorical(
            promo_seniority["Seniority at Join"], categories=order, ordered=True)
        promo_seniority = promo_seniority.sort_values("Seniority at Join")

        fig10 = px.bar(promo_seniority, x="Seniority at Join", y="Promotion Rate %",
                        color="Promotion Rate %",
                        color_continuous_scale=[[0, "#F5E8D8"], [0.5, STATUS_AT_RISK], [1, STATUS_ACTIVE]],
                        title="Promotion Rate by Starting Seniority",
                        labels={"Seniority at Join": ""})
        fig10.add_hline(y=12, line_dash="dot", line_color=LEAN_DARK,
                         annotation_text="Non-Circle benchmark (~12%)")
        fig10.update_layout(height=320, coloraxis_showscale=False, showlegend=False,
                             **{**PLOTLY_LAYOUT, "margin": dict(l=0, r=0, t=40, b=60)})
        st.plotly_chart(fig10, use_container_width=True)

    with col_y:
        promo_industry = members_f.groupby("industry")["promoted"].mean().reset_index()
        promo_industry.columns = ["Industry", "Promotion Rate"]
        promo_industry["Promotion Rate %"] = (promo_industry["Promotion Rate"] * 100).round(1)
        promo_industry = promo_industry.sort_values("Promotion Rate %", ascending=True)

        fig11 = px.bar(promo_industry, x="Promotion Rate %", y="Industry",
                        orientation="h", color="Promotion Rate %",
                        color_continuous_scale=[[0, "#F5E8D8"], [0.5, STATUS_AT_RISK], [1, STATUS_ACTIVE]],
                        title="Promotion Rate by Industry")
        fig11.add_vline(x=12, line_dash="dot", line_color=LEAN_DARK,
                         annotation_text="Benchmark")
        fig11.update_layout(height=320, coloraxis_showscale=False, **PLOTLY_LAYOUT)
        st.plotly_chart(fig11, use_container_width=True)

    st.markdown('<div class="section-header">Engagement Depth — Career Outcomes</div>',
                unsafe_allow_html=True)

    members_f["sessions_bucket"] = pd.cut(
        members_f["sessions_attended"], bins=[0, 3, 8, 15, 30],
        labels=["1–3 sessions", "4–8 sessions", "9–15 sessions", "16+ sessions"]
    )
    cohort = members_f.groupby("sessions_bucket", observed=True).agg(
        members=("member_id", "count"),
        promoted=("promoted", "sum"),
    ).reset_index()
    cohort["promotion_rate_pct"] = (cohort["promoted"] / cohort["members"] * 100).round(1)

    fig12 = px.bar(cohort, x="sessions_bucket", y="promotion_rate_pct",
                    text="promotion_rate_pct",
                    color="promotion_rate_pct",
                    color_continuous_scale=[[0, "#F5E8D8"], [0.5, STATUS_AT_RISK], [1, STATUS_ACTIVE]],
                    labels={"sessions_bucket": "Sessions Attended",
                            "promotion_rate_pct": "Promotion Rate (%)"},
                    title="More sessions = higher promotion rate  (dose-response relationship)")
    fig12.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig12.add_hline(y=12, line_dash="dot", line_color=LEAN_MAUVE,
                     annotation_text="Non-Circle benchmark")
    fig12.update_layout(height=320, coloraxis_showscale=False, **PLOTLY_LAYOUT)
    st.plotly_chart(fig12, use_container_width=True)

    high_session_rows = cohort[cohort["sessions_bucket"] == "16+ sessions"]
    high_session_rate = high_session_rows["promotion_rate_pct"].values[0] if len(high_session_rows) > 0 else "N/A"
    st.markdown(f"""
    <div class="insight-box">
        <strong>Dose-response signal:</strong> Members attending 16+ sessions are promoted at
        <strong>{high_session_rate}%</strong> vs. 12% for women outside Circles.
        This validates the Circle model — deeper engagement drives outcomes.
        The strategic priority: get members past session 8.
    </div>""", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════════════
# TAB 4  –  GEOGRAPHIC EXPANSION
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Global Footprint</div>', unsafe_allow_html=True)

    geo_circles = circles_f.groupby("country").agg(
        circles=("circle_id", "count"),
        active=("status", lambda x: (x == "Active").sum()),
        avg_nps=("nps_score", "mean"),
    ).reset_index()
    geo_circles["active_pct"] = (geo_circles["active"] / geo_circles["circles"] * 100).round(1)
    geo_circles["avg_nps"]    = geo_circles["avg_nps"].round(1)

    fig14 = px.choropleth(
        geo_circles, locations="country", locationmode="country names",
        color="circles", hover_name="country",
        hover_data={"active_pct": True, "avg_nps": True, "circles": True},
        color_continuous_scale=[[0, "#FDE8EB"], [0.4, "#E07080"], [1, LEAN_RED]],
        title="Circles by Country",
        labels={"circles": "Circles", "active_pct": "Active %", "avg_nps": "Avg NPS"},
    )
    fig14.update_layout(height=440,
                         geo=dict(showframe=False, showcoastlines=True, bgcolor="rgba(0,0,0,0)"),
                         coloraxis_colorbar=dict(title="Circles"),
                         **{**PLOTLY_LAYOUT, "margin": dict(l=0, r=0, t=40, b=0)})
    st.plotly_chart(fig14, use_container_width=True)

    st.markdown('<div class="section-header">Top Countries — Interactive Comparison</div>',
                unsafe_allow_html=True)

    metric_choice = st.radio(
        "Select metric",
        ["circles", "active_pct", "avg_nps"],
        format_func=lambda x: {"circles": "Total Circles",
                                "active_pct": "Active Circle %",
                                "avg_nps": "Avg NPS"}[x],
        horizontal=True,
    )
    n_countries = st.slider("Show top N countries", min_value=5, max_value=14, value=10)

    top_n = geo_circles.nlargest(n_countries, "circles")
    fig15 = px.bar(
        top_n.sort_values(metric_choice, ascending=True),
        x=metric_choice, y="country", orientation="h", color=metric_choice,
        color_continuous_scale=[[0, "#FDE8EB"], [0.5, "#E07080"], [1, LEAN_RED]],
        labels={"country": "", "circles": "Total Circles",
                "active_pct": "Active %", "avg_nps": "Avg NPS"},
        title=f"Top {n_countries} Countries by {metric_choice.replace('_', ' ').title()}",
    )
    fig15.update_layout(height=400, coloraxis_showscale=False, **PLOTLY_LAYOUT)
    st.plotly_chart(fig15, use_container_width=True)

    st.markdown('<div class="section-header">Geographic Expansion Over Time</div>',
                unsafe_allow_html=True)
    fig16 = go.Figure(go.Scatter(
        x=kpis_f["month"], y=kpis_f["countries_reached"],
        mode="lines+markers", line=dict(color=LEAN_RED, width=2.5),
        fill="tozeroy", fillcolor="rgba(204,20,40,0.07)",
    ))
    fig16.add_hline(y=183, line_dash="dash", line_color=LEAN_SAND,
                     annotation_text="Current reach: 183 countries")
    fig16.update_layout(height=250, yaxis=dict(title="Countries Reached"),
                         showlegend=False,
                         **{**PLOTLY_LAYOUT, "margin": dict(l=0, r=0, t=20, b=0)})
    st.plotly_chart(fig16, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# TAB 5  –  SIGNAL STRATEGY
# ══════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""
    ## Signal Strategy: What We Measure & Why

    > *"Metrics are a proxy for truth. Choose signals that connect directly to the mission —
    not just what's easy to count."*

    Lean In's north star is **accelerating women's advancement into leadership**.
    Every metric here must answer: *does this bring us closer to that goal?*

    ---
    """)

    signals = [
        {
            "tier": "Tier 1 — Mission-Critical",
            "color": LEAN_RED,
            "signals": [
                {
                    "name": "Member Promotion Rate",
                    "why": "The closest proxy we have to mission achievement. Lean In's own research shows Circle members are nearly 2× as likely to be promoted. This is our impact claim — we must measure it rigorously.",
                    "formula": "# members promoted / # members tracked (12-month cohort)",
                    "limitation": "Self-reported; selection bias (motivated women join Circles). Needs comparison to a matched control group for causal claims.",
                    "frequency": "Quarterly cohort",
                },
                {
                    "name": "Active Circle Rate",
                    "why": "An active Circle (≥1 meeting/month) is a live community generating support. A dormant Circle is a broken promise. This is the leading indicator for all downstream outcomes.",
                    "formula": "Circles with ≥1 meeting in last 30 days / Total circles",
                    "limitation": "Doesn't capture meeting quality. A circle can be technically 'active' with low impact.",
                    "frequency": "Weekly",
                },
                {
                    "name": "Circle NPS",
                    "why": "Women who'd recommend their Circle are getting value. NPS captures overall health as a single, leadership-legible number. Decompose by circle type for diagnostics.",
                    "formula": "% Promoters (9–10) − % Detractors (0–6)",
                    "limitation": "Lags reality by weeks. Low response rates can bias results.",
                    "frequency": "Quarterly survey",
                },
            ],
        },
        {
            "tier": "Tier 2 — Growth & Scale",
            "color": LEAN_SAGE,
            "signals": [
                {
                    "name": "New Circles Started (MoM)",
                    "why": "Growth fuels mission reach. Each new Circle is a new community of 8–12 women gaining support. Tracks the pipeline of future impact.",
                    "formula": "# circles with founded_date in calendar month",
                    "limitation": "Quantity ≠ quality. A spike in new circles followed by high early churn is a vanity signal.",
                    "frequency": "Monthly",
                },
                {
                    "name": "Corporate Partners",
                    "why": "Corporate partnerships are the force multiplier — they unlock systematic change where women work. One corporate partner can reach thousands of women.",
                    "formula": "# organizations running active Circles for Companies programs",
                    "limitation": "Partnership count doesn't equal employee engagement. Track utilization rate within partners.",
                    "frequency": "Monthly",
                },
                {
                    "name": "Geographic Reach",
                    "why": "Lean In's mission is explicitly global. Breadth of reach signals movement legitimacy and supports the funding narrative.",
                    "formula": "# distinct countries with ≥1 active circle",
                    "limitation": "Doesn't reflect depth of penetration. 1 circle in 50 countries < 50 circles in 1 country for true impact.",
                    "frequency": "Quarterly",
                },
            ],
        },
        {
            "tier": "Tier 3 — Health & Early Warning",
            "color": LEAN_MAUVE,
            "signals": [
                {
                    "name": "Circle Lifecycle Funnel (Founded → 3rd Meeting)",
                    "why": "Research shows 3 meetings is the 'sticky' threshold — circles that reach it are far more likely to survive. This funnel identifies where drop-off happens so we can intervene.",
                    "formula": "% of new circles reaching each milestone within 90 days",
                    "limitation": "Only actionable if we have mechanisms to intervene (e.g., automated nudges, facilitator check-ins).",
                    "frequency": "Monthly cohort",
                },
                {
                    "name": "Sessions Attended per Member (Engagement Depth)",
                    "why": "The dose-response relationship shows more sessions = higher promotion rates. This is the engagement metric most predictive of outcomes — not just presence, but depth.",
                    "formula": "Avg sessions attended per member over trailing 6 months",
                    "limitation": "Average masks bimodal distribution (power users vs. lurkers). Median is more informative.",
                    "frequency": "Monthly",
                },
                {
                    "name": "Facilitator Training Adoption",
                    "why": "Trained facilitators run better circles (higher attendance, lower churn). This is an input metric — an actionable lever we control directly.",
                    "formula": "% of circle leaders with facilitator training completed",
                    "limitation": "Training quality varies. Completion ≠ capability.",
                    "frequency": "Monthly",
                },
            ],
        },
    ]

    for tier_data in signals:
        st.markdown(
            f'<div style="display:inline-block; background:{tier_data["color"]}; '
            f'color:white; font-size:0.72rem; font-weight:700; letter-spacing:.8px; '
            f'text-transform:uppercase; padding:3px 10px; border-radius:3px; '
            f'margin:24px 0 12px 0;">{tier_data["tier"]}</div>',
            unsafe_allow_html=True
        )
        for sig in tier_data["signals"]:
            with st.expander(f"**{sig['name']}**  ·  {sig['frequency']}"):
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.markdown(f"**Why it matters:** {sig['why']}")
                    st.markdown(f"**Formula:** `{sig['formula']}`")
                with col2:
                    st.markdown(f"**Limitation:** {sig['limitation']}")
        st.markdown("---")



# ─────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<hr style="margin:40px 0 16px 0; border-color:#E8E4DF">
<div style="text-align:center; color:#9CA3AF; font-size:0.75rem; font-family:Barlow,sans-serif;">
    Lean In Mission Dashboard &nbsp;·&nbsp; Synthetic data for illustrative purposes &nbsp;·&nbsp;
    Built for the Lean In Data Scientist take-home assignment &nbsp;·&nbsp; May 2025
</div>
""", unsafe_allow_html=True)
