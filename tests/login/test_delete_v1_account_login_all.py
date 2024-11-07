import allure


@allure.parent_suite("Login service")
@allure.suite("DELETE /v1/account/login/all")
class TestDeleteV1AccountLoginAll:
    @allure.title("Логаут со всех устройств под авторизованным пользователем")
    def test_delete_v1_account_login_all(self, auth_account_helper):
        helper, _ = auth_account_helper

        with allure.step("Логаут пользователя со всех устройств"):
            response = helper.dm_account_api.login_api.delete_v1_account_login_all()

        with allure.step("Пользователь успешно разлогинен"):
            assert response.status_code == 204, f'Не удалось разлогинить пользователя'
