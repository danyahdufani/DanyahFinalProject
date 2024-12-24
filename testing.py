import unittest
import pandas as pd
import matplotlib.pyplot as plt
import os
from graphs import read_data, filter_data, calculate_average_mortality, create_bar_plot, calculate_time_series, create_time_series_plot

class TestGraphFunctions(unittest.TestCase):

    def setUp(self):
        # For the sake of testing, you can create a small test Excel file or assume that it's already there.
        self.file_path = 'data.xlsx'

        # Sample data (you can use real data in your tests)
        data = {
            'estimate': [1, 2, 3, 4],
            'wbincome2024': [1000, 2000, 3000, 4000],
            'date': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01']
        }
        df = pd.DataFrame(data)
        df.to_excel(self.file_path, index=False)

    def test_read_data(self):
        #Test that data is read correctly from the file.
        df = read_data(self.file_path)
        self.assertFalse(df.empty, "The data should not be empty.")
        self.assertIn("estimate", df.columns)
        self.assertIn("wbincome2024", df.columns)
        self.assertIn("date", df.columns)

    def test_filter_data(self):
        #Test the filtering function to remove rows with missing values
        df = pd.read_excel(self.file_path)
        filtered_df = filter_data(df)
        self.assertFalse(filtered_df.empty, "Filtered DataFrame should not be empty.")
        self.assertIn("estimate", filtered_df.columns)
        self.assertIn("wbincome2024", filtered_df.columns)

    def test_calculate_average_mortality(self):
        #Test the calculation of average mortality by income group
        df = pd.read_excel(self.file_path)
        average_mortality = calculate_average_mortality(df)
        self.assertEqual(len(average_mortality), 4, "There should be 4 unique income groups.")
        self.assertTrue(average_mortality.is_monotonic_increasing, "Average mortality should be sorted by income.")

    def test_create_bar_plot(self):
        #Test the bar plot creation by checking if the plot file is saved
        output_file = "test_output.png"
        df = pd.read_excel(self.file_path)
        create_bar_plot(df, output_file)

        # Check if the file was created
        self.assertTrue(os.path.exists(output_file), "The bar plot should be saved as 'test_output.png'.")

        # Clean up the created plot file
        os.remove(output_file)

    def test_calculate_time_series(self):
        #Test the calculation of the time series
        df = pd.read_excel(self.file_path)
        time_series = calculate_time_series(df)
        self.assertEqual(len(time_series), 4, "There should be 4 time points.")
        self.assertTrue(time_series.index.is_monotonic_increasing, "Time series should be sorted by date.")

    def test_create_time_series_plot(self):
        #Test the time series plot creation by checking if the plot file is saved
        output_file = "time_series_output.png"
        df = pd.read_excel(self.file_path)
        create_time_series_plot(df, output_file)

        # Check if the file was created
        self.assertTrue(os.path.exists(output_file), "The time series plot should be saved as 'time_series_output.png'.")

        # Clean up the created plot file
        os.remove(output_file)

    def tearDown(self):
        """Clean up any files that were created during testing."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

if __name__ == '__main__':
    unittest.main()
