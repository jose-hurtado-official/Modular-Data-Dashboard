import streamlit as st
import pandas as pd

from dashboard_code.data_loader import load_data
from dashboard_code.filter_utils import build_filters
import dashboard_code.visuals as visuals


st.title("Welcome!")

data = st.text_input(
    "Introduce the source of the data",
    label_visibility="collapsed",
    placeholder="Introduce the source of the data",
)

if data:
    data_frame = load_data(data)
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

        if filtered_data_frame is not None:
            st.title("Welcome to the visualitations page!")

            if "visual" not in st.session_state:
                st.session_state.visual = 0

            left, right = st.columns(2)

            if left.button("Add visualitation", key="add_vis_button"):
                st.session_state.visual += 1

            if right.button("Remove last visualitation", key="rem_vis_button"):
                if st.session_state.visual > 0:
                    st.session_state.visual -= 1
                else:
                    st.warning("There are not visualitations for removing")

            vis_options = [
                "Bar chart",
                "Area chart",
                "Line chart",
                "Scatter chart",
                "Histogram chart",
            ]

            for index in range(st.session_state.visual):
                st.markdown(f":blue[***{index + 1}. Option***]")
                chosen_vis = st.selectbox(
                    "Which visualitation do you want to display?",
                    vis_options,
                    key=f"menus_vis_{index}",
                )

            for index in range(st.session_state.visual):
                visualitation = st.session_state.get(f"menus_vis_{index}", None)
                if visualitation:
                    st.markdown(f":green[***{index + 1}. {visualitation}***]")

                    match visualitation:
                        case "Bar chart":
                            visuals.bar_chart(filtered_data_frame, index)
                        case "Area chart":
                            visuals.area_chart(filtered_data_frame, index)
                        case "Line chart":
                            visuals.line_chart(filtered_data_frame, index)
                        case "Scatter chart":
                            visuals.scatter_chart(filtered_data_frame, index)
                        case "Histogram chart":
                            visuals.histogram_chart(filtered_data_frame, index)

            if st.button("Finish the program", type="primary"):
                st.session_state.finished = True

    else:
        st.error(data_frame)
