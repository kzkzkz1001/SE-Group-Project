import requests
import mysql.connector
import os
import time
from dotenv import load_dotenv

# loading enviroment variables
load_dotenv()

JC_KEY = os.getenv("JC_API_KEY")
STATIONS_URL = f"https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey={JC_KEY}"


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )


def scrape_bikes():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] start to scrape bike data...")
    try:
        # 1. send API request to JCDecaux
        response = requests.get(STATIONS_URL)
        if response.status_code != 200:
            print(f"API Request failed: {response.status_code}")
            return

        stations_data = response.json()

        # 2. connect to MySQL and update/insert data
        conn = get_db_connection()
        cursor = conn.cursor()

        for station in stations_data:
            # A. Upsert station static info (station table)
            sql_st = """INSERT INTO station (number, name, address, pos_lat, pos_lng, bike_stands) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE name=%s, address=%s"""
            cursor.execute(sql_st, (
                station['number'], station['name'], station['address'],
                station['position']['lat'], station['position']['lng'], station['bike_stands'],
                station['name'], station['address']
            ))

            # B. Insert availability data (availability table)
            sql_av = """INSERT INTO availability (number, available_bikes, available_bike_stands, last_update, status) 
                        VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql_av, (
                station['number'], station['available_bikes'], station['available_bike_stands'],
                station['last_update'], station['status']
            ))

        # 3. commit and close connection
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Updated {len(stations_data)} stations' real-time data.")

    except Exception as e:
        print(f"Error during scraping: {e}")


if __name__ == "__main__":
    # First run to populate the database
    scrape_bikes()

    print("Scraping will run every 5 minutes...")
    while True:
        time.sleep(300)
        scrape_bikes()
