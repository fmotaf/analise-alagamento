import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# 1. Carrega os dados com predições
df_pred = pd.read_csv("flood_previsao_2024_2025.csv")  # ou df_pred direto se ainda estiver em memória

# 2. Carrega bairros
gdf_bairros = gpd.read_file("feira_bairros.geojson")
gdf_bairros = gdf_bairros.to_crs("EPSG:4326")

# 3. Cria GeoDataFrame com os pontos
gdf_pred = gpd.GeoDataFrame(
    df_pred,
    geometry=gpd.points_from_xy(df_pred["lon"], df_pred["lat"]),
    crs="EPSG:4326"
)

# 4. Join espacial (associar ponto a bairro)
gdf_joined = gpd.sjoin(gdf_pred, gdf_bairros, how="left", predicate="within")

# 5. Renomeia a coluna de bairro se necessário (ex: name, NM_BAIRRO...)
gdf_joined = gdf_joined.rename(columns={"name": "bairro"})  # ajuste se necessário

# 6. Salva CSV com bairro
gdf_joined[["lon", "lat", "bairro", "date", "flood_pred"]].to_csv("flood_previsao_2024_2025.csv", index=False)

print("✅ Previsão final salva com bairros em: flood_previsao_2024_2025.csv")
