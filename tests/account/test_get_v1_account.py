from hamcrest import assert_that, equal_to


def test_get_v1_account(auth_account_helper):
    helper, user_data = auth_account_helper

    response = helper.dm_account_api.account_api.get_v1_account()

    assert_that(response.status_code, equal_to(200),
                f'Не удалось получить пользователя, {response.body, response.error}')
    assert_that(response.body['resource']['login'], equal_to(user_data.login))
    assert_that(response.body['resource']['rating']['enabled'], equal_to(True))

