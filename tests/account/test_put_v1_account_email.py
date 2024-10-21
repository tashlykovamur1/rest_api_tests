from datetime import datetime


def test_put_v1_account_email(auth_account_helper, prepare_user):
    helper, user_data = auth_account_helper
    login = user_data.login
    password = user_data.password

    # изменение email-а пользователя
    new_email = f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}@mail.ru"
    response = helper.change_user_email(login=login, new_email=new_email, password=password)
    assert response.status_code == 200, f'Не удалось изменить email пользователя'

    # авторизация с новым email-ом
    response = helper.login_user(login=login, password=password)
    assert response.status_code == 403, f'Не удалось получить 403 статус код'

    # активация пользователя c измененным email-ом
    response = helper.activate_registered_user(login=login)
    assert response.status_code == 200, f'Не удалось активировать пользователя'

    # авторизация
    response = helper.login_user(login=login, password=password)
    assert response.status_code == 200, f'Не удалось авторизовать пользователя'

