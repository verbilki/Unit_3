import pytest

from src.processing import analyze_categories, search_by_str, sort_by_date


@pytest.fixture(scope="module")
def test_sort_by_date_fixt_bad_data() -> list[dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-13-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "bad date"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-32T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T24:21:33.419441"},
    ]


# def test_sort_by_date_bad_date(test_sort_by_date_fixt_bad_data: list[dict]) -> None:
#     """
#     A test function to check if sort_by_date raises a ValueError when a bad date format is encountered.
#     :param test_sort_by_date_fixt_bad_data: List of dictionaries with test data containing bad date formats.
#     :return: None
#     """
#     with pytest.raises(ValueError) as exc_info:
#         sort_by_date(test_sort_by_date_fixt_bad_data)
#     assert str(exc_info.value)[:24] == "Формат даты не распознан"


@pytest.fixture(scope="module")
def test_sort_by_date_fixt_no_key_date() -> list[dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_sort_by_date_no_key_date(test_sort_by_date_fixt_no_key_date: list[dict]) -> None:
    with pytest.raises(KeyError) as exc_info:
        sort_by_date(test_sort_by_date_fixt_no_key_date)
    assert exc_info.value.args[0][:36] == "Ключ 'date' отсутствует в транзакции"


@pytest.mark.parametrize(
    "search_str, transaction_index, number_of_transactions",
    [
        ("Перевод", 0, 5),
        ("Переводить", 0, 5),
        ("Перевести", 0, 5),
        ("перев", 0, 5),
        ("карта", 3, 1),
        ("открыть", 5, 1),
        ("открывать", 5, 1),
        ("Орг", 0, 2),
        ("со счета", 1, 2),
    ],
)
def test_search_by_str(
    transactions: list[dict], search_str: str, transaction_index: int, number_of_transactions: int
) -> None:
    """
    Test function to verify the correctness of the search_by_str function.

    Parameters:
    transactions (list): A list of dictionaries representing transactions.
    search_str (str): A string to search for in the transaction descriptions.
    transaction_index (int): The index of the expected transaction in the transactions list.
    number_of_transactions (int): The expected number of transactions that match the search string.

    Returns:
    None. The function asserts the correctness of the search_by_str function.
    """
    assert search_by_str(transactions, search_str)[0] == transactions[transaction_index]
    assert len(search_by_str(transactions, search_str)) == number_of_transactions


def test_search_by_str_no_such_transactions(transactions: list[dict]) -> None:
    """
    Test function to verify the correctness of the search_by_str function when a transaction contains
    no matching search string in its description.

    Parameters:
    transactions (list): A list of dictionaries representing transactions.

    Returns:
    None. The function asserts the correctness of the search_by_str function.
    """
    assert search_by_str(transactions, "Недопустимое слово в описании транзакции") == []


def test_search_by_str_no_description() -> None:
    """
    Test function to verify the search_by_str function when a transaction has no description.

    Parameters:
    data (list): A list of dictionaries representing transactions. Each dictionary should contain the following keys:
        - id (int): The unique identifier of the transaction.
        - state (str): The state of the transaction.
        - date (str): The date and time of the transaction in the format '%Y-%m-%dT%H:%M:%S.%f'.
        - operationAmount (dict): A dictionary containing the amount and currency of the transaction.
        - from (str): The source of the transaction.
        - to (str): The destination of the transaction.

    search_str (str): A string to search for in the transaction descriptions.
    In this case, it should be "Перевод организации".

    Returns:
    None. The function asserts that the search_by_str function returns an empty list
    when searching for "Перевод организации" in a transaction with no description.
    """
    data = [
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]
    assert search_by_str(data, "Перевод организации") == []


def test_analyze_categories(transactions: list[dict]) -> None:
    """Tests normal work of analyze_categories function."""
    categories_list = [
        "Перевод со счета на счет",
        "Перевод организации",
        "Перевод с карты на карту",
        "Открытие вклада",
    ]
    assert analyze_categories(transactions, categories_list) == {
        "Перевод со счета на счет": 2,
        "Перевод организации": 2,
        "Перевод с карты на карту": 1,
        "Открытие вклада": 1,
    }


def test_analyze_categories_no_such_category(transactions: list[dict]) -> None:
    """Tests analyze_categories function when category is not found."""
    assert analyze_categories(transactions, ["Not existing category"]) == {"Not existing category": 0}


def test_analyze_categories_no_descriptions() -> None:
    """Tests analyze_categories function when transaction has no description."""
    data = [
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]
    assert analyze_categories(data, ["Перевод организации", "Перевод с карты на карту"]) == {
        "Перевод организации": 0,
        "Перевод с карты на карту": 0,
    }
