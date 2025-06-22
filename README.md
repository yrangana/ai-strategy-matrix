# 🚀 AI Strategy Matrix Builder

A Streamlit application for creating and visualizing AI strategy matrices to prioritize AI use cases based on actionability, feasibility, and business value.

> This project is based on the prioritization framework described in Google Cloud's article ["How to build an effective AI strategy"](https://cloud.google.com/transform/how-to-build-an-effective-ai-strategy), which recommends evaluating AI use cases based on business value, actionability, and feasibility.

## Overview

The AI Strategy Matrix Builder helps organizations make data-driven decisions about which AI initiatives to pursue. By evaluating potential AI use cases across three key dimensions, this tool creates a visual matrix that clearly identifies which projects should be prioritized.

According to Google Cloud's research, organizations with a comprehensive AI strategy see ROI from generative AI much faster. A key part of this strategy is prioritizing the right use cases using a matrix that evaluates initiatives based on:

- **Business Value**: Impact on customer/employee needs, alignment with business objectives
- **Actionability**: Ease of adoption, speed of implementation, usability
- **Feasibility**: Technical fit, data readiness, risk tolerance

This application implements this prioritization framework as an interactive tool.

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
- uv (fast Python package installer)

### Development Setup

1. Clone the repository

```bash
git clone https://github.com/yrangana/ai-strategy-matrix.git
cd ai-strategy-matrix
```

2. Install dependencies

```bash
make setup-dev  # Install all dependencies including development tools
```

Or for production only:

```bash
make setup  # Install only production dependencies
```

### Development Workflow

You can use the Makefile commands directly, as they handle dependencies automatically:

- **Run the application**: `make run`
- **Format code**: `make format` (uses Black)
- **Run tests**: `make test`
- **Run tests with coverage**: `make coverage`
- **Lint code**: `make lint`

Note: All development commands (lint, format, test) will automatically install required dev dependencies if needed.

Alternatively, you can use `uv` directly to run commands in the virtual environment without activation:

```bash
uv run -- streamlit run main.py  # Run the application
uv run -- pytest tests/          # Run tests
uv run -- black *.py tests/*.py  # Format code
uv run -- pylint *.py tests/*.py # Lint code
```

### Manage dependencies:

- **Synchronize dependencies**: `uv sync` (updates dependencies to match pyproject.toml)
- **Add new dependencies**: Update `pyproject.toml` and run `uv sync`

## Usage

1. **Add Use Cases**: Fill out the form with a name and ratings for each dimension
2. **View the Matrix**: See your use cases plotted on the quadrant visualization
3. **Edit Existing Data**: Modify your entries directly in the data table
4. **Export Your Work**: Download your data as a CSV file for future use
5. **Import Previous Work**: Upload a previously saved CSV file

### Screenshots

#### AI Strategy Matrix Visualization
![AI Strategy Matrix](img/AI%20Strategy%20Matrix.png)

#### Data Management Interface
![Add, Import, Export, Delete Use Cases](img/Add,%20Import,%20Export,%20Delete%20Use%20Cases.png)

## Project Structure

```
.
├── main.py               # Main Streamlit application
├── tests/               # Test directory
│   ├── __init__.py      # Makes tests directory a package
│   ├── test_main.py     # Tests for main functionality
│   └── test_utils.py    # Tests for utility functions
├── pyproject.toml       # Project configuration and dependencies
├── requirements.txt     # Pinned dependencies
├── Makefile            # Development workflow commands
└── README.md           # This file
```

## Testing

This project uses pytest for testing. Run the tests with:

```bash
make test
```

Or with coverage information:

```bash
make coverage
```

## Example Use Cases

- Implementing chatbots for customer service
- Developing predictive maintenance for manufacturing equipment
- Creating an AI-powered recommendation engine for products
- Building a computer vision system for quality control
