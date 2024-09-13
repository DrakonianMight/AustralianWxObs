import ftplib
import os
import sqlite3
import tarfile
import json
from datetime import datetime, timedelta
import pandas as pd

# Configuration
FTP_SERVER = 'ftp.bom.gov.au'
FTP_DIR = '/anon/gen/fwo/'
LOCAL_DIR = './weather_data'
DB_FILE = 'weather_observations.db'
RETENTION_DAYS = 10
TARBALL_EXTENSIONS = ['.tgz', '.tar.gz']  # Adjust if necessary

# Create local directory if it doesn't exist
if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

def download_files_from_ftp():
    """Download tarball files from FTP server and return the list of local file paths."""
    ftp = ftplib.FTP(FTP_SERVER)
    ftp.login()
    ftp.cwd(FTP_DIR)

    filenames = ['IDD60910', 'IDQ60910', 'IDN60910', 'IDV60910', 'IDT60910', 'IDW60910', 'IDS60910']
    local_files = []
    
    for filename in filenames:
        for ext in TARBALL_EXTENSIONS:
            local_file_path = os.path.join(LOCAL_DIR, filename + ext)
            try:
                with open(local_file_path, 'wb') as local_file:
                    ftp.retrbinary(f'RETR {filename + ext}', local_file.write)
                local_files.append(local_file_path)
                break  # Stop trying other extensions if successful
            except ftplib.error_perm:
                print(f"Failed to download {filename + ext}. Skipping.")
    
    ftp.quit()
    return local_files

def extract_tarball(tarball_path):
    """Extract JSON files from a tarball and return the list of extracted JSON file paths."""
    extracted_files = []
    with tarfile.open(tarball_path, 'r:*') as tar:
        tar.extractall(path=LOCAL_DIR)
        for member in tar.getmembers():
            if member.name.endswith('.json'):
                extracted_files.append(os.path.join(LOCAL_DIR, member.name))
    return extracted_files

def process_json_file(json_file_path):
    """Process a JSON file and return a DataFrame."""
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    records = []
    for entry in data.get('observations', {}).get('data', []):
        records.append({
            'date': entry.get('aifstime_utc'),
            'station_id': entry.get('wmo'),
            'name': data.get('observations', {}).get('header', [{}])[0].get('name'),
            'timezone': data.get('observations', {}).get('header', [{}])[0].get('time_zone_name'),
            'latitude': entry.get('lat'),
            'longitude': entry.get('lon'),
            'wind_direction_deg': entry.get('wind_dir_deg'),
            'wind_speed_kmh': entry.get('wind_spd_kmh')
        })
    
    df = pd.DataFrame(records)
    return df

def store_data_in_db(df):
    """Store data in SQLite database, avoiding duplicates."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            station_id TEXT,
            name TEXT,
            timezone TEXT,
            latitude REAL,
            longitude REAL,
            wind_direction_deg REAL,
            wind_speed_kmh REAL
        )
    ''')

    # Check for duplicates and insert new data
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT OR IGNORE INTO observations (date, station_id, name, timezone, latitude, longitude, wind_direction_deg, wind_speed_kmh)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['date'], row['station_id'], row['name'], row['timezone'], row['latitude'], row['longitude'], row['wind_direction_deg'], row['wind_speed_kmh']))

    conn.commit()
    conn.close()

def archive_old_data():
    """Archive data older than RETENTION_DAYS."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cutoff_date = (datetime.now() - timedelta(days=RETENTION_DAYS)).strftime('%Y-%m-%dT%H:%M:%S')
    cursor.execute('''
        DELETE FROM observations WHERE date < ?
    ''', (cutoff_date,))

    conn.commit()
    conn.close()

def cleanup_files():
    """Remove downloaded tarballs and extracted JSON files."""
    for filename in os.listdir(LOCAL_DIR):
        file_path = os.path.join(LOCAL_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def main():
    # Download files
    files = download_files_from_ftp()
    
    for file_path in files:
        # Extract JSON files from tarballs
        json_files = extract_tarball(file_path)
        
        for json_file in json_files:
            # Process JSON file
            df = process_json_file(json_file)
            
            # Store data in DB
            store_data_in_db(df)
    
    # Archive old data
    archive_old_data()
    
    # Clean up files
    cleanup_files()

if __name__ == '__main__':
    main()
