from markovtweetgenerator import MarkovTweetGenerator
from twitterapi import TwitterApi
from tweetloader import TweetLoader
from argparse import ArgumentParser


def main():

    args = parse_arguments()

    loader = TweetLoader()
    generator = MarkovTweetGenerator(loader.get_tweets())
    tweet = generator.get_formatted_tweet()

    if args.print:
        print(tweet)

    if args.tweet:
        twitter_api = TwitterApi()
        twitter_api.tweet(tweet)

def parse_arguments():

    parser = ArgumentParser()

    output_opts = parser.add_argument_group('output options')

    output_opts.add_argument('-t', '--tweet', action='store_true', help='Generated tweet is tweeted via the configured API')
    output_opts.add_argument('-p', '--print', action='store_true', help='Generated tweet is printed to stdout')

    args = parser.parse_args()

    if not (args.tweet or args.print):
        ArgumentParser.exit(1, 'At least one of --tweet or --print must be specified')

    return args

if __name__ == '__main__':
    main()
