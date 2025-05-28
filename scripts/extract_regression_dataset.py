import os
import rasterio
import pandas as pd
import numpy as np
from rasterio.transform import xy

# Define intervals and matching explanatory years
change_intervals = [("1996_2010", "2010"), ("2010_2015", "2015"), ("2015_2020", "2020")]

# Paths
change_dir = "data/mosaics"
predictor_dir = "data/processed_rasters"
output_dir = "data/csv"
os.makedirs(output_dir, exist_ok=True)
output_csv = os.path.join(output_dir, "mangrove_loss_regression_data.csv")

# Predictor rasters expected per year (except elevation)
predictors = ["chirps", "lst", "population", "landcover"]
elevation_fp = os.path.join(predictor_dir, "elevation_palawan.tif")

# Labels in change raster
LOSS_LABEL = 0
NO_CHANGE_LABEL = 2

# Store rows here
all_data = []

for interval, year in change_intervals:
    print(f"\n🔍 Interval: {interval} | Using predictors from: {year}")
    change_fp = os.path.join(change_dir, f"change_{interval}.tif")
    if not os.path.exists(change_fp):
        print(f"⚠️ Skipping interval: missing {change_fp}")
        continue

    with rasterio.open(change_fp) as change_src:
        change_arr = change_src.read(1)
        rows, cols = np.where(np.isin(change_arr, [LOSS_LABEL, NO_CHANGE_LABEL]))
        coords = [
            xy(change_src.transform, r, c, offset="center") for r, c in zip(rows, cols)
        ]
        labels = [
            1 if change_arr[r, c] == LOSS_LABEL else 0 for r, c in zip(rows, cols)
        ]

    # Extract predictors
    predictor_values = {}

    for p in predictors:
        pred_fp = os.path.join(predictor_dir, f"{p}_{year}_palawan.tif")
        if not os.path.exists(pred_fp):
            print(f"❌ Missing predictor raster: {pred_fp}")
            predictor_values[p] = [np.nan] * len(coords)
            continue

        with rasterio.open(pred_fp) as src:
            arr = src.read(1)
            values = []
            for x, y in coords:
                try:
                    r, c = src.index(x, y)
                    if 0 <= r < src.height and 0 <= c < src.width:
                        values.append(arr[r, c])
                    else:
                        values.append(np.nan)
                except:
                    values.append(np.nan)
            predictor_values[p] = values

    # Elevation (only once)
    if not os.path.exists(elevation_fp):
        print(f"❌ Missing elevation raster: {elevation_fp}")
        elevation_values = [np.nan] * len(coords)
    else:
        with rasterio.open(elevation_fp) as src:
            arr = src.read(1)
            elevation_values = []
            for x, y in coords:
                try:
                    r, c = src.index(x, y)
                    if 0 <= r < src.height and 0 <= c < src.width:
                        elevation_values.append(arr[r, c])
                    else:
                        elevation_values.append(np.nan)
                except:
                    elevation_values.append(np.nan)

    # Compile rows
    for i in range(len(coords)):
        row = {
            "x": coords[i][0],
            "y": coords[i][1],
            "interval": interval,
            "predictor_year": year,  # ✅ NEW COLUMN
            "loss": labels[i],
            "elevation": elevation_values[i],
        }
        for p in predictors:
            row[p] = predictor_values[p][i]
        all_data.append(row)

# Save as CSV
df = pd.DataFrame(all_data)
print(f"\n🧹 Dropping rows with missing values...")
df = df.dropna()
df.to_csv(output_csv, index=False)

print(f"\n✅ Saved: {output_csv}")
