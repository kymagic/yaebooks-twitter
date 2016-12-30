from markovtweetgenerator import MarkovTweetGenerator
from twitterapi import TwitterApi
from tweetloader import TweetLoader
from argparse import ArgumentParser
import os


def main():

    args = parse_arguments()

    loader = TweetLoader(data_dir=args.data_dir)
    generator = MarkovTweetGenerator(loader.get_tweets())
    tweet = generator.get_formatted_tweet()

    if args.print:
        print(tweet)

    if args.tweet:
        twitter_api = TwitterApi()
        twitter_api.tweet(tweet)

def parse_arguments():

    parser = ArgumentParser()

    input_opts = parser.add_argument_group('input options')

    script_dir = os.path.dirname(os.path.realpath(__file__))
    default_data_dir = os.path.join(script_dir, 'data')
    input_opts.add_argument('-d', '--data-dir',
        help='Location of the data directory',
        default=default_data_dir)

    output_opts = parser.add_argument_group('output options')

    output_opts.add_argument('-t', '--tweet', action='store_true', help='Generated tweet is tweeted via the configured API')
    output_opts.add_argument('-p', '--print', action='store_true', help='Generated tweet is printed to stdout')

    args = parser.parse_args()

    if not (args.tweet or args.print):
        ArgumentParser.exit(1, 'At least one of --tweet or --print must be specified')

    return args

if __name__ == '__main__':
    main()
