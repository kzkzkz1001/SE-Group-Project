import os
import time
import logging
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Optional

import requests
import pymysql


# =========================
# Config
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

JCDECAUX_API_KEY = os.getenv("JCDECAUX_API_KEY")
BASE = "https://api.jcdecaux.com/vls/v1"

POLL_SECONDS = int(os.getenv("POLL_SECONDS", "300"))  # default 5 min

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "bike_db")


# =========================
# SQL
# =========================
CREATE_DB_SQL = f"""
CREATE DATABASE IF NOT EXISTS `{DB_NAME}`
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci
"""

CREATE_SNAPSHOTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS station_snapshots (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  ts_utc DATETIME(6) NOT NULL,
  station_number INT NOT NULL,
  name VARCHAR(100) NULL,
  address VARCHAR(255) NULL,
  lat DECIMAL(9,6) NULL,
  lng DECIMAL(9,6) NULL,
  status VARCHAR(20) NULL,
  banking BOOLEAN NULL,
  capacity INT NULL,
  available_bikes INT NULL,
  available_stands INT NULL,
  last_update_ms BIGINT NULL,

  INDEX idx_ts (ts_utc),
  INDEX idx_station_ts (station_number, ts_utc)
);
"""

CREATE_CURRENT_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS station_current (
  station_number INT PRIMARY KEY,
  ts_utc DATETIME(6) NOT NULL,
  name VARCHAR(100) NULL,
  address VARCHAR(255) NULL,
  lat DECIMAL(9,6) NULL,
  lng DECIMAL(9,6) NULL,
  status VARCHAR(20) NULL,
  banking BOOLEAN NULL,
  capacity INT NULL,
  available_bikes INT NULL,
  available_stands INT NULL,
  last_update_ms BIGINT NULL,

  INDEX idx_ts (ts_utc),
  INDEX idx_status (status)
);
"""

SNAPSHOT_INSERT_SQL = """
INSERT INTO station_snapshots
(ts_utc, station_number, name, address, lat, lng, status, banking, capacity,
 available_bikes, available_stands, last_update_ms)
VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

CURRENT_UPSERT_SQL = """
INSERT INTO station_current
(station_number, ts_utc, name, address, lat, lng, status, banking, capacity,
 available_bikes, available_stands, last_update_ms)
VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE
ts_utc=VALUES(ts_utc),
name=VALUES(name),
address=VALUES(address),
lat=VALUES(lat),
lng=VALUES(lng),
status=VALUES(status),
banking=VALUES(banking),
capacity=VALUES(capacity),
available_bikes=VALUES(available_bikes),
available_stands=VALUES(available_stands),
last_update_ms=VALUES(last_update_ms)
"""

PURGE_SQL = """
DELETE FROM station_snapshots
WHERE ts_utc < (UTC_TIMESTAMP() - INTERVAL 7 DAY)
"""


# =========================
# DB helpers
# =========================
def _connect_no_db():
    """Connect to MySQL server without selecting a database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        charset="utf8mb4",
        autocommit=True,
    )


def get_conn():
    """Connect to the target database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


def db_init():
    """
    Create database + tables if missing.
    Safe to run multiple times.
    """
    logging.info("DB init: ensuring database and tables exist...")
    conn = _connect_no_db()
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_DB_SQL)
            cur.execute(f"USE `{DB_NAME}`")
            cur.execute(CREATE_SNAPSHOTS_TABLE_SQL)
            cur.execute(CREATE_CURRENT_TABLE_SQL)
    finally:
        conn.close()
    logging.info("DB init: OK")


# =========================
# API fetch + transform
# =========================
def fetch_dublin_stations() -> List[Dict]:
    if not JCDECAUX_API_KEY:
        raise RuntimeError("Missing env var JCDECAUX_API_KEY")

    r = requests.get(
        f"{BASE}/stations",
        params={"contract": "Dublin", "apiKey": JCDECAUX_API_KEY},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()


def build_rows(stations: List[Dict], ts_utc_naive: datetime) -> Tuple[List[Tuple], List[Tuple]]:
    """
    Return:
      - snapshot_rows for station_snapshots (insert many)
      - current_rows for station_current (upsert many)
    """
    snapshot_rows: List[Tuple] = []
    current_rows: List[Tuple] = []

    for s in stations:
        pos = s.get("position") or {}
        station_number = s.get("number")

        row_snapshot = (
            ts_utc_naive,
            station_number,
            s.get("name"),
            s.get("address"),
            pos.get("lat"),
            pos.get("lng"),
            s.get("status"),
            1 if s.get("banking") else 0,
            s.get("bike_stands"),
            s.get("available_bikes"),
            s.get("available_bike_stands"),
            s.get("last_update"),
        )
        snapshot_rows.append(row_snapshot)

        row_current = (
            station_number,
            ts_utc_naive,
            s.get("name"),
            s.get("address"),
            pos.get("lat"),
            pos.get("lng"),
            s.get("status"),
            1 if s.get("banking") else 0,
            s.get("bike_stands"),
            s.get("available_bikes"),
            s.get("available_bike_stands"),
            s.get("last_update"),
        )
        current_rows.append(row_current)

    return snapshot_rows, current_rows


# =========================
# Ingestion
# =========================
def ingest_once() -> Tuple[int, datetime]:
    # MySQL DATETIME stores no timezone. We store UTC as naive datetime.
    ts_utc_naive = datetime.now(timezone.utc).replace(tzinfo=None)

    stations = fetch_dublin_stations()
    snapshot_rows, current_rows = build_rows(stations, ts_utc_naive)

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.executemany(SNAPSHOT_INSERT_SQL, snapshot_rows)
            cur.executemany(CURRENT_UPSERT_SQL, current_rows)
            cur.execute(PURGE_SQL)
    finally:
        conn.close()

    return len(stations), ts_utc_naive


def main():
    db_init()

    logging.info("Starting ingestion loop. POLL_SECONDS=%s", POLL_SECONDS)

    while True:
        start = time.time()
        try:
            n, ts = ingest_once()
            logging.info("Ingested %s stations at %s UTC", n, ts.isoformat())
        except Exception:
            logging.exception("Ingestion failed")

        elapsed = time.time() - start
        sleep_for = max(1, POLL_SECONDS - int(elapsed))
        time.sleep(sleep_for)


if __name__ == "__main__":
    main()
