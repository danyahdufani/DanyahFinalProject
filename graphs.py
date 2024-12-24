import pandas as pd
import matplotlib.pyplot as plt

# Read the dataset
df = pd.read_excel("data.xlsx")

# Clean and filter the data
filtered_df = df.dropna(subset=["estimate", "wbincome2024"])
average_mortality = filtered_df.groupby("wbincome2024")["estimate"].mean().sort_values()

# Create the bar plot
plt.figure(figsize=(10, 6))
average_mortality.plot(kind="bar", color="skyblue")
plt.title("Average AIDS Mortality by Income Group", fontsize=16)
plt.ylabel("AIDS Mortality Rate (per 1000)", fontsize=12)
plt.xlabel("Income Group", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("mortality_by_income_group.png")
plt.show()


# Group data by year and calculate mean mortality
time_series = filtered_df.groupby("date")["estimate"].mean()

# Create the line plot
plt.figure(figsize=(12, 6))
time_series.plot(kind="line", marker="o", color="orange")
plt.title("Global AIDS Mortality Trends Over Time", fontsize=16)
plt.ylabel("Mean Mortality Rate (per 1000)", fontsize=12)
plt.xlabel("Year", fontsize=12)
plt.grid(axis="both", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("mortality_trends_over_time.png")
plt.show()
