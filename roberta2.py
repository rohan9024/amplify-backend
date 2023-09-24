import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Define the preprocess_tweet function


def preprocess_tweet(tweet):
    tweet_words = []
    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)
    return " ".join(tweet_words)


# Load pre-trained model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

# Read data from CSV
data = pd.read_csv("training2.csv")
tweets = data["tweet"].tolist()
sentiments = data["sentiment"].tolist()

# Initialize counters for positive and negative tweets
positive_count = 0
negative_count = 0

for tweet, sentiment in zip(tweets, sentiments):
    tweet_proc = preprocess_tweet(tweet)

    # Sentiment analysis
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)

    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)

    # Find the label with the highest score
    index = scores.argmax()
    sentiment_label = labels[index]

    # Count positive and negative tweets
    if sentiment_label.lower() == "positive":
        positive_count += 1
    elif sentiment_label.lower() == "negative":
        negative_count += 1

# Calculate overall score out of 10
total_tweets = len(tweets)
if positive_count == total_tweets:
    overall_score = 10.0
elif negative_count == total_tweets:
    overall_score = 0.0
else:
    overall_score = (positive_count / total_tweets) * 10

# Calculate overall score out of 10
total_positive_tweets = positive_count
overall_score = (total_positive_tweets / total_tweets) * 10

# Round the overall score to 2 decimal places
overall_score = round(overall_score, 2)

print(overall_score)