import requests
import json

url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F&downloadType=WEB&format=JSON"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
    first_loc = locations[0]
    
    print(f"Location: {first_loc['locationName']}")
    print("Keys in location object:", first_loc.keys())
    
    # Check for lat/lon keys
    possible_keys = ['lat', 'lon', 'latitude', 'longitude', 'geocodes', 'coordinates']
    for key in first_loc.keys():
        if any(k in key.lower() for k in possible_keys):
            print(f"Found potential coordinate key: {key} -> {first_loc[key]}")

except Exception as e:
    print(f"Error: {e}")
