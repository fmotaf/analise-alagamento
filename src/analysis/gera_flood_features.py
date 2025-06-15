import glob
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd
import rasterio
from rasterio import features as rfeatures
from shapely.geometry import mapping, shape

# Caminho dos arquivos .tif
TIF_DIR = "../data/raw/satellite/"
# Nome do arquivo de saída
OUT_CSV = "../src/flood_features_updated_for_neighbors.csv"


# Função para extrair estatísticas de um raster
def extract_raster_stats(raster_path):
    with rasterio.open(raster_path) as src:
        arr = src.read(1)
        arr = arr[arr != src.nodata]
        stats = {
            "hand_mean": np.mean(arr),
            "hand_median": np.median(arr),
            "hand_min": np.min(arr),
            "hand_max": np.max(arr),
            "hand_std": np.std(arr),
        }
    return stats


# Encontrar todos os arquivos .tif
raster_files = glob.glob(os.path.join(TIF_DIR, "*.tif"))

# Carregar geojson dos bairros e calcular centroide do(s) bairro(s)
GEOJSON_PATH = "../src/feira_bairros_urbanos.geojson"
with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
    geo = json.load(f)

# Gerar lista de meses de 2010-01 até 2025-12
start = datetime(2010, 1, 1)
end = datetime(2025, 12, 1)
months = pd.date_range(start, end, freq="MS").strftime("%Y%m").tolist()

# Para cada bairro, extrair estatísticas do HAND dentro do polígono
rows = []
for feature in geo["features"]:
    bairro_nome = feature["properties"].get("name", "bairro_sem_nome")
    polygon = shape(feature["geometry"])
    centroid = polygon.centroid
    latitude = centroid.y
    longitude = centroid.x
    # Extrair estatísticas de cada raster para o bairro
    bairro_stats = []
    for raster_path in raster_files:
        with rasterio.open(raster_path) as src:
            mask = rfeatures.geometry_mask([mapping(polygon)], src.shape, src.transform, invert=True)
            arr = src.read(1)
            arr = arr[mask]
            arr = arr[arr != src.nodata]
            if arr.size > 0:
                stats = {
                    "hand_mean": np.mean(arr),
                    "hand_median": np.median(arr),
                    "hand_min": np.min(arr),
                    "hand_max": np.max(arr),
                    "hand_std": np.std(arr),
                }
            else:
                stats = {
                    "hand_mean": np.nan,
                    "hand_median": np.nan,
                    "hand_min": np.nan,
                    "hand_max": np.nan,
                    "hand_std": np.nan,
                }
            bairro_stats.append(stats)
    # Média das estatísticas entre todos os rasters
    mean_stats = {k: np.nanmean([d[k] for d in bairro_stats]) for k in bairro_stats[0]}
    # Para cada mês, criar uma linha
    for month in months:
        row = {"bairro": bairro_nome, "month": month, "latitude": latitude, "longitude": longitude}
        row.update(mean_stats)
        rows.append(row)

# Criar DataFrame final
final_df = pd.DataFrame(rows)
final_df.to_csv(OUT_CSV, index=False)
print(f"Arquivo salvo em {OUT_CSV}")
