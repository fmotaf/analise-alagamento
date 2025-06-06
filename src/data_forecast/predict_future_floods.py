import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# === 1. Carrega os dados
df = pd.read_csv("flood_dataset_com_heuristica.csv")

# Converte date para datetime
df["date"] = pd.to_datetime(df["date"])

# === 2. Filtra apenas dados de previsão (jun/2024 a mai/2025)
df_pred = df[(df["date"] >= "2024-06-01") & (df["date"] <= "2025-05-31")].copy()

# Remove linhas com NaN
features = ["hand", "PRECTOTCORR_SUM", "RH2M", "GWETROOT"]
df_pred = df_pred.dropna(subset=features)

# === 3. Carrega o modelo treinado
# (certifique-se de que 'modelo_flood_rf.pkl' foi salvo previamente com joblib)
model = joblib.load("modelo_flood_rf.pkl")

# === 4. Faz a previsão
X_pred = df_pred[features]
df_pred["flood_pred"] = model.predict(X_pred)

# === 5. Seleciona e salva as colunas úteis
df_pred[["lon", "lat", "bairro", "date", "flood_pred"]].to_csv("flood_previsao_2024_2025.csv", index=False)

print("✅ Previsões salvas em: flood_previsao_2024_2025.csv")
print("Distribuição das previsões:")
print(df_pred["flood_pred"].value_counts())
