import json
import twitter
from util import eprint

"""
Wrapper class for the Twitter API.

Handles two api connections: one for the source account,
and one for the bot that will tweet the 'ebooks' version.

Methods relating to these two take a which argument, specifying which
account the action should be performed on. Pass to these methods one of the following:
    - self.BOT
    - self.SRC

On initialisation, the class expects credtials for both accounts to be in a
JSON file located at ./credentials.json . The structure for the JSON object
can be seen in the file credentials.json.sample .

Authentication is performed at the point when an API call is needed, though
this class will throw an exception in the constructor if the credentials file
cannot be read or deserialised.
"""
class TwitterApi:

    BOT = "bot"
    SRC = "src"

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

        # Create the variables to store the API objects in
        self._api = {
            self.BOT: None,
            self.SRC: None
        }

    """
    Gatekeeper method checking that the requested API is authenticated.
    """
    def _requireAuth(self, which):
        if self._api[which] == None:
            self._api[which] = twitter.Api(
                consumer_key = self._credentials[which]['consumer_key'],
                consumer_secret = self._credentials[which]['consumer_secret'],
                access_token_key = self._credentials[which]['access_token_key'],
                access_token_secret = self._credentials[which]['access_token_secret']
            )

        if self._api[which] == None:
            raise ApiException('Could not authenticate API for', which)

    """
    Send a tweet as the specified account
    """
    def tweet(self, message, which):
        self._requireAuth(which)
        self._api[which].PostUpdate(message)

"""
Generic Exception for errors in the TwitterAPI class
"""
class ApiException(Exception):
    def __init__(self, message):
        self.message = message
