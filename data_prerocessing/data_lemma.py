import re
import string
import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def lemmatize_text(text):
    """
    Lemmatizes each word using WordNet.
    """
    tokens = text.split()
    lemmatized_tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(lemmatized_tokens)
