from pathlib import Path

import geopandas as gpd
import rasterio
from rasterio.mask import mask

# Paths to your files
file_path = Path(__file__).resolve().parent.parent.parent.parent

hand_fsa = file_path / "static" / "tiff" / "HAND_merged_fsa.tif"

# Caminhos dos arquivos
tif_path = hand_fsa
geojson_path = file_path / "src" / "data_transformation" / "feira_de_santana_convertido.geojson"
output_tif = "feira_hand_recortado.tif"

# Carrega os bairros
gdf = gpd.read_file(geojson_path)

# Garante que está no mesmo CRS do raster
with rasterio.open(tif_path) as src:
    gdf = gdf.to_crs(src.crs)

    # Correto: Converte os bairros para o formato esperado pelo rasterio.mask
    geometries = [geom.__geo_interface__ for geom in gdf.geometry]

    # Recorta o raster com a máscara dos bairros
    out_image, out_transform = mask(src, geometries, crop=True)
    out_meta = src.meta.copy()

# Atualiza metadados para o novo raster recortado
out_meta.update({"height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})

# Salva o novo raster
with rasterio.open(output_tif, "w", **out_meta) as dest:
    dest.write(out_image)

print(f"✅ Raster recortado salvo em: {output_tif}")
