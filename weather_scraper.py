# weather_scraper.py
import requests
import time
from sqlalchemy import create_engine, text
from datetime import datetime
from weather_config import API_KEY, LATITUDE, LONGITUDE, WEATHER_URL, URI, SCRAPE_INTERVAL

def get_weather_data():
    """Fetch current weather data from OpenWeather API"""
    params = {
        'lat': LATITUDE,
        'lon': LONGITUDE,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    response = requests.get(WEATHER_URL, params=params)
    response.raise_for_status()
    return response.json()

def extract_weather_info(data):
    """Extract relevant weather information from API response"""
    weather_info = {
        'dt': data['dt'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'temp': data['main']['temp'],
        'weather_id': data['weather'][0]['id'],
        'weather_main': data['weather'][0]['main'],
        'weather_description': data['weather'][0]['description'],
        'wind_speed': data['wind']['speed'],
        'wind_gust': data['wind'].get('gust', 0),
        'rain_1h': data.get('rain', {}).get('1h', 0),
        'clouds_all': data['clouds']['all']
    }
    return weather_info

def save_to_database(weather_info):
    """Save weather data to MySQL database - skip if duplicate"""
    engine = create_engine(URI)
    
    # Use INSERT IGNORE to skip duplicates without error
    insert_sql = text("""
    INSERT IGNORE INTO current_weather 
    (dt, feels_like, humidity, pressure, temp, weather_id, weather_main, 
     weather_description, wind_speed, wind_gust, rain_1h, clouds_all)
    VALUES 
    (:dt, :feels_like, :humidity, :pressure, :temp, :weather_id, 
     :weather_main, :weather_description, :wind_speed, :wind_gust, 
     :rain_1h, :clouds_all)
    """)
    
    with engine.connect() as connection:
        result = connection.execute(insert_sql, weather_info)
        connection.commit()
        return result.rowcount  # Returns 1 if inserted, 0 if duplicate

def scrape_weather():
    """Main scraping function - fetch and save weather data"""
    try:
        data = get_weather_data()
        weather_info = extract_weather_info(data)
        rows_inserted = save_to_database(weather_info)
        
        timestamp = datetime.fromtimestamp(weather_info['dt'])
        
        if rows_inserted > 0:
            print(f"✓ Weather data saved: {timestamp} | Temp: {weather_info['temp']}°C | {weather_info['weather_description']}")
        else:
            print(f"⊘ Duplicate skipped: {timestamp} (already in database)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error scraping weather: {e}")
        return False

def main():
    """Run continuous scraping every hour"""
    print(f"Starting weather scraper (every {SCRAPE_INTERVAL/3600} hours)...")
    print(f"Script started at: {datetime.now()}")
    
    while True:
        print(f"\n[{datetime.now()}] Starting scrape...")
        success = scrape_weather()
        
        if success:
            print(f"Next scrape in {SCRAPE_INTERVAL} seconds ({SCRAPE_INTERVAL/3600} hours)")
        else:
            print(f"Will retry in {SCRAPE_INTERVAL} seconds")
        
        time.sleep(SCRAPE_INTERVAL)

if __name__ == "__main__":
    main()