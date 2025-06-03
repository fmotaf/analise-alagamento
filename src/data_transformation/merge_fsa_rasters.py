from pathlib import Path

import rasterio
from rasterio.merge import merge

# Paths to your files
file_path = Path(__file__).resolve(strict=True).parent.parent.parent

hand1 = file_path / "static" / "tiff" / "Feira_Dados_Copernicus_DSM_COG_10_S13_00_W039_00_HAND.tif"
hand2 = file_path / "static" / "tiff" / "Feira_dados_Copernicus_DSM_COG_10_S13_00_W040_00_HAND.tif"

# Lista de caminhos dos .tif que você quer mesclar
tif_files = [hand1, hand2]

# Abre os arquivos
src_files_to_mosaic = [rasterio.open(fp) for fp in tif_files]

# Faz o merge (mosaico)
mosaic, out_transform = merge(src_files_to_mosaic)

# Pega metadados do primeiro arquivo
out_meta = src_files_to_mosaic[0].meta.copy()

# Atualiza metadados com nova forma e transformação
out_meta.update({"driver": "GTiff", "height": mosaic.shape[1], "width": mosaic.shape[2], "transform": out_transform})

# Salva o raster mesclado
with rasterio.open(file_path / "static" / "tiff" / "HAND_merged_fsa.tif", "w", **out_meta) as dest:
    dest.write(mosaic)

print("✅ Raster mesclado salvo como: HAND_merged_fsa.tif")
