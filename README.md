# ISP Analytics Pipeline 

An end-to-end data engineering pipeline that simulates a fictional Sri Lankan ISP — taking data from synthetic generation and ingestion all the way to a live cloud analytics dashboard,using Python, PostgreSQL, dbt, Airflow, and Streamlit.

> Built as a portfolio project to gain hands-on experience with production data engineering tools and workflows.

🔗 **[Live Dashboard](https://isp-analytics-pipeline.streamlit.app/)** &nbsp;|&nbsp; 📦 **Stack:** Python · PostgreSQL · dbt · Apache Airflow · Streamlit · Docker · Supabase

---

## 📌 Project Overview

This project simulates a real-world ISP data environment with 100+ synthetic customer records across multiple service plans and regions. The pipeline handles everything from raw data generation to transformed analytics marts, orchestrated with Airflow and visualized via a deployed Streamlit dashboard.

**Key business metrics tracked:**
- Customer churn by plan and region
- SLA breach rates and average ticket resolution time
- Bandwidth and data usage trends
- Subscription distribution across service tiers

---

## 🏗️ Architecture

```
Raw Data (CSV/JSON)
      │
      ▼
Python Ingestion Scripts (psycopg2)
      │
      ▼
PostgreSQL (Docker → Supabase)
      │
      ▼
dbt Transformations
  staging → dimensions → facts → marts
      │
      ▼
Apache Airflow (DAG Orchestration)
      │
      ▼
Streamlit Dashboard (Deployed on Streamlit Community Cloud)
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Synthetic data generation (Faker) & ingestion scripts |
| **PostgreSQL** | Relational database for raw and transformed data |
| **Docker** | Containerized local development environment |
| **dbt** | Data transformation layer — staging → dims → facts → marts |
| **Apache Airflow** | Pipeline orchestration and scheduling |
| **Supabase** | Cloud-hosted PostgreSQL (production database) |
| **Streamlit + Plotly** | Interactive analytics dashboard |

---

## 📁 Project Structure

```
ISP-Analytics_Pipeline/
│
├── data/                   # Raw synthetic data (CSV & JSON)
├── Ingestion/              # Python ingestion scripts (psycopg2)
├── dbt_project/            # dbt models
│   ├── models/
│   │   ├── staging/        # Raw source cleaning
│   │   ├── dimensions/     # Dimension tables (customers, plans, regions)
│   │   ├── facts/          # Fact tables (usage, tickets)
│   │   └── marts/          # Final analytics models
├── airflow/
│   └── dag/                # Airflow DAG definitions
├── dashboard/              # Streamlit app
├── docker-compose.yml      # Docker setup for PostgreSQL & Airflow
├── requirements.txt        # Python dependencies
├── profiles.yml            # dbt connection profiles
└── isp_dump.sql            # PostgreSQL schema dump
```

---

## 📊 dbt Mart Models

Three mart models power the dashboard:

| Mart | Description |
|------|-------------|
| `mart_churn_analysis` | Customer retention and churn metrics segmented by plan and region |
| `mart_sla_performance` | Support ticket SLA breach rates and average resolution times |
| `mart_usage_trends` | Bandwidth consumption and data usage patterns over time |

---

## ⚙️ Airflow DAG

The `isp_analytics_pipeline` DAG automates the full pipeline with three sequential tasks:

```
generate_data → ingest_data → run_dbt
```

Each task runs as a `BashOperator`, with Airflow handling scheduling, dependencies, and retries.

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- dbt-postgres
- A Supabase account (for cloud deployment)

### 1. Clone the repo
```bash
git clone https://github.com/yuwaniyash/ISP-Analytics_Pipeline.git
cd ISP-Analytics_Pipeline
```

### 2. Set up environment variables
Create a `.env` file in the root directory:
```env
DB_HOST=your-supabase-host
DB_PORT=5432
DB_NAME=postgres
DB_USER=your-username
DB_PASSWORD=your-password
```

### 3. Start Docker services
```bash
docker-compose up -d
```

### 4. Run ingestion
```bash
cd Ingestion
python ingest.py
```

### 5. Run dbt transformations
```bash
cd dbt_project
dbt run
```

### 6. Trigger Airflow DAG
Access Airflow UI at `http://localhost:8080` and trigger the `isp_analytics_pipeline` DAG.

### 7. Run the dashboard locally
```bash
cd dashboard
streamlit run app.py
```

---

## 📈 Dashboard Features

- **KPI Cards** — Total customers, churn rate, SLA breach rate, avg resolution time
- **Churn Analysis** — Donut chart and bar chart segmented by region and plan
- **SLA Performance** — Breach rates and resolution time trends
- **Usage Trends** — Bandwidth and data consumption over time
- **Interactive Filters** — Filter by region and service plan

---

## 🌐 Live Demo

The dashboard is deployed on Streamlit Community Cloud and connected live to Supabase.

👉 **[https://isp-analytics-pipeline.streamlit.app/](https://isp-analytics-pipeline.streamlit.app/)**

---

## 👩‍💻 About

Built by **Yuwani Yasmada** — 3rd year IT undergraduate specializing in Data Science at SLIIT (Sri Lanka Institute of Information Technology).
