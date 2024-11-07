import allure


@allure.parent_suite("Account service")
@allure.suite("PUT /v1/account/password")
class TestPutV1AccountPassword:
    @allure.title("Изменение пароля пользователя")
    def test_put_v1_account_password(self, auth_account_helper):
        helper, user_data = auth_account_helper
        new_pwd = '9876543210'

        with allure.step("Изменение пароля пользователя"):
            helper.change_user_password(
                login=user_data.login,
                email=user_data.email,
                old_password=user_data.password,
                new_password=new_pwd
            )

        with allure.step("Авторизация пользователя с новым паролем"):
            helper.login_user(login=user_data.login, password=new_pwd)
