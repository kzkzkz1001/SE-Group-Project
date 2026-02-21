import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify
from db_connect import get_db_connection

db_weather_api_bp = Blueprint('db_weather', __name__)

# GET /api/db/weather — 50 most recent weather rows from database
@db_weather_api_bp.route("/api/db/weather")
def get_weather_history():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM current_weather ORDER BY dt DESC LIMIT 50;")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(rows)