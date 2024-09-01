from unittest import mock
from unittest.mock import patch

import requests

from src.external_api import get_exchange_rate


@patch("src.external_api.requests.get")
def test_get_exchange_rate(mock_get: mock.Mock) -> None:
    """
    Tests get_exchange_rate function with a successful response.

    This test tests the get_exchange_rate function when it receives a successful response.
    It checks that the function returns a tuple with the first element being True and the second element
    being the converted amount.

    Parameters:
        mock_get (unittest.mock.Mock): A mock object for the requests.get function.

    Returns:
        None
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 25},
        "info": {"timestamp": 1722061984, "rate": 85.972867},
        "date": "2024-07-27",
        "result": "2149.321675",
    }
    assert get_exchange_rate(25, "USD") == (True, "2149.32")


@patch("src.external_api.requests.get")
def test_get_exchange_rate_denied_access(mock_get: mock.Mock) -> None:
    """
    Tests get_exchange_rate function with a denied access response.

    This test tests the get_exchange_rate function when it receives a denied access response.
    It checks that the function returns a tuple with the first element being False and the second element
    being the error message.

    Parameters:
        mock_get (unittest.mock.Mock): A mock object for the requests.get function.

    Returns: None
    """
    mock_get.return_value.status_code = 401
    mock_get.return_value.reason = "Unauthorized"
    mock_get.return_value.json.return_value = {"message": "Invalid authentication credentials"}
    result = get_exchange_rate(25, "USD")
    assert result == (False, "Unauthorized")


def test_get_exchange_rate_request_error() -> None:
    """
    Tests get_exchange_rate function when the request to the external API fails.

    This test tests the get_exchange_rate function when the request to the external API fails.
    It checks that the function returns a tuple with the first element being False and the second element
    being the error message.

    Parameters: None
    Returns: None
    """
    with mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Something went wrong")):
        result = get_exchange_rate(25, "USD")
    assert result == (False, "Something went wrong")
