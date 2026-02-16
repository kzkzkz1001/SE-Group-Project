# weather_db_setup.py
from sqlalchemy import create_engine, text
from weather_config import USER, PASSWORD, PORT, DB_NAME

def create_database_and_table():
    """Create the database if it doesn't exist, then create the table"""
    
    # First, connect WITHOUT specifying a database
    temp_uri = f"mysql+pymysql://{USER}:{PASSWORD}@127.0.0.1:{PORT}"
    temp_engine = create_engine(temp_uri, echo=False)
    
    # Create the database
    with temp_engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        connection.commit()
    
    print(f"✓ Database '{DB_NAME}' created/verified")
    
    # Now connect to the specific database
    uri = f"mysql+pymysql://{USER}:{PASSWORD}@127.0.0.1:{PORT}/{DB_NAME}"
    engine = create_engine(uri, echo=False)
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS current_weather (
        dt BIGINT PRIMARY KEY,
        feels_like FLOAT,
        humidity INT,
        pressure INT,
        temp FLOAT,
        weather_id INT,
        weather_main VARCHAR(50),
        weather_description VARCHAR(100),
        wind_speed FLOAT,
        wind_gust FLOAT,
        rain_1h FLOAT,
        clouds_all INT
    )
    """
    
    with engine.connect() as connection:
        connection.execute(text(create_table_sql))
        connection.commit()
    
    print(f"✓ Table 'current_weather' created successfully in database '{DB_NAME}'")

if __name__ == "__main__":
    create_database_and_table()