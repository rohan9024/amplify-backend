from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# tweet = "@MehranShakarami today's cold @ home 😒 https://mehranshakarami.com"
tweet = 'Worst content! subscribed 😉'

# precprcess tweet
tweet_words = []

for word in tweet.split(' '):
    if word.startswith('@') and len(word) > 1:
        word = '@user'
    
    elif word.startswith('http'):
        word = "http"
    tweet_words.append(word)

tweet_proc = " ".join(tweet_words)

# load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

# sentiment analysis
encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
output = model(**encoded_tweet)

scores = output.logits[0].detach().numpy()
scores = softmax(scores)

# Find the label with the highest score
index = scores.argmax()
sentiment_label = labels[index]

print("Sentiment: ", sentiment_label)
