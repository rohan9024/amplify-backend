import pandas as pd
from faker import Faker
import random

# Create a Faker instance to generate random data
fake = Faker()

# Function to generate a random tweet
def generate_tweet():
    tweet = fake.text(max_nb_chars=140)
    # Add random emojis
    tweet += " " + "".join(random.choice(["😀", "😂", "😍", "🚀", "❤️", "🎉", "😊", "🤔", "😎", "🤷", "🤗", "😒", "😃", "😔", "😌", "🤩"]))
    return tweet

# Create a list of tweets
tweets = [generate_tweet() for _ in range(100)]

# Create a DataFrame
df = pd.DataFrame({'Tweet': tweets, 'Sentiment': ''})

# Save the DataFrame to CSV file with UTF-8 encoding
df.to_csv('tweets_dataset.csv', index=False, encoding='utf-8')
