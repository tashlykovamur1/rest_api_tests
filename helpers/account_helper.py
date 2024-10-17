import json

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from retrying import retry


def retry_if_result_none(result):
    return result is None


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login: str, password: str, remember_me: bool = True):
        response = self.login_user(login=login, password=password, remember_me=remember_me)
        auth_token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(auth_token)
        self.dm_account_api.login_api.set_headers(auth_token)

    def register_new_user(self, login: str, password: str, email: str):
        self.create_new_user(login=login, password=password, email=email)
        response = self.activate_registered_user(login=login)
        return response

    def create_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password
        }
        reg_response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        return reg_response

    def activate_registered_user(self, login: str):
        token = self.get_token_by_login(login=login)
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    def login_user(self, login: str, password: str, remember_me: bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        return response

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_token_by_login(self, login: str, token_type: str = "activation"):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f'Не удалось получить письма'

        for item in response.json()['items']:
            user_data = json.loads(item['Content']['Body'])
            user_login = user_data.get('Login')
            if user_login == login:
                key_ = "ConfirmationLinkUrl" if token_type == 'activation' else "ConfirmationLinkUri"
                token = user_data.get(key_).split('/')[-1]
                break

        assert token is not None, f'Не удалось получить токен для пользователя {login}'
        return token

    def change_user_email(self, login: str, new_email: str, password: str):
        json_data = {
            'login': login,
            'email': new_email,
            'password': password
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        return response

    def change_user_password(self, login: str, email: str, old_pwd: str, new_pwd: str):
        # сброс пароля
        self.dm_account_api.account_api.post_v1_account_password(json_data={'login': login, 'email': email})

        # получение токена для сброса пароля
        token = self.get_token_by_login(login=login, token_type='reset')

        json_data = {
            'login': login,
            'token': token,
            'oldPassword': old_pwd,
            'newPassword': new_pwd
        }

        # смена пароля
        response = self.dm_account_api.account_api.put_v1_account_password(json_data=json_data)
        auth_token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(auth_token)
        self.dm_account_api.login_api.set_headers(auth_token)
        return response
