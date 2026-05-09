import random
from faker import Faker
import psycopg2

fake = Faker()
conn = psycopg2.connect(
    dbname="event_analytics",
    user="postgres",
    password="YOUR_PASSWORD_HERE",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Skewed event types: 'concert' dominates so you see both
# Index Scan (rare types) and Seq Scan (common types) in your experiments
EVENT_TYPES = (
    ["concert"] * 60 +
    ["wedding"] * 20 +
    ["conference"] * 15 +
    ["birthday"] * 4 +
    ["corporate"] * 1
)
REGIONS = ["West", "East", "South", "Midwest", "Northwest"]

# Insert 10,000 users
print("Inserting users...")
users = [
    (fake.name(), fake.unique.email(), random.choice(REGIONS))
    for _ in range(10_000)
]
cur.executemany(
    "INSERT INTO users (name, email, region) VALUES (%s, %s, %s)",
    users
)
conn.commit()

# Insert 100,000 events
print("Inserting events...")
cur.execute("SELECT user_id FROM users")
user_ids = [row[0] for row in cur.fetchall()]

events = [
    (
        random.choice(user_ids),
        random.choice(EVENT_TYPES),
        fake.city(),
        fake.date_between(start_date="-3y", end_date="today"),
        random.randint(10, 5000),
        random.choice(["active", "cancelled", "completed"])
    )
    for _ in range(100_000)
]
cur.executemany(
    """INSERT INTO events
       (user_id, event_type, location, event_date, attendees, status)
       VALUES (%s, %s, %s, %s, %s, %s)""",
    events
)
conn.commit()
cur.close()
conn.close()
print("Done.")