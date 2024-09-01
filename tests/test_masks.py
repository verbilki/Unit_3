import pytest

from src.masks import get_mask_account, get_mask_card_number


# ---- get_mask_card_number ------
@pytest.fixture(scope="module")
def fixture_card_number() -> tuple[str, str]:
    return "4321000000332345", "4321 00** **** 2345"


def test_get_mask_card_number_fixture(fixture_card_number: tuple[str, str]) -> None:
    """
    Checks that the `get_mask_card_number` function returns the expected masked card number.

    The `fixture_card_number` fixture provides a tuple of a card number and its expected masked value.
    This function tests that the `get_mask_card_number` function returns the expected masked value
    when given the card number as input.

    Parameters:
        fixture_card_number (tuple[str, str]): A tuple of a card number and its expected masked value.
    """
    assert get_mask_card_number(fixture_card_number[0]) == fixture_card_number[1]


@pytest.mark.parametrize(
    "card_number, expected_mask",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("7000792289606361", "7000 79** **** 6361"),
        ("4321000000012345", "4321 00** **** 2345"),
        ("", ""),
    ],
)
def test_get_mask_card_number(card_number: str, expected_mask: str) -> None:
    """
    This function tests the functionality of the get_mask_card_number function.

    Parameters:
    card_number (str): The card number to be masked. It should be a string of 16 digits.
    expected_mask (str): The expected masked card number.

    Returns:
    None: The function does not return anything.
    It asserts whether the get_mask_card_number function returns the expected masked card number.
    """
    assert get_mask_card_number(card_number) == expected_mask


def test_get_mask_card_number_length_error() -> None:
    """
    This function tests the behavior of the `get_mask_card_number` function when the input card number
    has a length other than 16 digits.

    Parameters:
    None: This function does not take any parameters.

    Returns:
    None: The function does not return anything.
    It asserts whether the `get_mask_card_number` function raises a `ValueError`
           with the expected error message when given a card number with a length other than 16 digits.

    Raises:
    ValueError: If the `get_mask_card_number` function does not raise a `ValueError` with the expected error message,
                this exception will be raised.
    """
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number("123456789012345")
    assert str(exc_info.value) == "Номер карты должен состоять из 16 цифр."


# Тест на проверку наличия нецифровых символов в номере карты.
@pytest.mark.parametrize(
    "card_number",
    [
        "1234abcd56789012",  # Contains letters
        "1234 5678 9012 3456",  # Contains spaces
        "1234-5678-9012-3456",  # Contains hyphens
        "1234!5678@9012#3456",  # Contains special characters
        "1234.5678.9012.3456",  # Contains dots
    ],
)
def test_get_mask_card_number_non_digital_symbols(card_number: str) -> None:
    """
    This function tests the behavior of the `get_mask_card_number` function when the input card number
    contains non-digital symbols.

    Parameters:
    card_number (str): The card number to be tested. It should be a string that contains non-digital symbols.

    Returns:
    None: The function does not return anything.
        It asserts whether the `get_mask_card_number` function raises a `ValueError`
        with the expected error message when given a card number with non-digital symbols.

    Raises:
    ValueError: If the `get_mask_card_number` function does not raise a `ValueError` with the expected error message,
                this exception will be raised.
    """
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(card_number)
    assert str(exc_info.value) == "Номер карты должен состоять только из цифр."


# ----- get_mask_account ------
@pytest.fixture(scope="module")
def account_number() -> tuple[str, str]:
    return "43210810000000017890", "**7890"


def test_get_mask_account_fixture(account_number: tuple[str, str]) -> None:
    """
    Tests the `get_mask_account` function with valid account numbers.

    Parameters:
    account_number (tuple[str, str]): A tuple containing the account number and its expected masked value.

    Returns:
    None: The function does not return anything.
          It asserts whether the `get_mask_account` function returns the expected masked account number.
    """
    assert get_mask_account(account_number[0]) == account_number[1]


@pytest.mark.parametrize(
    "account_number, expected_mask",
    [
        ("43210810000000012345", "**2345"),
        ("73654108430135874305", "**4305"),
        ("", ""),
    ],
)
def test_get_mask_account(account_number: str, expected_mask: str) -> None:
    """
    This function tests the `get_mask_account` function with valid account numbers.

    Parameters:
    account_number (str): The account number to be masked. It should be a string.
    expected_mask (str): The expected masked account number. It should be a string.

    Returns:
    None: The function does not return anything.
          It asserts whether the `get_mask_account` function returns the expected masked account number.
    """
    assert get_mask_account(account_number) == expected_mask
