import pandas as pd
import matplotlib.pyplot as plt

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

def create_bar_plot(df, output_file):
    """Creates and saves a bar plot of average mortality by income group."""
    average_mortality = calculate_average_mortality(df)
    plt.figure(figsize=(10, 6))
    average_mortality.plot(kind="bar", color="skyblue")
    plt.title("Average AIDS Mortality by Income Group", fontsize=16)
    plt.ylabel("AIDS Mortality Rate (per 1000)", fontsize=12)
    plt.xlabel("Income Group", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def calculate_time_series(df):
    """Calculates the time series of mean mortality rates over time."""
    filtered_df = filter_data(df)
    return filtered_df.groupby("date")["estimate"].mean()

def create_time_series_plot(df, output_file):
    """Creates and saves a time series plot of global AIDS mortality trends."""
    time_series = calculate_time_series(df)
    plt.figure(figsize=(12, 6))
    time_series.plot(kind="line", marker="o", color="orange")
    plt.title("Global AIDS Mortality Trends Over Time", fontsize=16)
    plt.ylabel("Mean Mortality Rate (per 1000)", fontsize=12)
    plt.xlabel("Year", fontsize=12)
    plt.grid(axis="both", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
