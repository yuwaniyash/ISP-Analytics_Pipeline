import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# --- Page config ---
st.set_page_config(page_title="ISP Analytics Dashboard", layout="wide", page_icon="📡")

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #0f1117; }
    
    .metric-card {
        background: linear-gradient(135deg, #1e2130 0%, #252a3d 100%);
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 4px 0;
    }
    .metric-label {
        color: #8892a4;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 32px;
        font-weight: 700;
        line-height: 1;
    }
    .metric-accent { color: #6c8eff; }
    
    .page-header {
        padding: 8px 0 24px 0;
        border-bottom: 1px solid #2d3250;
        margin-bottom: 28px;
    }
    .page-title {
        color: #ffffff;
        font-size: 26px;
        font-weight: 700;
        margin: 0;
    }
    .page-subtitle {
        color: #8892a4;
        font-size: 13px;
        margin-top: 4px;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #141720;
        border-right: 1px solid #2d3250;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #c8cfe0 !important;
        font-size: 14px;
    }
    
    .stPlotlyChart { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# --- DB connection ---
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

# --- Plotly dark theme ---
DARK_LAYOUT = dict(
    paper_bgcolor="#1e2130",
    plot_bgcolor="#1e2130",
    font=dict(color="#c8cfe0", family="Inter"),
    title_font=dict(color="#ffffff", size=15, family="Inter"),
    legend=dict(bgcolor="#252a3d", bordercolor="#2d3250", borderwidth=1),
    margin=dict(t=50, b=40, l=40, r=20),
    colorway=["#6c8eff", "#4ecdc4", "#ff6b9d", "#ffd93d", "#c77dff"]
)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 📡 ISP Analytics")
    st.markdown("<hr style='border-color:#2d3250;margin:12px 0'>", unsafe_allow_html=True)
    page = st.radio("", ["Churn Analysis", "Usage Trends", "SLA Performance"], label_visibility="collapsed")
    st.markdown("<hr style='border-color:#2d3250;margin:12px 0'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8892a4;font-size:11px;'>Powered by dbt + Supabase</p>", unsafe_allow_html=True)

# --- Pages ---
if page == "Churn Analysis":
    st.markdown("""<div class='page-header'>
        <p class='page-title'>Customer Churn Analysis</p>
        <p class='page-subtitle'>Churn rates across regions and service plans</p>
    </div>""", unsafe_allow_html=True)

    df = run_query("SELECT * FROM mart_churn_analysis")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Total Customers</div>
            <div class='metric-value'>{int(df['total_customers'].sum()):,}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Churned Customers</div>
            <div class='metric-value metric-accent'>{int(df['churned_customers'].sum()):,}</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Avg Churn Rate</div>
            <div class='metric-value'>{df['churn_rate_pct'].mean():.1f}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    fig = px.bar(df, x="region", y="churn_rate_pct", color="plan",
                 title="Churn Rate by Region and Plan", barmode="group",
                 labels={"churn_rate_pct": "Churn Rate (%)", "region": "Region"})
    fig.update_layout(**DARK_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

elif page == "Usage Trends":
    st.markdown("""<div class='page-header'>
        <p class='page-title'>Data Usage Trends</p>
        <p class='page-subtitle'>Monthly usage patterns by service plan</p>
    </div>""", unsafe_allow_html=True)

    df = run_query("SELECT * FROM mart_usage_trends ORDER BY year, month_number")

    fig = px.line(df, x="month_name", y="avg_usage_pct", color="plan_name",
                  title="Average Usage % by Plan Over Time",
                  markers=True,
                  labels={"avg_usage_pct": "Avg Usage (%)", "month_name": "Month"})
    fig.update_layout(**DARK_LAYOUT)
    fig.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig, use_container_width=True)

elif page == "SLA Performance":
    st.markdown("""<div class='page-header'>
        <p class='page-title'>SLA Performance</p>
        <p class='page-subtitle'>Breach rates and resolution times by ticket category</p>
    </div>""", unsafe_allow_html=True)

    df = run_query("SELECT * FROM mart_sla_performance")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df, x="category", y="breach_rate_pct", color="region",
                     title="SLA Breach Rate by Category", barmode="group",
                     labels={"breach_rate_pct": "Breach Rate (%)", "category": "Category"})
        fig.update_layout(**DARK_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(df, x="category", y="avg_days_to_resolve",
                     title="Avg Days to Resolve by Category",
                     labels={"avg_days_to_resolve": "Avg Days", "category": "Category"})
        fig.update_layout(**DARK_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)