import geopandas as gpd
import matplotlib.pyplot as plt
import os

# File paths
geojson_files = {
    "2010": "data/gwr_outputs/gwr_2010_coefficients.geojson",
    "2015": "data/gwr_outputs/gwr_2015_coefficients.geojson",
    "2020": "data/gwr_outputs/gwr_2020_coefficients.geojson",
}

# GWR variables and labels
variables = {
    "elevation_norm": "Elevation",
    "chirps_norm": "Rainfall",
    "lst_norm": "Temperature",
}

# Prepare figure
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 12))
fig.suptitle("Spatial Variation of GWR Coefficients (2010–2020)", fontsize=16)

# Plot loop
for row_idx, (year, path) in enumerate(geojson_files.items()):
    gdf = gpd.read_file(path)
    for col_idx, (var, label) in enumerate(variables.items()):
        ax = axes[row_idx, col_idx]
        gdf.plot(
            column=var,
            cmap="coolwarm",
            markersize=5,
            legend=True,
            legend_kwds={"shrink": 0.6},
            ax=ax,
            edgecolor="none",
        )
        ax.set_title(f"{label} Coefficient ({year})", fontsize=10)
        ax.set_axis_off()

# Save the output
plt.tight_layout(rect=[0, 0, 1, 0.96])
output_path = "outputs/figures/gwr_spatial_coefficients_grid_updated.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300)
plt.show()
