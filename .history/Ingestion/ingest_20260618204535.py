import csv
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'), override=True)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cur = conn.cursor()

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Create tables

cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id VARCHAR(10) PRIMARY KEY,
        name VARCHAR(100),
        region VARCHAR(50),
        plan VARCHAR(50),
        signup_date DATE,
        is_churned INTEGER
    );

    CREATE TABLE IF NOT EXISTS usage_logs (
        log_id INTEGER PRIMARY KEY,
        customer_id VARCHAR(10),
        date DATE,
        gb_used FLOAT,
        plan_limit_gb INTEGER,
        exceeded_limit INTEGER
    );

    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id VARCHAR(10) PRIMARY KEY,
        customer_id VARCHAR(10),
        category VARCHAR(50),
        status VARCHAR(20),
        created_at DATE,
        resolved_at DATE,
        sla_breached INTEGER
    );
""")
conn.commit()
print("✅ Tables created")

# Load customers.csv
with open(f'{DATA_DIR}/customers.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute("""
            INSERT INTO customers VALUES (%s,%s,%s,%s,%s,%s)
            ON CONFLICT (customer_id) DO NOTHING
        """, list(row.values()))
conn.commit()
print("✅ customers loaded")

# Load usage_logs.json
with open(f'{DATA_DIR}/usage_logs.json', 'r') as f:
    logs = json.load(f)

rows = [
    (log['log_id'], log['customer_id'], log['date'], log['gb_used'],
     log['plan_limit_gb'], log['exceeded_limit'])
    for log in logs
]

execute_values(
    cur,
    """
    INSERT INTO usage_logs (log_id, customer_id, date, gb_used, plan_limit_gb, exceeded_limit)
    VALUES %s
    ON CONFLICT (log_id) DO NOTHING
    """,
    rows
)
conn.commit()
print("✅ usage_logs loaded")


# Load tickets.csv
with open(f'{DATA_DIR}/tickets.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute("""
            INSERT INTO tickets VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (ticket_id) DO NOTHING
        """, [v if v != '' else None for v in row.values()])
conn.commit()
print("✅ tickets loaded")

cur.close()
conn.close()
print("\n🎉 All data ingested into PostgreSQL!")
