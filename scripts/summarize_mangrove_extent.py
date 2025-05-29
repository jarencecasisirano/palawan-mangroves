import rasterio
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing your mangrove rasters
input_dir = "data/mosaics"
years = ["1996", "2010", "2015", "2020"]
pixel_area_ha = 0.0625  # 25m x 25m = 625 m² = 0.0625 ha

# Output list
results = []

for year in years:
    filepath = os.path.join(input_dir, f"mangroves_{year}.tif")
    if not os.path.exists(filepath):
        print(f"❌ Missing file: {filepath}")
        continue

    with rasterio.open(filepath) as src:
        arr = src.read(1)
        mangrove_pixels = np.sum(arr == 1)
        area_ha = mangrove_pixels * pixel_area_ha
        results.append(
            {
                "Year": int(year),
                "Mangrove Pixels": int(mangrove_pixels),
                "Area (ha)": round(area_ha, 2),
            }
        )

# Save and print summary
df = pd.DataFrame(results).sort_values("Year")
df.to_csv("data/stats/mangrove_extent_summary.csv", index=False)
print(df)


# Plot
# Line plot of mangrove extent
plt.figure(figsize=(8, 5))
plt.plot(df["Year"], df["Area (ha)"], marker="o", color="seagreen", linewidth=2)
plt.title("Mangrove Area in Palawan (1996–2020)")
plt.xlabel("Year")
plt.ylabel("Area (ha)")
plt.grid(True)
plt.tight_layout()

# Save plot
output_dir = "outputs/figures"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, "mangrove_extent_trend.png"), dpi=300)
plt.show()
