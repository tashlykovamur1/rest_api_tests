from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from rest_client.client import RestClient


# http://5.63.153.31:5051/index.html?urls.primaryName=Account

class LoginApi(RestClient):

    def post_v1_account_login(self, login_credentials_json: LoginCredentials, **kwargs):
        """
        Authenticate via credentials
        :param login_credentials_json
        """
        response = self.post(
            path='/v1/account/login',
            json=login_credentials_json.model_dump(exclude_none=True, by_alias=True),
            **kwargs,
        )
        return self.format_response(response=response, response_schema=UserEnvelope)

    def delete_v1_account_login(self, **kwargs):
        """
        Logout as current user
        """
        response = self.delete(
            path='/v1/account/login',
            **kwargs
        )
        return response

    def delete_v1_account_login_all(self, **kwargs):
        """
        Logout from every device
        """
        response = self.delete(
            path='/v1/account/login/all',
            **kwargs
        )
        return response
