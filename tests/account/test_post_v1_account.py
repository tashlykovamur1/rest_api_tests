import random
from datetime import datetime
import pytest
from hamcrest import assert_that, equal_to, has_entries

from checkers.http_checkers import check_http_status_code


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)

    # авторизация пользователя
    response = account_helper.login_user(login=login, password=password)
    assert_that(response.body['resource']['login'], equal_to(login))


@pytest.mark.parametrize(
    'login, email, password, error_msg',
    [
        (
                f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}",
                f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}@mail.ru",
                ''.join(str(random.randint(0, 9)) for _ in range(5)),
                {"Password": ["Short"]},
        ),
        (
                'a',
                f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}@mail.ru",
                ''.join(str(random.randint(0, 9)) for _ in range(6)),
                {"Login": ["Short"]},
        ),
        (
                f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}",
                f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}mail.ru",
                ''.join(str(random.randint(0, 9)) for _ in range(6)),
                {"Email": ["Invalid"]},
        ),
    ]
)
def test_post_v1_account_negative_data(account_helper, login, email, password, error_msg):
    with check_http_status_code(400, 'Validation failed'):
        response = account_helper.register_new_user(login=login, password=password, email=email)
        assert_that(response, has_entries(
            {'errors': has_entries(error_msg)}
        ))
