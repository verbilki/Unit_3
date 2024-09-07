import os

import requests
from dotenv import load_dotenv


def get_exchange_rate(amount: float, from_currency: str, to_currency: str = "RUB") -> tuple[bool, str]:
    """
    Perform a currency exchange rate conversion.

    Args:
        amount (float): The amount of money to convert.
        from_currency (str): The currency code of the money to convert.
        to_currency (str, optional): The currency code to convert to. Defaults to 'RUB'.

    Returns:
        tuple[bool, str]: A tuple where the first element is a boolean indicating
            whether the conversion was successful, and the second element is either the
            converted amount or an error message.
    """
    load_dotenv()

    url = (
        f"{os.getenv("API_URL", "https://api.apilayer.com/exchangerates_data")}"
        "/convert?to={to_currency}&from={from_currency}&amount={amount}"
    )
    headers = {"apikey": os.getenv("API_KEY")}

    try:
        response = requests.get(url, headers=headers)
        status_code = response.status_code

        if status_code == 200:
            response_result = response.json().get("result")
            return True, str(round(float(response_result), 2))

        return False, str(response.reason)

    except requests.exceptions.RequestException as ex:
        return False, str(ex)
