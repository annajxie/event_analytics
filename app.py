from flask import Flask, render_template, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

def get_conn():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="event_analytics",
        user="postgres",
        password="YOUR_PASSWORD_HERE"
    )
    cur = conn.cursor()
    cur.execute("SET random_page_cost = 2.0;")
    conn.commit()
    cur.close()
    return conn

# The 9 benchmark queries
QUERIES = {
    "seq_scan": """
        EXPLAIN ANALYZE
        SELECT * FROM events
        WHERE event_type = 'concert'
    """,
    "index_scan": """
        EXPLAIN ANALYZE
        SELECT * FROM events
        WHERE event_type = 'corporate'
    """,
    "bitmap_scan": """
        EXPLAIN ANALYZE
        SELECT * FROM events
        WHERE event_date BETWEEN '2024-06-01' AND '2024-09-01'
    """,
    "index_only_scan": """
        EXPLAIN ANALYZE
        SELECT status, COUNT(*) FROM events
        WHERE status = 'active'
        GROUP BY status
    """,
    "hash_join": """
        EXPLAIN ANALYZE
        SELECT u.name, e.event_type, e.event_date
        FROM users u
        JOIN events e ON u.user_id = e.user_id
        WHERE e.event_date >= '2024-01-01'
    """,
    "nested_loop": """
        EXPLAIN ANALYZE
        SELECT u.name, e.event_type, e.event_date
        FROM users u
        JOIN events e ON u.user_id = e.user_id
        WHERE u.user_id = 42
    """,
    "composite_index": """
        EXPLAIN ANALYZE
        SELECT * FROM events
        WHERE event_type = 'corporate'
        AND event_date BETWEEN '2024-03-01' AND '2024-12-01'
    """,
    "hash_aggregate": """
        EXPLAIN ANALYZE
        SELECT event_type, region, COUNT(*) AS event_count, AVG(attendees) AS avg_attendees
        FROM events e
        JOIN users u ON e.user_id = u.user_id
        GROUP BY event_type, region
        ORDER BY event_count DESC
    """
}

@app.route("/")
def index():
    return render_template("index.html", active_page="explorer")

@app.route("/explain")
def explain():
    return render_template("explain.html", active_page="explain")

# Run a query and return the EXPLAIN ANALYZE output
@app.route("/run/<query_name>")
def run_query(query_name):
    if query_name not in QUERIES:
        return jsonify({"error": "Query not found"}), 404
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(QUERIES[query_name])
        rows = cur.fetchall()
        plan = [row[0] for row in rows]   # each row is one line of the plan
        cur.close()
        conn.close()
        return jsonify({"plan": plan})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)