from mailhog.apis.mailhog_api import MailhogApi
from rest_client.configuration import Configuration


class MailHogApi:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mailhog_api = MailhogApi(configuration=self.configuration)
