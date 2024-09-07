import pytest

from src.widget import format_str_date, mask_account_card


# --- mask_account_card ---
@pytest.fixture(scope="module")
def card_or_acc_number() -> tuple[str, str]:
    """
    Fixture that provides a tuple of two card or account numbers. The first number is a Visa Classic card number
    with the last 4 digits masked, and the second number is a Visa Classic card number with all digits except the
    first 6 masked. This fixture is used to test the `mask_account_card` function in the `src/widget.py` module.

    Returns:
        tuple[str, str]: A tuple of two card or account numbers.
    """
    return "Visa Classic 2200792289606361", "Visa Classic 2200 79** **** 6361"


def test_mask_account_card_fixture(card_or_acc_number: str) -> None:
    """
    Test the `mask_account_card` function to ensure it correctly masks card and account numbers.

    This test uses a fixture to provide a card or account number and its expected masked output. The function
    `mask_account_card` is called with the card or account number and the result is asserted to be equal to the
    expected masked output.

    Args:
        card_or_acc_number (str): A tuple containing the card or account number and its expected masked output.

    Returns:
        None: This function does not return a value. It asserts that the output of `mask_account_card` matches the
              expected value.
    """
    assert mask_account_card(card_or_acc_number[0]) == card_or_acc_number[1]


@pytest.mark.parametrize(
    "card_or_acc_number, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Visa 4111111111111111", "Visa 4111 11** **** 1111"),
    ],
)
def test_mask_account_card(card_or_acc_number: str, expected: str) -> None:
    """
    Test the `mask_account_card` function to ensure it correctly masks card and account numbers.

    This test uses parameterized inputs to check that the `mask_account_card` function returns the expected masked
    output for various card and account numbers.

    Args:
        card_or_acc_number (str): The card or account number to be masked.
        expected (str): The expected masked output.

    Returns:
        None: This function does not return a value. It asserts that the output of `mask_account_card`
        matches the expected value.
    """
    assert mask_account_card(card_or_acc_number) == expected


def test_mask_account_card_error() -> None:
    """
    Test the `mask_account_card` function to ensure it raises a ValueError for invalid card or account numbers.

    This test checks that the `mask_account_card` function raises a ValueError when the input string does not start
    with a valid payment system name for card numbers or the word 'Счет' for account numbers.

    Raises:
        ValueError: If the input string does not start with a valid payment system name or 'Счет'.
    """
    with pytest.raises(ValueError) as exc_info:
        mask_account_card("12345678901234567890")
    assert (
        str(exc_info.value)
        == "Номер карты должен начинаться с наименования платежной системы, \
а номер счёта должен начинаться со слова 'Счет'."
    )


def test_mask_account_card_non_digital_symbols_card() -> None:
    """
    Test the `mask_account_card` function to ensure it raises a ValueError for card numbers
    containing non-digital symbols.

    This test checks that the `mask_account_card` function raises a ValueError when the card number contains any
    non-digital symbols, ensuring that only numeric characters are allowed in the card number.

    Raises:
        ValueError: If the card number contains any non-digital symbols.
    """
    with pytest.raises(ValueError) as exc_info:
        mask_account_card("Visa Classic 220O79228960636")
    assert str(exc_info.value) == "Номер карты должен состоять только из цифр."


def test_mask_account_card_non_digital_symbols_acc() -> None:
    """
    Test the `mask_account_card` function to ensure it raises a `ValueError` for account numbers
     containing non-digital symbols.

    This test checks that the `mask_account_card` function raises a `ValueError` when the account number contains any
    non-digital symbols, ensuring that only numeric characters are allowed in the account number.

    Raises:
        ValueError: If the account number contains any non-digital symbols.

    Returns:
        None: This function does not return a value. It asserts that the raised `ValueError`
        has the expected error message.
    """
    with pytest.raises(ValueError) as exc_info:
        mask_account_card("Счет 1234567890123456789O")
    assert str(exc_info.value) == "Номер счета должен состоять только из цифр."


# --- format_str_date ---
@pytest.mark.parametrize(
    "raw_date_str, expected",
    [
        ("2023-10-01T12:34:56.789012", "01.10.2023"),
        ("2022-01-15T00:00:00.000000", "15.01.2022"),
        ("2020-02-29T23:59:59.999999", "29.02.2020"),
        ("2019-12-31T23:59:59.999999", "31.12.2019"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
        ("", ""),
    ],
)
def test_format_str_date(raw_date_str: str, expected: str) -> None:
    """
    Test function to verify the `format_str_date` function with the provided test data.

    This function tests the `format_str_date` function by passing different `raw_date_str` values
    and their corresponding expected results.
    It uses the `pytest.mark.parametrize` decorator to generate multiple test cases dynamically.

    Parameters:
        raw_date_str (str): The raw date string to be passed to the `format_str_date` function.
        expected (str): The expected result of calling `format_str_date` with the `raw_date_str`.

    Returns: None
    Raises: AssertionError: If the actual result of calling `format_str_date` does not match the expected result.
    """
    assert format_str_date(raw_date_str) == expected


def test_format_str_date_error() -> None:
    """
    Test the `format_str_date` function to ensure it raises a ValueError for invalid date strings.

    This test checks that the `format_str_date` function raises a ValueError
    when the input string does not match the expected
    datetime format.

    Raises:
        ValueError: If the input string does not match the expected datetime format.
    """
    err_datetime_str = "2023-13-01T12:34:56.789012"
    with pytest.raises(ValueError) as exc_info:
        format_str_date(err_datetime_str)
    assert (
        str(exc_info.value)
        == "Ошибка: строка даты-времени '" + err_datetime_str + "' не соответствует ни одному из допустимых форматов."
    )
