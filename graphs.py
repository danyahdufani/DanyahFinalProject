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

def calculate_average_mortality(df):
    """Calculates the average mortality rate by income group."""
    filtered_df = filter_data(df)
    return filtered_df.groupby("wbincome2024")["estimate"].mean().sort_values()

def create_bar_chart_with_numbers(df):
    """
    Creates and saves a bar chart of AIDS mortality rates by income group with numbers displayed above the bars.
    """
    # Calculate average mortality for each income group
    average_mortality = calculate_average_mortality(df)
    
    # Create the bar chart
    plt.figure(figsize=(12, 7))
    bars = plt.bar(
        average_mortality.index, 
        average_mortality.values, 
        color=sns.color_palette("Blues", n_colors=len(average_mortality)), 
        edgecolor="black"
    )
    
    # Add numbers above the bars
    for bar, value in zip(bars, average_mortality.values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # X position (center of the bar)
            bar.get_height() + 0.1,            # Y position (just above the bar)
            f"{value:.2f}",                   # Format to 2 decimal places
            ha="center", va="bottom",         # Center-align the text
            fontsize=12, fontweight="bold", color="black"
        )
    
    # Add titles and labels
    plt.title("AIDS Mortality Rates by Income Group", fontsize=18, fontweight='bold', color='darkblue')
    plt.ylabel("Mean Mortality Rate (per 1000)", fontsize=14, fontweight='bold')
    plt.xlabel("Income Group", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Final adjustments and save
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "aids_mortality_by_income_group_bar_chart.png"))
    plt.close()

def calculate_time_series(df):
    """Calculates the time series of mean mortality rates over time."""
    filtered_df = filter_data(df)
    return filtered_df.groupby("date")["estimate"].mean()
def create_line_plot(df):
    """
    Fixes and saves a line plot of global AIDS mortality trends from 2000 to 2022.
    """
    # Filter data for years between 2000 and 2022
    filtered_df = df[df["date"].between(2000, 2022)]
    
    # Group data by year and calculate mean mortality rates
    time_series = filtered_df.groupby("date")["estimate"].mean()
    
    plt.figure(figsize=(12, 7))
    ax = time_series.plot(
        kind="line", 
        marker="o", 
        color="orange", 
        linewidth=2.5, 
        markersize=6,
        label="Mean Mortality Rate"
    )
    
    # Add titles and labels
    ax.set_title("Global AIDS Mortality Trends Over Time (2000-2022)", fontsize=18, fontweight='bold', color='black')
    ax.set_ylabel("Mean Mortality Rate (per 1000)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Year", fontsize=14, fontweight='bold')
    ax.set_xticks(range(2000, 2023, 2))  # Show ticks every 2 years
    ax.set_xticklabels(range(2000, 2023, 2), rotation=45, fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.legend(fontsize=12)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "global_aids_mortality_trends_2000_2022.png"))
    plt.close()

def create_map_plot(df):
    """
    Creates and saves a corrected world map showing AIDS-related deaths by country for 2022.
    """
    # Aggregate data for 2022
    aggregated_data = df[df["date"] == 2022].groupby("setting")["estimate"].sum().reset_index()
    aggregated_data.rename(columns={"setting": "country", "estimate": "total_deaths"}, inplace=True)
    
    # Load the shapefile
    world = gpd.read_file("data/maps/ne_110m_admin_0_countries.shp")
    
    # Merge aggregated data with shapefile data
    merged_world = world.merge(aggregated_data, how="left", left_on="SOVEREIGNT", right_on="country")
    
    # Handle missing data (countries without mortality data)
    merged_world["total_deaths"] = merged_world["total_deaths"].fillna(0)
    
    # Plot the map
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
            "shrink": 0.5,  # Adjust size of the color bar
            "pad": 0.02,    # Add space between the map and the color bar
        }
    )
    
    plt.title("Global Distribution of AIDS-Related Deaths (2022)", fontsize=18, fontweight='bold', color='black')
    plt.axis("off")
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(os.path.join(output_folder, "global_aids_mortality_map_2022.png"))
    plt.close()

# Main execution
if __name__ == "__main__":
    file_path = "data/data.xlsx"  # Update with your actual data file path
    df = read_data(file_path)
    
    # Create and save plots
    create_bar_chart_with_numbers(df)  # New bar chart with numbers above bars
    create_line_plot(df)  # Corrected time-series plot
    create_map_plot(df)  # World map plot
