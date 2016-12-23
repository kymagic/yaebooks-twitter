import json
import twitter
from util import eprint

class TwitterApi:

    BOT = "bot"
    SRC = "src"

    def __init__(self):
        try:
            credentials_json = open('./credentials.json').read()
        except IOError:
            raise ApiException('Could not read credentials file!')

        self._credentials = json.loads(credentials_json)

        self._api = {
            self.BOT: None,
            self.SRC: None
        }

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

    def tweet(self, message, which):
        self._requireAuth(which)
        self._api[which].PostUpdate(message)

class ApiException(Exception):
    def __init__(self, message):
        self.message = message
