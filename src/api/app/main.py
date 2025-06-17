from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from typing import List


# === Base path of this file ===
BASE_DIR = Path(__file__).resolve().parent

# === Load Data ===
df = pd.read_csv(BASE_DIR / "flood_features_3.csv")
df.columns = df.columns.str.strip().str.upper()

df_pred = pd.read_csv(BASE_DIR / "flood_predictions.csv")  

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FloodRequest(BaseModel):
    lat: float
    lon: float
    year: int
    month: int

@app.get("/")
def read_root():
    return {"message": "Welcome."}


@app.get("/flood-map")
def get_flood_points(year: int = Query(...), month: int = Query(...)) -> List[dict]:
    df_pred.columns = df_pred.columns.str.strip().str.lower()

    filtered = df_pred[
        (df_pred["year"] == year) &
        (df_pred["month"] == month) &
        (df_pred["predicted_flood"] == 1)
    ]

    points = (
        filtered[["lat", "lon"]]
        .drop_duplicates()
        .round(5)
        .to_dict(orient="records")
    )
    return points


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
