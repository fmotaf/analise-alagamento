import requests
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define region bounds and step size (adjust step for resolution/performance)
lat_min, lat_max = -12.35, -12.15
lon_min, lon_max = -39.10, -38.90
lat_step = 0.01
lon_step = 0.01

# List of parameters to extract
params = [
    'CLOUD_AMT', 'GWETPROF', 'GWETROOT', 'GWETTOP',
    'PRECTOTCORR', 'QV2M', 'RH2M'
]
param_str = ','.join(params)

lats = np.arange(lat_min, lat_max + lat_step, lat_step)
lons = np.arange(lon_min, lon_max + lon_step, lon_step)
points = [(lat, lon) for lat in lats for lon in lons]

all_records = []

def fetch_point_data(lat, lon):
    url = (
        f'https://power.larc.nasa.gov/api/temporal/monthly/point?'
        f'latitude={lat}&longitude={lon}'
        f'&parameters={param_str}&community=AG&start=2010&end=2024&format=JSON'
    )
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        param_data = data['properties']['parameter']
        dates = next(iter(param_data.values())).keys()
        records = []
        for date in dates:
            record = {'lat': lat, 'lon': lon, 'date': date}
            for param in params:
                record[param] = param_data.get(param, {}).get(date, None)
            records.append(record)
        return records
    except Exception as e:
        print(f'Error for lat={lat}, lon={lon}: {e}')
        return []

# Use ThreadPoolExecutor for parallel requests
max_workers = 8
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(fetch_point_data, lat, lon) for lat, lon in points]
    for future in as_completed(futures):
        all_records.extend(future.result())

# Create DataFrame and save to CSV
if all_records:
    df = pd.DataFrame(all_records)
    print(df.head())
    df.to_csv('flood_features_3.csv', index=False)
    print('Saved to flood_features_3.csv')
else:
    print('No data records found.')
