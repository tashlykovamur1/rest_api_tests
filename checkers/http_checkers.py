import requests
from contextlib import contextmanager
from requests.exceptions import HTTPError
import json


@contextmanager
def check_http_status_code(expected_status_code: requests.codes = requests.codes.OK, expected_msg: str = ""):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(f"Ожидаемый статус код должен быть равен {expected_status_code}")
        if expected_msg:
            raise AssertionError(f"Должно быть получено сообщение '{expected_msg}', но запрос прошел успешно")

    except HTTPError as exc:
        return HTTPError(json.loads(exc.response.text))
