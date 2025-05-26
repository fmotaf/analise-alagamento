from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import rasterio
from rasterio.plot import show

# Paths to your files
file_path = Path(__file__).resolve(strict=True).parent.parent
hand_path = file_path / "static" / "tiff" / "Copernicus_DSM_COG_10_S13_00_W039_00_HAND.tif"
flood_csv = "flood_features.csv"  # Your CSV should have 'lat' and 'lon' columns


# Load HAND raster
with rasterio.open(hand_path) as src:
    hand_data = src.read(1)
    hand_extent = rasterio.plot.plotting_extent(src)
    raster_crs = src.crs

    # Load your extracted HAND points
    df = pd.read_csv(flood_csv)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326").to_crs(raster_crs)

    # Plot everything
    fig, ax = plt.subplots(figsize=(12, 8))

    # Show the background HAND raster
    show((src, 1), ax=ax, cmap="terrain", title="HAND Raster + Sampled HAND Points")

    # Overlay the points with color based on 'hand' value
    gdf.plot(
        ax=ax,
        column="hand",
        cmap="coolwarm_r",  # blue=low, red=high HAND values
        markersize=40,
        legend=True,
        legend_kwds={"label": "HAND Elevation (m)"},
        alpha=0.9,
    )

    plt.axis("off")
    plt.tight_layout()
    plt.show()

#
# # Load HAND raster and extract what you need inside the context
# with rasterio.open(hand_path) as src:
#     hand_data = src.read(1)
#     hand_extent = rasterio.plot.plotting_extent(src)
#     raster_crs = src.crs
#     hand_cmap = "terrain"  # you can change this if you like
#
#     # Prepare figure
#     fig, ax = plt.subplots(figsize=(12, 8))
#     show((src, 1), ax=ax, cmap=hand_cmap, title="HAND + Historical Flood Events")
#
#     # Load flood event points
#     df = pd.read_csv(flood_csv)
#     gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326")
#
#     # Reproject flood points to match HAND raster
#     gdf = gdf.to_crs(raster_crs)
#
#     # Plot points
#     gdf.plot(ax=ax, color="blue", markersize=25, label="Flood Events")
#
#     # Final layout
#     plt.legend()
#     plt.axis("off")
#     plt.tight_layout()
#     plt.show()
