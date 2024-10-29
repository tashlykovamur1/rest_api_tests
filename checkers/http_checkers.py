import requests
from contextlib import contextmanager

from hamcrest import assert_that, equal_to
from requests.exceptions import HTTPError

@contextmanager
def check_http_status_code(expected_status_code: requests.codes = requests.codes.OK, expected_msg: str = ""):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(f"Ожидаемый статус код должен быть равен {expected_status_code}")
        if expected_msg:
            raise AssertionError(f"Должно быть получено сообщение '{expected_msg}', но запрос прошел успешно")

    except HTTPError as exc:
        assert_that(exc.response.status_code, equal_to(expected_status_code))
        assert_that(exc.response.json()['title'], equal_to(expected_msg))
