from datetime import datetime

import structlog

from helpers.account_helper import AccountHelper
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

from rest_client.configuration import Configuration as MailhogConfiguration
from rest_client.configuration import Configuration as DmApiConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)
    ]
)


def test_put_v1_account_email():
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

    # изменение email-а пользователя
    new_email = f"tashlykova_{datetime.now().strftime('%Y.%m.%d.%H.%M.%S.%f')}@mail.ru"
    response = account_helper.change_user_email(login=login, new_email=new_email, password=password)
    assert response.status_code == 200, f'Не удалось изменить email пользователя'

    # авторизация с новым email-ом
    response = account_helper.login_user(login=login, password=password)
    assert response.status_code == 403, f'Не удалось получить 403 статус код'

    # активация пользователя c измененным email-ом
    response = account_helper.activate_registered_user(login=login)
    assert response.status_code == 200, f'Не удалось активировать пользователя'

    # авторизация
    response = account_helper.login_user(login=login, password=password)
    assert response.status_code == 200, f'Не удалось авторизовать пользователя'

