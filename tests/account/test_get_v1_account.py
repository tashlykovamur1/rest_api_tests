from hamcrest import assert_that, equal_to

from checkers.http_checkers import check_http_status_code


def test_get_v1_account(auth_account_helper):
    helper, user_data = auth_account_helper
    with check_http_status_code():
        response = helper.dm_account_api.account_api.get_v1_account()
        assert_that(response.body['resource']['login'], equal_to(user_data.login))
        assert_that(response.body['resource']['rating']['enabled'], equal_to(True))


def test_get_v1_account_unauth(account_helper):
    with check_http_status_code(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account()
