import pandas as pd
import geopandas as gpd
from mgwr.gwr import GWR
import numpy as np
import os

# Set paths
predictor_years = [2010, 2015, 2020]
predictors = ["chirps", "lst", "population", "landcover", "elevation"]
bandwidth = 2000

rows = []

for year in predictor_years:
    path = f"data/gwr_outputs/gwr_{year}_coefficients.geojson"
    gdf = gpd.read_file(path)

    # Clean & prepare
    for col in predictors + ["loss"]:
        gdf[col] = pd.to_numeric(gdf[col], errors="coerce")
    gdf = gdf.dropna(subset=predictors + ["loss"])
    coords = np.column_stack((gdf.geometry.x, gdf.geometry.y))
    X = gdf[predictors].values
    y = gdf["loss"].values.reshape(-1, 1)

    # Fit GWR again using same bandwidth
    model = GWR(coords, y, X, bw=bandwidth)
    results = model.fit()

    rows.append(
        {
            "predictor_year": year,
            "pseudo_r2": results.R2,
            "aic": results.aic,
            "log_likelihood": results.llf,
            "n_observations": len(y),
        }
    )

    print(f"\n📅 {year} GWR Model Evaluation:")
    print(f"  Pseudo R²       = {results.R2:.4f}")
    print(f"  AIC             = {results.aic:.2f}")
    print(f"  Log-Likelihood  = {results.llf:.2f}")
    print(f"  N Observations  = {len(y)}")

# Save summary
summary = pd.DataFrame(rows)
summary.to_csv("data/stats/gwr_model_fit_summary.csv", index=False)
print("\n✅ Summary saved to: data/stats/gwr_model_fit_summary.csv")
