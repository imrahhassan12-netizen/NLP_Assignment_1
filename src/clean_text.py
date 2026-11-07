
from pathlib import Path
import pandas as pd
import re
import unicodedata
from nltk.stem import PorterStemmer

# Project folders
PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_DIR / "data" / "processed" / "imdb_reviews.csv"
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "cleaned_reviews.csv"

# Stemmer
stemmer = PorterStemmer()

# Stopwords: common words that usually carry little meaning
# Negation words are deliberately preserved.
STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "am", "be", "been", "being", "and", "or", "but",
    "of", "to", "in", "on", "at", "for", "with",
    "this", "that", "these", "those", "it", "its",
    "he", "she", "they", "them", "we", "you", "i",
    "my", "your", "our", "their", "me", "him", "her",
    "as", "by", "from", "so", "if", "then", "than",
    "too", "very", "can", "could", "would", "should",
    "have", "has", "had", "do", "does", "did"
}

def clean_text(text):
    # 1. Unicode normalization
    text = unicodedata.normalize("NFKC", str(text))

    # 2. Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # 3. Convert to lowercase
    text = text.lower()

    # 4. Extract words
    tokens = re.findall(r"\b[a-z0-9]+\b", text)

    # 5. Remove stopwords and apply stemming
    cleaned_tokens = [
        stemmer.stem(word)
        for word in tokens
        if word not in STOPWORDS
    ]

    return " ".join(cleaned_tokens)


# Load dataset
df = pd.read_csv(INPUT_FILE)

# Calculate vocabulary before cleaning
before_tokens = [
    word
    for review in df["review"]
    for word in re.findall(r"\b\w+\b", str(review).lower())
]

# Apply cleaning function
df["cleaned_review"] = df["review"].apply(clean_text)

# Calculate vocabulary after cleaning
after_tokens = [
    word
    for review in df["cleaned_review"]
    for word in review.split()
]

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print("Cleaning completed successfully!")
print("Total reviews:", len(df))
print("Vocabulary before cleaning:", len(set(before_tokens)))
print("Vocabulary after cleaning:", len(set(after_tokens)))
print("\nOriginal review:")
print(df["review"].iloc[0][:300])
print("\nCleaned review:")
print(df["cleaned_review"].iloc[0][:300])
print("\nSaved at:", OUTPUT_FILE)
