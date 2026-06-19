import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(page_title="SLT-Fiber Analytics", layout="wide")

# --- DB connection ---
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="localhost", port=5432,
        dbname="isp_db", user="isp_user", password="isp_pass"
    )

@st.cache_data
def run_query(query):
    conn = get_connection()
    return pd.read_sql(query, conn)

# --- Sidebar ---
st.sidebar.title("SLT-Fiber Analytics")
page = st.sidebar.radio("Navigate", ["Churn Analysis", "Usage Trends", "SLA Performance"])

# --- Pages ---
if page == "Churn Analysis":
    st.title("Customer Churn Analysis")
    df = run_query("SELECT * FROM mart_churn_analysis")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", df["total_customers"].sum())
    col2.metric("Churned Customers", df["churned_customers"].sum())
    col3.metric("Avg Churn Rate", f"{df['churn_rate_pct'].mean():.1f}%")
    
    fig = px.bar(df, x="region", y="churn_rate_pct", color="plan",
                 title="Churn Rate by Region and Plan", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Usage Trends":
    st.title("Data Usage Trends")
    df = run_query("SELECT * FROM mart_usage_trends ORDER BY year, month_number")
    
    fig = px.line(df, x="month_name", y="avg_usage_pct", color="plan_name",
                  title="Average Usage % by Plan Over Time")
    st.plotly_chart(fig, use_container_width=True)

elif page == "SLA Performance":
    st.title("SLA Performance")
    df = run_query("SELECT * FROM mart_sla_performance")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df, x="category", y="breach_rate_pct", color="region",
                     title="SLA Breach Rate by Category", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(df, x="category", y="avg_days_to_resolve",
                     title="Avg Days to Resolve by Category")
        st.plotly_chart(fig, use_container_width=True)