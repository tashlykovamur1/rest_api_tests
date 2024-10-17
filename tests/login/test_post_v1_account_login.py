def test_post_v1_account_login(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # регистрация пользователя
    response = account_helper.register_new_user(login=login, password=password, email=email)

    # авторизация пользователя
    account_helper.login_user(login=login, password=password)
    assert response.status_code == 200, f'Не удалось авторизовать пользователя'
