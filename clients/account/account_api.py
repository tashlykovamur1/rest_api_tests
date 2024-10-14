import requests


# http://5.63.153.31:5051/index.html?urls.primaryName=Account

class AccountApi:
    def __init__(self, host: str, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account(self, json_data: dict):
        """
        Register new user
        :param json_data
        """
        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(self, token: str):
        """
        Activate registered user
        :param token
        """
        headers = {'accept': 'text/plain'}
        response = requests.put(
            url=f'{self.host}/v1/account/{token}',
            headers=headers
        )
        return response

    def put_v1_account_email(self, json_data: dict):
        """
        Change registered user email
        :param new_email
        """
        response = requests.put(
            url=f'{self.host}/v1/account/email',
            json=json_data
        )
        return response
