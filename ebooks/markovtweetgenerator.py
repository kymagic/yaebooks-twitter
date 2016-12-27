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

        self._punctuation = '\'"()[]{}<>,.;:?§±\\+_=-!£€$%^&*/`~'

        self._chain_map = {
            TweetComponent(None, TweetComponent.TWEET_BEGIN): {},
            TweetComponent(None, TweetComponent.TWEET_END): None,
        }

        self._generate_chain()
        self._calculate_totals()

        for precedent, transition_count in self._totals.items():
            print(precedent, transition_count)

        # for precedent, possibilities in self._chain_map.items():
        #     print(precedent)
        #     if precedent.content:
        #         for word, count in possibilities.items():
        #             print(' ', word, count)

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
            if precedent.position != TweetComponent.TWEET_END:
                self._totals[precedent] = sum(map(lambda x: x[1], possiblities.items()))
            else:
                self._totals[TweetComponent(None, TweetComponent.TWEET_END)] = None

    """
    Updates the internal chain map with a word and its preceding word.

    If the sequence "<precedent> <word>" has never been seen before, the
    chain map will include this sequence with a count of 1.

    If the sequence has been seen before, the chain map will increment the count
    on this sequence.
    """
    def _update_map(self, precedent, word):
        if word.content:
            word.content = word.content.lower()
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
            words = self._split_tweet(tweet)
            precedent = TweetComponent(None, TweetComponent.TWEET_BEGIN)
            for word in words[1:]:
                if not word.startswith("@"): # Exclude usernames
                    if not word.startswith('http:'):
                        self._update_map(precedent, word)
                        precedent = word

    """
    Splits a tweet into a list of words.

    This function also handles punctuation like brackets, quotes, and commas.
    Additionally, the TWEET_BEGIN and TWEET_END markers are added

    Arguments:
        - tweet: The tweet to explode, as a string

    Returns: The tweet as an array of TweetComponents, with punctuation marked appropriately
    """
    def _split_tweet(self, tweet):
        exploded_tweet = [TweetComponent(None, TweetComponent.TWEET_BEGIN)]
        for raw_word in tweet.split():
            while len(raw_word) and raw_word[0] in self._punctuation:
                exploded_tweet.append(TweetComponent(raw_word[0], TweetComponent.PREFIX))
                raw_word = raw_word[1:]
            while len(raw_word) and raw_word[len(raw_word)-1] in self._punctuation:
                exploded_tweet.append(TweetComponent(raw_word[0], TweetComponent.SUFFIX))
                raw_word = raw_word[:-1]

            if len(raw_word): # We may have eaten the whole 'word'
                exploded_tweet.append(TweetComponent(raw_word, TweetComponent.WORD))
            else:
                # Regardless, the last item should be a WORD, TWEET_BEGIN, or SUFFIX
                if exploded_tweet[len(exploded_tweet) - 1].position != TweetComponent.SUFFIX:
                    if exploded_tweet[len(exploded_tweet) - 1].position != TweetComponent.TWEET_BEGIN:
                        exploded_tweet[len(exploded_tweet) - 1].position = TweetComponent.WORD

        return exploded_tweet + [TweetComponent(None, TweetComponent.TWEET_END)]

"""
A string in a tweet, tagged with its position
"""
class TweetComponent:

    # Tweet Boundaries
    TWEET_BEGIN = 0
    TWEET_END   = 1

    # E.g. £100 would tag '£' as a PREFIX
    PREFIX      = 2
    SUFFIX      = 3
    WORD        = 4

    def __init__(self, word, position=WORD):
        self.content = word
        self.position = position

    def startswith(self, prefix):
        if self.content == None:
            return False
        else:
            return self.content.startswith(prefix)

    def endswith(self, suffix):
        if self.content == None:
            return False
        else:
            return self.content.endswith(prefix)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        prefix = {
            TweetComponent.TWEET_BEGIN : 'B',
            TweetComponent.TWEET_END   : 'E',
            TweetComponent.PREFIX      : 'P',
            TweetComponent.SUFFIX      : 'S',
            TweetComponent.WORD        : 'W'
        }[self.position]

        return '[' + prefix + '] ' + str(self.content)

    """
    Hash Function. Simply returns the hash of the content and position tuple
    """
    def __hash__(self):
        return hash((self.content, self.position))

    def __eq__(self, other):
        return self.content == other.content and self.position == other.position

    def __neq__(self, other):
        return self.content != other.content or self.position != other.position

    def __lt__(self, other):
        if self.content == other.content:
            return self.position < other.position
        else:
            return self.content < other.content

    def __le__(self, other):
        if self.content == other.content:
            return self.position <= other.position
        else:
            return self.content <= other.content

    def __gt__(self, other):
        if self.content == other.content:
            return self.position > other.position
        else:
            return self.content > other.content

    def __ge__(self, other):
        if self.content == other.content:
            return self.position >= other.position
        else:
            return self.content >= other.content
