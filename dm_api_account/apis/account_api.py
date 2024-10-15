from rest_client.client import RestClient


# http://5.63.153.31:5051/index.html?urls.primaryName=Account

class AccountApi(RestClient):

    def post_v1_account(self, json_data: dict):
        """
        Register new user
        :param json_data
        """
        response = self.post(
            path='/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(self, token: str):
        """
        Activate registered user
        :param token
        """
        headers = {'accept': 'text/plain'}
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        return response

    def put_v1_account_email(self, json_data: dict):
        """
        Change registered user email
        :param new_email
        """
        response = self.put(
            path='/v1/account/email',
            json=json_data
        )
        return response
