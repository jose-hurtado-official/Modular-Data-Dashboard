"""Module for loading data from URLs or local files (CSV/JSON) into pandas DataFrames."""

import json
import pandas as pd
import requests as rq


def load_data(source: str):
    """We are going to collect the data from the
    source given by the user which could be either
    and URL or a path to its own machine"""

    try:
        if source.lower().startswith(("https://", "http://")):  # URL
            if source.lower().endswith(".csv"):  # Csv
                return pd.read_csv(source), True
            else:  # Json
                payload = rq.get(source, timeout=10).json()  # Convert to Python objects
                return pd.json_normalize(payload), True  # Flatten the payload

        else:  # We assume that it is locally stored
            if source.lower().endswith(".csv"):
                return pd.read_csv(source), True
            elif source.lower().endswith(".json"):
                with open(source, "r", encoding="utf-8") as read_file:
                    data = json.load(read_file)  # Convert it into Python Objects
                return pd.json_normalize(data), True  # Flatten the payload
            else:
                return (
                    'Unsupported file type\nSupported ones: "csv" and "json"'
                ), False

    except FileNotFoundError as e:
        return (
            "File does not exist.\n",
            e,
        ), False
    except pd.errors.ParserError as e:
        return ("CSV parsing error.\n", e), False
    except json.JSONDecodeError as e:
        return ("JSON decoding error.\n", e), False
    except rq.exceptions.Timeout as e:
        return ("Request timed out.\n", e), False
    except rq.exceptions.RequestException as e:
        return ("Request error while fetching data from URL.\n", e), False
    except ValueError as e:
        return ("Invalid arguments.\n", e), False
    except OSError as e:
        return ("File system error.\n", e), False
