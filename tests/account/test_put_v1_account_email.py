from datetime import datetime


def test_put_v1_account_email(auth_account_helper, prepare_user):
    helper, user_data = auth_account_helper
    login = user_data.login
    password = user_data.password

    # изменение email-а пользователя
    new_email = f"tashlykova_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}@mail.ru"
    helper.change_user_email(login=login, new_email=new_email, password=password)

    # активация пользователя c измененным email-ом
    helper.activate_registered_user(login=login)

    # авторизация
    helper.login_user(login=login, password=password)
