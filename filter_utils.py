from typing import Optional
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
    "1. Equal to a specific string (regarding capital letters ...)",
    "2. Starting with a specific letter (or phrase)",
    "3. Finishing with a specific letter (or phrase)",
    "4. Not including a specific word",
    "5. Has at least X times certain letter (you specify the letter)",
    "6. Has at most X times certain letter (you specify the letter)",
    "7. Is in between X and Y times certain letter (you specify the letters)",
    "8. Contains a specific word (or letter ...)",
]


def select_the_filter(suffix=""):
    """
    Parameters
    ----------
    suffix : str, optional
        A string to append to the Streamlit widget's key to ensure uniqueness. Default is "".
    Returns
    -------
    str
        The selected filter from the list of specific date filters.
    """

    return st.selectbox(
        "Select the filter you want to apply:",
        specific_dates_filters,
        key=f"select the filter you want to apply_{suffix}",
    )


def get_date(message):
    """
    Displays a date input widget using Streamlit and returns the selected date.

    Parameters
    ----------
    message : str
        The label or prompt message to display above the date input widget.

    Returns
    -------
    datetime.date
        The date selected by the user.

    Notes
    -----
    - The default value for the date input is set to today's date.
    - The minimum selectable date is January 1, 1900.
    """

    return st.date_input(message, value="today", min_value="1900-01-01")


def filtering_menu(data_frame: pd.DataFrame, column: str, suffix: Optional[str] = ""):
    """
    Displays a dynamic filtering menu for a given DataFrame column using Streamlit widgets.
    Depending on the data type of the selected column (numeric, datetime, or string),
    presents appropriate filtering options to the user and returns a boolean mask
    (comparison sentence) that can be used to filter the DataFrame.

    Parameters
    ----------
    data_frame : pandas.DataFrame
        The DataFrame containing the data to be filtered.
    column : str
        The name of the column to apply the filter on.
    suffix : str, optional
        A suffix to ensure unique Streamlit widget keys, by default "".

    Returns
    -------
    comparison_sentence : pandas.Series or None
        A boolean Series representing the filter condition to be applied to the DataFrame.
        Returns None if the input is invalid or conversion fails.

    Notes
    -----
    - For numeric columns, allows selection of comparison operators and input of comparison value.
    - For datetime columns, allows filtering by specific date, year, month, day, or range.
    - For string columns, allows various string matching and repetition-based filters.
    - Uses Streamlit widgets for user interaction.
    """

    data_type = data_frame[column].dtype
    comparison_sentence = None

    if data_type in ["int", "float"]:
        filter_selected = st.selectbox(
            f"Column's Data Type: {data_type}\nSelect the comparison you want to make:",
            list(comparison_filters.keys()),
            key=f"select the comparison you want to make_{suffix}",
        )

        comparison_data = st.text_input(
            "Introduce the data for making the comparison",
            label_visibility="collapsed",
            placeholder="Write here the data you want to compare",
            key=f"data for making the comparison_{suffix}",
        )

        try:
            if comparison_data.strip() == "":
                st.error("You must provide a value to compare.")
                return None
            elif pd.api.types.is_integer_dtype(data_type):
                converted_data = int(comparison_data)
            else:
                converted_data = float(comparison_data)

        except ValueError as e:
            st.error(f"Unable to convert value: {e}")
            return None

        operation = comparison_filters[filter_selected]

        comparison_sentence = operation(data_frame[column], converted_data)

    elif pd.api.types.is_datetime64_any_dtype(data_frame[column]):
        filter_selected = select_the_filter("general date")

        match filter_selected[0]:
            case "1":

                specific_date_filter = select_the_filter("specific date")

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
                    key=f"select a specific year{suffix}",
                )

                comparison_sentence = data_frame[column].year == comparison_date
            case "3":
                comparison_date = st.selectbox(
                    "Select a specific month",
                    list(range(1, 13)),
                    key=f"select a sepecific month{suffix}",
                )

                comparison_sentence = data_frame[column].month == comparison_date
            case "4":
                comparison_date = st.selectbox(
                    "Select a specific day",
                    list(range(1, 32)),
                    key=f"select a specific day{suffix}",
                )

                comparison_sentence = data_frame[column].day == comparison_date
            case "5":
                one_comparison_date = get_date("Select one date")
                another_comparison_date = get_date("Select another date")

                start_date = min(one_comparison_date, another_comparison_date)
                end_date = max(one_comparison_date, another_comparison_date)

                comparison_sentence = (data_frame[column] >= start_date) & (
                    data_frame[column] <= end_date
                )

    else:  # Are normal strings
        filter_selected = st.selectbox(
            "Select the filter you want to apply:",
            list(string_filters),
            key=f"select the filter you want to apply_{suffix}",
        )

        string_given = st.text_input(
            "Introduce a phrase",
            label_visibility="collapsed",
            placeholder="Introduce a letter (or phrase for comparing)",
            key=f"introduce a phrase_{suffix}",
        )

        match filter_selected[0]:
            case "1":
                comparison_sentence = (
                    data_frame[column].str.lower() == string_given.lower().strip()
                )
            case "2":
                comparison_sentence = data_frame[column].str.contains(
                    f"^{string_given.strip()}", case=False
                )
            case "3":
                comparison_sentence = data_frame[column].str.contains(
                    f"{string_given.strip()}$", case=False
                )
            case "4":
                comparison_sentence = ~data_frame[column].str.contains(
                    string_given.strip(), case=False
                )
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
            case "8":
                comparison_sentence = data_frame[column].str.contains(
                    string_given.strip(), case=False
                )

    return comparison_sentence


def asking_information(data_frame: pd.DataFrame, suffix=""):
    column = st.selectbox(
        "Choose the column you want to apply the filters",
        list(data_frame.columns),
        key=f"choose the column where you want to apply the filters_{suffix}",
    )
    st.success(f"Column {column} selected correctly!")

    try:
        sentence = filtering_menu(data_frame, column, suffix)
    except ValueError as e:
        st.error(e)
        sentence = None

    return sentence


def build_filters(df: pd.DataFrame):
    st.title("Welcome to the filtering page!")
    filtered = df.copy()
    dif_filters = st.selectbox(
        "Do you want to combine different filers?",
        ["No", "Yes"],
        key="combine different filters",
    )

    if dif_filters == "No":
        sentence = asking_information(filtered, "one filter")

        if sentence is not None:
            return filtered[sentence]
        else:
            return None

    else:
        keep_asking = True
        combined_sentence = None
        cont = 0

        while keep_asking:
            sentence = asking_information(filtered, f"several filters {cont}")
            cont += 1

            if sentence is None:
                keep_asking = False
                continue

            if combined_sentence is None:
                combined_sentence = sentence
            else:
                concatenation = st.radio(
                    "Select how it will be related to the other conditions",
                    ["AND", "OR"],
                    key=f"relation with other conditions_{cont}",
                )

                if concatenation == "AND":
                    combined_sentence = combined_sentence & sentence
                else:
                    combined_sentence = combined_sentence | sentence

            selection = st.radio(
                "Do you want to add another filter?",
                ["Yes", "No"],
                index=1,
                key=f"add another filter_{cont}",
            )

            if selection == "No":
                keep_asking = False

        if combined_sentence is not None:
            return filtered[combined_sentence]
        else:
            return None
