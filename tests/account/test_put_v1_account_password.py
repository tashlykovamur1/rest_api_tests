def test_put_v1_account_password(auth_account_helper):
    helper, user_data = auth_account_helper
    new_pwd = '9876543210'

    # Смена пароля
    response = helper.change_user_password(
        login=user_data.login,
        email=user_data.email,
        old_password=user_data.password,
        new_password=new_pwd
    )

    # Авторизация пользователя с новым паролем
    helper.login_user(login=user_data.login, password=new_pwd,
                      auth_header={"x-dm-auth-token": response.headers["X-Dm-Auth-Token"]})
