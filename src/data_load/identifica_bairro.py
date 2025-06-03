import geopandas as gpd
import pandas as pd
from pathlib import Path

# 1. Carrega os pontos do flood_features.csv como GeoDataFrame
df = pd.read_csv("flood_features.csv")
gdf_points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326")


file_path = Path(__file__).resolve(strict=True).parent.parent.parent
# 2. Carrega os bairros
gdf_bairros = gpd.read_file(file_path / "src" / "data_transformation" / "feira_de_santana_convertido.geojson")

# 3. Garante que ambos estão no mesmo CRS
gdf_bairros = gdf_bairros.to_crs(gdf_points.crs)

# 4. Faz join espacial: encontra qual ponto pertence a qual bairro
joined = gpd.sjoin(gdf_points, gdf_bairros, how="left", predicate="within")

# 5. Seleciona apenas colunas úteis
# Substitua "name" abaixo pelo nome real da coluna de bairro (ex: NM_BAIRRO)
joined = joined.rename(columns={"NM_BAIRRO": "bairro"})  # opcional
output = joined[["lon", "lat", "hand", "bairro"]]

# 6. Salva resultado
output.to_csv("flood_features_com_bairro.csv", index=False)
print("✅ Arquivo 'flood_features_com_bairro.csv' gerado com bairros atribuídos.")
