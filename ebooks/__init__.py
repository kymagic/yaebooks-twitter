from markovtweetgenerator import MarkovTweetGenerator
from twitterapi import TwitterApi
from tweetloader import TweetLoader


def main():
    loader = TweetLoader()
    generator = MarkovTweetGenerator(loader.get_tweets())

if __name__ == '__main__':
    main()
