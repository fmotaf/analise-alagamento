from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path


# === Base path of this file ===
BASE_DIR = Path(__file__).resolve().parent

# === Load Data ===
df = pd.read_csv(BASE_DIR / "flood_features_3.csv")
df.columns = df.columns.str.strip().str.upper()

# Extract year/month if missing
if "YEAR" not in df.columns and "DATE" in df.columns:
    df["YEAR"] = df["DATE"].astype(str).str[:4].astype(int)
    df["MONTH"] = df["DATE"].astype(str).str[4:6].astype(int)

# === Load Baseline Climate Lookup ===
climate_lookup = pd.read_csv(BASE_DIR / "climate_lookup.csv")
climate_lookup.columns = climate_lookup.columns.str.upper()

# === Load model ===
model = joblib.load(BASE_DIR / "flood_model.pkl")

# === API Setup ===
app = FastAPI(title="Flood Risk Predictor", version="2.1")

class FloodRequest(BaseModel):
    lat: float
    lon: float
    year: int
    month: int

@app.get("/")
def read_root():
    return {"message": "Welcome."}

@app.post("/predict")
def predict_flood(req: FloodRequest):
    lat = round(req.lat, 4)
    lon = round(req.lon, 4)
    year = req.year
    month = req.month
    features = ["PRECTOTCORR", "RH2M", "QV2M", "GWETROOT", "GWETPROF", "GWETTOP", "CLOUD_AMT"]

    # First try: lookup exact historical record
    row = df[
        (df["LAT"].round(4) == lat) &
        (df["LON"].round(4) == lon) &
        (df["YEAR"] == year) &
        (df["MONTH"] == month)
    ]

    if not row.empty:
        X = row[features]
        pred = model.predict(X)[0]
        return {
            "source": "historical",
            "lat": lat,
            "lon": lon,
            "year": year,
            "month": month,
            "predicted_flood": int(pred)
        }

    # Fallback: use climate baseline from same lat/lon/month
    baseline = climate_lookup[
        (climate_lookup["LAT"].round(4) == lat) &
        (climate_lookup["LON"].round(4) == lon) &
        (climate_lookup["MONTH"] == month)
    ]

    if baseline.empty:
        raise HTTPException(status_code=404, detail="No climate baseline found for this location/month.")

    X = baseline[features]
    pred = model.predict(X)[0]
    return {
        "source": "climate-baseline",
        "lat": lat,
        "lon": lon,
        "year": year,
        "month": month,
        "predicted_flood": int(pred)
    }
