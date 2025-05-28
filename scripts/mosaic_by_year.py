import os
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
from collections import defaultdict

# 1. Define folders
input_folder = "data/mangroves_filtered"
output_folder = "data/mosaics"
os.makedirs(output_folder, exist_ok=True)

# 2. Group tiles by year
tiles_by_year = defaultdict(list)

for filename in os.listdir(input_folder):
    if filename.endswith(".tif") and "GMW" in filename:
        # Extract year from filename
        parts = filename.split("_")
        year = [p for p in parts if p.isdigit() and len(p) == 4]
        if year:
            year = year[0]
            tiles_by_year[year].append(os.path.join(input_folder, filename))

# 3. Mosaic and save each year
for year, file_list in tiles_by_year.items():
    src_files = [rasterio.open(fp) for fp in file_list]
    mosaic, transform = merge(src_files)

    meta = src_files[0].meta.copy()
    meta.update(
        {"height": mosaic.shape[1], "width": mosaic.shape[2], "transform": transform}
    )

    output_path = os.path.join(output_folder, f"mangroves_{year}.tif")
    with rasterio.open(output_path, "w", **meta) as dest:
        dest.write(mosaic)

    print(f"Mosaicked and saved: mangroves_{year}.tif")
