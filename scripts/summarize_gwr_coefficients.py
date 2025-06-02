import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Setup
predictor_years = [2010, 2015, 2020]
predictors = ["chirps_norm", "lst_norm", "elevation_norm"]
summary_rows = []

# Load each GWR result and summarize
for year in predictor_years:
    path = f"data/gwr_outputs/gwr_{year}_coefficients.geojson"
    print(f"📂 Reading: {path}")
    gdf = gpd.read_file(path)

    year_summary = []

    for var in predictors:
        col = f"coef_{var}"
        if col in gdf.columns:
            mean_val = gdf[col].mean()
            abs_mean = gdf[col].abs().mean()
            row = {
                "predictor_year": year,
                "variable": var,
                "mean_coef": mean_val,
                "median_coef": gdf[col].median(),
                "std_coef": gdf[col].std(),
                "abs_mean_coef": abs_mean,
            }
            summary_rows.append(row)
            year_summary.append(row)

    # Rank by absolute mean coefficient
    ranked = sorted(year_summary, key=lambda x: x["abs_mean_coef"], reverse=True)
    for i, row in enumerate(ranked, start=1):
        row["rank"] = i

# Create summary DataFrame
summary_df = pd.DataFrame(summary_rows)

# Save to CSV
out_csv = "data/gwr_outputs/gwr_coefficients_summary.csv"
summary_df.to_csv(out_csv, index=False)
print(f"✅ Summary with rankings saved to: {out_csv}")

# Plotting coefficient trends
plt.figure(figsize=(10, 6))
for var in predictors:
    subset = summary_df[summary_df["variable"] == var]
    plt.plot(subset["predictor_year"], subset["mean_coef"], marker="o", label=var)

plt.title("Mean GWR Coefficients Over Time")
plt.xlabel("Predictor Year")
plt.ylabel("Mean Coefficient")
plt.axhline(0, color="gray", linestyle="--")
plt.legend(title="Variable")
plt.grid(True)
plt.tight_layout()

# Save plot
plot_path = "data/gwr_outputs/gwr_coefficient_trends.png"
plt.savefig(plot_path, dpi=300)
print(f"📈 Plot saved to: {plot_path}")
