import random
from datetime import datetime

import allure
import pytest
from hamcrest import assert_that, equal_to, has_entries

from checkers.http_checkers import check_http_status_code


@allure.parent_suite("Account service")
@allure.suite("POST /v1/account")
class TestPostV1Account:
    @allure.title("Регистрация нового пользователя")
    def test_post_v1_account(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        with allure.step("Регистрация нового пользователя"):
            account_helper.register_new_user(login=login, password=password, email=email)

        with allure.step("Авторизация пользователя"):
            response = account_helper.login_user(login=login, password=password)

        with allure.step("Пользователь авторизован"):
            with allure.step("В ответе содержится логин зарегистрированного пользователя"):
                assert_that(response.body['resource']['login'], equal_to(login))

    @pytest.mark.parametrize(
        'description, login, email, password, error_msg',
        [
            (
                    "Длина пароля меньше допустимой",
                    f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}",
                    f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}@mail.ru",
                    ''.join(str(random.randint(0, 9)) for _ in range(5)),
                    {"Password": ["Short"]},
            ),
            (
                    "Длина логина меньше допустимой",
                    'a',
                    f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}@mail.ru",
                    ''.join(str(random.randint(0, 9)) for _ in range(6)),
                    {"Login": ["Short"]},
            ),
            (
                    "Email не содержит @",
                    f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}",
                    f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}mail.ru",
                    ''.join(str(random.randint(0, 9)) for _ in range(6)),
                    {"Email": ["Invalid"]},
            ),
        ]
    )
    @allure.title("Нельзя зарегистрировать пользователя с невалидными данными ({description})")
    def test_post_v1_account_negative_data(self, account_helper, login, email, password, error_msg, description):
        with check_http_status_code(400, 'Validation failed'):
            with allure.step("Регистрация нового пользователя"):
                response = account_helper.register_new_user(login=login, password=password, email=email)

            with allure.step("Нельзя зарегистрировать пользователя с невалидными данными"):
                with allure.step(f"Ответ содержит валидационное сообщение '{error_msg}'"):
                    assert_that(response, has_entries(
                        {'errors': has_entries(error_msg)}
                    ))
