import unittest
import pandas as pd
import os
from graphs import (
    read_data, filter_data, calculate_average_mortality, 
    create_bar_chart_with_numbers, calculate_time_series, create_line_plot, 
    create_map_plot
)

class TestGraphFunctions(unittest.TestCase):

    def setUp(self):
        """Setup test environment with existing data."""
        self.file_path = 'data/data.xlsx'  # Updated to the correct file path
        self.output_dir = 'test_outputs'
        os.makedirs(self.output_dir, exist_ok=True)

    def test_read_data(self):
        """Test if data is read correctly from the Excel file."""
        df = read_data(self.file_path)
        self.assertFalse(df.empty, "The data should not be empty.")
        self.assertIn("estimate", df.columns, "Data should have 'estimate' column.")
        self.assertIn("wbincome2024", df.columns, "Data should have 'wbincome2024' column.")
        self.assertIn("date", df.columns, "Data should have 'date' column.")

    def test_filter_data(self):
        """Test the filtering function to remove rows with missing values."""
        df = pd.read_excel(self.file_path)
        filtered_df = filter_data(df)
        self.assertFalse(filtered_df.empty, "Filtered DataFrame should not be empty.")
        self.assertIn("estimate", filtered_df.columns, "Filtered data should have 'estimate' column.")
        self.assertIn("wbincome2024", filtered_df.columns, "Filtered data should have 'wbincome2024' column.")
        
        # Check for rows with missing values being dropped
        self.assertTrue(filtered_df.isnull().sum().sum() == 0, "Filtered data should have no missing values.")

    def test_calculate_average_mortality(self):
        """Test the calculation of average mortality by income group."""
        df = pd.read_excel(self.file_path)
        average_mortality = calculate_average_mortality(df)
        self.assertGreater(len(average_mortality), 0, "There should be calculated average mortality.")
        self.assertTrue(average_mortality.is_monotonic_increasing, "Average mortality should be sorted by income.")

    def test_create_bar_chart_with_numbers(self):
        """Test if the bar chart creation works and the plot file is saved."""
        output_file = os.path.join(self.output_dir, "test_bar_chart.png")
        df = pd.read_excel(self.file_path)
        create_bar_chart_with_numbers(df)

        # Check if the plot file was created
        self.assertTrue(os.path.exists(output_file), "The bar chart should be saved as 'test_bar_chart.png'.")
        
        # Clean up the plot file
        os.remove(output_file)

    def test_calculate_time_series(self):
        """Test the time series calculation function."""
        df = pd.read_excel(self.file_path)
        time_series = calculate_time_series(df)
        self.assertGreater(len(time_series), 0, "There should be calculated time series.")
        self.assertTrue(time_series.index.is_monotonic_increasing, "Time series should be sorted by date.")

    def test_create_line_plot(self):
        """Test if the time-series line plot is created and saved correctly."""
        output_file = os.path.join(self.output_dir, "test_line_plot.png")
        df = pd.read_excel(self.file_path)
        create_line_plot(df)

        # Check if the plot file was created
        self.assertTrue(os.path.exists(output_file), "The line plot should be saved as 'test_line_plot.png'.")
        
        # Clean up the plot file
        os.remove(output_file)

    def test_create_map_plot(self):
        """Test if map plot is created and saved successfully for 2022 data."""
        output_file = os.path.join(self.output_dir, "test_map_plot.png")
        df = pd.read_excel(self.file_path)
        create_map_plot(df)

        # Check if the plot file was created
        self.assertTrue(os.path.exists(output_file), "The map plot should be saved as 'test_map_plot.png'.")
        
        # Clean up the plot file
        os.remove(output_file)

    def test_invalid_data_format(self):
        """Test that invalid data format raises errors (e.g., missing 'date' or 'estimate' column)."""
        # Remove the 'date' column and save it as a temporary file
        df = pd.read_excel(self.file_path)
        df_invalid = df.drop(columns=['date'])
        df_invalid.to_excel('data_invalid.xlsx', index=False)

        # Test that creating a plot will raise a KeyError due to missing 'date' column
        with self.assertRaises(KeyError):
            create_line_plot(df_invalid)
        
        # Clean up the invalid file
        os.remove('data_invalid.xlsx')

    def tearDown(self):
        """Clean up any files created during testing."""
        # Clean up test plot files
        for file in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.output_dir)


if __name__ == '__main__':
    unittest.main()
