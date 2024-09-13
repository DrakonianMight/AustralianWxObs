import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def retrieve_data(station_name=None, date_time=None):
    """
    Retrieve data from the SQLite database based on station name, date and time, or both.
    By default, retrieves all stations' data from the last 24 hours before the current time.
    
    Parameters:
    - station_name (str): Name of the weather station to filter by.
    - date_time (str): Date and time (in UTC) to filter by, format "YYYYMMDDHHMMSS". 
                       If not provided, defaults to retrieving data from the last 24 hours.
    
    Returns:
    - DataFrame: Pandas DataFrame with the retrieved data.
    """
    conn = sqlite3.connect(DB_FILE)
    query = "SELECT * FROM observations WHERE 1=1"
    params = []

    # If station name is provided, add to the query
    if station_name:
        query += " AND name = ?"
        params.append(station_name)
    
    # If date_time is provided, retrieve specific data at that time
    if date_time:
        query += " AND date = ?"
        params.append(date_time)
    else:
        # If no date_time provided, retrieve data from the last 24 hours
        current_time = datetime.utcnow()
        last_24_hours = current_time - timedelta(hours=24)
        query += " AND date BETWEEN ? AND ?"
        params.append(last_24_hours.strftime('%Y%m%d%H%M%S'))
        params.append(current_time.strftime('%Y%m%d%H%M%S'))
    
    # Execute query
    df = pd.read_sql_query(query, conn, params)
    
    conn.close()
    return df


def get_station_locations():
    """
    Retrieve latitude, longitude, and station name for each station from the weather_observations.db SQLite database.
    
    Returns:
    - DataFrame: Pandas DataFrame with 'name', 'lat', and 'lon' columns.
    """
    DB_FILE = 'weather_observations.db'
    conn = sqlite3.connect(DB_FILE)
    
    # Query to select distinct station names, latitudes, and longitudes
    query = """
    SELECT DISTINCT name, latitude, longitude
    FROM observations
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    """
    
    # Execute query and load into a DataFrame
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    return df


    
if __name__ == "__main__":
    retrieve_data()