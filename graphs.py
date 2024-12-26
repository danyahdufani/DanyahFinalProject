import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import os
import numpy as np
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Set Seaborn style for aesthetic improvement
sns.set(style="whitegrid", palette="muted")

# Ensure output folder exists
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

def read_data(file_path):
    """Reads data from an Excel file."""
    return pd.read_excel(file_path)

def filter_data(df):
    """Cleans and filters the data to remove rows with missing 'estimate' or 'wbincome2024'."""
    return df.dropna(subset=["estimate", "wbincome2024"])

def encode_income_groups(df):
    """Encodes income groups into numerical values."""
    income_mapping = {
        "High income": 4,
        "Upper middle income": 3,
        "Lower middle income": 2,
        "Low income": 1
    }
    df["income_encoded"] = df["wbincome2024"].map(income_mapping)
    return df

 # Check all column names in the DataFrame

def calculate_average_mortality(df):
    """Calculates the average mortality rate by income group."""
    filtered_df = filter_data(df)
    return filtered_df.groupby("wbincome2024")["estimate"].mean().sort_values()

def create_bar_chart_with_numbers(df):
    """Creates and saves a bar chart of AIDS mortality rates by income group with numbers displayed above the bars."""
    average_mortality = calculate_average_mortality(df)

    plt.figure(figsize=(12, 7))
    bars = plt.bar(
        average_mortality.index,
        average_mortality.values,
        color=sns.color_palette("Blues", n_colors=len(average_mortality)),
        edgecolor="black"
    )

    for bar, value in zip(bars, average_mortality.values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f"{value:.2f}",
            ha="center", va="bottom", fontsize=12, fontweight="bold", color="black"
        )

    plt.title("AIDS Mortality Rates by Income Group", fontsize=18, fontweight='bold', color='darkblue')
    plt.ylabel("Mean Mortality Rate (per 1000)", fontsize=14, fontweight='bold')
    plt.xlabel("Income Group", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "aids_mortality_by_income_group_bar_chart.png"))
    plt.close()

def create_line_plot_by_income_group(df):
    """Creates and saves a line plot of AIDS mortality trends over time (2000-2022) by income group."""
    filtered_df = df[df["date"].between(2000, 2022)]
    time_series_by_income = filtered_df.groupby(["date", "wbincome2024"])["estimate"].mean().unstack()

    line_styles = ["-", "--", "-.", ":"]
    color_palette = sns.color_palette("colorblind", n_colors=len(time_series_by_income.columns))

    plt.figure(figsize=(16, 10))
    for (income_group, line_style, color) in zip(time_series_by_income.columns, line_styles, color_palette):
        plt.plot(
            time_series_by_income.index,
            time_series_by_income[income_group],
            label=income_group,
            linestyle=line_style,
            linewidth=2.5,
            marker="o",
            markersize=6,
            color=color
        )

    plt.title("AIDS Mortality Trends Over Time by Income Group (2000-2022)", fontsize=18, fontweight='bold', color='black')
    plt.ylabel("Mean Mortality Rate (per 1000)", fontsize=14, fontweight='bold')
    plt.xlabel("Year", fontsize=14, fontweight='bold')
    plt.xticks(range(2000, 2023, 2), fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title="Income Group", fontsize=12, title_fontsize=14)
    plt.grid(axis="both", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "aids_mortality_by_income_group_line_plot.png"))
    plt.close()

def create_map_plot(df):
    """Creates and saves a corrected world map showing AIDS-related deaths by country for 2022."""
    aggregated_data = df[df["date"] == 2022].groupby("setting")["estimate"].sum().reset_index()
    aggregated_data.rename(columns={"setting": "country", "estimate": "total_deaths"}, inplace=True)

    world = gpd.read_file("data/maps/ne_110m_admin_0_countries.shp")
    merged_world = world.merge(aggregated_data, how="left", left_on="SOVEREIGNT", right_on="country")
    merged_world["total_deaths"] = merged_world["total_deaths"].fillna(0)

    plt.figure(figsize=(15, 10))
    ax = merged_world.plot(
        column="total_deaths",
        cmap="Reds",
        linewidth=0.8,
        edgecolor="0.8",
        legend=True,
        legend_kwds={
            "label": "AIDS-Related Deaths",
            "orientation": "horizontal",
            "shrink": 0.5,
            "pad": 0.02,
        }
    )

    plt.title("Global Distribution of AIDS-Related Deaths (2022)", fontsize=18, fontweight='bold', color='black')
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "global_aids_mortality_map_2022.png"))
    plt.close()

def correlation_analysis(df):
    """Performs correlation analysis."""
    if "income_encoded" not in df.columns:
        print("Column 'income_encoded' not found. Encoding it now.")
        df = encode_income_groups(df)

    clean_df = df.dropna(subset=["income_encoded", "estimate"])
    clean_df = clean_df[~np.isinf(clean_df["income_encoded"])]
    clean_df = clean_df[~np.isinf(clean_df["estimate"])]

    correlation, p_value = stats.pearsonr(clean_df["income_encoded"], clean_df["estimate"])
    print("--- Correlation Analysis ---")
    print(f"Pearson Correlation: {correlation:.3f}")
    print(f"P-value: {p_value:.3e}")

def statistical_analysis_pipeline(df):
    """Performs statistical and descriptive analysis."""
    print("--- Descriptive Statistics ---")
    print(df.groupby("wbincome2024")["estimate"].describe())

    correlation_analysis(df)

# Main execution
if __name__ == "__main__":
    file_path = "data/data.xlsx"  # Update with your actual data file path
    df = read_data(file_path)

    # Encode income groups
    df = encode_income_groups(df)

    # Create and save plots
    create_bar_chart_with_numbers(df)
    create_line_plot_by_income_group(df)
    create_map_plot(df)

    # Perform statistical analysis
    statistical_analysis_pipeline(df)
