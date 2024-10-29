from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_http_status_code


def test_get_v1_account(auth_account_helper):
    helper, user_data = auth_account_helper

    with check_http_status_code():
        response = helper.dm_account_api.account_api.get_v1_account()

    GetV1Account.check_received_user_info(response=response, login=user_data.login)


def test_get_v1_account_unauth(account_helper):
    with check_http_status_code(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account()
