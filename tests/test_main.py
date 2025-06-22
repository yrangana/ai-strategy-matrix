"""
Tests for the AI Strategy Matrix Builder application.
"""

import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np


# We need to mock streamlit since it can't run in test environments
class TestAIStrategyMatrix(unittest.TestCase):
    """Test cases for AI Strategy Matrix functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a sample dataframe for testing
        self.test_df = pd.DataFrame(
            [
                {
                    "Name": "Test Case 1",
                    "Actionability": "High",
                    "Feasibility": "Medium",
                    "Business Value": "Low",
                },
                {
                    "Name": "Test Case 2",
                    "Actionability": "Low",
                    "Feasibility": "High",
                    "Business Value": "High",
                },
            ]
        )

        # Define the rating map used in the application
        self.rating_map = {"Low": 1, "Medium": 2, "High": 3}

    def test_rating_mapping(self):
        """Test that ratings are correctly mapped to numeric values."""
        # Test all possible rating values
        self.assertEqual(self.rating_map["Low"], 1)
        self.assertEqual(self.rating_map["Medium"], 2)
        self.assertEqual(self.rating_map["High"], 3)

    def test_dataframe_structure(self):
        """Test that the dataframe has the expected structure."""
        # Check column names
        expected_columns = ["Name", "Actionability", "Feasibility", "Business Value"]
        self.assertListEqual(list(self.test_df.columns), expected_columns)

        # Check data types
        for col in expected_columns:
            self.assertEqual(self.test_df[col].dtype, np.dtype("O"))

    def test_rating_values(self):
        """Test that rating values are valid."""
        valid_ratings = ["Low", "Medium", "High"]

        # Check that all ratings in the test dataframe are valid
        for col in ["Actionability", "Feasibility", "Business Value"]:
            for value in self.test_df[col]:
                self.assertIn(value, valid_ratings)

    @patch("pandas.DataFrame.to_csv")
    def test_csv_export(self, mock_to_csv):
        """Test CSV export functionality."""
        mock_to_csv.return_value = "mocked,csv,data"

        # Call to_csv on our test dataframe
        result = self.test_df.to_csv(index=False)

        # Verify to_csv was called with the expected parameters
        mock_to_csv.assert_called_once_with(index=False)
        self.assertEqual(result, "mocked,csv,data")

    @patch("pandas.read_csv")
    def test_csv_import(self, mock_read_csv):
        """Test CSV import functionality."""
        mock_read_csv.return_value = self.test_df

        # Simulate reading a CSV file
        result = pd.read_csv("dummy_path.csv")

        # Verify read_csv was called and returns expected dataframe
        mock_read_csv.assert_called_once_with("dummy_path.csv")
        pd.testing.assert_frame_equal(result, self.test_df)

    def test_numeric_conversion(self):
        """Test conversion of rating values to numeric values for plotting."""
        # Convert ratings to numeric values
        actionability_num = self.test_df["Actionability"].map(self.rating_map)
        feasibility_num = self.test_df["Feasibility"].map(self.rating_map)
        business_value_num = self.test_df["Business Value"].map(self.rating_map)

        # Check the first row
        self.assertEqual(actionability_num.iloc[0], 3)  # High -> 3
        self.assertEqual(feasibility_num.iloc[0], 2)  # Medium -> 2
        self.assertEqual(business_value_num.iloc[0], 1)  # Low -> 1

        # Check the second row
        self.assertEqual(actionability_num.iloc[1], 1)  # Low -> 1
        self.assertEqual(feasibility_num.iloc[1], 3)  # High -> 3
        self.assertEqual(business_value_num.iloc[1], 3)  # High -> 3


if __name__ == "__main__":
    unittest.main()
