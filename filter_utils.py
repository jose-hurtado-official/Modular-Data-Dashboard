import datetime
import operator
import pandas as pd
import streamlit as st

# Options for choosing the filters to apply
comparison_filters = {
    "1. Greater than (>)": operator.gt,
    "2. Greater equal (>=)": operator.ge,
    "3. Exactly (==)": operator.eq,
    "4. Less equal (<=)": operator.le,
    "5. Less than (<)": operator.lt,
}
dates_filters = [
    "1. Specific date",
    "2. Specific year",
    "3. Specific month",
    "4. Specific day",
    "5. Between two given dates",
]
specific_dates_filters = [
    "1. The precise date",
    "2. Before that date",
    "3. After that date",
]
string_filters = [
    "1. Equal to a specific string",
    "2. Starting with a specific letter (or phrase)",
    "3. Finishing with a specific letter (or phrase)",
    "4. Not including a specific word",
    "5. Has at least X times certain letter (you specify the letter)",
    "6. Has at most X times certain letter (you specify the letter)",
    "7. Is in between X and Y times certain letter (you specify the letters)",
]


"""def filtering_menu(data_type):
    category = st.selectbox(
        "Select the category of filter that you want to apply:", category_of_filters
    )

    if category[0] == "1":
        filter_selected = st.selectbox(
            "Select the comparison you want to make:", list(comparison_filters.keys())
        )

        comparison_data = st.text_input(
            "Introduce the data",
            label_visibility="collapsed",
            placeholder="Write here the data for making the comparison",
        )

        try:
            comp_data_converted = data_type(comparison_data)
        except ValueError as e:
            return False, e

        return comparison_filters[filter_selected], comp_data_converted

    else:
        pass"""


def get_date(message):
    return st.date_input(message, value="today", min_value="1900-01-01")


def filtering_menu(data_frame, column):
    data_type = data_frame[column].dtype
    comparison_sentence = None

    if data_type in ["int", "float"]:
        filter_selected = st.selectbox(
            f"Column's Data Type: {data_type}\nSelect the comparison you want to make:",
            list(comparison_filters.keys()),
        )

        comparison_data = st.text_input(
            "Introduce the data for making the comparison",
            label_visibility="collapsed",
            placeholder="Write here the data you want to compare",
        )

        try:
            if pd.api.types.is_integer_dtype(data_type):
                converted_data = int(comparison_data)
            else:
                converted_data = float(comparison_data)

        except ValueError as e:
            return False, e

        operation = comparison_filters[filter_selected]

        comparison_sentence = operation(data_frame[column], converted_data)

    elif data_type == pd.api.types.is_datetime64_any_dtype(data_frame[column]):
        filter_selected = st.selectbox(
            f"Column's Data Type: {data_type}\nSelect the filter you want to apply:",
            list(dates_filters),
        )

        match filter_selected[0]:
            case "1":

                specific_date_filter = st.selectbox(
                    "Select the filter you want to apply:",
                    list(specific_dates_filters),
                )

                comparison_date = get_date("Select a specific date")
                match specific_date_filter[0]:
                    case "1":
                        comparison_sentence = data_frame[column] == comparison_date
                    case "2":
                        comparison_sentence = data_frame[column] < comparison_date
                    case "3":
                        comparison_sentence = data_frame[column] > comparison_date

            case "2":
                comparison_date = st.selectbox(
                    "Select a specific year",
                    list(range(1900, datetime.datetime.now().year + 1)),
                )

                comparison_sentence = data_frame[column].year == comparison_date
            case "3":
                comparison_date = st.selectbox(
                    "Select a specific month", list(range(1, 13))
                )

                comparison_sentence = data_frame[column].month == comparison_date
            case "4":
                comparison_date = st.selectbox(
                    "Select a specific day", list(range(1, 32))
                )

                comparison_sentence = data_frame[column].day == comparison_date
            case "5":
                one_comparison_date = get_date("Select one date")
                another_comparison_date = get_date("Select another date")

                comparison_sentence = (
                    data_frame[column]
                    > max(one_comparison_date, another_comparison_date)
                ) & (
                    data_frame[column]
                    < min(one_comparison_date, another_comparison_date)
                )
    else:  # Are normal strings
        filter_selected = st.selectbox(
            f"Column's Data Type: {data_type}\nSelect the filter you want to apply:",
            list(string_filters),
        )

        string_given = st.text_input(
            "Introduce a phrase",
            label_visibility="collapsed",
            placeholder="introduce a letter (or phrase for comparing)",
        )

        match filter_selected[0]:
            case "1":
                comparison_sentence = data_frame[column] == string_given
            case "2":
                comparison_sentence = data_frame[column].str.contains(
                    f"^{string_given}"
                )
            case "3":
                comparison_sentence = data_frame[column].str.contains(
                    f"{string_given}$"
                )
            case "4":
                comparison_sentence = ~data_frame[column].str.contains(string_given)
            case "5":
                amount = st.number_input(
                    "How many times can be the letter (or word ...) repeted",
                    label_visibility="collapsed",
                    placeholder="How many times can be the letter (or word ...) repeted",
                    step=1,
                )
                comparison_sentence = data_frame[column].str.contains(
                    f"{string_given}{{{int(amount)},}}"
                )
            case "6":
                amount = st.number_input(
                    "How many times can be the letter (or word ...) repeted",
                    label_visibility="collapsed",
                    placeholder="How many times can be the letter (or word ...) repeted",
                    step=1,
                )
                comparison_sentence = data_frame[column].str.contains(
                    f"{string_given}{{,{int(amount)}}}"
                )
            case "7":
                smaller_amount = st.number_input(
                    "Minimum times that the letter (or word ...) will be repeted",
                    label_visibility="collapsed",
                    placeholder="How many times can be the letter (or word ...) repeted",
                    step=1,
                )
                bigger_amount = st.number_input(
                    "Maximum times that the letter (or word ...) will be repeted",
                    label_visibility="collapsed",
                    placeholder="How many times can be the letter (or word ...) repeted",
                    step=1,
                )
                if smaller_amount > bigger_amount:
                    st.error(
                        f"The smaller amount ({smaller_amount}) is bigger than the larger one ({bigger_amount})"
                    )

                comparison_sentence = data_frame[column].str.contains(
                    f"{string_given}{{{int(smaller_amount)},{int(bigger_amount)}}}"
                )

    return comparison_sentence


def built_filters(df: pd.DataFrame):
    st.title(
        "Welcome to the filtering page!"
    )  # Todo: search for a filter icon or something like that
    filtered = df.copy()

    dif_filters = "Inicialising"
    while dif_filters.lower().strip() not in ["y", "n"]:
        dif_filters = st.text_input(
            "Do you want to combine different filters or you will use just one (y/n)? "
        )
        if dif_filters.lower().strip() not in ["y", "n"]:
            st.warning('Wrong answer, you must type "y" or "n"\n')

    if dif_filters.lower().strip() == "n":
        column = st.selectbox(
            "Choose the column you want to applu the filters", list(filtered.columns)
        )
        st.success(f"Column {column} selected correctly!")

    else:
        pass
