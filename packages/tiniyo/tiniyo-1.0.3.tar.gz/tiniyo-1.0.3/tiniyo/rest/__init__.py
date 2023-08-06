from twilio.rest import Client as TwilioClient
from twilio.rest.api import Api as TwilioApi
from twilio.rest.api.v2010 import V2010 as TwilioV2010

def tiniyo_version(self,domain):
  super(V2010, self).__init__(domain)
  self.version = "v1"

class Client(TwilioClient):
    def __init__(self, username=None, password=None, account_sid=None, region=None,
                 http_client=None, environment=None):
        super().__init__(username,password, account_sid, region, http_client, environment)
        self._api = TwilioApi(self)
        self._api.base_url = 'https://api.tiniyo.com'
        self._api._v2010 = TwilioV2010(self._api)
        self._api._v2010.version = "v1"

