import tweepy
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

bearer_key = config['twitter']['bearer_key']
auth = tweepy.OAuth2BearerHandler(bearer_key)
api = tweepy.API(auth)

username = 'imVkohli'

# Fetch one tweet
tweet_id = "1420294875412086272"  # Replace with the tweet ID you want to fetch
tweet = api.get_status(tweet_id, tweet_mode='extended')

# Print the tweet content
print("Tweet ID:", tweet.id_str)
print("Author:", tweet.user.screen_name)
print("Content:", tweet.full_text)
print("Retweets:", tweet.retweet_count)
print("Likes:", tweet.favorite_count)