import json

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
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
            "x-dm-auth-token": response.headers["X-Dm-Auth-Token"]
        }
        self.dm_account_api.account_api.set_headers(auth_token)
        self.dm_account_api.login_api.set_headers(auth_token)

    def register_new_user(self, login: str, password: str, email: str):
        self.create_new_user(login=login, password=password, email=email)
        response = self.activate_registered_user(login=login)
        return response

    def create_new_user(self, login: str, password: str, email: str):
        registration = Registration(
            login=login,
            email=email,
            password=password
        )
        reg_response = self.dm_account_api.account_api.post_v1_account(registration_json=registration)
        assert reg_response.status_code == 201, f'Не удалось создать пользователя'
        return reg_response

    def activate_registered_user(self, login: str):
        token = self.get_token_by_login(login=login)
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f'Не удалось активировать пользователя'
        return response

    def login_user(self, login: str, password: str, remember_me: bool = True):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me,
        )

        response = self.dm_account_api.login_api.post_v1_account_login(login_credentials_json=login_credentials)
        assert response.status_code == 200, f'Не удалось авторизовать пользователя с новым паролем'
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
        change_email = ChangeEmail(
            login=login,
            email=new_email,
            password=password
        )
        response = self.dm_account_api.account_api.put_v1_account_email(change_email_json=change_email)
        assert response.status_code == 200, f'Не удалось изменить email пользователя'
        return response

    def change_user_password(self, login: str, email: str, old_password: str, new_password: str):
        # сброс пароля
        reset_password = ResetPassword(
            login=login, email=email
        )
        response = self.dm_account_api.account_api.post_v1_account_password(reset_password_json=reset_password)
        assert response.status_code == 200, f'Не удалось сбросить пароль пользователя'

        # получение токена для сброса пароля
        token = self.get_token_by_login(login=login, token_type='reset')

        change_password = ChangePassword(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
        )

        # смена пароля
        response = self.dm_account_api.account_api.put_v1_account_password(change_password_json=change_password)
        assert response.status_code == 200, f'Не удалось изменить пароль пользователя'

        auth_token = {
            "x-dm-auth-token": response.headers["X-Dm-Auth-Token"]
        }
        self.dm_account_api.account_api.set_headers(auth_token)
        self.dm_account_api.login_api.set_headers(auth_token)
        return response
