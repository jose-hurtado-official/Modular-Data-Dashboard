import streamlit as st
import pandas as pd
from data_loader import load_data
from filter_utils import build_filters


st.title("Welcome!")

data = st.text_input(
    "Introduce the source of the data",
    label_visibility="collapsed",
    placeholder="Introduce the source of the data",
)

if data:
    data_frame = load_data(data)
    st.map(data_frame)
    if isinstance(data_frame, pd.DataFrame):
        rows = st.radio(
            "Select the amount of row you want to be displied in the preview of the data frame",
            [1, 5, 10],
            index=1,
        )
        st.dataframe(data_frame.head(rows))
        filtered_data_frame = build_filters(data_frame)
        st.write("`Filtered data frame`")
        st.dataframe(filtered_data_frame)
    else:
        st.error(data_frame)
