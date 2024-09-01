## Приложение 'Анализ банковских транзакций'

Этот проект представляет собой Домашнее Задание по Уроку 12-1 курса по Python на платформе SkyPro
ученика Олега Жадана (поток Prof 40.0).

## Инструкция по установке

SSH-ссылка для клонирования проекта с Github:

```
git@github.com:verbilki/Unit_3.git
```

Найти в корне проекта файл .env_template, скопировать его в .env и заполнить конфиденциальными данными
(например, для ключа API_KEY ввести токен подключения к API конвертации валют).

1. Создать в PyCharm виртуальное окружение

### Для Windows

```commandline
python -m venv venv
```

### Для Linux, macOS

```bash
python3 -m venv venv
```

2. Активировать виртуальное окружение
   Следующую команду следует запускать из корня проекта:

### Для Windows

```commandline
venv\Scripts\activate
```

### Для Linux, macOS

```bash
source ./venv/bin/activate
```

3. Установить Poetry.

```bash
poetry install
```

4. Установить линтер flake8, анализатор статического кода mypy, форматтеры (black, isort) на основании файла
   конфигурации pyproject.toml.

Пример настройки flake8, black, isort и mypy в файле pyproject.toml:

```
[tool.poetry.dependencies]
   python = "^3.8"
   flake8 = "^3.8.4"
   black = "^20.8b1"
   isort = "^5.6.4"
   mypy = "^0.790"
```

5. Установить в терминале дополнительные пакеты:

```bash
poetry add requests  
poetry add python-dotenv

pip install pandas
pip install pandas-stubs
```

6. Функциональные модули

* [папка src](#src)
    + [модуль utils.py](#utilspy)
        - [функция read_transactions_from_json](#read_transactions_from_json)
        - [функция get_transaction_amount](#get_transaction_amount)
    + [модуль external_api.py](#external_apipy)
        - [функция get_exchange_rate](#get_exchange_rate)

* [папка tests](#tests)
    + [модуль глобальных фикстур conftest.py](#conftestpy)

  Модули test_utils.py и test_external_api.py содержат функции тестирования перечисленных выше функций.

Папка src
----

### Модуль utils.py

#### Функция read_transactions_from_json

Назначение: Reads transactions from a JSON file specified by the `json_file_path` argument.

Args:
json_file_path (str)`: The path to the JSON file containing transactions.

Returns:
list[dict]`: A list of dictionaries representing transactions.
Each dictionary contains keys for the transaction's ID, state, date,
operation amount, description, from account, and to account.
Returns an empty list if the file cannot be opened or if the
deserialized data is not a list.

Raises: `json.JSONDecodeError`

#### функция get_transaction_amount

Назначение: получить объём заданной транзакции в рублях с учётом возможной конвертации валюты.
Args:
transaction (dict[str, Any]): A dictionary representing a transaction.

    Returns:
        float: The amount of the transaction. If the transaction is in USD, an exchange rate is
        requested from the external API.

### Модуль external_api.py

#### Функция get_exchange_rate

Назначение: получить текущий обменный курс иностранной валюты к рублю из внешнего API.
Args: None
Returns: `float`: The exchange rate.

## 7. Тестирование

Исходный код модулей покрыт юнит-тестами Pytest на более, чем 95%. Для запуска выполните команды:

```bash
poetry add --group dev pytest # установка pytest в виртуальное окружение приложения
pytest # запуск тестов
```

Команда для формирования HTML-отчёта в терминале:

```bash
pytest --cov=src --cov-report=html
```

В результате зтого запуска будет сформирован HTML-отчет (файл htmlcov/index.html) о покрытии тестами.

## Лицензия

[GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.html#license-text)