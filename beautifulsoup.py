import requests
from bs4 import BeautifulSoup
import time

def fetch_recent_tweets(username, count=10):
    url = f"https://twitter.com/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        print("Twitter page fetched successfully.")
        soup = BeautifulSoup(response.content, "html.parser")
        tweets = soup.select("div[data-testid='tweet']")

        recent_tweets = []
        for tweet in tweets[:count]:
            tweet_text = tweet.select_one("div[lang]")['aria-label']
            recent_tweets.append(tweet_text)

        return recent_tweets
    else:
        print(f"Failed to fetch tweets. Status code: {response.status_code}")
        return []

if __name__ == "__main__":
    account_name = "eddiejaoude"  # Replace this with the account you want to fetch tweets from
    recent_tweets = fetch_recent_tweets(account_name, count=10)

    if recent_tweets:
        for index, tweet in enumerate(recent_tweets, start=1):
            print(f"{index}. {tweet}")
    else:
        print("No tweets fetched.")
