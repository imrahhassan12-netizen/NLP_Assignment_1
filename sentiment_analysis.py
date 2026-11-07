
import pandas as pd
import nltk
import re

from nltk.corpus import stopwords
from collections import Counter

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

print("MOVIE REVIEW SENTIMENT ANALYSIS")

# Load Dataset
data = pd.read_csv("movie_reviews.csv")

print("\nMovie Reviews Dataset:")
print(data.head())

print("\nDataset Shape:")
print(data.shape)

print("\nSentiment Distribution:")
print(data["sentiment"].value_counts())

# Text Preprocessing
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

data["cleaned_review"] = data["review"].apply(clean_text)

print("\nCleaned Movie Reviews:")
print(data[["review", "cleaned_review"]].head())

# Tokenization
data["tokens"] = data["cleaned_review"].apply(lambda x: x.split())

print("\nTokenized Reviews:")
print(data[["cleaned_review", "tokens"]].head())

# Word Frequency
all_words = []

for words in data["tokens"]:
    all_words.extend(words)

word_frequency = Counter(all_words)

print("\nMost Common Words:")
print(word_frequency.most_common(10))

# Machine Learning Model
X = data["cleaned_review"]
y = data["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# TF-IDF
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Logistic Regression
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Prediction
y_pred = model.predict(X_test_tfidf)

# Evaluation
print("\nModel Accuracy:")
print(accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nPROGRAM COMPLETED SUCCESSFULLY!")

# Test New Movie Reviews
print("\nNew Movie Review Predictions:")

new_reviews = [
    "This movie was fantastic and enjoyable",
    "This film was boring and terrible",
    "I loved this wonderful movie"
]

for review in new_reviews:
    cleaned = clean_text(review)
    tfidf = vectorizer.transform([cleaned])
    prediction = model.predict(tfidf)
    print("Review:", review)
    print("Predicted Sentiment:", prediction[0])
    print("---------------------------")
