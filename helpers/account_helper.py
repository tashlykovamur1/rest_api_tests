import json

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password
        }
        reg_response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        return reg_response

    def activate_registered_user(self, login: str):
        token = self.get_activation_token_by_login(login=login)
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

    def get_activation_token_by_login(self, login: str):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f'Не удалось получить письма'
        token = None
        for item in response.json()['items']:
            user_data = json.loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break
        assert token is not None, f'Не удалось получить токен для пользователя {login}'
        return token

    def change_user_email(self, login: str, new_email: str, password: str):
        json_data = {
            'login': login,
            'email': new_email,
            'password': password
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data)
        return response
