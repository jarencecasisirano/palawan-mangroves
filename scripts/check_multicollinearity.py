import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
import os

# GWR
# Load regression dataset
df = pd.read_csv("data/csv/mangrove_loss_regression_data.csv")

# Clean no-data values
df["population"] = df["population"].replace(-3.4028230607370965e38, pd.NA)
df["elevation"] = df["elevation"].replace(-32768.0, pd.NA)
df = df.dropna()

# Filter for a specific year (e.g. 2015)
df = df[df["predictor_year"] == 2015].copy()

# Select predictors
predictors = ["chirps", "lst", "population", "landcover", "elevation"]
X = df[predictors].copy()

# Correlation matrix
corr = X.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("Predictor Correlation Matrix (2015)")
plt.tight_layout()
os.makedirs("data/stats", exist_ok=True)
plt.savefig("data/stats/correlation_matrix_2015.png", dpi=300)
print("📊 Correlation matrix saved to data/stats/correlation_matrix_2015.png")

# VIF calculation
# Ensure numeric data
for col in predictors:
    X[col] = pd.to_numeric(X[col], errors="coerce")

X = X.dropna()

# Add constant and ensure float dtype
X_const = add_constant(X).astype("float64")

# VIF calculation
vif_df = pd.DataFrame()
vif_df["Variable"] = X_const.columns
vif_df["VIF"] = [
    variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])
]


# Save to CSV
vif_df.to_csv("data/stats/vif_2015.csv", index=False)
print("📈 VIF results saved to data/stats/vif_2015.csv")
