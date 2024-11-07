from datetime import datetime

import allure


@allure.parent_suite("Account service")
@allure.suite("PUT /v1/account/email")
class TestPutV1AccountEmail:
    @allure.title("Изменение email-а пользователя")
    def test_put_v1_account_email(self, auth_account_helper, prepare_user):
        helper, user_data = auth_account_helper
        login = user_data.login
        password = user_data.password

        with allure.step("Изменение email-а пользователя"):
            new_email = f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}@mail.ru"
            helper.change_user_email(login=login, new_email=new_email, password=password)

        with allure.step("Активация пользователя с новым email-ом"):
            helper.activate_registered_user(login=login)

        with allure.step("Авторизация пользователя"):
            helper.login_user(login=login, password=password)
