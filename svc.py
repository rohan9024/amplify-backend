from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from scipy.special import softmax

tweet = 'Great content! subscribed 😉'

# preprocess tweet
tweet_words = []

for word in tweet.split(' '):
    if word.startswith('@') and len(word) > 1:
        word = '@user'
    elif word.startswith('http'):
        word = "http"
    tweet_words.append(word)

tweet_proc = " ".join(tweet_words)

# Convert the tweet into BoW representation for SVM
bow_vectorizer = CountVectorizer()
bow_vectorizer.fit([tweet_proc])  # Fit the vectorizer on the tweet
tweet_bow = bow_vectorizer.transform([tweet_proc])

# Load the SVM model
# Assuming you have trained an SVC model and saved it as 'svc_model.pkl'
import pickle

with open('svc_model.pkl', 'rb') as f:
    svc_model = pickle.load(f)

# Predict sentiment using the SVC model
predicted_label = svc_model.predict(tweet_bow)

print("Predicted Sentiment (SVC):", predicted_label[0])
