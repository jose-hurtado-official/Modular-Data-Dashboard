import pandas as pd
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px


def bar_chart(data_frame: pd.DataFrame, suffix: int):

    column_x = st.selectbox(
        "Choose the column you want to display in the x-axis",
        list(data_frame.columns),
        key=f"bar_x_{suffix}",
    )
    column_y = st.selectbox(
        "Choose the column you want to display in the y-axis",
        list(data_frame.columns),
        key=f"bar_y_{suffix}",
    )

    horizontal = (
        st.radio(
            "Do you want to display the information horizontally?",
            ["Yes", "No"],
            index=1,
            key=f"horizontal_bars_{suffix}",
        )
        == "Yes"
    )

    return st.bar_chart(data_frame, x=column_x, y=column_y, horizontal=horizontal)


def area_chart(data_frame: pd.DataFrame, suffix: int):

    if "area_chart" not in st.session_state:
        st.session_state.area_chart = 0

    left, right = st.columns(2)

    if left.button("➕ Add area", key=f"add_areachart_button_{suffix}"):
        st.session_state.area_chart += 1

    if right.button("➖ Remove last area", key=f"rem_areachart_button_{suffix}"):
        if st.session_state.area_chart > 0:
            st.session_state.area_chart -= 1
        else:
            st.warning("There are no more areas to remove")

    areas = []

    for index in range(st.session_state.area_chart):
        if index == 0:
            col_choices = list(data_frame.columns)
        else:
            first_area = areas[0]
            dtype_fc = data_frame[first_area].dtype
            col_choices = [
                col for col, dtype in data_frame.dtypes.items() if dtype == dtype_fc
            ]

        column = st.selectbox(
            "Choose the column you want to display",
            col_choices,
            key=f"areachart_colum_{index}",
        )
        areas.append(column)

    if not areas:
        st.info("Add at least one column to see the area chart")
        return

    return st.area_chart(
        data_frame[areas],
    )


def line_chart(data_frame: pd.DataFrame, suffix: int):

    if "line_chart" not in st.session_state:
        st.session_state.line_chart = 0

    left, right = st.columns(2)

    if left.button("➕ Add line", key=f"add_linechart_button_{suffix}"):
        st.session_state.line_chart += 1

    if right.button("➖ Remove last line", key=f"rem_linechart_button_{suffix}"):
        if st.session_state.line_chart > 0:
            st.session_state.line_chart -= 1
        else:
            st.warning("There are no more lines to remove")

    lines = []

    for index in range(st.session_state.line_chart):
        if index == 0:
            col_choices = list(data_frame.columns)
        else:
            first_column = lines[0]
            dtype_fc = data_frame[first_column].dtype
            col_choices = [
                col for col, dtype in data_frame.dtypes.items() if dtype == dtype_fc
            ]

        column = st.selectbox(
            "Choose the column you want to display",
            col_choices,
            key=f"linechart_colum_{index}",
        )
        lines.append(column)

    if not lines:
        st.info("Add at least one column to see the line chart")
        return

    return st.line_chart(
        data_frame[lines],
    )


def scatter_chart(data_frame: pd.DataFrame, suffix: int):

    if "scatter_chart" not in st.session_state:
        st.session_state.scatter_chart = 0

    left, right = st.columns(2)

    if left.button("➕ Add scatter", key=f"add_scatterchart_button_{suffix}"):
        st.session_state.scatter_chart += 1

    if right.button("➖ Remove last scatter", key=f"rem_scatterchart_button_{suffix}"):
        if st.session_state.scatter_chart > 0:
            st.session_state.scatter_chart -= 1
        else:
            st.warning("There are no more scatters to remove")

    scatter = []

    for index in range(st.session_state.scatter_chart):
        if index == 0:
            col_choices = list(data_frame.columns)
        else:
            first_column = scatter[0]
            dtype_fc = data_frame[first_column].dtype
            col_choices = [
                col for col, dtype in data_frame.dtypes.items() if dtype == dtype_fc
            ]

        column = st.selectbox(
            "Choose the column you want to display",
            col_choices,
            key=f"scatterchart_colum_{index}",
        )
        scatter.append(column)

    if not scatter:
        st.info("Add at least one column to see the scatter chart")
        return

    return st.scatter_chart(
        data_frame[scatter],
        size=65,
    )


def histogram_chart(data_frame: pd.DataFrame, suffix: int):
    """
    Dynamic histogram or frequency plot for selected DataFrame columns.
    Supports numeric, boolean, datetime, and categorical (object) types.

    Parameters:
    - data_frame: pandas DataFrame to visualize
    - suffix: unique suffix for Streamlit widget keys
    """
    # Initialize counter for number of columns to include
    key_count = f"histogram_count_{suffix}"
    if key_count not in st.session_state:
        st.session_state[key_count] = 1

    # Controls to add/remove columns
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add column", key=f"add_hist_{suffix}"):
            st.session_state[key_count] += 1
    with col2:
        if st.button("➖ Remove column", key=f"rem_hist_{suffix}"):
            if st.session_state[key_count] > 1:
                st.session_state[key_count] -= 1
            else:
                st.warning("At least one column must remain.")

    # Select columns
    selections = []
    for i in range(st.session_state[key_count]):
        choices = list(data_frame.columns)
        col = st.selectbox(
            f"{i+1}. Choose column to include in histogram:",
            choices,
            key=f"hist_col_{suffix}_{i}",
        )
        selections.append(col)

    if not selections:
        st.info("Add at least one column to see the histogram.")
        return

    # Prepare and plot
    hist_data = []
    hist_labels = []
    for col in selections:
        series = data_frame[col].dropna()
        col_dtype = series.dtype
        if pd.api.types.is_numeric_dtype(col_dtype):
            hist_data.append(series)
            hist_labels.append(col)
        elif pd.api.types.is_bool_dtype(col_dtype):
            hist_data.append(series.astype(int))
            hist_labels.append(col)
        elif pd.api.types.is_datetime64_any_dtype(col_dtype):
            hist_data.append(series.astype("int64"))
            hist_labels.append(col)
        else:
            # Categorical or object: bar chart of frequencies
            counts = series.value_counts()
            fig = px.bar(
                x=counts.index,
                y=counts.values,
                labels={"x": col, "y": "count"},
                title=f"Frequency of {col}",
            )
            st.plotly_chart(fig, use_container_width=True)

    # If any numeric/bool/datetime, overlay distplot
    if hist_data:
        fig = ff.create_distplot(hist_data, hist_labels, show_hist=True, show_rug=False)
        st.plotly_chart(fig, use_container_width=True)
