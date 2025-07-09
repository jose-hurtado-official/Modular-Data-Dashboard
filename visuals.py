import pandas as pd
import streamlit as st

# Add the rest of the possible visualitations


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
