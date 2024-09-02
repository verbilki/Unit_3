from unittest.mock import MagicMock, patch

import pandas as pd

from src.read_from_file import read_transactions_from_csv, read_transactions_from_excel


@patch("src.read_from_file.pd.read_csv")
def test_read_transactions_from_csv(mock_read_csv: MagicMock, get_df: pd.DataFrame) -> None:
    """
    This function tests the read_transactions_from_csv function by mocking the pd.read_csv function.
    It asserts that the function returns the expected list of transactions when given an existing CSV file.

    Parameters:
    mock_read_csv (MagicMock): A mock object for pd.read_csv function.
    get_df (pd.DataFrame): A pandas DataFrame containing the expected transactions.

    Returns:
    None. The function asserts the behavior of read_transactions_from_csv function.
    """
    mock_read_csv.return_value = get_df
    assert read_transactions_from_csv("existing.csv")[:2] == [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "operationAmount": {"amount": 16210, "currency": {"name": "Sol", "code": "PEN"}},
            "description": "Перевод организации",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
        },
        {
            "id": 5380041,
            "state": "CANCELED",
            "date": "2021-02-01T11:54:58Z",
            "operationAmount": {"amount": 23789, "currency": {"name": "Peso", "code": "UYU"}},
            "description": "Открытие вклада",
            "to": "Счет 23294994494356835683",
        },
    ]
    mock_read_csv.assert_called_once_with("existing.csv", delimiter=";")


def test_read_transactions_from_csv_not_exist() -> None:
    """
    Test the function `read_transactions_from_csv` when it is given a non-existing CSV-file.

    This function tests the `read_transactions_from_csv` function when it is given a non-existing CSV-file.
    It checks that the function returns an empty list.

    Parameters: None
    Returns: None
    """
    assert read_transactions_from_csv("not_existing.csv") == []


@patch("src.read_from_file.pd.read_excel")
def test_read_transactions_from_excel(mock_read_excel: MagicMock, get_df: pd.DataFrame) -> None:
    """
    This function tests the read_transactions_from_excel function by mocking the pd.read_excel function.
    It asserts that the function returns the expected list of transactions when given an existing Excel file.

    Parameters:
    mock_read_excel (MagicMock): A mock object for pd.read_excel function.
    get_df (pd.DataFrame): A pandas DataFrame containing the expected transactions.

    Returns:
    None. The function asserts the behavior of read_transactions_from_excel function.
    """
    mock_read_excel.return_value = get_df
    assert read_transactions_from_excel("existing.xlsx")[:2] == [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "operationAmount": {"amount": 16210, "currency": {"name": "Sol", "code": "PEN"}},
            "description": "Перевод организации",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
        },
        {
            "id": 5380041,
            "state": "CANCELED",
            "date": "2021-02-01T11:54:58Z",
            "operationAmount": {"amount": 23789, "currency": {"name": "Peso", "code": "UYU"}},
            "description": "Открытие вклада",
            "to": "Счет 23294994494356835683",
        },
    ]
    mock_read_excel.assert_called_once_with("existing.xlsx")


def test_read_transactions_from_excel_not_exist() -> None:
    """
    Test the function `read_transactions_from_excel` when it is given a non-existing Excel file.

    This function tests the `read_transactions_from_excel` function when it is given a non-existing Excel file.
    It checks that the function returns an empty list.

    Parameters: None
    Returns: None
    """
    assert read_transactions_from_excel("not_existing.xlsx") == []
