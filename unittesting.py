import unittest
import pandas as pd
import os
import numpy as np
from DanyahFinalProject.data.graphs import (read_data, filter_data, encode_income_groups,
                         calculate_average_mortality, create_bar_chart_with_numbers,
                         create_line_plot_by_income_group, create_map_plot,
                         correlation_analysis, statistical_analysis_pipeline)

class TestGraphFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load test data from the Excel file in the 'data' folder
        cls.file_path = os.path.join('data', 'data.xlsx')  # Path to your test data file
        cls.test_data = read_data(cls.file_path)
        cls.filtered_data = filter_data(cls.test_data)

        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)

    def test_read_data(self):
        result = read_data(self.file_path)
        self.assertIsInstance(result, pd.DataFrame)

    def filter_data(df):
        """Cleans and filters the data to remove rows with missing 'estimate' or 'wbincome2024'."""
        return df.dropna(subset=["estimate", "wbincome2024"]).copy() 

    def test_encode_income_groups(self):
        result = encode_income_groups(self.filtered_data)
        print(result)  # Print the DataFrame to check the encoding

        # Ensure the income_encoded column exists
        self.assertIn("income_encoded", result.columns)

        # Look for "High income" and check its encoding
        high_income_rows = result[result["wbincome2024"] == "High income"]
        
        if not high_income_rows.empty:
            self.assertEqual(high_income_rows["income_encoded"].iloc[0], 4)  # Ensure 'High income' is encoded as 4
        else:
            self.fail("No 'High income' group found in the DataFrame.")



    def test_calculate_average_mortality(self):
        result = calculate_average_mortality(self.filtered_data)
        expected = self.filtered_data.groupby("wbincome2024")["estimate"].mean().sort_values()
        pd.testing.assert_series_equal(result, expected)

    def test_create_bar_chart_with_numbers(self):
        output_file = os.path.join("output", "aids_mortality_by_income_group_bar_chart.png")
        create_bar_chart_with_numbers(self.filtered_data)
        self.assertTrue(os.path.exists(output_file), "The bar chart should be saved as 'aids_mortality_by_income_group_bar_chart.png'.")

    def test_create_line_plot(self):
        output_file = os.path.join("output", "aids_mortality_by_income_group_line_plot.png")
        create_line_plot_by_income_group(self.filtered_data)
        self.assertTrue(os.path.exists(output_file), "The line plot should be saved as 'aids_mortality_by_income_group_line_plot.png'.")

    def test_create_map_plot(self):
        output_file = os.path.join("output", "global_aids_mortality_map_2022.png")
        create_map_plot(self.filtered_data)
        self.assertTrue(os.path.exists(output_file), "The map plot should be saved as 'global_aids_mortality_map_2022.png'.")

    def test_correlation_analysis(self):
        encoded_df = encode_income_groups(self.filtered_data)
        correlation_analysis(encoded_df)  # Output of correlation will be printed in the console

    def test_statistical_analysis_pipeline(self):
        statistical_analysis_pipeline(self.filtered_data)  # Output of stats will be printed in the console

if __name__ == "__main__":
    unittest.main()