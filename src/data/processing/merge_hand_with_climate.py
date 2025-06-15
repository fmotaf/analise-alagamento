import pandas as pd
import json
from pathlib import Path

file_path = Path(__file__).resolve().parent.parent.parent.parent
flood_features_file = file_path / "src" / "data_load" / "flood_features.csv"
json_data_file = file_path / "data" / "json_dados_2010_2025_POWER_Point_Monthly_20100101_20251231_012d25S_038d95W_UTC.json"
# === 1. Carrega os pontos de HAND ===
df_hand = pd.read_csv(flood_features_file)  # deve conter lon, lat, hand

# === 2. Carrega os dados climáticos da NASA (JSON formatado pelo POWER API) ===
with open(json_data_file, "r") as f:
    nasa_data = json.load(f)

# === 3. Converte os parâmetros mensais para DataFrames separados ===
params = nasa_data["properties"]["parameter"]
dfs = []

for var_name, values in params.items():
    df = pd.DataFrame.from_dict(values, orient="index", columns=[var_name])
    df.index.name = "yyyymm"
    dfs.append(df)

# === 4. Junta todos os parâmetros em um único DataFrame ===
df_clima = pd.concat(dfs, axis=1).reset_index()
df_clima = df_clima[df_clima["yyyymm"].str[-2:] != "13"]  # remove entradas inválidas com mês 13
df_clima["date"] = pd.to_datetime(df_clima["yyyymm"], format="%Y%m")
df_clima.drop(columns=["yyyymm"], inplace=True)

# === 5. Produto cartesiano: cada ponto com cada mês ===
df_hand["key"] = 1
df_clima["key"] = 1

df_final = pd.merge(df_hand, df_clima, on="key").drop(columns="key")
# === 6. Salva o resultado para modelagem ===
df_final.to_csv("flood_dataset_full_with_flood_occurrence.csv", index=False)
print("✅ Dataset gerado com sucesso: flood_dataset_full.csv")
print(f"Total de linhas: {len(df_final):,}")
