from typing import Any

import pandas as pd


def read_transactions_from_csv(file_path: str) -> list[dict[str, Any]]:
    """
    Reads transactions from a CSV file specified by the `file_path` argument.

    Args:
        file_path (str): The path to the CSV file containing transactions. The file should be semicolon-separated.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing transactions.
            Each dictionary contains keys for the transaction's ID, state, date,
            operation amount, description, from account, and to account.
            Returns an empty list if the file cannot be opened or if the
            deserialized data is not a list.
    """
    try:
        df = pd.read_csv(file_path, delimiter=";")
        transactions_dict = df.fillna(0).to_dict(orient="records")
        dict_formatted = [
            {
                "id": int(i.get("id", "0")),
                "state": i.get("state", "UNKNOWN"),
                "date": i.get("date"),
                "operationAmount": {
                    "amount": int(i.get("amount", "0")),
                    "currency": {"name": i.get("currency_name"), "code": i.get("currency_code")},
                },
                "description": i.get("description"),
                "from": i.get("from"),
                "to": i.get("to"),
            }
            for i in transactions_dict
        ]

        for operation in dict_formatted:
            for key, value in list(operation.items()):
                if value == 0:
                    del operation[key]

        return dict_formatted

    except FileNotFoundError:
        return []


def read_transactions_from_excel(file_path: str) -> list[dict[str, Any]]:
    """
    Reads transactions from an Excel file specified by the `file_path` argument.

    Args:
        file_path (str): The path to the Excel file containing transactions.
            The file should be in a format compatible with pandas' read_excel function.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing transactions.
            Each dictionary contains keys for the transaction's ID, state, date,
            operation amount, description, from account, and to account.
            Returns an empty list if the file cannot be opened or if the
            deserialized data is not a list.
            Note: Any keys with a value of 0 are removed from the final dictionary.
    """
    try:
        df = pd.read_excel(file_path)
        transactions_dict = df.fillna(0).to_dict(orient="records")

        dict_formatted = [
            {
                "id": int(i.get("id", "0")),
                "state": i.get("state", "UNKNOWN"),
                "date": i.get("date"),
                "operationAmount": {
                    "amount": int(i.get("amount", "0")),
                    "currency": {"name": i.get("currency_name"), "code": i.get("currency_code")},
                },
                "description": i.get("description"),
                "from": i.get("from"),
                "to": i.get("to"),
            }
            for i in transactions_dict
        ]

        for operation in dict_formatted:
            for key, value in list(operation.items()):
                if value == 0:
                    del operation[key]

        return dict_formatted

    except FileNotFoundError:
        return []
