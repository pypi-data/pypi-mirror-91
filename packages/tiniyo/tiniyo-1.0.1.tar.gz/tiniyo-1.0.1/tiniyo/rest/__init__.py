from twilio.rest import Client as TwilioClient
from twilio.rest.api import Api as TwilioApi

class Client(TwilioClient):
    def __init__(self, username=None, password=None, account_sid=None, region=None,
                 http_client=None, environment=None, edge=None):
        super().__init__(self, username, password, account_sid, region, http_client, environment, edge)
        self._api = TwilioApi(self)
        self._api.base_url = 'https://api.tiniyo.com'
