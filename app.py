import streamlit as st
import pandas as pd

from data_loader import load_data
from filter_utils import build_filters
import visuals


# Use dictionaries to store the different types of visualitations so you can alter them, remove them ...


def form(suffix: int):
    with st.form(f"add_vis_form_{suffix}"):
        vis_options = ["Bar chart"]

        chosen_vis = st.selectbox(
            "Which visualitation do you want?",
            vis_options,
            key=f"menus_vis_{suffix}",
        )
        add = st.form_submit_button("Add visualitation")

        if add:
            st.session_state.visual.append(chosen_vis)


def more_visuals(suffix: int):
    return (
        st.radio(
            "Do you want to add more visualitations?",
            ["Yes", "No"],
            index=1,
            key=f"more_visuals_{suffix}",
        )
        == "Yes"
    )


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
                st.session_state.visual = []

            cont = 0
            form(cont)
            more_forms = more_visuals(cont)
            cont += 1

            while more_forms:
                form(cont)
                more_forms = more_visuals(cont)
                cont += 1

            for index, visualitation in enumerate(st.session_state.visual):
                st.write(f"{index + 1}. {visualitation}")

                match visualitation:
                    case "Bar chart":
                        visuals.bar_chart(filtered_data_frame, index)

            if st.button("Finish the program", type="primary"):
                st.session_state.finished = True

    else:
        st.error(data_frame)
