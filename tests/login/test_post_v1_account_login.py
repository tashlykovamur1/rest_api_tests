import allure


@allure.parent_suite("Login service")
@allure.suite("POST /v1/account/login")
class TestPostV1AccountLogin:
    @allure.title("Авторизация под зарегистрированным пользователем")
    def test_post_v1_account_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        with allure.step("Регистрация нового пользователя"):
            account_helper.register_new_user(login=login, password=password, email=email)

        with allure.step("Авторизация пользователя"):
            account_helper.login_user(login=login, password=password)
