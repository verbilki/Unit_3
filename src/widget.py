import re
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_acc_number: str) -> str:
    """
    Функция преобразования банковской карты или счёта вида
    Visa Platinum 7000792289606361
    или Счет 73654108430135874305
    в маскированные строки вида
    Visa Platinum 7000 79** **** 6361
    или Счет **4305
    соответственно.
    """

    # определение позиции первой цифры во входном аргументе card_or_acc_number
    first_digit_pos = 0

    for i, char in enumerate(card_or_acc_number):
        if char.isdigit():
            first_digit_pos = i
            break

    if first_digit_pos == 0:
        exception_msg = (
            "Номер карты должен начинаться с наименования платежной системы,"
            " а номер счёта должен начинаться со слова 'Счет'."
        )
        raise ValueError(exception_msg)

    pattern = r"[\D]"
    nondigits = re.findall(pattern, card_or_acc_number[first_digit_pos:])

    if card_or_acc_number[: first_digit_pos - 1] == "Счет":
        if nondigits:
            raise ValueError("Номер счета должен состоять только из цифр.")
        return card_or_acc_number[:first_digit_pos] + get_mask_account(card_or_acc_number[first_digit_pos:])
    else:
        if nondigits:
            raise ValueError("Номер карты должен состоять только из цифр.")
        return card_or_acc_number[:first_digit_pos] + get_mask_card_number(card_or_acc_number[first_digit_pos:])


def format_str_date(raw_date_str: str) -> str:
    """
    Converts a date string in ISO 8601 format to a string in the format "dd.mm.yyyy".

    Parameters:
    raw_date_str (str): A date string in ISO 8601 format (e.g., "2022-01-01T12:00:00.000000").

    Returns:
    str: The date string in the format "dd.mm.yyyy". If the input string is empty, an empty string is returned.

    Raises:
    ValueError: If the input string does not match the expected format "%Y-%m-%dT%H:%M:%S.%f".
    """
    if not raw_date_str:
        return ""

    date_formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
    ]
    date_obj = None
    for date_format in date_formats:
        try:
            date_obj = datetime.strptime(raw_date_str, date_format)
        except ValueError:
            continue

    if date_obj is None:
        raise ValueError(f"Ошибка: строка даты-времени '{raw_date_str}' не соответствует ни одному из допустимых форматов.")
    return date_obj.strftime("%d.%m.%Y")
