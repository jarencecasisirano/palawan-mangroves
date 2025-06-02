import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
import os

# Settings
predictor_years = [2010, 2015, 2020]
predictors = ["chirps_norm", "lst_norm", "elevation_norm"]

# Load and clean dataset
df = pd.read_csv("data/csv/mangrove_loss_regression_data.csv")
df["elevation_norm"] = df["elevation_norm"].replace(-32768.0, pd.NA)
df = df.dropna()

# Output folder
os.makedirs("data/stats", exist_ok=True)

for year in predictor_years:
    print(f"\n📅 Checking multicollinearity for predictor year: {year}")
    df_year = df[df["predictor_year"] == year].copy()

    # Subset and drop missing values
    X = df_year[predictors].copy()
    X = X.apply(pd.to_numeric, errors="coerce").dropna()

    if X.empty:
        print(f"⚠️ No valid data for year {year}. Skipping.")
        continue

    # Generate and save correlation heatmap
    corr = X.corr()
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f")
    plt.title(f"Correlation Matrix ({year})")
    plt.tight_layout()
    corr_path = f"data/stats/correlation_matrix_{year}.png"
    plt.savefig(corr_path, dpi=300)
    plt.close()
    print(f"📊 Correlation matrix saved to: {corr_path}")

    # VIF calculation
    X_const = add_constant(X).astype("float64")
    vif_df = pd.DataFrame()
    vif_df["Variable"] = X_const.columns
    vif_df["VIF"] = [
        variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])
    ]

    # Save VIF to CSV
    vif_path = f"data/stats/vif_{year}.csv"
    vif_df.to_csv(vif_path, index=False)
    print(f"📈 VIF results saved to: {vif_path}")
