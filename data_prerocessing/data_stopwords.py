import re
import string
import nltk
from nltk.corpus import stopwords

# Download NLTK resources (only needed once)
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")


stop_words = set(stopwords.words("english"))


def remove_stopwords(text):
    """
    Removes common English stopwords.
    """
    tokens = text.split()
    filtered_tokens = [t for t in tokens if t not in stop_words]
    return " ".join(filtered_tokens)
