import requests
import os
from dotenv import load_dotenv
from flask import Blueprint, jsonify

load_dotenv()

weather_bp = Blueprint('weather', __name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Dublin"

@weather_bp.route("/api/weather")
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather"}), 500
    data = response.json()
    return jsonify({
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    })

@weather_bp.route("/api/weather/forecast")
def get_forecast():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch forecast"}), 500
    data = response.json()
    forecast = []
    for entry in data["list"][:6]:
        forecast.append({
            "time": entry["dt_txt"],
            "temperature": entry["main"]["temp"],
            "description": entry["weather"][0]["description"],
            "wind_speed": entry["wind"]["speed"]
        })
    return jsonify(forecast)
