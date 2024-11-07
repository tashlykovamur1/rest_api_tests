import random
import string
from collections import namedtuple
from datetime import datetime
from pathlib import Path

import allure
from vyper import v
import pytest
from helpers.account_helper import AccountHelper
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from rest_client.configuration import Configuration as MailhogConfiguration
from rest_client.configuration import Configuration as DmApiConfiguration

import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)
    ]
)

options = (
    "service.dm_api_account",
    "service.mailhog"
)  # из yaml файлов


@pytest.fixture(scope="session", autouse=True)
def set_config(request):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()

    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="stg", help="run stg")
    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get("service.mailhog"))
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"))
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@allure.title("Регистрация и авторизация пользователя")
@pytest.fixture
def auth_account_helper(mailhog_api, prepare_user):
    account = DMApiAccount(configuration=DmApiConfiguration(host=v.get("service.dm_api_account")))
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.auth_client(
        login=login,
        password=password
    )
    return account_helper, prepare_user


@pytest.fixture
def prepare_user():
    date_now = datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + f'_{datetime.now().microsecond // 1000:03d}'
    login = f"tashlykova_{date_now}"
    password = '123456789'
    email = f'{login}@mail.ru'
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user
