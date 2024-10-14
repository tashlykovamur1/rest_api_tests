import requests


# http://5.63.153.31:5051/index.html?urls.primaryName=Account

class LoginApi:
    def __init__(self, host: str, headers=None):
        self.host = host
        self.headers = headers

    def put_v1_account_login(self, json_data: dict):
        """
        Authenticate via credentials
        :param json_data
        """
        response = requests.post(
            url=f'{self.host}/v1/account/login',
            json=json_data
        )
        return response
