import csv
import json
import random
from datetime import datetime, timedelta
import os

random.seed(42)

NUM_CUSTOMERS = 100
NUM_DAYS = 90
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

REGIONS = ['Colombo', 'Kandy', 'Galle', 'Jaffna', 'Negombo']
PLANS = ['Basic_10Mbps', 'Standard_25Mbps', 'Premium_100Mbps', 'Ultra_200Mbps']
PLAN_LIMITS = {'Basic_10Mbps': 50, 'Standard_25Mbps': 100, 'Premium_100Mbps': 300, 'Ultra_200Mbps': 500}
TICKET_CATEGORIES = ['No Internet', 'Slow Speed', 'Billing Issue', 'Router Problem', 'Outage']
STATUSES = ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED']

start_date = datetime(2026, 1, 1)

# 1. customers.csv
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    plan = random.choice(PLANS)
    customers.append({
        'customer_id': f'CUST{i:04d}',
        'name': f'Customer {i}',
        'region': random.choice(REGIONS),
        'plan': plan,
        'signup_date': (start_date - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
        'is_churned': random.choices([0, 1], weights=[85, 15])[0]
    })

with open(f'{OUTPUT_DIR}/customers.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=customers[0].keys())
    writer.writeheader()
    writer.writerows(customers)

print(f"✅ customers.csv — {len(customers)} rows")

# 2. usage_logs.json
PLAN_USAGE_PROFILES = {
    'Basic_10Mbps':     {'min_pct': 0.60, 'max_pct': 0.95},  # budget users, consistently high usage %
    'Standard_25Mbps':  {'min_pct': 0.40, 'max_pct': 0.85},  # moderate usage
    'Premium_100Mbps':  {'min_pct': 0.20, 'max_pct': 0.70},  # power users, lots of headroom
    'Ultra_200Mbps':    {'min_pct': 0.10, 'max_pct': 0.50},  # rarely hits limit
}

usage_logs = []
for customer in customers:
    profile = PLAN_USAGE_PROFILES[customer['plan']]
    for day in range(NUM_DAYS):
        date = start_date + timedelta(days=day)
        limit = PLAN_LIMITS[customer['plan']]
        usage_pct = random.uniform(profile['min_pct'], profile['max_pct'])
        usage = round(usage_pct * limit, 2)
        usage_logs.append({
            'log_id': len(usage_logs) + 1,
            'customer_id': customer['customer_id'],
            'date': date.strftime('%Y-%m-%d'),
            'gb_used': usage,
            'plan_limit_gb': limit,
            'exceeded_limit': 1 if usage > limit else 0
        })

with open(f'{OUTPUT_DIR}/usage_logs.json', 'w') as f:
    json.dump(usage_logs, f, indent=2)

print(f"✅ usage_logs.json — {len(usage_logs)} records")

# 3. tickets.csv
tickets = []
for i in range(1, 201):
    customer = random.choice(customers)
    created = start_date + timedelta(days=random.randint(0, NUM_DAYS - 1))
    resolved_days = random.randint(1, 10)
    status = random.choice(STATUSES)
    tickets.append({
        'ticket_id': f'TKT{i:04d}',
        'customer_id': customer['customer_id'],
        'category': random.choice(TICKET_CATEGORIES),
        'status': status,
        'created_at': created.strftime('%Y-%m-%d'),
        'resolved_at': (created + timedelta(days=resolved_days)).strftime('%Y-%m-%d') if status in ['RESOLVED', 'CLOSED'] else '',
        'sla_breached': 1 if resolved_days > 7 else 0
    })

with open(f'{OUTPUT_DIR}/tickets.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=tickets[0].keys())
    writer.writeheader()
    writer.writerows(tickets)

print(f"✅ tickets.csv — {len(tickets)} rows")
print("\n🎉 All data generated in /data folder!")