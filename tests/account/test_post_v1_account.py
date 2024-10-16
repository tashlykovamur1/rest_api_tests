from datetime import datetime

from helpers.account_helper import AccountHelper
from rest_client.configuration import Configuration as MailhogConfiguration
from rest_client.configuration import Configuration as DmApiConfiguration

import structlog

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)
    ]
)


def test_post_v1_account():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = f"tashlykova_{datetime.now().strftime('%Y.%m.%d.%H.%M.%S.%f')}"
    password = '123456789'
    email = f'{login}@mail.ru'

    # регистрация пользователя
    response = account_helper.register_new_user(login=login, password=password, email=email)
    assert response.status_code == 201, f'Не удалось зарегистрировать пользователя, {response.json()}'

    # активация пользователя
    response = account_helper.activate_registered_user(login=login)
    assert response.status_code == 200, f'Не удалось активировать пользователя'

    # авторизация пользователя
    account_helper.login_user(login=login, password=password)
    assert response.status_code == 200, f'Не удалось авторизовать пользователя'

