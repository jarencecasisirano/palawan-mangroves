import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the change summary
df = pd.read_csv("data/stats/change_area_summary.csv")

# Clean and structure
df.columns = [col.strip() for col in df.columns]
df["Interval"] = pd.Categorical(
    df["Interval"], categories=["1996–2010", "2010–2015", "2015–2020"], ordered=True
)
df_melted = df.melt(id_vars="Interval", var_name="Category", value_name="Hectares")

# Plot
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.barplot(data=df_melted, x="Interval", y="Hectares", hue="Category")
plt.title("Mangrove Change Summary in Palawan by Interval")
plt.ylabel("Area (Hectares)")
plt.xlabel("Change Interval")
plt.legend(title="Change Type")
plt.tight_layout()

# Save
os.makedirs("outputs/figures", exist_ok=True)
plt.savefig("outputs/figures/mangrove_change_summary.png")
print("📁 Saved to: outputs/figures/mangrove_change_summary.png")
