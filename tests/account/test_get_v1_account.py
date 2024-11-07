import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_http_status_code


@allure.parent_suite("Account service")
@allure.suite("GET /v1/account")
class TestGetV1Account:
    @allure.title("Получение данных пользователя")
    def test_get_v1_account(self, auth_account_helper):
        helper, user_data = auth_account_helper

        with check_http_status_code():
            with allure.step("Получение данных пользователя"):
                response = helper.dm_account_api.account_api.get_v1_account()

        with allure.step("Приходят данные пользователя"):
            with allure.step("В ответе содержится логин пользователя, запросившего данные"):
                GetV1Account.check_received_user_info(response=response, login=user_data.login)

    @allure.title("Нельзя получить данные пользователя без авторизационного токена")
    def test_get_v1_account_unauth(self, account_helper):
        with check_http_status_code(401, 'User must be authenticated'):
            with allure.step("Получение данных пользователя без авторизационного токена"):
                account_helper.dm_account_api.account_api.get_v1_account()
