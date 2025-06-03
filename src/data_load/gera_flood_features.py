from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

file_path = Path(__file__).resolve(strict=True).parent.parent.parent

# Caminho do arquivo .tif já recortado pelos bairros
raster_path = file_path / "src" / "data_aggregation" / "feira_hand_recortado.tif"
output_csv = "flood_features.csv"

# Abre o raster
with rasterio.open(raster_path) as src:
    hand = src.read(1).astype(float)
    transform = src.transform

    # Máscara: pega apenas valores positivos (HAND > 0)
    mask = hand > 0
    rows, cols = np.where(mask)

    # Converte coordenadas de matriz para lon/lat
    lons, lats = rasterio.transform.xy(transform, rows, cols)

    # Cria DataFrame com os pontos
    df = pd.DataFrame({"lon": lons, "lat": lats, "hand": hand[rows, cols]})

# Salva em CSV
df.to_csv(output_csv, index=False)
print(f"✅ flood_features.csv gerado com {len(df)} pontos.")
