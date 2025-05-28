import pandas as pd
import statsmodels.api as sm
import os

# Load the cleaned regression dataset
df = pd.read_csv("data/csv/mangrove_loss_regression_data.csv")

# Replace known no-data values
df["population"] = df["population"].replace(-3.4028230607370965e38, pd.NA)
df["elevation"] = df["elevation"].replace(-32768.0, pd.NA)

# Drop rows with missing values
df = df.dropna()

# Define predictors
predictors = ["chirps", "lst", "population", "landcover", "elevation"]

# Create output folder
output_dir = "data/regression_outputs"
os.makedirs(output_dir, exist_ok=True)

# Loop over each predictor year and run logistic regression
for year in sorted(df["predictor_year"].unique()):
    print("\n" + "=" * 60)
    print(f"📅 Logistic Regression for predictor year: {year}")
    print("=" * 60)

    df_year = df[df["predictor_year"] == year]

    # Ensure all predictors are numeric
    X = df_year[predictors].apply(pd.to_numeric, errors="coerce")
    X = sm.add_constant(X)
    y = pd.to_numeric(df_year["loss"], errors="coerce")

    # Drop rows with invalid values
    valid_rows = X.notnull().all(axis=1) & y.notnull()
    X = X[valid_rows]
    y = y[valid_rows]

    if len(X) == 0:
        print(f"⚠️ No valid data for year {year}. Skipping.")
        continue

    # Fit the model
    model = sm.Logit(y, X).fit(disp=False)

    # Print to terminal
    print(model.summary())

    # Save to file
    output_path = os.path.join(output_dir, f"logit_summary_{year}.txt")
    with open(output_path, "w") as f:
        f.write(f"Logistic Regression Summary for {year}\n")
        f.write("=" * 60 + "\n\n")
        f.write(str(model.summary()))
    print(f"📁 Saved summary: {output_path}")
