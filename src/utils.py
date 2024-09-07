import json
import logging
import os
from typing import Any

from src.external_api import get_exchange_rate

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "utils.log")
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_transactions_from_json(json_file_path: str) -> list[dict]:
    """
    Reads transactions from a JSON file specified by the `json_file_path` argument.
    Args:
        json_file_path (str): The path to the JSON file containing transactions.
    Returns:
        list[dict]: A list of dictionaries representing transactions.
            Each dictionary contains keys for the transaction's ID, state, date,
            operation amount, description, from account, and to account.
            Returns an empty list if the file cannot be opened or if the
            deserialized data is not a list.

    Raises: json.JSONDecodeError
    """
    try:
        logger.info(f"Попытка открытия файла {json_file_path} на чтение.")
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            try:
                logger.info(f"Начало чтения файла {json_file_path} с транзакциями.")
                json_data = json.load(json_file)

            except json.JSONDecodeError as ex:
                logger.error(ex)
                return []
            else:
                if type(json_data) is not list:
                    logger.warning(f"Содержимое файла {json_file_path} не является списочным объектом.")
                    return []

                logger.info(f"Чтение файла {json_file_path} с транзакциями прошло успешно.")
                return json_data

    except FileNotFoundError as ex:
        logger.error(ex)
        return []


def get_transaction_amount(transaction: dict[str, Any]) -> float:
    """
    Расчёт рублевогоо эквивалента заданной транзакции с учётом конверсионной операции.

    Args:
        transaction (dict[str, Any]): A dictionary representing a transaction.

    Returns:
        float: The amount of the transaction. If the transaction is in USD, an exchange rate is
        requested from the external API.
    """
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code", "")
    trn_amount = float(transaction.get("operationAmount", {}).get("amount", ""))
    rub_amount = ""

    if currency == "RUB":
        logger.info(f"Объём рублевой транзакции (id: {transaction.get('id')}).")
        rub_amount = str(trn_amount)
    else:
        logger.info(f"Попытка расчёта рублевого эквивалента {currency}-транзакции (id: {transaction.get('id')}).")
        status, rub_amount = get_exchange_rate(trn_amount, currency)

        if status:
            logger.info(
                "Обменная операция успешно рассчитана, "
                "рублевый эквивалент транзакции составляет " + str(rub_amount) + " руб."
            )

    return float(rub_amount)


if __name__ == "__main__":
    transactions = read_transactions_from_json(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
    )
    for transaction in transactions:
        print(transaction)

    for transaction in transactions[:5]:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code", "") != "RUB":
            print(
                transaction["id"],
                transaction.get("operationAmount", {}).get("currency", {}).get("code"),
                transaction.get("operationAmount", {}).get("amount"),
                get_transaction_amount(transaction),
            )
