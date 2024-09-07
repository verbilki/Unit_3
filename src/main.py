import importlib
import os

from src.generators import filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, search_by_str, sort_by_date
from src.widget import format_str_date, mask_account_card


def main() -> None:
    # Путь к папке с данными
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

    commands = {
        "1": {"format": "JSON", "file_name": "operations.json", "module_name": "src.utils"},
        "2": {"format": "CSV", "file_name": "transactions.csv", "module_name": "src.read_from_file"},
        "3": {"format": "Excel", "file_name": "transactions_excel.xlsx", "module_name": "src.read_from_file"},
    }
    while True:
        print(
            "Добро пожаловать в консольное приложение по анализу банковских транзакций.\n"
            "Выберите цифру пункта меню:\n"
            "1. Получить информацию о транзакциях из JSON-файла\n"
            "2. Получить информацию о транзакциях из CSV-файла\n"
            "3. Получить информацию о транзакциях из XLSX-файла\n"
            "4. Выход."
        )

        user_input = input("\nВаш выбор: ")
        if user_input == "4":
            print("До свидания.")
            break

        user_choice = commands.get(user_input)

        if not user_choice:
            print("Запрошена недопустимая операция.")
            return

        file_format = user_choice["format"]
        file_path = os.path.join(data_path, user_choice["file_name"])
        module = importlib.import_module(user_choice["module_name"])
        func_name = getattr(module, f"read_transactions_from_{file_format.lower()}")
        print(f"Для обработки выбран файл {os.path.join(data_path, user_choice["file_name"])}.\n")

        transactions = func_name(file_path)

        statuses_list = ["EXECUTED", "CANCELED", "PENDING"]
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        )

        raw_user_input = input("Выбор статуса: ")
        user_input = raw_user_input.upper()

        while user_input not in statuses_list:
            print(f'Статус операции "{raw_user_input}" недоступен.')
            print(
                "Введите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные статусы: EXECUTED, CANCELED, PENDING\n"
            )
            raw_user_input = input("Выбор статуса: ")
            user_input = raw_user_input.upper()

        print(f"\nТранзакции отфильтрованы по статусу {raw_user_input}")
        filtered_transactions = filter_by_state(transactions, user_input)

        is_sort_by_date = input("\nОтсортировать транзакции по дате? (Да/Нет): ")
        if is_sort_by_date.lower() == "да":
            is_sort_order = (
                False
                if input("\nОтсортировать по возрастанию или по убыванию? ").lower() == "по возрастанию"
                else True
            )
            filtered_transactions = sort_by_date(filtered_transactions, is_sort_order)

        is_sort_by_currency = input("\nВыводить только рублевые транзакции? (Да/Нет): ")
        if is_sort_by_currency.lower() == "да":
            filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))

        is_filter_by_word = input("\nФильтровать транзакции по определенному слову в описании? (Да/Нет): ")
        if is_filter_by_word.lower() == "да":
            search_word = input("\nВведите слово для поиска: ").split()[0]
            filtered_transactions = search_by_str(filtered_transactions, search_word)

        print("\nИтоговый список транзакций ...")

        if len(filtered_transactions) == 0 or filtered_transactions == "State is invalid":
            print("\nНе найдено ни одной транзакции, подходящей под ваши условия отбора.")
        else:
            print(f"\nВсего транзакций в выборке: {len(filtered_transactions)}\n")
            # Создаём итератор по описаниям транзакций
            descriptions = transaction_descriptions(filtered_transactions)

            for transaction in filtered_transactions:
                date = format_str_date(transaction.get("date", "1900-01-01T00:00:00.000000"))
                description = next(descriptions)
                to_card = mask_account_card(transaction.get("to", "0" * 16))
                amount = " ".join(
                    [
                        str(transaction.get("operationAmount", {}).get("amount")),
                        transaction.get("operationAmount", {}).get("currency", {}).get("name"),
                    ]
                )

                if transaction.get("from"):
                    from_card = mask_account_card(transaction.get("from", "0" * 16))
                    print(f"{date} {description}\n{from_card} -> {to_card}\nСумма: {amount}\n")
                else:
                    print(f"{date} {description}\n{to_card}\nСумма: {amount}\n")


if __name__ == "__main__":
    main()
