import json

import pandas as pd

# Caminhos dos arquivos
json_path = "../data/json_dados_2010_2025_POWER_Point_Monthly_20100101_20251231_012d25S_038d95W_UTC.json"
flood_pred_path = "../src/flood_predictions.csv"
flood_feat_path = "../src/flood_features.csv"

# Carregar dados climáticos (NASA)
with open(json_path, "r", encoding="utf-8") as f:
    nasa_data = json.load(f)

# Extrair parâmetros e datas
parameters = nasa_data["properties"]["parameter"]
months = list(parameters[list(parameters.keys())[0]].keys())

# Montar DataFrame dos dados climáticos
climate_df = pd.DataFrame({"month": months})
for param, values in parameters.items():
    climate_df[param] = climate_df["month"].map(values)

# Carregar flood_predictions.csv
flood_pred = pd.read_csv(flood_pred_path)

# Carregar flood_features.csv (features estáticas)
flood_feat = pd.read_csv(flood_feat_path)

# Juntar features estáticas a todos os meses (broadcast)
for col in flood_feat.columns:
    climate_df[col] = flood_feat[col][0]

# Unir com flood_predictions pelo campo de data/mês
# Supondo que flood_predictions tem coluna 'month' no mesmo formato (ex: '201001')
df = pd.merge(climate_df, flood_pred, on="month", how="inner")

# Tratar valores ausentes (-999)
df.replace(-999, pd.NA, inplace=True)
df = df.dropna()

# Salvar dataset pronto para treino
df.to_csv("../data/dataset_treino.csv", index=False)

print("Dataset de treino salvo em ../data/dataset_treino.csv")
