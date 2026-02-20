from flask import Flask
from dotenv import load_dotenv

# Import the blueprints
from api.bike_api import bike_api_bp
from api.db_station_api import db_station_api_bp
from api.db_bike_api import db_bike_api_bp
from api.weather_api import weather_bp

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
    app.run(debug=True, port=5001)
