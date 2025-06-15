from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.plot import show
from shapely.geometry import box

PARENT_DIR = Path(__file__).resolve(strict=True).parent.parent
print(PARENT_DIR)
HAND_FILE = PARENT_DIR / "static" / "tiff" / "Copernicus_DSM_COG_10_S13_00_W039_00_HAND.tif"
print(HAND_FILE)
# --- File paths ---
# hand_path = HAND_FILE
# flood_csv = "flood_features.csv"
# neigh_path = "feira_neighborhoods.geojson"  # from OSM
#
# # --- Load the HAND raster and get CRS/extents ---
# with rasterio.open(hand_path) as src:
#     hand_data = src.read(1).astype(float)
#     hand_data[hand_data <= 0] = np.nan  # mask no-data
#     hand_extent = rasterio.plot.plotting_extent(src)
#     raster_crs = src.crs
#
# # --- Load sampled HAND points ---
# df = pd.read_csv(flood_csv)
# gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326")
# gdf = gdf.to_crs(raster_crs)
#
# # --- Load neighborhood boundaries ---
# neigh_gdf = gpd.read_file(neigh_path)
# neigh_gdf = neigh_gdf.to_crs(raster_crs)
#
# # --- Plot everything ---
# fig, ax = plt.subplots(figsize=(12, 8))
#
# # Show HAND raster
# with rasterio.open(hand_path) as src:
#     show((src, 1), ax=ax, cmap="terrain", title="HAND Raster + Flood Points + Neighborhoods")
#
# # Plot HAND points
# gdf.plot(ax=ax, column="hand", cmap="coolwarm_r", markersize=40, legend=True,
#          legend_kwds={"label": "HAND Elevation (m)", "shrink": 0.6})
#
# # Plot neighborhood boundaries
# neigh_gdf.boundary.plot(ax=ax, edgecolor="black", linewidth=0.7)
#
# # Optional: label neighborhoods by name
# for idx, row in neigh_gdf.iterrows():
#     name = row.get("name") or row.get("name:pt") or row.get("NOME") or None
#     if name:
#         centroid = row.geometry.centroid
#         ax.annotate(name, xy=(centroid.x, centroid.y), fontsize=8, color='black', ha='center')
#
# plt.axis("off")
# plt.tight_layout()
# plt.show()


# Paths to your files
hand_path = HAND_FILE
flood_csv = "flood_features.csv"
neigh_path = "feira_neighborhoods.geojson"

# Load the HAND raster
with rasterio.open(hand_path) as src:
    hand_data = src.read(1).astype(float)
    hand_data[hand_data <= 0] = np.nan  # mask no-data
    raster_bounds = box(*src.bounds)
    raster_extent = rasterio.plot.plotting_extent(src)
    raster_crs = src.crs

# Load sampled HAND points
df = pd.read_csv(flood_csv)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326")
gdf = gdf.to_crs(raster_crs)

# Load neighborhood GeoJSON and reproject to match raster
neigh_gdf = gpd.read_file(neigh_path).to_crs(raster_crs)

# Filter neighborhoods that intersect the raster area
neigh_gdf = neigh_gdf[neigh_gdf.intersects(raster_bounds)]

# Start plotting
fig, ax = plt.subplots(figsize=(12, 8))

# HAND raster
with rasterio.open(hand_path) as src:
    show((src, 1), ax=ax, cmap="terrain", title="HAND Raster + Flood Points + Neighborhoods")

# Flood feature points (colored by HAND value)
gdf.plot(
    ax=ax,
    column="hand",
    cmap="coolwarm_r",
    markersize=40,
    legend=True,
    legend_kwds={"label": "HAND Elevation (m)", "shrink": 0.6},
)

# Neighborhood boundaries
neigh_gdf.boundary.plot(ax=ax, edgecolor="black", linewidth=0.7)

# Label neighborhoods (if a name field exists)
for idx, row in neigh_gdf.iterrows():
    name = row.get("name") or row.get("name:pt") or row.get("NOME") or None
    if name:
        centroid = row.geometry.centroid
        ax.annotate(name, xy=(centroid.x, centroid.y), fontsize=7, color="black", ha="center")

# Limit view to the raster extent
ax.set_xlim(raster_bounds.bounds[0], raster_bounds.bounds[2])
ax.set_ylim(raster_bounds.bounds[1], raster_bounds.bounds[3])

plt.axis("off")
plt.tight_layout()
plt.show()
