from random import randrange

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

    """
    Pretty-print the given tweet (Array of TweetComponents) into a string
    """
    def format_tweet(self, tweet):
        formatted = ""
        previous_component = TweetComponent(None, TweetComponent.PREFIX)
        for next_component in tweet:
            if previous_component.position != TweetComponent.PREFIX:
                if next_component.position != TweetComponent.SUFFIX:
                    formatted += ' '
            formatted += next_component.content
            previous_component = next_component
        return formatted

    """
    Generate a tweet and return the formatted version
    """
    def get_formatted_tweet(self):
        return self._to_sentence_case(
            self.truncate_tweet(
            self.format_tweet(
            self.generate_tweet())))

    """
    Converts the given (String) tweet into  sentence case
    """
    def _to_sentence_case(self, tweet):
        found_first = False
        tweet_array = list(tweet)
        for i in range(len(tweet)):
            if not found_first:
                if tweet[i].isalpha():
                    found_first = True
                    tweet_array[i] = tweet[i].upper()
            previous_string = tweet[i-2:i]
            if previous_string == '. ' or previous_string == '! ' or previous_string == '; ':
                tweet_array[i] = tweet[i].upper()
        return ''.join(tweet_array)

    """
    Generate a tweet based on the internal chain map
    """
    def generate_tweet(self):
        current_word = TweetComponent(None, TweetComponent.TWEET_BEGIN)
        tweet = []
        while current_word != TweetComponent(None, TweetComponent.TWEET_END):
            # Pick a random word from the possible endings
            # So if we've seen 10 transitions from current_word
            # we pick a number between 0 and 9, and walk along the
            # Chain map entry for the current word until we encounter
            # that number
            possibilities = self._chain_map[current_word]
            count = self._totals[current_word]
            target = randrange(0,count+1)
            for word, count in possibilities.items():
                target -= count
                if target <= 0:
                    current_word = word
                    break
            tweet.append(current_word)
        return tweet[:-1]

    """
    Truncates the (String) tweet to the given length.
    If the given tweet is longer than the supplied length, then it is
    cut to the largest number of words that will fit in
    """
    def truncate_tweet(self, tweet, length=140):
        if len(tweet) > length:
            new_tweet = tweet[0:length]
            # Check if we coincidentally cut at a word boundary
            if tweet[length] != ' ':
                # We didn't; remove everything right of the rightmost space
                new_tweet = new_tweet[0:new_tweet.rfind(' ')]
            return new_tweet
        # If we got here then we did nothing to the tweet
        return tweet

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
                    if not (word.lower().startswith('http:') or word.lower().startswith('https:')):
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
                exploded_tweet.append(TweetComponent(raw_word[len(raw_word)-1], TweetComponent.SUFFIX))
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

    def lower(self):
        if self.content:
            return self.content.lower()
        else:
            return ''

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
