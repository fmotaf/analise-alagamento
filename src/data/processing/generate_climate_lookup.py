import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent

df = pd.read_csv(BASE_PATH / "notebooks/flood_features_3.csv")
df.columns = df.columns.str.strip().str.upper()

# Extract YEAR/MONTH from DATE if needed
if "YEAR" not in df.columns and "DATE" in df.columns:
    df["YEAR"] = df["DATE"].astype(str).str[:4].astype(int)
    df["MONTH"] = df["DATE"].astype(str).str[4:6].astype(int)

# Climate features to average
features = ["PRECTOTCORR", "RH2M", "QV2M", "GWETROOT", "GWETPROF", "GWETTOP", "CLOUD_AMT"]

# Create the lookup table
climate_lookup = (
    df.groupby(["LAT", "LON", "MONTH"])[features]
    .mean()
    .reset_index()
)

# Save to file
climate_lookup.to_csv(BASE_PATH / "notebooks/climate_lookup.csv", index=False)
print("✅ Saved climate_lookup.csv")
