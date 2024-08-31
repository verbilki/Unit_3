import json
import tempfile
from typing import Any
from unittest.mock import patch, MagicMock

from src.utils import read_transactions_from_json, get_transaction_amount


@patch("src.utils.json.load")
@patch("src.utils.open")
def test_read_transactions_from_json(mock_open: MagicMock, mock_json_load: MagicMock,
                                     transactions: list[dict]) -> None:
    """
    Test the function `read_transactions_from_json` when it is given an existing JSON-file.

    This function tests the `read_transactions_from_json` function when it is given an existing JSON-file.
    It checks that the function reads the JSON-file correctly and returns the data in the correct format.

    Parameters:
        mock_open (MagicMock): A mock for the `open` function.
        mock_json_load (MagicMock): A mock for the `json.load` function.
        transactions (list): A list of dictionaries representing transactions.

    Returns: None
    """
    mock_json_load.return_value = transactions
    assert read_transactions_from_json("existing.json")[:2] == [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]
    mock_open.assert_called_once_with("existing.json", "r", encoding="utf-8")


def test_read_transactions_from_json_no_such_file() -> None:
    """
    Test the function `read_transactions_from_json` when it is given a non-existing JSON-file.

    This function tests the `read_transactions_from_json` function when it is given a non-existing JSON-file.
    It checks that the function returns an empty list.

    Parameters: None
    Returns: None
    """
    file_name = "i_am_not_exist.json"
    assert read_transactions_from_json(file_name) == []


def test_read_transactions_from_json_empty_file() -> None:
    """
    Test the function `read_transactions_from_json` when it is given an empty JSON-file.

    This function tests the `read_transactions_from_json` function when it is given an empty JSON-file.
    It checks that the function returns an empty list.

    Parameters: None
    Returns: None
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        file_path = tmp_file.name
    assert read_transactions_from_json(file_path) == []


def test_read_transactions_from_json_not_a_list() -> None:
    """
    Test the function `read_transactions_from_json` when it is given a JSON-file with a non-list root object.

    This function tests the `read_transactions_from_json` function
    when it is given a JSON-file with a non-list root object.
    It checks that the function returns an empty list.

    Parameters: None
    Returns: None
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        data = {
            "people": [
                {
                    "name": "John Smith",
                    "phone": "666-555-444",
                    "emails": ["johnsmith@home.com", "john.smith@work.com"],
                    "has_license": False,
                },
                {"name": "Jane Doe", "phone": "111-222-333", "emails": None, "has_license": True},
            ]
        }
        json.dump(data, tmp_file)
        file_path = tmp_file.name
    assert read_transactions_from_json(file_path) == []


def test_get_transaction_amount(transactions: list[dict[str, Any]]) -> None:
    """
    Test the function `get_transaction_amount`.

    Parameters:
        fixture transactions (list) from conftest.py: A list of dictionaries representing transactions.

    Returns: None
    """
    assert get_transaction_amount(transactions[2]) == 43318.34


@patch("src.utils.get_exchange_rate")
def test_get_transaction_amount_non_rub_transactions(mock_get_exchange_rate: MagicMock) -> None:
    """
    Test the function `get_transaction_amount` for a USD transaction.

    This function tests the `get_transaction_amount` function for a transaction
    in a non-RUB currency. It checks that the function returns the correct amount
    after converting the transaction amount to RUB using the `get_exchange_rate`
    function.

    Parameters:
        mock_get_exchange_rate (MagicMock): A mock object for the `get_exchange_rate` function.

    Returns: None
    """
    mock_get_exchange_rate.return_value = (True, 2149.32)
    usd_transaction = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "25", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    result = get_transaction_amount(usd_transaction)
    assert result == 2149.32
    mock_get_exchange_rate.return_value = (True, 2149.32)
    usd_transaction = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "25", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    result = get_transaction_amount(usd_transaction)
    assert result == 2149.32

# @pytest.mark.parametrize("return_status, return_result", [(False, "Unauthorized"), (False, "Something went wrong")])
# @patch("src.utils.get_exchange_rate")
# def test_get_transaction_amount_non_ruble_transactions_unsuccessful(
#         mock_get_exchange_rate: MagicMock, return_status: bool, return_result: str
# ):
#     """
#     Test the function `get_transaction_amount` for a USD transaction with unsuccessful
#     `get_exchange_rate` calls.
#
#     This function tests the `get_transaction_amount` function for a transaction
#     in a non-RUB currency. It checks that the function returns None when the
#     `get_exchange_rate` function call is unsuccessful.
#
#     Parameters:
#         mock_get_exchange_rate (MagicMock): A mock object for the `get_exchange_rate` function.
#         return_status (bool): The status of the `get_exchange_rate` function call.
#         return_result (str): The result of the `get_exchange_rate` function call.
#
#     Returns: None
#     """
#     mock_get_exchange_rate.return_value = (return_status, return_result)
#     usd_transaction = {
#         "id": 939719570,
#         "state": "EXECUTED",
#         "date": "2018-06-30T02:08:58.425572",
#         "operationAmount": {"amount": "25", "currency": {"name": "USD", "code": "USD"}},
#         "description": "Перевод организации",
#         "from": "Счет 75106830613657916952",
#         "to": "Счет 11776614605963066702",
#     }
#     transaction_amount = get_transaction_amount(usd_transaction)
#     assert transaction_amount is None
