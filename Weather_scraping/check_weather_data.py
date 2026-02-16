# check_weather_data.py
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from weather_config import URI

def check_data():
    """Display recent weather data and statistics"""
    engine = create_engine(URI)
    
    # Get last 24 records
    query = """
    SELECT * FROM current_weather 
    ORDER BY dt DESC 
    LIMIT 24
    """
    
    df = pd.read_sql(query, engine)
    
    if df.empty:
        print("No data found in database yet!")
        return
    
    # Convert timestamp to readable format
    df['timestamp'] = pd.to_datetime(df['dt'], unit='s')
    
    print("\n" + "="*80)
    print("RECENT WEATHER DATA")
    print("="*80)
    print(df[['timestamp', 'temp', 'feels_like', 'humidity', 'weather_description']].to_string(index=False))
    
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Total records: {len(df)}")
    print(f"Average temperature: {df['temp'].mean():.1f}°C")
    print(f"Min temperature: {df['temp'].min():.1f}°C")
    print(f"Max temperature: {df['temp'].max():.1f}°C")
    print(f"Average humidity: {df['humidity'].mean():.1f}%")
    print("="*80 + "\n")

if __name__ == "__main__":
    check_data()
    
