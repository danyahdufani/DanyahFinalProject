import unittest
import pytest
import pandas as pd

def test_read_file():
    try:
        df = pd.read_excel("data.xlsx")
        assert not df.empty, "The file should not be empty."
    except Exception as e:
        pytest.fail(f"Reading the file failed: {e}")

def test_data_filtering():
    df = pd.read_excel("data.xlsx")
    filtered_df = df.dropna(subset=["estimate", "wbincome2024"])
    assert not filtered_df.empty, "Filtered DataFrame should not be empty."
    assert "estimate" in filtered_df.columns and "wbincome2024" in filtered_df.columns, \
        "Filtered DataFrame must contain 'estimate' and 'wbincome2024'."


def test_data_filtering():
    df = pd.read_excel("data.xlsx")
    filtered_df = df.dropna(subset=["estimate", "wbincome2024"])
    assert not filtered_df.empty, "Filtered DataFrame should not be empty."
    assert "estimate" in filtered_df.columns and "wbincome2024" in filtered_df.columns, \
        "Filtered DataFrame must contain 'estimate' and 'wbincome2024'."


def test_create_bar_plot():
    df = pd.read_excel("data.xlsx")
    filtered_df = df.dropna(subset=["estimate", "wbincome2024"])
    average_mortality = filtered_df.groupby("wbincome2024")["estimate"].mean()
    
    assert not average_mortality.empty, "Average mortality data should not be empty."
    assert average_mortality.min() >= 0, "Mortality rates should be non-negative."

def test_create_time_series_plot():
    df = pd.read_excel("data.xlsx")
    filtered_df = df.dropna(subset=["estimate"])
    time_series = filtered_df.groupby("date")["estimate"].mean()
    
    assert not time_series.empty, "Time-series data should not be empty."
    assert time_series.index.is_monotonic_increasing, "Time-series data should be sorted by year."


if __name__ == '__main__':
    unittest.main()
