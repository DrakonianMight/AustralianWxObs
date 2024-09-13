# Weather Observation Data Management and Visualization

## Overview

This repository contains Python scripts for downloading, processing, storing, and visualizing weather observation data from the Bureau of Meteorology's FTP server. The data is archived in an SQLite database to avoid duplicates and keep only the last 10 days of observations. The scripts include features for querying the database and creating interactive maps of weather stations using Plotly.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Scripts](#scripts)
  - [Download and Archive Weather Data](#download-and-archive-weather-data)
  - [Query Weather Data](#query-weather-data)
  - [Generate Station Map](#generate-station-map)
- [Usage](#usage)
- [Crontab Setup](#crontab-setup)
- [License](#license)

## Features

1. **Download and Archive Data**: Fetches weather observation tarballs from the Bureau of Meteorology FTP server and stores the extracted data in an SQLite database (`weather_observations.db`). Only data from the last 10 days is retained to ensure efficiency and avoid duplication.
   
2. **Query Data**: Retrieve weather data from the database by station name, date, and/or time. By default, fetches data from all stations for the last 24 hours.
   
3. **Visualize Data**: Creates an interactive map with weather station locations using Plotly, with markers displaying the station name.

## Requirements

- Python 3.x
- Required libraries: 
  ```bash
  pip install pandas sqlite3 plotly requests tarfile

  ### 2. Query Weather Data

**Script**: `query_weather_data.py`

This script provides functions to query the weather observation data stored in the SQLite database.

- **Main Functions**:
  - `query_data(station_name=None, start_time=None, end_time=None)`: Allows querying weather data by station name, date, and time. Defaults to retrieving data from the last 24 hours if no parameters are provided.
  - `get_station_locations()`: Retrieves the latitude, longitude, and name of all stations with valid geographical coordinates.


### 3. Generate Station Map

**Script**: `generate_map.py`

This script generates an interactive map using Plotly that displays all weather station locations as markers. The markers show the station name when hovered over.

- **Main Functions**:
  - `create_station_map(output_html='station_map.html')`: Creates a map with station markers and saves it as an HTML file (`station_map.html` by default).


## Usage

1. **Download and Store Data**:
   Run the script to download, extract, and archive weather data:
   ```bash
   python download_and_archive.py
