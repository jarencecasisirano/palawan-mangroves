import pandas as pd
import geopandas as gpd
from mgwr.gwr import GWR
from shapely.geometry import Point
import numpy as np
import os

# Settings
predictor_years = [2010, 2015, 2020]
predictors = ["chirps", "lst", "population", "landcover", "elevation"]
bandwidth = 2000
sample_size = 30000  # Adjust for performance

# Load and clean data
df = pd.read_csv("data/csv/mangrove_loss_regression_data.csv")
df["population"] = df["population"].replace(-3.4028230607370965e38, pd.NA)
df["elevation"] = df["elevation"].replace(-32768.0, pd.NA)
df = df.dropna()

for year in predictor_years:
    print(f"\n📅 Running GWR for predictor year: {year} (bandwidth = {bandwidth})")

    df_year = df[df["predictor_year"] == year].copy()

    # Optional sampling
    if len(df_year) > sample_size:
        df_year = df_year.sample(n=sample_size, random_state=42)

    # Build GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df_year,
        geometry=gpd.points_from_xy(df_year["x"], df_year["y"]),
        crs="EPSG:4326",
    ).to_crs("EPSG:32651")

    # Ensure numeric
    for col in predictors + ["loss"]:
        gdf[col] = pd.to_numeric(gdf[col], errors="coerce")
    gdf = gdf.dropna(subset=predictors + ["loss"])

    # Prepare inputs
    coords = np.column_stack((gdf.geometry.x, gdf.geometry.y))
    X = gdf[predictors].values
    y = gdf["loss"].values.reshape(-1, 1)

    # Run GWR
    print("🧠 Fitting model...")
    model = GWR(coords, y, X, bandwidth)
    results = model.fit()

    # Store local coefficients
    for i, var in enumerate(["Intercept"] + predictors):
        gdf[f"coef_{var}"] = results.params[:, i]

    # Save output
    out_path = f"data/gwr_outputs/gwr_{year}_coefficients.geojson"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    gdf.to_file(out_path, driver="GeoJSON")
    print(f"✅ Saved: {out_path}")
