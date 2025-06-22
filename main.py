# AI Strategy Matrix Builder
# Created by Yash
# MIT License

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="AI Strategy Matrix", layout="wide")
st.title("🚀 AI Strategy Matrix Builder")

# Mapping
rating_map = {"Low": 1, "Medium": 2, "High": 3}
reverse_rating_map = {1: "Low", 2: "Medium", 3: "High"}

# Initialize session state
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(
        columns=["Name", "Actionability", "Feasibility", "Business Value"]
    )


# Add new use case
# Initialize error state if not exists
if "form_error" not in st.session_state:
    st.session_state.form_error = ""

with st.form("new_use_case", clear_on_submit=True):
    st.subheader("Add New Use Case")

    # Display error if exists
    if st.session_state.form_error:
        st.error(st.session_state.form_error)
        st.session_state.form_error = ""

    name = st.text_input("Use Case Name", help="Required field")

    actionability = st.selectbox(
        "Actionability — How ready is your business/team to adopt this AI solution?",
        ["High", "Medium", "Low"],
    )

    feasibility = st.selectbox(
        "Feasibility — How technically feasible is this solution today?",
        ["High", "Medium", "Low"],
    )

    business_value = st.selectbox(
        "Business Value — How much potential business impact does this solution offer?",
        ["High", "Medium", "Low"],
    )

    submitted = st.form_submit_button("Add")

    if submitted:
        if not name.strip():
            st.session_state.form_error = "⚠️ Use Case Name is required"
            st.rerun()
        else:
            new_row = {
                "Name": name,
                "Actionability": actionability,
                "Feasibility": feasibility,
                "Business Value": business_value,
            }
            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([new_row])], ignore_index=True
            )
            st.success(f"Added '{name}'")

st.text("📤 Import Saved Data")
# st.text("You can import a CSV file containing the use cases and their ratings.")
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    try:
        imported_df = pd.read_csv(uploaded_file)
        # Validate columns
        required_columns = ["Name", "Actionability", "Feasibility", "Business Value"]
        if all(col in imported_df.columns for col in required_columns):
            st.session_state.df = imported_df
            st.success("Data imported successfully.")
        else:
            st.error(f"CSV must contain columns: {required_columns}")
    except pd.errors.ParserError as e:
        st.error(f"CSV parsing error: {e}")
    except (IOError, OSError) as e:
        st.error(f"File I/O error: {e}")
    except ValueError as e:
        st.error(f"Value error: {e}")
    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Unexpected error reading file: {e}")
        import traceback

        st.error(f"Details: {traceback.format_exc()}")

# Show editable table
if not st.session_state.df.empty:
    st.subheader("📊 Current Use Cases (Editable)")
    edited_df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        use_container_width=True,
        disabled=("Actionability", "Feasibility", "Business Value"),
    )
    st.session_state.df = edited_df

# Export button
if not st.session_state.df.empty:
    csv = st.session_state.df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Export as CSV",
        data=csv,
        file_name="ai_strategy_matrix.csv",
        mime="text/csv",
    )


