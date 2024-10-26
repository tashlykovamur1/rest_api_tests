from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from rest_client.client import RestClient


# http://5.63.153.31:5051/index.html?urls.primaryName=Account

class AccountApi(RestClient):

    def post_v1_account(self, registration_json: Registration):
        """
        Register new user
        :param registration_json
        """
        response = self.post(
            path='/v1/account',
            json=registration_json.model_dump(exclude_none=True)
        )
        return response

    def put_v1_account_token(self, token: str, validate_response: bool = True):
        """
        Activate registered user
        :param validate_response
        :param token
        """
        headers = {'accept': 'text/plain'}
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json()), response
        return response

    def put_v1_account_email(self, change_email_json: ChangeEmail, validate_response: bool = True):
        """
        Change registered user email
        :param validate_response
        :param change_email_json
        """
        response = self.put(
            path='/v1/account/email',
            json=change_email_json.model_dump(exclude_none=True)
        )
        if validate_response:
            return UserEnvelope(**response.json()), response
        return response

    def get_v1_account(self, validate_response: bool = True, **kwargs):
        """
        Get current user
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json()), response
        return response

    def put_v1_account_password(self, change_password_json: ChangePassword, validate_response: bool = True, **kwargs):
        """
        Change registered user password
        """
        response = self.put(
            path='/v1/account/password',
            json=change_password_json.model_dump(exclude_none=True, by_alias=True),
            **kwargs

        )
        if validate_response:
            return UserEnvelope(**response.json()), response
        return response

    def post_v1_account_password(self, reset_password_json: ResetPassword, validate_response: bool = True, **kwargs):
        """
        Reset registered user password
        """
        response = self.post(
            path='/v1/account/password',
            json=reset_password_json.model_dump(exclude_none=True),
            **kwargs

        )
        if validate_response:
            return UserEnvelope(**response.json()), response
        return response
