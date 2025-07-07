"""Module for loading data from URLs or local files (CSV/JSON) into pandas DataFrames."""

import json
import pandas as pd
import requests as rq
import platform


def load_data(source: str):
    """We are going to collect the data from the
    source given by the user which could be either
    and URL or a path to its own machine"""

    try:
        if source.lower().startswith(("https://", "http://")):  # URL
            if source.lower().endswith(".csv"):  # Csv
                return pd.read_csv(source)
            elif source.lower().endswith((".xlsx", ".xls")):  # Excel
                return pd.read_excel(source, engine="openpyxl")
            else:  # Json
                payload = rq.get(source, timeout=10).json()  # Convert to Python objects
                return pd.json_normalize(payload)  # Flatten the payload

        else:  # We assume that it is locally stored
            if source.lower().endswith(".csv"):
                return pd.read_csv(source)
            elif source.lower().endswith((".xlsx", ".xls")):
                return pd.read_excel(source, engine="openpyxl")
            elif source.lower().endswith(".json"):
                with open(source, "r", encoding="utf-8") as read_file:
                    data = json.load(read_file)  # Convert it into Python Objects
                return pd.json_normalize(data)  # Flatten the payload
            else:
                if platform.system() == "Windows":  # Windows users use \n\r
                    return (
                        "Unsupported file type\n\r"
                        "Supported extensions: '.csv', '.json', '.xls', '.xlsx'"
                    )
                else:  # Linux and IOS users use \n
                    return (
                        "Unsupported file type\n"
                        "Supported extensions: '.csv', '.json', '.xls', '.xlsx'"
                    )

    except FileNotFoundError as e:
        return (
            "File does not exist.\n",
            e,
        )
    except pd.errors.ParserError as e:
        return ("CSV parsing error.\n", e)
    except json.JSONDecodeError as e:
        return ("JSON decoding error.\n", e)
    except rq.exceptions.Timeout as e:
        return ("Request timed out.\n", e)
    except rq.exceptions.RequestException as e:
        return ("Request error while fetching data from URL.\n", e)
    except ValueError as e:
        return ("Invalid arguments.\n", e)
    except OSError as e:
        return ("File system error.\n", e)
