def test_put_v1_account_password(auth_account_helper):
    helper, user_data = auth_account_helper
    new_pwd = '9876543210'

    # Смена пароля
    response = helper.change_user_password(
        login=user_data.login,
        email=user_data.email,
        old_pwd=user_data.password,
        new_pwd=new_pwd
    )
    assert response.status_code == 200, f'Не удалось сменить пароль пользователя'

    # Авторизация пользователя с новым паролем
    helper.login_user(login=user_data.login, password=new_pwd)
    assert response.status_code == 200, f'Не удалось авторизовать пользователя с новым паролем'
