from markovtweetgenerator import MarkovTweetGenerator
from twitterapi import TwitterApi
from tweetloader import TweetLoader


def main():
    loader = TweetLoader()
    generator = MarkovTweetGenerator(loader.get_tweets())
    print(generator.get_formatted_tweet())

if __name__ == '__main__':
    main()
