# 🚀 AI Strategy Matrix Builder

A Streamlit application for creating and visualizing AI strategy matrices to prioritize AI use cases based on actionability, feasibility, and business value.

## Overview

The AI Strategy Matrix Builder helps organizations make data-driven decisions about which AI initiatives to pursue. By evaluating potential AI use cases across three key dimensions, this tool creates a visual matrix that clearly identifies which projects should be prioritized.

## Key Features

- **Interactive Input Form**: Easily add new AI use cases with ratings for actionability, feasibility, and business value
- **Editable Data Table**: View and modify your use cases directly in the application
- **Quadrant Visualization**: See your AI initiatives plotted on a strategic matrix with clear quadrant labels:
  - **PRIORITY** (High Feasibility, High Actionability): Focus here first
  - **RESEARCH** (Low Feasibility, High Actionability): Investigate further
  - **BACKLOG** (Low Feasibility, Low Actionability): Consider for future
  - **ENABLEMENT** (High Feasibility, Low Actionability): Build capabilities
- **CSV Import/Export**: Save and load your data for future sessions or sharing

## Rating Dimensions

- **Actionability**: How ready is your business/team to adopt this AI solution?
- **Feasibility**: How technically feasible is this solution today?
- **Business Value**: How much potential business impact does this solution offer?

Each dimension is rated as High, Medium, or Low.

## Getting Started

### Prerequisites

- Python 3.12+

## Usage

1. **Add Use Cases**: Fill out the form with a name and ratings for each dimension
2. **View the Matrix**: See your use cases plotted on the quadrant visualization
3. **Edit Existing Data**: Modify your entries directly in the data table
4. **Export Your Work**: Download your data as a CSV file for future use
5. **Import Previous Work**: Upload a previously saved CSV file

## Example Use Cases

- Implementing chatbots for customer service
- Developing predictive maintenance for manufacturing equipment
- Creating an AI-powered recommendation engine for products
- Building a computer vision system for quality control
