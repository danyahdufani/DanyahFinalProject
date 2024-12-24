import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for aesthetic improvement
sns.set(style="whitegrid", palette="muted")

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
    """
    Creates and saves a bar plot of average mortality by income group.
    
    Args:
    - df: pandas DataFrame containing the 'estimate' and 'wbincome2024' columns.
    - output_file: Path where the plot will be saved.
    """
    # Calculate average mortality
    average_mortality = calculate_average_mortality(df)

    # Create the bar plot with improved aesthetics
    plt.figure(figsize=(12, 7))
    ax = average_mortality.plot(kind="bar", color=sns.color_palette("Blues", n_colors=len(average_mortality)))

    # Enhance chart design
    ax.set_title("Average AIDS Mortality by Income Group", fontsize=18, fontweight='bold', color='darkblue')
    ax.set_ylabel("AIDS Mortality Rate (per 1000)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Income Group", fontsize=14, fontweight='bold')
    ax.set_xticklabels(average_mortality.index, rotation=45, ha="right", fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Tight layout to avoid overlap
    plt.tight_layout()

    # Save the plot to the specified file
    plt.savefig(output_file)
    plt.close()

def calculate_time_series(df):
    """Calculates the time series of mean mortality rates over time."""
    filtered_df = filter_data(df)
    return filtered_df.groupby("date")["estimate"].mean()

def create_time_series_plot(df, output_file):
    """
    Creates and saves a time series plot of global AIDS mortality trends.
    
    Args:
    - df: pandas DataFrame containing 'estimate' and 'date' columns.
    - output_file: Path where the plot will be saved.
    """
    # Calculate time series data
    time_series = calculate_time_series(df)

    # Create the time series plot with improved aesthetics
    plt.figure(figsize=(12, 7))
    ax = time_series.plot(kind="line", marker="o", color=sns.color_palette("Set2")[1], linewidth=3, markersize=8)

    # Enhance chart design
    ax.set_title("Global AIDS Mortality Trends Over Time", fontsize=18, fontweight='bold', color='darkred')
    ax.set_ylabel("Mean Mortality Rate (per 1000)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Year", fontsize=14, fontweight='bold')
    ax.set_xticklabels(time_series.index, rotation=45, ha="right", fontsize=12)
    ax.grid(True, axis="both", linestyle="--", alpha=0.6)

    # Add annotations on the plot points
    for i, txt in enumerate(time_series):
        ax.annotate(f'{txt:.2f}', (time_series.index[i], txt), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=10)

    # Tight layout to avoid overlap
    plt.tight_layout()

    # Save the plot to the specified file
    plt.savefig(output_file)
    plt.close()
