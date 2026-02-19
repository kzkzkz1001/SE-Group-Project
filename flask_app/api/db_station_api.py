from flask import Blueprint, jsonify
from db_connect import get_db_connection

db_station_api_bp = Blueprint('db_station_api', __name__)


@db_station_api_bp.route('/api/db/stations', methods=['GET'])
def get_db_stations():
    try:
        conn = get_db_connection()
        # Returns results as a dictionary
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM station")
        stations = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(stations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
