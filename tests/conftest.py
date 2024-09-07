from typing import Any

import numpy as np
import pandas as pd
import pytest


def operations_data() -> list[dict[str, str | int]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "20190703"},
        {"id": 939719571, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 615064591, "state": "CANCELED"},
        {"id": 615064591, "date": "2017-10-14T08:21:33.419441"},
        {"id": 615064592, "date": "2017.10"},
    ]


@pytest.fixture
def transactions() -> list[dict[str, Any]]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                },
            },
            "description": "Открытие вклада",
            "to": "Счет 14211924144426031657",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


@pytest.fixture
def card_number_range() -> tuple[int, int]:
    return 1234567890123456, 1234567890123459


@pytest.fixture
def get_df() -> pd.DataFrame:
    data = {
        "id": [650703, 5380041],
        "state": ["EXECUTED", "CANCELED"],
        "date": ["2023-09-05T11:30:32Z", "2021-02-01T11:54:58Z"],
        "amount": [16210, 23789],
        "currency_name": ["Sol", "Peso"],
        "currency_code": ["PEN", "UYU"],
        "from": ["Счет 58803664561298323391", np.nan],
        "to": ["Счет 39745660563456619397", "Счет 23294994494356835683"],
        "description": ["Перевод организации", "Открытие вклада"],
    }

    return pd.DataFrame(data)
