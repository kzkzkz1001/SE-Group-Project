from flask import Blueprint, jsonify
import requests
import os

# Create a Blueprint object
bike_api_bp = Blueprint('bike_api', __name__)


@bike_api_bp.route('/api/bikes', methods=['GET'])
def get_live_bikes():
    jc_key = os.getenv("JC_API_KEY")
    url = f"https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey={jc_key}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json())  # Return JSON data to the frontend
        else:
            return jsonify({"error": "Failed to fetch from JCDecaux"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
