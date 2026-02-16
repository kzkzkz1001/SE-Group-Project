# export_to_json.py
import pandas as pd
import json
from sqlalchemy import create_engine, text
from datetime import datetime
from weather_config import URI

def export_to_json():
    """Export all weather data to JSON file"""
    engine = create_engine(URI)
    
    query = text("SELECT * FROM current_weather ORDER BY dt ASC")
    
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    
    if df.empty:
        print("No data to export!")
        return
    
    # Convert timestamp to readable format
    df['timestamp'] = pd.to_datetime(df['dt'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Convert DataFrame to list of dictionaries
    weather_records = df.to_dict('records')
    
    # Create final JSON structure
    json_data = {
        "collection_info": {
            "total_records": len(weather_records),
            "first_record": weather_records[0]['timestamp'] if weather_records else None,
            "last_record": weather_records[-1]['timestamp'] if weather_records else None,
            "location": {
                "city": "Dublin",
                "latitude": 53.3498,
                "longitude": -6.2603
            }
        },
        "weather_data": weather_records
    }
    
    # Save to JSON file
    filename = 'weather_data.json'
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=2)
    
    print(f"✓ Exported {len(weather_records)} records to {filename}")
    print(f"\nFirst record: {weather_records[0]['timestamp']}")
    print(f"Last record: {weather_records[-1]['timestamp']}")
    print(f"Temperature range: {df['temp'].min():.1f}°C to {df['temp'].max():.1f}°C")

if __name__ == "__main__":
    export_to_json()
    