import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from flask import Flask
from dotenv import load_dotenv

# Import the blueprints
from api.bike_api import bike_api_bp
from api.db_station_api import db_station_api_bp
from api.db_bike_api import db_bike_api_bp
from api.db_weather_api import weather_bp

load_dotenv()

app = Flask(__name__)

# Register the blueprints
app.register_blueprint(bike_api_bp)
app.register_blueprint(db_station_api_bp)
app.register_blueprint(db_bike_api_bp)
app.register_blueprint(weather_bp)
@app.route('/')
def home():
    return "Dublin Bikes Flask Server is Running!"


if __name__ == '__main__':
    # Run the server
    app.run(debug=True,host='0.0.0.0', port=5001)
