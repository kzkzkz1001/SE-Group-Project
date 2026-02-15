# weather_config.py
API_KEY = "cc9bbc141e4c17a1623f941947a3938c"
LATITUDE = 53.3498
LONGITUDE = -6.2603

# Database credentials - CHANGE 'your_password' to your actual MySQL password
USER = "root"
PASSWORD = "Loganpaul17_"  # ← PUT YOUR MYSQL PASSWORD HERE
PORT = "3306"
DB_NAME = "bike"

# Scraping settings
SCRAPE_INTERVAL = 3600  # 1 hour in seconds
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Database URI
URI = f"mysql+pymysql://{USER}:{PASSWORD}@127.0.0.1:{PORT}/{DB_NAME}"
