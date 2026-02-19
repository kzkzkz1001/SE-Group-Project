from flask import Blueprint, jsonify
from db_connect import get_db_connection

db_bike_api_bp = Blueprint('db_bike_api', __name__)


@db_bike_api_bp.route('/api/db/bikes', methods=['GET'])
def get_db_recent_bikes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Inner Join to get only the latest record per station
        sql = """
            SELECT a.number, a.available_bikes, a.available_bike_stands, a.status, a.last_update
            FROM availability a
            INNER JOIN (
                SELECT number, MAX(id) as max_id
                FROM availability
                GROUP BY number
            ) b ON a.id = b.max_id;
        """
        cursor.execute(sql)
        recent_bikes = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(recent_bikes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
