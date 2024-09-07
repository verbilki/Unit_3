import logging
import os
import re

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", __name__ + ".log")
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    if not card_number:
        return ""

    logger.info(f"Начало маскирования банковской карты {card_number}.")
    pattern = r"[\D]"
    if re.findall(pattern, card_number):
        logger.critical(f"Обнаружены нецифровые символы в банковской карте {card_number}.")
        raise ValueError("Номер карты должен состоять только из цифр.")

    if len(card_number) != 16:
        logger.critical(f"Недопустимый размер ({len(card_number)}) банковской карты {card_number}.")
        raise ValueError("Номер карты должен состоять из 16 цифр.")

    load_dotenv()
    bank_card_last_visible_digits = int(os.getenv("BANK_CARD_LAST_VISIBLE_DIGITS", "4"))
    masked_card_number = card_number[:6] + "******" + card_number[-bank_card_last_visible_digits:]
    formatted_mask_card_number = " ".join(
        masked_card_number[i : i + bank_card_last_visible_digits]
        for i in range(0, len(masked_card_number), bank_card_last_visible_digits)
    )
    logger.info(f"Создана маска {formatted_mask_card_number} для номера банковской карты.")
    return formatted_mask_card_number


def get_mask_account(account_number: str) -> str:
    """
    Функция принимает на вход номер счета и возвращает его маску.
    Номер счета замаскирован и отображается в формате **XXXX,
    где X — это цифра номера.
    """
    if not account_number:
        return ""

    logger.info(f"Начало маскирования счёта {account_number}.")
    pattern = r"[\D]"  # регулярное выражение для поиска нецифровых символов
    if re.findall(pattern, account_number):
        logger.critical(f"Обнаружены нецифровые символы в счёте {account_number}.")
        raise ValueError("Номер счета должен состоять только из цифр.")

    if len(account_number) != 20:
        logger.critical(
            f"Номера счёта {account_number} имеет размер ({len(account_number)}), " "что отличается от требуемого 20."
        )
        raise ValueError("Номер счета должен состоять из 20 цифр.")

    load_dotenv()
    bank_card_last_visible_digits = int(os.getenv("BANK_CARD_LAST_VISIBLE_DIGITS", "4"))
    masked_account_number = "**" + account_number[-bank_card_last_visible_digits:]
    logger.info(f"Создана маска {masked_account_number} для номера счёта.")
    return masked_account_number
