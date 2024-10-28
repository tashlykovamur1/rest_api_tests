def test_put_v1_account_token(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # регистрация пользователя
    account_helper.create_new_user(login=login, password=password, email=email)

    # активация пользователя
    account_helper.activate_registered_user(login=login)
