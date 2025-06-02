import rasterio
import numpy as np
import os
import pandas as pd
import geopandas as gpd
from rasterio.mask import mask

# Folder setup
input_dir = "data/mosaics"
output_dir = "data/stats"
os.makedirs(output_dir, exist_ok=True)

# Pixel size from GMW (25m x 25m)
pixel_area_ha = (25 * 25) / 10000  # = 0.0625 hectares

# Time intervals
intervals = [("1996", "2010"), ("2010", "2015"), ("2015", "2020")]

# Load municipal boundaries
muni_path = "data/admin_boundaries/palawan_muni.geojson"
muni_gdf = gpd.read_file(muni_path)
muni_gdf = muni_gdf.to_crs("EPSG:4326")

# Lists to hold output
province_summary = []
municipality_summary = []

for start_year, end_year in intervals:
    raster_path = os.path.join(input_dir, f"change_{start_year}_{end_year}.tif")
    interval = f"{start_year}–{end_year}"

    if not os.path.exists(raster_path):
        print(f"Missing raster: {raster_path}")
        continue

    with rasterio.open(raster_path) as src:
        data = src.read(1)

        # Province-wide summary
        province_summary.append(
            {
                "Interval": interval,
                "Loss (ha)": round(np.sum(data == 0) * pixel_area_ha, 2),
                "Gain (ha)": round(np.sum(data == 1) * pixel_area_ha, 2),
                "No Change (ha)": round(np.sum(data == 2) * pixel_area_ha, 2),
            }
        )

        # Municipal summaries
        for idx, row in muni_gdf.iterrows():
            name = row["NAME_2"]
            geometry = [row["geometry"]]

            try:
                out_image, _ = mask(src, geometry, crop=True)
                masked = out_image[0]

                loss = np.sum(masked == 0)
                gain = np.sum(masked == 1)
                nochange = np.sum(masked == 2)

                municipality_summary.append(
                    {
                        "Municipality": name,
                        "Interval": interval,
                        "Loss (ha)": round(loss * pixel_area_ha, 2),
                        "Gain (ha)": round(gain * pixel_area_ha, 2),
                        "No Change (ha)": round(nochange * pixel_area_ha, 2),
                    }
                )
            except Exception as e:
                print(f"Error processing {name} in {interval}: {e}")

# Save CSV outputs
pd.DataFrame(province_summary).to_csv(
    os.path.join(output_dir, "change_area_summary.csv"), index=False
)

pd.DataFrame(municipality_summary).to_csv(
    os.path.join(output_dir, "change_area_by_municipality.csv"), index=False
)

print("\n✅ Summary files saved to data/stats/")
