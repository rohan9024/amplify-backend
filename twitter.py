import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "python"
tweets = []
limit = 100
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    print(vars(tweet))

    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.user.username, tweet.content])


df = pd.DataFrame(tweets, columns=['Dates', 'User', 'Tweet'])

print(df)
