from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from rest_client.client import RestClient


# http://5.63.153.31:5051/index.html?urls.primaryName=Account

class AccountApi(RestClient):

    def post_v1_account(self, registration_json: Registration, **kwargs):
        """
        Register new user
        :param registration_json
        """
        response = self.post(
            path='/v1/account',
            json=registration_json.model_dump(exclude_none=True, by_alias=True),
            **kwargs,
        )
        return response

    def put_v1_account_token(self, token: str, **kwargs):
        """
        Activate registered user
        :param token
        """
        headers = {'accept': 'text/plain'}
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers,
            **kwargs
        )
        return self.format_response(response=response, response_schema=UserEnvelope)

    def put_v1_account_email(self, change_email_json: ChangeEmail, **kwargs):
        """
        Change registered user email
        :param change_email_json
        """
        response = self.put(
            path='/v1/account/email',
            json=change_email_json.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        return self.format_response(response=response, response_schema=UserEnvelope)

    def get_v1_account(self, **kwargs):
        """
        Get current user
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        return self.format_response(response=response, response_schema=UserDetailsEnvelope)

    def put_v1_account_password(self, change_password_json: ChangePassword, **kwargs):
        """
        Change registered user password
        :param change_password_json
        """
        response = self.put(
            path='/v1/account/password',
            json=change_password_json.model_dump(exclude_none=True, by_alias=True),
            **kwargs

        )
        return self.format_response(response=response, response_schema=UserEnvelope)

    def post_v1_account_password(self, reset_password_json: ResetPassword, **kwargs):
        """
        Reset registered user password
        :param reset_password_json
        """
        response = self.post(
            path='/v1/account/password',
            json=reset_password_json.model_dump(exclude_none=True, by_alias=True),
            **kwargs

        )
        return self.format_response(response=response, response_schema=UserEnvelope)
