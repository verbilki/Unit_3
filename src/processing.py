import re
from collections import Counter
from datetime import datetime
from typing import Any


def filter_by_state(data: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """
    :Назначение функции: фильтрация списка словарей банковских операций по значению ключа 'state'.

    :param data: список словарей банковских операций для фильтрации.
    :param state: значение ключа 'state' для фильтрации. По умолчанию, 'EXECUTED'.
    :return: список словарей.
    """
    return [item for item in data if item.get("state", "UNKNOWN") == state]


def sort_by_date(data: list[dict[str, Any]], is_sort_order: bool = True) -> list[dict[str, Any]]:
    """
    :Назначение функции: сортировка списка словарей банковских транзакций по дате операции
    :param data: список словарей банковских операций для фильтрации.
    :param: is_sort_order: булевый флаг направления сортировки по датам транзакций.
                          (True (по умолчанию) - по убыванию дат; False - по возрастанию дат).
    :return: отсортированный список словарей транзакций.
    """
    date_formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
    ]

    for d in data:
        if "date" in d:
            for date_format in date_formats:
                try:
                    datetime.strptime(d["date"], date_format)
                except ValueError:
                    continue
            # raise ValueError(f"Формат даты не распознан {d["date"]}.")

        else:
            raise KeyError(f"Ключ 'date' отсутствует в транзакции {d}.")

    return sorted(data, key=lambda item: item["date"], reverse=is_sort_order)


def search_by_str(transactions: list[dict], search_str: str) -> list[dict]:
    """
    This function searches for banking operations that contain a specific string in their descriptions.
    The search is case-insensitive and ignores the endings 'ть', 'сти', and 'вать' in the search string.

    Parameters:
    transactions (list[dict]): A list of dictionaries representing banking operations.
                                Each dictionary should have a 'description' key.
    search_str (str): The string to search for in the operation descriptions.

    Returns:
    list[dict]: A list of dictionaries representing banking operations
                that contain the search string in their descriptions.
    """
    pattern = rf"{re.escape(re.sub(r'ть|сти|вать', '', search_str))}?.*"
    return [
        operation
        for operation in transactions
        if re.search(pattern, operation.get("description", ""), flags=re.IGNORECASE)
    ]


def analyze_categories(transactions: list[dict], categories_list: list[str]) -> dict[str, int]:
    """
    This function analyzes the descriptions of banking transactions
    and categorizes them based on a given list of categories.
    It counts the occurrences of each category in the descriptions
    and returns a dictionary with the category counts.

    Parameters:
    transactions (list[dict]): A list of dictionaries representing banking transactions.
    Each dictionary should have a 'description' key.
    categories_list (list[str]): A list of strings representing the categories to analyze.

    Returns:
    dict: A dictionary where the keys are the categories and the values are the counts of occurrences
            of each category in the descriptions.
    """
    descriptions_list = [operation.get("description") for operation in transactions]
    descriptions_count = Counter(descriptions_list)
    result = {}

    for category in categories_list:
        result[category] = descriptions_count.get(category, 0)

    return result
