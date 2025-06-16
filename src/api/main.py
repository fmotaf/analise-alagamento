from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# === Load assets ===
df = pd.read_csv("../notebooks/flood_features_3.csv")
if 'year' not in df.columns and 'date' in df.columns:
    df['year'] = df['date'].astype(str).str[:4].astype(int)
    df['month'] = df['date'].astype(str).str[4:6].astype(int)

print(df.columns.tolist())

# === Load the pre-trained model ===
model = joblib.load("../models/flood_model.pkl")

# === Define API ===
app = FastAPI(title="Flood Risk Predictor", version="1.0")

class FloodRequest(BaseModel):
    lat: float
    lon: float
    year: int
    month: int

@app.post("/predict")
def predict_flood(req: FloodRequest):
    # Find row in data
    row = df[
        (df["lat"].round(4) == round(req.lat, 4)) &
        (df["lon"].round(4) == round(req.lon, 4)) &
        (df["year"] == req.year) &
        (df["month"] == req.month)
    ]
    
    if row.empty:
        raise HTTPException(status_code=404, detail="No data found for this location and date.")
    
    # Normalize column names to uppercase for feature selection
    # Use the exact feature order as in model training
    features = ["PRECTOTCORR", "RH2M", "QV2M", "GWETROOT", "GWETPROF", "GWETTOP", "CLOUD_AMT"]
    X = row[features]
    pred = model.predict(X)[0]
    
    return {
        "lat": req.lat,
        "lon": req.lon,
        "year": req.year,
        "month": req.month,
        "predicted_flood": int(pred)
    }
