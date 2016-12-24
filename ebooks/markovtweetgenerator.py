
"""
Generates tweets using a Markov Chain (probably), given some training tweets
"""
class MarkovTweetGenerator:

    """
    Constructor with specified training data

    Arguments:
        - tweets: a list of tweets to train the generator
    """
    def __init__(self, tweets):
        self._tweets = tweets

        self._TWEET_BEGIN = 0
        self._TWEET_END = 1

        self._chain_map = {
            self._TWEET_BEGIN: {},
            self._TWEET_END: None,
        }

        self._generate_chain()

    def _update_map(self, precedent, word):
        if precedent in self._chain_map:
            pMap = self._chain_map[precedent]
            if word in pMap:
                pMap[word] += 1
            else:
                pMap[word] = 1
        else:
            self._chain_map[precedent] = {word: 1}


    def _generate_chain(self):
        for tweet in self._tweets:
            words = tweet.split()
            precedent = self._TWEET_BEGIN
            for word in words:
                if not word.startswith("@"):
                    self._update_map(precedent, word)
                    precedent = word
            self._update_map(word, self._TWEET_END)
