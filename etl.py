import requests
import sqlite3
import json

# 1. Download Data
url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F&downloadType=WEB&format=JSON"
print(f"Downloading data from {url}...")
response = requests.get(url)
response.raise_for_status()
data = response.json()

# 2. Parse Data
locations_data = []
try:
    raw_locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
    
    for loc in raw_locations:
        name = loc['locationName']
        
        # Get the first day's forecast
        # Note: Assuming the lists are aligned by date.
        min_t_obj = loc['weatherElements']['MinT']['daily'][0]
        max_t_obj = loc['weatherElements']['MaxT']['daily'][0]
        wx_obj = loc['weatherElements']['Wx']['daily'][0]
        
        min_temp = float(min_t_obj['temperature'])
        max_temp = float(max_t_obj['temperature'])
        description = wx_obj['weather']
        
        locations_data.append((name, min_temp, max_temp, description))
        print(f"Parsed: {name}, Min: {min_temp}, Max: {max_temp}, Desc: {description}")

except KeyError as e:
    print(f"Error parsing JSON structure: {e}")
    exit(1)

# 3. Design & Create Database
db_name = "data.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Drop table if exists to ensure clean slate for this exercise
cursor.execute("DROP TABLE IF EXISTS weather")

create_table_sql = """
CREATE TABLE weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    min_temp REAL,
    max_temp REAL,
    description TEXT
);
"""
cursor.execute(create_table_sql)
print("Database and table created.")

# 4. Insert Data
insert_sql = "INSERT INTO weather (location, min_temp, max_temp, description) VALUES (?, ?, ?, ?)"
cursor.executemany(insert_sql, locations_data)
conn.commit()

print(f"Inserted {cursor.rowcount} rows into weather table.")

# Verify
cursor.execute("SELECT * FROM weather")
rows = cursor.fetchall()
print("Current data in DB:")
for row in rows:
    print(row)

conn.close()
print("Done.")
