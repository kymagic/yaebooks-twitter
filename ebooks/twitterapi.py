import json
import twitter
from util import eprint

"""
Wrapper class for the Twitter API.

On initialisation, the class expects credtials for the bot account to be in a
JSON file located at ./credentials.json . The structure for the JSON object
can be seen in the file credentials.json.sample .

Authentication is performed at the point when an API call is needed, though
this class will throw an exception in the constructor if the credentials file
cannot be read or deserialised.
"""
class TwitterApi:

    """
    Default constructor. Attempts to load the credentials file, and will fail
    if this is not possible.
    """
    def __init__(self):
        try:
            credentials_json = open('./credentials.json').read()
        except IOError:
            raise ApiException('Could not read credentials file!')

        self._credentials = json.loads(credentials_json)

        # The API object will live here
        self._api = None

    """
    Gatekeeper method checking that the API is authenticated.
    """
    def _requireAuth(self):
        if self._api == None:
            self._api = twitter.Api(
                consumer_key = self._credentials['consumer_key'],
                consumer_secret = self._credentials['consumer_secret'],
                access_token_key = self._credentials['access_token_key'],
                access_token_secret = self._credentials['access_token_secret']
            )

        if self._api[which] == None:
            raise ApiException('Could not authenticate API')

    """
    Send a tweet
    """
    def tweet(self, message):
        self._requireAuth()
        self._api.PostUpdate(message)

"""
Generic Exception for errors in the TwitterAPI class
"""
class ApiException(Exception):
    def __init__(self, message):
        self.message = message
