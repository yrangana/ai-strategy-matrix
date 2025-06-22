"""
Tests for utility functions of the AI Strategy Matrix Builder.
"""

import unittest
import pandas as pd
import numpy as np


class TestMatrixUtilities(unittest.TestCase):
    """Test cases for matrix utility functions."""

    def setUp(self):
        """Set up test environment before each test."""
        # Sample data for testing
        self.sample_data = [
            {
                "Name": "AI Chatbot",
                "Actionability": "High",
                "Feasibility": "High",
                "Business Value": "Medium",
            },
            {
                "Name": "Predictive Maintenance",
                "Actionability": "Medium",
                "Feasibility": "Low",
                "Business Value": "High",
            },
            {
                "Name": "Document Analysis",
                "Actionability": "Low",
                "Feasibility": "Medium",
                "Business Value": "Low",
            },
        ]
        self.df = pd.DataFrame(self.sample_data)

        # Rating map
        self.rating_map = {"Low": 1, "Medium": 2, "High": 3}

    def test_determine_quadrant(self):
        """Test function to determine which quadrant a use case belongs to."""

        def determine_quadrant(actionability, feasibility):
            """Determine which quadrant a use case belongs to based on ratings."""
            if actionability == "High" and feasibility == "High":
                return "Priority"
            if actionability == "High" and feasibility != "High":
                return "Research"
            if actionability != "High" and feasibility == "High":
                return "Enablement"
            return "Backlog"

        # Test all combinations
        self.assertEqual(determine_quadrant("High", "High"), "Priority")
        self.assertEqual(determine_quadrant("High", "Medium"), "Research")
        self.assertEqual(determine_quadrant("High", "Low"), "Research")
        self.assertEqual(determine_quadrant("Medium", "High"), "Enablement")
        self.assertEqual(determine_quadrant("Low", "High"), "Enablement")
        self.assertEqual(determine_quadrant("Medium", "Medium"), "Backlog")
        self.assertEqual(determine_quadrant("Medium", "Low"), "Backlog")
        self.assertEqual(determine_quadrant("Low", "Medium"), "Backlog")
        self.assertEqual(determine_quadrant("Low", "Low"), "Backlog")

    def test_add_jitter(self):
        """Test adding jitter to data points."""

        def add_jitter(values, jitter_range=0.1):
            """Add random jitter to values to prevent overlap in visualization."""
            return values + np.random.uniform(-jitter_range, jitter_range, size=len(values))

        # Convert ratings to numeric
        actionability_num = self.df["Actionability"].map(self.rating_map).values

        # Add jitter
        jittered = add_jitter(actionability_num)

        # Check that jitter was added (values changed)
        self.assertFalse(np.array_equal(actionability_num, jittered))

        # Check that jitter is within expected range
        self.assertTrue(
            all(
                abs(jittered[i] - actionability_num[i]) <= 0.1
                for i in range(len(actionability_num))
            )
        )

    def test_validate_csv_columns(self):
        """Test validation of CSV columns."""

        def validate_csv_columns(df, required_columns):
            """Validate that DataFrame has all required columns."""
            return all(col in df.columns for col in required_columns)

        # Test with valid DataFrame
        required_columns = ["Name", "Actionability", "Feasibility", "Business Value"]
        self.assertTrue(validate_csv_columns(self.df, required_columns))

        # Test with invalid DataFrame (missing column)
        invalid_df = self.df.drop(columns=["Business Value"])
        self.assertFalse(validate_csv_columns(invalid_df, required_columns))

    def test_validate_rating_values(self):
        """Test validation of rating values."""

        def validate_rating_values(df, rating_columns, valid_ratings):
            """Validate that all ratings in the DataFrame are valid."""
            for col in rating_columns:
                if not all(val in valid_ratings for val in df[col]):
                    return False
            return True

        # Test with valid ratings
        rating_columns = ["Actionability", "Feasibility", "Business Value"]
        valid_ratings = ["Low", "Medium", "High"]
        self.assertTrue(validate_rating_values(self.df, rating_columns, valid_ratings))

        # Test with invalid ratings
        invalid_df = self.df.copy()
        invalid_df.loc[0, "Actionability"] = "Invalid"
        self.assertFalse(validate_rating_values(invalid_df, rating_columns, valid_ratings))


if __name__ == "__main__":
    unittest.main()
