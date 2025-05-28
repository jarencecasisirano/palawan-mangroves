import geopandas as gpd
from shapely.geometry import box
import rasterio
import os
import shutil

# 1. Load Palawan boundary
palawan = gpd.read_file("data/admin-boundaries/palawan.geojson")

# 2. Source folder containing raster tiles
tiles_folder = "data/mangroves"

# 3. Destination folder for filtered tiles
filtered_folder = "data/mangroves_filtered"
os.makedirs(filtered_folder, exist_ok=True)

# 4. Loop through raster tiles
for filename in os.listdir(tiles_folder):
    if filename.endswith(".tif"):
        tile_path = os.path.join(tiles_folder, filename)
        with rasterio.open(tile_path) as src:
            bounds = box(*src.bounds)
            tile_geom = gpd.GeoDataFrame(geometry=[bounds], crs=src.crs)

            # Ensure CRS alignment
            palawan_proj = palawan.to_crs(tile_geom.crs)

            if tile_geom.intersects(palawan_proj.geometry.union_all()).any():
                dest_path = os.path.join(filtered_folder, filename)
                if not os.path.exists(dest_path):
                    shutil.copy(tile_path, dest_path)
                    print(f"Copied: {filename}")
                else:
                    print(f"Already exists: {filename}")
