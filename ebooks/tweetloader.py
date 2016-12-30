import csv
import html
import pickle
from util import eprint, md5sum
import os
import sys

"""
Loader class for turning a Twitter Archive into a list of tweets to be used later on.

Source file is expected at ./tweets.csv , which any twitter user can download
as their Twitter Archive.
"""
class TweetLoader:

    """
    Constructor.

    Arguments:
        - ignore_retweets: Whether or not to ignore retweets (default True)
        - ignore_replies:  Whether or not to ignore replies  (default False)
    """
    def __init__(
        self,
        data_dir='./data',
        ignore_retweets=True,
        ignore_replies=False):

        self._data_dir = data_dir
        if not os.path.isdir(self._data_dir):
            eprint('Data directory does not exist')
            sys.exit(1)

        self._ignore_retweets = ignore_retweets
        self._ignore_replies = ignore_replies

        # Try to load an existing archive
        loaded_data =  self._load_sample()
        if not loaded_data:
            # Couldn't load a sample. Try to generate one and write it out
            tweet_sample = self._generate_sample_and_write()
            if not tweet_sample:
                raise LoaderException('Couldn\'t load sample or Twitter Archive')
        else:
            (archive_hash, tweet_sample) = loaded_data
            # Check hash against disk version
            try:
                current_archive_hash = md5sum('tweets.csv')
                if current_archive_hash != archive_hash:
                    # We should try regenerating the archive
                    old_tweet_sample = tweet_sample
                    tweet_sample = self._generate_sample_and_write()
                    # Keep the one we loaded from disk if generating a new one failed
                    if not tweet_sample:
                        tweet_sample = old_tweet_sample
            except IOError:
                # We could not load the Twitter Archive for some reason
                # Fall back to the deserialised version, but first Check
                # that we have something left
                if not tweet_sample:
                    tweet_sample = loaded_data[1]

        self._tweet_sample = tweet_sample

    """
    Returns the list of tweets that were loaded
    """
    def get_tweets(self):
        return self._tweet_sample

    """
    Attempts to generate a new tweet sample from a Twitter Archive.
        * Loads the Twitter Archive from disk
        * Filters the Archive
        * Attempts to write it back out to disk

    Returns: A list of tweets in the tweet sample if one could be loaded and
        filtered; None otherwise
    """
    def _generate_sample_and_write(self):
        (archive_hash, tweet_sample) = self._load_filtered_archive()
        if not tweet_sample:
            return False
        self._write_sample(archive_hash, tweet_sample)
        return tweet_sample

    """
    Loads the Twitter Archive from the tweets.csv file, keeping only
    tweets that match the filters specified in the constructor

    Arguments:
        - filename: the location of the Twitter Archive (default 'tweets.csv')

    Returns: A tuple where the first element is the md5 hash of the archive
        and the second is a list of the filtered tweets. Returns None if
        the archive could not be loaded.
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

                    tweet_sample.append(html.unescape(tweet['text']))

                if len(tweet_sample) < 1:
                    return None

            archive_hash = md5sum(filename)
            return (archive_hash, tweet_sample)

        except IOError:
            return None

    """
    Writes the tweet sample to disk.

    Arguments:
        - tweet_sample: A list of tweets
        - filename: The file to write to (default: 'tweets.dat')

    Returns: True if writing was successful, False otherwise
    """
    def _write_sample(self, archive_hash, tweet_sample, filename='tweets.dat'):
        try:
            with open('tweets.dat', mode='wb') as tweet_data:
                data = (archive_hash, tweet_sample)
                pickle.dump(data, tweet_data)
                return True

        except IOError:
            return False

    """
    Attempts to load a filtered tweet sample from disk

    Returns: A tuple where the first element is the md5 hash of the archive from
        which the tweets were taken, and the second is a list of the filtered
        tweets. Returns None if deserialisation was unsuccessful.
    """
    def _load_sample(self):
        try:
            with open('tweets.dat', mode='rb') as tweet_data:
                deserialised = pickle.load(tweet_data)
                return deserialised
        except IOError:
            return None

"""
Generic Exception for errors in the TweetLoader class
"""
class LoaderException(Exception):
    def __init__(self, message):
        self.message = message
