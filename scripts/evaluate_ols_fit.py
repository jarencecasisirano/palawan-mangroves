import pandas as pd
import statsmodels.api as sm
import os

# Setup
predictor_years = [2010, 2015, 2020]
predictors = ["chirps", "lst", "population", "landcover", "elevation"]
rows = []

# Load and clean data
df = pd.read_csv("data/csv/mangrove_loss_regression_data.csv")
df["population"] = df["population"].replace(-3.4028230607370965e38, pd.NA)
df["elevation"] = df["elevation"].replace(-32768.0, pd.NA)
df = df.dropna()

# Loop through years
for year in predictor_years:
    print(f"📅 Evaluating OLS model for predictor year: {year}")
    df_year = df[df["predictor_year"] == year].copy()

    # Ensure numeric
    X = df_year[predictors].apply(pd.to_numeric, errors="coerce")
    y = pd.to_numeric(df_year["loss"], errors="coerce")

    # Drop rows with any NaNs
    valid = X.notna().all(axis=1) & y.notna()
    X = X[valid].astype("float64")
    y = y[valid].astype("float64")

    # Add intercept and fit model
    X = sm.add_constant(X)
    model = sm.Logit(y, X).fit(disp=False)

    rows.append(
        {
            "predictor_year": year,
            "pseudo_r2": model.prsquared,
            "aic": model.aic,
            "log_likelihood": model.llf,
            "n_observations": int(model.nobs),
        }
    )

# Save to CSV
out_df = pd.DataFrame(rows)
os.makedirs("data/stats", exist_ok=True)
out_df.to_csv("data/stats/ols_model_fit_summary.csv", index=False)
print("✅ Summary saved to: data/stats/ols_model_fit_summary.csv")
