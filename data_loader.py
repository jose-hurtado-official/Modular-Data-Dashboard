# data_loader.py

import json
import pandas as pd
import requests as rq


def collecting(source: str):
    """We are going to collect the data from the
    source given by the user which could be either
    and URL or a path to its own machine"""

    try:
        if source.lower().startswith(("https://" or "http://")):  # URL
            if source.lower().endswith(".csv"):  # Csv
                return pd.read_csv(source), True
            else:  # Json
                payload = rq.get(source).json()  # Convert to Python objects
                return pd.json_normalize(payload), True  # Flatten the payload

        else:  # We assume that it is locally stored
            if source.lower().endswith(".csv"):
                return pd.read_csv(source), True
            elif source.lower().endswith(".json"):
                with open(source, "r") as read_file:
                    data = json.load(read_file)  # Convert it into Python Objects
                return pd.json_normalize(data), True  # Flatten the payload
            else:
                return (
                    f'Unsupported file type\nSuported ones: "csv" and "json"'
                ), False

    except Exception as e:
        return (
            f"We could not access to the data provided by the source: {source}\n",
            e,
        ), False
