import requests
import pandas as pd
import numpy as np  # <-- Add this import
import time

# Define grid bounds (Feira de Santana region, adjust as needed)
lat_min, lat_max = -12.35, -12.15
lon_min, lon_max = -39.10, -38.90
lat_step = 0.01  # ~1km
lon_step = 0.01

dates = ['2024-01-01', '2024-12-31']  # Change to your desired period (start, end)

# Generate grid points
lats = [round(x, 4) for x in list(np.arange(lat_min, lat_max, lat_step))]
lons = [round(x, 4) for x in list(np.arange(lon_min, lon_max, lon_step))]

results = []

for lat in lats:
    for lon in lons:
        url = (
            f'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR'
            f'&community=AG&longitude={lon}&latitude={lat}'
            f'&start={dates[0].replace("-","")}&end={dates[1].replace("-","")}&format=JSON'
        )
        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
            # Extract daily precipitation
            daily = data['properties']['parameter']['PRECTOTCORR']
            for date, value in daily.items():
                results.append({'lat': lat, 'lon': lon, 'date': date, 'PRECTOTCORR': value})
            print(f"Downloaded {lat}, {lon}")
        except Exception as e:
            print(f"Failed {lat}, {lon}: {e}")
        time.sleep(0.5)  # Be polite to the API

# Save to CSV
out = pd.DataFrame(results)
out.to_csv('flood_features2.csv', index=False)
print(f"✅ flood_features2.csv generated with {len(out)} rows.")