# Show matrix plot
if not st.session_state.df.empty:
    st.subheader("🎯 AI Strategy Matrix")

    # Convert to numeric values for plotting
    plot_df = st.session_state.df.copy()
    plot_df["Actionability_num"] = plot_df["Actionability"].map(rating_map)
    plot_df["Feasibility_num"] = plot_df["Feasibility"].map(rating_map)
    plot_df["BusinessValue_num"] = plot_df["Business Value"].map(rating_map)

    # Add jitter
    plot_df["Feasibility_jitter"] = plot_df["Feasibility_num"] + np.random.uniform(
        -0.1, 0.1, size=len(plot_df)
    )
    plot_df["Actionability_jitter"] = plot_df["Actionability_num"] + np.random.uniform(
        -0.1, 0.1, size=len(plot_df)
    )

    # Create custom hover text
    plot_df["hover_text"] = plot_df.apply(
        lambda row: f"<b>{row['Name']}</b><br>"
        + f"Feasibility: {row['Feasibility']}<br>"
        + f"Actionability: {row['Actionability']}<br>"
        + f"Business Value: {row['Business Value']}",
        axis=1,
    )

    fig = px.scatter(
        plot_df,
        x="Feasibility_jitter",
        y="Actionability_jitter",
        size="BusinessValue_num",
        size_max=60,
        text="Name",
        color="BusinessValue_num",  # Use numeric values for continuous color scale
        hover_name="Name",
        custom_data=["Feasibility", "Actionability", "Business Value"],
        color_continuous_scale=["#AEDFF7", "#007BFF"],
    )

    # Use the custom hover template
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>"
        + "Feasibility: %{customdata[0]}<br>"
        + "Actionability: %{customdata[1]}<br>"
        + "Business Value: %{customdata[2]}<br>"
    )

    # Improve text display with wrapping and better visibility
    # Don't set textposition here as we'll handle it individually for each point

    # Add text wrapping for better readability and prevent overlap
    # Create a list of wrapped text labels and assign different positions to prevent overlap
    wrapped_labels = []
    text_positions = []

    # First, wrap the text labels
    for name in plot_df["Name"]:
        # Split long names into multiple lines (max 15 chars per line)
        if len(name) > 15:
            words = name.split()
            lines = []
            current_line = ""

            for word in words:
                if len(current_line + " " + word) > 15 and current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word

            if current_line:  # Add the last line
                lines.append(current_line)

            wrapped_labels.append("<br>".join(lines))
        else:
            wrapped_labels.append(name)

    # Create a grid-based positioning system to prevent overlap
    # Define possible text positions
    positions = [
        "top center",
        "top right",
        "top left",
        "bottom center",
        "bottom right",
        "bottom left",
        "middle right",
        "middle left",
    ]

    # Group points that are close to each other
    # This is a simplified approach - we'll use a grid-based system
    grid_size = 0.5  # Size of each grid cell
    grid = {}  # Dictionary to store points in each grid cell

    for i, row in plot_df.iterrows():
        # Calculate grid position
        grid_x = int(row["Feasibility_jitter"] / grid_size)
        grid_y = int(row["Actionability_jitter"] / grid_size)
        grid_key = (grid_x, grid_y)

        # Add point to grid
        if grid_key not in grid:
            grid[grid_key] = []
        grid[grid_key].append(i)

    # Assign positions to avoid overlap
    for grid_key, indices in grid.items():
        if len(indices) == 1:
            # If only one point in this grid cell, use default position
            text_positions.append("top center")
        else:
            # If multiple points in this grid cell, distribute positions
            for idx, point_idx in enumerate(indices):
                position_idx = idx % len(positions)
                if point_idx < len(text_positions):
                    text_positions[point_idx] = positions[position_idx]
                else:
                    text_positions.append(positions[position_idx])

    # Ensure we have a position for each point
    while len(text_positions) < len(plot_df):
        text_positions.append("top center")

    # Update the text with wrapped labels and positions
    fig.update_traces(
        text=wrapped_labels,
        textposition=text_positions,
        textfont=dict(size=11, color="black", family="Arial, sans-serif", weight="bold"),
    )

    # Add quadrant shapes with different colors
    # Q1: High Feasibility, High Actionability (Top Right) - Priority
    fig.add_shape(
        type="rect",
        x0=2,
        x1=3.5,
        y0=2,
        y1=3.5,
        line=dict(color="green", width=2),
        fillcolor="green",
        opacity=0.1,
    )

    # Q2: Low Feasibility, High Actionability (Top Left) - Research
    fig.add_shape(
        type="rect",
        x0=0.5,
        x1=2,
        y0=2,
        y1=3.5,
        line=dict(color="orange", width=2),
        fillcolor="orange",
        opacity=0.1,
    )

    # Q3: Low Feasibility, Low Actionability (Bottom Left) - Backlog
    fig.add_shape(
        type="rect",
        x0=0.5,
        x1=2,
        y0=0.5,
        y1=2,
        line=dict(color="red", width=2),
        fillcolor="red",
        opacity=0.1,
    )

    # Q4: High Feasibility, Low Actionability (Bottom Right) - Enablement
    fig.add_shape(
        type="rect",
        x0=2,
        x1=3.5,
        y0=0.5,
        y1=2,
        line=dict(color="blue", width=2),
        fillcolor="blue",
        opacity=0.1,
    )

    fig.update_layout(
        xaxis=dict(title="Feasibility", tickvals=[1, 2, 3], ticktext=["Low", "Medium", "High"]),
        yaxis=dict(
            title="Actionability",
            tickvals=[1, 2, 3],
            ticktext=["Low", "Medium", "High"],
        ),
        coloraxis_colorbar=dict(
            title="Business Value",
            tickvals=[1, 2, 3],
            ticktext=["Low", "Medium", "High"],
        ),
        height=900,  # Increase the height for better visualization
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            bordercolor="#DFE2E6",
            namelength=-1,  # Show the full label name
        ),
        # Add some margin to ensure text labels have room
        margin=dict(l=50, r=50, t=50, b=50),
    )

    st.plotly_chart(fig, use_container_width=True)

# Reset button
if st.button("🔄 Reset All Data"):
    st.session_state.df = pd.DataFrame(
        columns=["Name", "Actionability", "Feasibility", "Business Value"]
    )
    st.rerun()

# Add footer with attribution
st.markdown("---")
st.caption("© 2025 Created by [Yash](https://github.com/yrangana) | MIT License")
