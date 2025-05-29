import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the dataset
df = pd.read_csv("data/stats/change_area_by_municipality.csv")

# Define interval durations in years
interval_years = {"1996–2010": 14, "2010–2015": 5, "2015–2020": 5}

# Compute rate of change
df["Loss Rate (ha/yr)"] = df["Loss (ha)"] / df["Interval"].map(interval_years)
df["Gain Rate (ha/yr)"] = df["Gain (ha)"] / df["Interval"].map(interval_years)

# Setup figure
intervals = list(interval_years.keys())
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
sns.set(style="whitegrid")

# Loop through each interval
for idx, interval in enumerate(intervals):
    df_interval = df[df["Interval"] == interval]

    # Top 5 Loss
    top5_loss = df_interval.nlargest(5, "Loss (ha)")
    ax_loss = axes[0, idx]
    sns.barplot(
        data=top5_loss, y="Municipality", x="Loss (ha)", ax=ax_loss, color="indianred"
    )
    ax_loss.set_title(f"Top 5 Mangrove Loss – {interval}")
    ax_loss.set_xlabel("Area Lost (ha)")
    ax_loss.set_ylabel("")

    # Annotate loss bars with rate
    for i, value in enumerate(top5_loss["Loss Rate (ha/yr)"]):
        ax_loss.text(value + 1, i, f"{value:.1f} ha/yr", va="center")

    # Top 5 Gain
    top5_gain = df_interval.nlargest(5, "Gain (ha)")
    ax_gain = axes[1, idx]
    sns.barplot(
        data=top5_gain, y="Municipality", x="Gain (ha)", ax=ax_gain, color="seagreen"
    )
    ax_gain.set_title(f"Top 5 Mangrove Gain – {interval}")
    ax_gain.set_xlabel("Area Gained (ha)")
    ax_gain.set_ylabel("")

    # Annotate gain bars with rate
    for i, value in enumerate(top5_gain["Gain Rate (ha/yr)"]):
        ax_gain.text(value + 1, i, f"{value:.1f} ha/yr", va="center")

# Final layout
plt.tight_layout()
os.makedirs("outputs/figures", exist_ok=True)
plt.savefig("outputs/figures/top5_loss_gain_by_interval_with_rates.png", dpi=300)
plt.show()
