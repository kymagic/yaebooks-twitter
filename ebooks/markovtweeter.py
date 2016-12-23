import csv

"""
Markov-like (probably) tweet generator.

Source file is expected at ./tweets.csv , which any twitter user can download
as their Twitter Archive.
"""
class MarkovTweeter:

    """
    Constructor.

    Arguments:
        << Twitter Archive Loading Options >>
        - ignore_retweets: Whether or not to ignore retweets (default True)
        - ignore_replies:  Whether or not to ignore replies  (default False)
    """
    def __init__(
        self,
        ignore_retweets=True,
        ignore_replies=False):

        self._ignore_retweets = ignore_retweets
        self._ignore_replies = ignore_replies

    """
    Loads the Twitter Archive from the tweets.csv file
    """
    def load_archive(self):
        try:
            with open('tweets.csv') as twitter_archive:
                tweetreader = csv.DictReader(twitter_archive)

                #### Twitter Archive Headers:
                # tweet_id
                # in_reply_to_status_id
                # in_reply_to_user_id
                # timestamp
                # source
                # text
                # retweeted_status_id
                # retweeted_status_user_id
                # retweeted_status_timestamp
                # expanded_urls

                tweet_sample = []

                for tweet in tweetreader:
                    # Check if we should ignore the tweet or not
                    if self._ignore_retweets and tweet['retweeted_status_id']:
                        continue
                    if self._ignore_replies and tweet['in_reply_to_user_id']:
                        continue

                tweet_sample.append(tweet['text'])

                if len(tweet_sample) < 1:
                    raise MarkovException('No usable tweets found in archive')

        except IOError:
            raise MarkovException('Could not load Twitter Archive')

"""
Generic Exception for errors in the MarkovTweeter class
"""
class MarkovException(Exception):
    def __init__(self, message):
        self.message = message
