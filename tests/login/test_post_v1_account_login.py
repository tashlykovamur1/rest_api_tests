import json
import random

from clients.account.account_api import AccountApi
from clients.account.login_api import LoginApi
from clients.mailhog.mailhog_api import MailhogApi


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = json.loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            break
    return token


def test_post_v1_account_login():
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = f'tashlykova_test{random.randint(1, 1000)}'
    password = '123456789'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    # регистрация пользователя
    reg_response = account_api.post_v1_account(json_data=json_data)
    print(reg_response.status_code)
    print(reg_response.text)
    assert reg_response.status_code == 201, f'Не удалось зарегистрировать пользователя, {reg_response.json()}'

    # получение письма из почтового сервера
    msg_response = mailhog_api.get_api_v2_messages()
    print(msg_response.status_code)
    print(msg_response.text)
    assert msg_response.status_code == 200, f'Не удалось получить письма'

    # получение активационного токена
    token = get_activation_token_by_login(login, msg_response)
    assert token is not None, f'Не удалось получить токен для пользователя {login}'

    # активация пользователя
    activate_response = account_api.put_v1_account_token(token)

    print(activate_response.status_code)
    print(activate_response.text)
    assert activate_response.status_code == 200, f'Не удалось активировать пользователя'

    # авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    login_response = login_api.put_v1_account_login(json_data)
    print(login_response.status_code)
    print(login_response.text)
    assert login_response.status_code == 200, f'Не удалось авторизовать пользователя'
