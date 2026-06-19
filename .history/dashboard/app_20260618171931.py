import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

load_dotenv(override=True)

st.set_page_config(page_title="ISP Analytics Dashboard", layout="wide", page_icon="📡")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.metric-card {
    background: #1e2130;
    border: 1px solid #2d3250;
    border-radius: 12px;
    padding: 18px 22px;
}
.metric-label {
    color: #8892a4;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.metric-value {
    color: #ffffff;
    font-size: 28px;
    font-weight: 700;
    line-height: 1;
}
            
.block-container {
    padding-top: 1.5rem !important;
}
.metric-blue { color: #6c8eff; }
.metric-red { color: #ff6b6b; }
.metric-green { color: #4ecdc4; }
.metric-yellow { color: #ffd93d; }
section[data-testid="stSidebar"] { background-color: #141720; border-right: 1px solid #2d3250; }
.filter-label { color: #8892a4; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

def run_query(query):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

DARK = dict(
    paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
    font=dict(color="#c8cfe0", family="Inter"),
    title_font=dict(color="#ffffff", size=14),
    legend=dict(bgcolor="#252a3d", bordercolor="#2d3250", borderwidth=1),
    margin=dict(t=40, b=30, l=10, r=10),
    colorway=["#6c8eff","#4ecdc4","#ff6b9d","#ffd93d","#c77dff","#ff6b6b"]
)

# --- Load data ---
df_churn = run_query("SELECT * FROM mart_churn_analysis")
df_usage = run_query("SELECT * FROM mart_usage_trends ORDER BY year, month_number")
df_sla = run_query("SELECT * FROM mart_sla_performance")

# --- Sidebar filters ---
with st.sidebar:
    st.markdown("### 📡 ISP Analytics")
    st.markdown("<hr style='border-color:#2d3250;margin:12px 0'>", unsafe_allow_html=True)
    st.markdown("<p class='filter-label'>Region</p>", unsafe_allow_html=True)
    regions = ["All"] + sorted(df_churn["region"].unique().tolist())
    selected_region = st.selectbox("", regions, label_visibility="collapsed")

    # Cascading — plans filter based on region
    if selected_region == "All":
        plans = ["All"] + sorted(df_churn["plan"].unique().tolist())
    else:
        plans = ["All"] + sorted(df_churn[df_churn["region"] == selected_region]["plan"].unique().tolist())

    st.markdown("<p class='filter-label' style='margin-top:16px'>Plan</p>", unsafe_allow_html=True)
    selected_plan = st.selectbox("", plans, label_visibility="collapsed", key="plan")

    st.markdown("<hr style='border-color:#2d3250;margin:16px 0'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8892a4;font-size:11px;'>Powered by dbt + Supabase</p>", unsafe_allow_html=True)

# --- Apply filters ---
churn_f = df_churn.copy()
if selected_region != "All":
    churn_f = churn_f[churn_f["region"] == selected_region]
if selected_plan != "All":
    churn_f = churn_f[churn_f["plan"] == selected_plan]

sla_f = df_sla.copy()
if selected_region != "All":
    sla_f = sla_f[sla_f["region"] == selected_region]

usage_f = df_usage.copy()
if selected_plan != "All":
    usage_f = usage_f[usage_f["plan_name"] == selected_plan]

# --- Header ---
region_label = selected_region if selected_region != "All" else "All Regions"
plan_label = selected_plan if selected_plan != "All" else "All Plans"
st.markdown(f"""
<div style='padding:8px 0 20px 0; border-bottom:1px solid #2d3250; margin-bottom:24px;'>
    <h2 style='color:#fff;margin:0;font-size:42px;font-weight:700;'>ISP Analytics Dashboard</h2>
    <p style='color:#8892a4;margin:4px 0 0 0;font-size:13px;'>
        Showing: <span style='color:#6c8eff'>{region_label}</span> · <span style='color:#4ecdc4'>{plan_label}</span>
    </p>
</div>
""", unsafe_allow_html=True)

# --- KPI Row ---
total = int(churn_f["total_customers"].sum())
churned = int(churn_f["churned_customers"].sum())
churn_rate = churn_f["churn_rate_pct"].mean() if len(churn_f) > 0 else 0
avg_breach = sla_f["breach_rate_pct"].mean() if len(sla_f) > 0 else 0
avg_resolve = sla_f["avg_days_to_resolve"].mean() if len(sla_f) > 0 else 0

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Total Customers</div><div class='metric-value metric-blue'>{total:,}</div></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Churned</div><div class='metric-value metric-red'>{churned:,}</div></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Churn Rate</div><div class='metric-value metric-yellow'>{churn_rate:.1f}%</div></div>", unsafe_allow_html=True)
with k4:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>SLA Breach Rate</div><div class='metric-value metric-red'>{avg_breach:.1f}%</div></div>", unsafe_allow_html=True)
with k5:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Avg Days to Resolve</div><div class='metric-value metric-green'>{avg_resolve:.1f}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Chart Row 1 ---
c1, c2 = st.columns(2)

with c1:
    fig = px.bar(churn_f, x="region", y="churn_rate_pct", color="plan",
                 title="Churn Rate by Region & Plan", barmode="group",
                 labels={"churn_rate_pct": "Churn Rate (%)", "region": "Region"})
    fig.update_layout(**DARK)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    if len(churn_f) > 0:
        retained = total - churned
        pie_df = pd.DataFrame({"Status": ["Retained", "Churned"], "Count": [retained, churned]})
        fig2 = px.pie(pie_df, names="Status", values="Count",
                      title="Retained vs Churned",
                      color_discrete_map={"Retained": "#4ecdc4", "Churned": "#ff6b6b"},
                      hole=0.45)
        fig2.update_layout(**DARK)
        fig2.update_traces(textfont_color="white")
        st.plotly_chart(fig2, use_container_width=True)

# --- Chart Row 2 ---
c3, c4 = st.columns(2)

with c3:
    fig3 = px.line(usage_f, x="month_name", y="avg_gb_used", color="plan_name",
                   title="Avg GB Used by Plan Over Time", markers=True,
                   labels={"avg_gb_used": "Avg GB Used", "month_name": "Month"})
    fig3.update_layout(**DARK)
    fig3.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig3, use_container_width=True)
    

with c4:
    fig4 = px.bar(sla_f, x="avg_days_to_resolve", y="category",
                  color="region", orientation="h",
                  title="Avg Days to Resolve by Category",
                  labels={"avg_days_to_resolve": "Avg Days", "category": "Category"})
    fig4.update_layout(**DARK)
    st.plotly_chart(fig4, use_container_width=True)