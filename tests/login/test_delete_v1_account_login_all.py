def test_delete_v1_account_login_all(auth_account_helper):
    helper, _ = auth_account_helper
    response = helper.dm_account_api.login_api.delete_v1_account_login_all()
    assert response.status_code == 204, f'Не удалось разлогинить пользователя'
