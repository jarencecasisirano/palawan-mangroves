import os
import rasterio
from rasterio.mask import mask
import geopandas as gpd

# Define folders for each dataset
dataset_folders = {
    "chirps": "data/chirps-rainfall",
    "landcover": "data/esa_land_cover",
    "population": "data/nasa-gpw",
    "lst": "data/modis-lst",
}

# SRTM (only one file, already merged)
srtm_path = "data/srtm-elevation/srtm_palawan.tif"

# Output folder
output_dir = "data/processed_rasters"
os.makedirs(output_dir, exist_ok=True)

# Load Palawan boundary
boundary = gpd.read_file("data/admin_boundaries/palawan.geojson")
boundary = boundary.to_crs("EPSG:4326")


def clip_raster(infile, outfile):
    with rasterio.open(infile) as src:
        out_image, out_transform = mask(src, boundary.geometry, crop=True)
        out_meta = src.meta.copy()
        out_meta.update(
            {
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
            }
        )

        with rasterio.open(outfile, "w", **out_meta) as dst:
            dst.write(out_image)
        print(f"✅ Clipped: {os.path.basename(outfile)}")


# Process each multi-year dataset
for dataset, folder in dataset_folders.items():
    for fname in os.listdir(folder):
        if fname.endswith(".tif") or fname.endswith(".tiff"):
            year = "".join(filter(str.isdigit, fname))[:4]
            in_path = os.path.join(folder, fname)
            out_path = os.path.join(output_dir, f"{dataset}_{year}_palawan.tif")
            clip_raster(in_path, out_path)

# Copy SRTM directly (already pre-clipped)
srtm_out = os.path.join(output_dir, "elevation_palawan.tif")
if os.path.exists(srtm_path):
    os.system(f"cp {srtm_path} {srtm_out}")
    print(f"✅ Copied SRTM: elevation_palawan.tif")
else:
    print("⚠️ SRTM file not found.")
