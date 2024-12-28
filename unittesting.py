import unittest
import pandas as pd
import os
import numpy as np
from graphs import (read_data, filter_data, encode_income_groups,
                         calculate_average_mortality, create_bar_chart_with_numbers,
                         create_line_plot_by_income_group, correlation_analysis, statistical_analysis_pipeline)

class TestGraphFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load test data from the Excel file in the 'data' folder
        cls.file_path = os.path.join('data', 'data.xlsx')  # Path to your test data file
        cls.test_data = read_data(cls.file_path)
        cls.filtered_data = filter_data(cls.test_data)

        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
    
    #Check data is read in 
    def test_read_data(self):
        result = read_data(self.file_path)
        self.assertIsInstance(result, pd.DataFrame)
    
    #Checks if income groups are encoded correctly
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

    #Checks if mean mortality is calculated correctly 
    def test_calculate_average_mortality(self):
        result = calculate_average_mortality(self.filtered_data)
        expected = self.filtered_data.groupby("wbincome2024")["estimate"].mean().sort_values()
        pd.testing.assert_series_equal(result, expected)

    #Checks if bar chart created and output file produced
    def test_create_bar_chart_with_numbers(self):
        output_file = os.path.join("output", "aids_mortality_by_income_group_bar_chart.png")
        create_bar_chart_with_numbers(self.filtered_data)
        self.assertTrue(os.path.exists(output_file), "The bar chart should be saved as 'aids_mortality_by_income_group_bar_chart.png'.")

    #The test checks for the file's existence after the plotting operation.
    def test_create_line_plot(self):
        output_file = os.path.join("output", "aids_mortality_by_income_group_line_plot.png")
        create_line_plot_by_income_group(self.filtered_data)
        self.assertTrue(os.path.exists(output_file), "The line plot should be saved as 'aids_mortality_by_income_group_line_plot.png'.")

    def test_correlation_analysis(self):
        encoded_df = encode_income_groups(self.filtered_data)
        correlation_analysis(encoded_df)  

    #  Checks it executes without errors and performs statisctial analyses on the filtered data
    def test_statistical_analysis_pipeline(self):
        statistical_analysis_pipeline(self.filtered_data)  


    #Test performance and correctness on a large dataset
    def test_average_mortality_large_dataset(self):
        large_data = pd.DataFrame({
            "wbincome2024": np.random.choice(["High income", "Low income"], size=1_000_000),
            "estimate": np.random.rand(1_000_000) * 100  
        })

        import time
        start_time = time.time()
        
        result = calculate_average_mortality(large_data)
        
        end_time = time.time()
        
        # Ensure results are computed
        self.assertFalse(result.empty, "Results should not be empty.")
        self.assertLess(end_time - start_time, 1, "Performance test took too long.")    

if __name__ == "__main__":
    unittest.main()

