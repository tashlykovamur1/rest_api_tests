from rest_client.client import RestClient


class MailhogApi(RestClient):

    def get_api_v2_messages(self, limit: str = 50):
        """
        Get users emails
        """
        params = {'limit': limit}
        response = self.get(
            path='/api/v2/messages',
            params=params,
            verify=False
        )
        return response
