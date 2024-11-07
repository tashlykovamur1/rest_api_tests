import allure


@allure.parent_suite("Account service")
@allure.suite("PUT /v1/account/{token}")
class TestPutV1AccountToken:
    @allure.title("Активация авторизационного токена пользователя")
    def test_put_v1_account_token(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        with allure.step("Регистрация нового пользователя"):
            account_helper.create_new_user(login=login, password=password, email=email)

        with allure.step("Активация пользователя"):
            account_helper.activate_registered_user(login=login)
