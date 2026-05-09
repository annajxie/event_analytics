# PostgreSQL Query Optimizer Explorer
**DSCI 551 — Anna Xie**

A Flask web application that demonstrates PostgreSQL's cost-based query 
optimizer by running and displaying EXPLAIN ANALYZE output for 8 different 
benchmark query types.

---

## Requirements
- Python 3.8+
- PostgreSQL 17
- pgAdmin 4 (optional, for browsing the database)

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/event_analytics.git
cd event_analytics
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv

# Mac/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL
Make sure PostgreSQL is installed and running locally on port 5432.

Open pgAdmin or psql and create the database:
```sql
CREATE DATABASE event_analytics;
```

### 5. Create the schema and indexes
In pgAdmin's Query Tool (connected to event_analytics), run the contents 
of schema.sql, or run it via psql:
```bash
psql -U postgres -d event_analytics -f schema.sql
```


### 6. Configure your database connection
Open app.py and generate_data.py and update the password field in 
both files to match your local PostgreSQL setup.
```python
def get_conn():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="event_analytics",
        user="postgres",
        password="YOUR_PASSWORD_HERE"
    )
```

### 7. Generate and load data
```bash
python generate_data.py
```
This inserts 10,000 users and 100,000 events with a skewed distribution 
designed to trigger different query plans.


### 8. Run the application
```bash
python app.py
```

Then open your browser and go to:
http://localhost:5000

---

## How to use it
- Click any query in the left sidebar to see its SQL
- Click **Run query** to execute it against your database and see the 
  real EXPLAIN ANALYZE output
- Read the Application Mapping section to understand what PostgreSQL 
  is doing internally and why

---

## Benchmark queries covered
| Query | Plan type |
|---|---|
| Filter by common event type | Sequential Scan |
| Filter by rare event type | Index Scan |
| Date range filter | Bitmap Heap Scan |
| Status count | Index-Only Scan |
| Users × Events join (broad) | Hash Join |
| Single-user lookup | Nested Loop Join |
| Type + date filter | Composite Index Scan |
| Group by type + region | HashAggregate |

---

## Project structure