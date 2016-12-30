# Yet Another Ebooks Bot
This is my own attempt at an ebooks twitter bot.

## Setup
1. Copy `credentials.json.sample` to `credentials.json` and fill in the twitter
authentication tokens for the bot account to tweet the tweets. More information
about API tokens can be found at https://dev.twitter.com/oauth/overview/application-owner-access-tokens .

2. Download your Twitter Archive. See https://support.twitter.com/articles/20170160 .

3. Copy the `tweets.csv` file from your archive and place it in the root of the
git repository.

## Usage
See `python3 __init__.py -h` for available options.

## Requirements
* python 3 (tested on 3.6.0)
* `python-twitter`
