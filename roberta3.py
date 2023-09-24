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

# Replace this dictionary with your own containing the number of occurrences of each tweet as keys and the tweet text as values
tweet_dict = {
    1: "This is a negative tweet!",
    2: "I'm feeling worst today!",
    3: "Such a beautiful day!",
    4: "I love this movie!",
    5: "Feeling happy and excited!",
}

# Initialize counters for positive and negative tweets
positive_count = 0
negative_count = 0

for tweet_occurrence, tweet_text in tweet_dict.items():
    tweet_proc = preprocess_tweet(tweet_text)

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
        positive_count += int(tweet_occurrence)
    elif sentiment_label.lower() == "negative":
        negative_count += int(tweet_occurrence)

# Calculate overall score out of 10
total_tweets = sum(int(tweet_occurrence) for tweet_occurrence in tweet_dict.keys())
if positive_count == total_tweets:
    overall_score = 10.0
elif negative_count == total_tweets:
    overall_score = 0.0
else:
    overall_score = (positive_count / total_tweets) * 10

# Round the overall score to 2 decimal places
overall_score = round(overall_score, 2)

print("Overall Score out of 10:", overall_score)
