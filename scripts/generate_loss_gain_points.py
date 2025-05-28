import rasterio
import numpy as np
import os
import geopandas as gpd
from shapely.geometry import Point

# Folder setup
input_dir = "data/mosaics"
output_dir = "data/spatial_points"
os.makedirs(output_dir, exist_ok=True)

# Define intervals to process
intervals = [("1996", "2010"), ("2010", "2015"), ("2015", "2020")]

# Loop over each change raster
for start, end in intervals:
    interval = f"{start}_{end}"
    raster_path = os.path.join(input_dir, f"change_{interval}.tif")

    if not os.path.exists(raster_path):
        print(f"Missing file: {raster_path}")
        continue

    with rasterio.open(raster_path) as src:
        data = src.read(1)
        transform = src.transform

        loss_points = []
        gain_points = []

        rows, cols = np.where((data == 0) | (data == 1))
        for r, c in zip(rows, cols):
            x, y = rasterio.transform.xy(transform, r, c, offset="center")
            value = data[r, c]
            point = Point(x, y)
            if value == 0:
                loss_points.append(point)
            elif value == 1:
                gain_points.append(point)

        # Save as GeoJSON
        if loss_points:
            gdf_loss = gpd.GeoDataFrame(geometry=loss_points, crs=src.crs)
            gdf_loss.to_file(
                os.path.join(output_dir, f"loss_points_{interval}.geojson"),
                driver="GeoJSON",
            )

        if gain_points:
            gdf_gain = gpd.GeoDataFrame(geometry=gain_points, crs=src.crs)
            gdf_gain.to_file(
                os.path.join(output_dir, f"gain_points_{interval}.geojson"),
                driver="GeoJSON",
            )

        print(f"Saved loss/gain point layers for {interval}")
