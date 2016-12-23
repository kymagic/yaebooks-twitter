from twitterapi import TwitterApi


def main():
    twapi = TwitterApi()
    twapi.tweet("Tweep Tweep", twapi.BOT)
    twapi.tweet("Twoop Twoop", twapi.SRC)

if __name__ == '__main__':
    main()
