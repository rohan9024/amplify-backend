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
data = pd.read_csv("training.csv")
tweets = data["tweet"].tolist()
sentiments = data["sentiment"].tolist()

# Perform sentiment analysis on each tweet and calculate accuracy
predicted_sentiments = []
correct_predictions = 0

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
    predicted_sentiments.append(sentiment_label)

    # Calculate accuracy
    if sentiment_label.lower() == sentiment.lower():
        correct_predictions += 1

# Add predicted sentiments to the dataframe and calculate accuracy
data["predicted_sentiment"] = predicted_sentiments
accuracy = correct_predictions / len(tweets) * 100

print("Accuracy:", accuracy)
