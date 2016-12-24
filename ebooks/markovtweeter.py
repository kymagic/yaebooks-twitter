import csv
import pickle

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

        filtered_archive = self._load_filtered_archive()
        self._write_sample(filtered_archive)

    """
    Loads the Twitter Archive from the tweets.csv file, keeping only
    tweets that match the filters specified in the constructor

    Arguments:
        - filename: the location of the Twitter Archive (default 'tweets.csv')

    Returns a list of matching tweets, or None if no tweets could be loaded because
    either no tweets matchd the filter, or the archive could not be read
    """
    def _load_filtered_archive(self, filename='tweets.csv'):
        try:
            with open(filename) as twitter_archive:
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
                    return None

                return tweet_sample

        except IOError:
            return None

    """
    Writes the tweet sample to disk.

    Arguments:
        - tweet_sample: A list of tweets
        - filename: The file to write to (default: 'tweets.dat')

    Returns: True if writing was successful, False otherwise
    """
    def _write_sample(self, tweet_sample, filename='tweets.dat'):
        try:
            with open('tweets.dat', mode='wb') as tweet_data:
                pickle.dump(tweet_sample, tweet_data)
                return True

        except IOError:
            return False

"""
Generic Exception for errors in the MarkovTweeter class
"""
class MarkovException(Exception):
    def __init__(self, message):
        self.message = message
