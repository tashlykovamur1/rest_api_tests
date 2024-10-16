from rest_client.client import RestClient


# http://5.63.153.31:5051/index.html?urls.primaryName=Account

class LoginApi(RestClient):

    def post_v1_account_login(self, json_data: dict):
        """
        Authenticate via credentials
        :param json_data
        """
        response = self.post(
            path='/v1/account/login',
            json=json_data
        )
        return response
