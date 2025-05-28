import rasterio
import numpy as np
import os

# Define intervals to analyze
intervals = [("1996", "2010"), ("2010", "2015"), ("2015", "2020")]

input_dir = "data/mosaics"
output_dir = "data/mosaics"

for start_year, end_year in intervals:
    file1 = os.path.join(input_dir, f"mangroves_{start_year}.tif")
    file2 = os.path.join(input_dir, f"mangroves_{end_year}.tif")
    output_file = os.path.join(output_dir, f"change_{start_year}_{end_year}.tif")

    with rasterio.open(file1) as src1, rasterio.open(file2) as src2:
        arr1 = src1.read(1)
        arr2 = src2.read(1)

        # Use 0 as NoData explicitly
        nodata1 = arr1 == 0
        nodata2 = arr2 == 0

        # Initialize change array with NoData (255)
        change = np.full(arr1.shape, 255, dtype=np.uint8)

        # Apply classification logic
        change[(arr1 == 1) & (arr2 == 1)] = 2  # No Change
        change[(arr1 == 1) & (nodata2)] = 0  # Loss
        change[(nodata1) & (arr2 == 1)] = 1  # Gain
        # All else remains 255 (NoData)

        # Update metadata
        meta = src1.meta.copy()
        meta.update(dtype=rasterio.uint8, nodata=255)

        with rasterio.open(output_file, "w", **meta) as dst:
            dst.write(change, 1)

        print(f"Saved classified change raster: {output_file}")
