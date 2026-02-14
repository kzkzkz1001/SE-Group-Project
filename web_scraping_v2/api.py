import os
import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "bike_db")

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )

@app.get("/api/health")
def health():
    # quick sanity check: can we read current table?
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS cnt FROM station_current")
            row = cur.fetchone()
    finally:
        conn.close()
    return jsonify({"ok": True, "station_current_rows": row["cnt"]})

@app.get("/api/stations/current")
def stations_current():
    status = request.args.get("status")  # optional filter
    sql = "SELECT * FROM station_current"
    params = []
    if status:
        sql += " WHERE status=%s"
        params.append(status)
    sql += " ORDER BY station_number"

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
    finally:
        conn.close()
    return jsonify(rows)

@app.get("/api/stations/history")
def station_history():
    station_number = request.args.get("station_number", type=int)
    if not station_number:
        return jsonify({"error": "station_number is required"}), 400

    hours = request.args.get("hours", default=24, type=int)
    hours = max(1, min(hours, 24 * 7))  # clamp to 7 days

    sql = """
    SELECT ts_utc, available_bikes, available_stands, capacity, status
    FROM station_snapshots
    WHERE station_number=%s
      AND ts_utc >= (UTC_TIMESTAMP() - INTERVAL %s HOUR)
    ORDER BY ts_utc
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (station_number, hours))
            rows = cur.fetchall()
    finally:
        conn.close()

    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
