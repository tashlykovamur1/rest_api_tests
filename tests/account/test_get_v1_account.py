def test_get_v1_account(auth_account_helper):
    helper, _ = auth_account_helper
    _, response = helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 200, f'Не удалось получить пользователя, {response.json()}'
