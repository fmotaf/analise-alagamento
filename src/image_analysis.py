from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio

file_path = Path(__file__).resolve(strict=True).parent.parent
IMAGE_PATH = file_path / "static" / "tiff" / "Copernicus_DSM_COG_10_S13_00_W039_00_HAND.tif"
print(IMAGE_PATH)

with rasterio.open(IMAGE_PATH) as src:
    hand = src.read(1)
    transform = src.transform
    crs = src.crs
    flood_prone = hand < 5  # Boolean mask


rows, cols = np.where(flood_prone)
lons, lats = rasterio.transform.xy(transform, rows, cols)

# Zip into points
flood_points = list(zip(lons, lats))


df = pd.DataFrame({"lon": lons, "lat": lats, "hand": hand[rows, cols]})
df.to_csv("flood_features.csv", index=False)

with rasterio.open(IMAGE_PATH) as src:
    hand = src.read(1)
    hand = hand.astype(float)  # Ensure float for masking

    # Optional: mask no-data values (usually 0 or negative)
    hand[hand <= 0] = np.nan

    plt.figure(figsize=(10, 6))
    img = plt.imshow(hand, cmap="terrain")  # or 'viridis', 'magma', etc.
    cbar = plt.colorbar(img)
    cbar.set_label("HAND (meters above nearest drainage)", fontsize=12)

    plt.title("Height Above Nearest Drainage (HAND)")
    plt.axis("off")  # Hide axis ticks
    plt.show()


def get_coords():
    rows, cols = np.where(flood_prone)
    lons, lats = rasterio.transform.xy(transform, rows, cols)

    # Zip into points
    # flood_points = list(zip(lons, lats))


def extract_to_json():
    df = pd.DataFrame({"lon": lons, "lat": lats, "hand": hand[rows, cols]})
    df.to_csv("flood_features.csv", index=False)
