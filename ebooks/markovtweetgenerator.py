
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
        self._calculate_totals()

    """
    Generate a tweet based on the internal chain map
    """
    def generate_tweet(self):
        pass

    """
    Generate a list of the total number of observed transitions from each
    precedent in the chain map.

    E.g. if the tweets list was as follows:
        [
            "Hello bob",
            "Hello bob",
            "Hello john"
        ]

    The count for "hello" would be 3 because we have seen a transition FROM
    "hello" three times (but only to two words)
    """
    def _calculate_totals(self):
        self._totals = {}
        for precedent, possiblities in self._chain_map.items():
            if precedent != self._TWEET_END:
                self._totals[precedent] = sum(map(lambda x: x[1], possiblities.items()))
            else:
                self._totals[self._TWEET_END] = None

        for precedent, count in self._totals.items():
            print(precedent, count)

    """
    Updates the internal chain map with a word and its preceding word.

    If the sequence "<precedent> <word>" has never been seen before, the
    chain map will include this sequence with a count of 1.

    If the sequence has been seen before, the chain map will increment the count
    on this sequence.
    """
    def _update_map(self, precedent, word):
        if precedent in self._chain_map:
            if word in self._chain_map[precedent]:
                self._chain_map[precedent][word] += 1
            else:
                self._chain_map[precedent][word] = 1
        else:
            self._chain_map[precedent] = {word: 1}

    """
    Populates the internal chain map with the number of times each given
    word transition has been seen. E.g. if the tweets list was as follows:
        [
            "Hello bob",
            "Hello bob",
            "Hello john"
        ]

    then the resulting chain map would be:

        TWEET_BEGIN => "Hello"  : 3
        "Hello"     => "bob"    : 2
        "Hello"     => "john"   : 1
        "bob"       => TWEET_END: 2
        "john"      => TWEET_END: 1
    """
    def _generate_chain(self):
        for tweet in self._tweets:
            words = tweet.split()
            precedent = self._TWEET_BEGIN
            for word in words:
                # Strip out some clutter we don't want
                if word.startswith('\'') or word.startswith('"'):
                    word = word[1:]
                if word.endswith('\'') or word.endswith('"'):
                    word = word[:-1]
                if word.startswith('(') or word.startswith('['):
                    word = word[1:]
                if word.endswith(']') or word.endswith(')'):
                    word = word[:-1]
                if not word.startswith("@"): # Exclude usernames
                    if not word.startswith('http:'):
                        self._update_map(precedent, word)
                        precedent = word

            self._update_map(precedent, self._TWEET_END)
