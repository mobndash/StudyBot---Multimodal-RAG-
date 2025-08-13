import re
import string
import nltk


def remove_special_chars(text):
    """
    Removes punctuation, extra whitespace, and non-printable characters.
    """
    # Remove non-printable chars
    text = "".join(c for c in text if c.isprintable())
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Remove multiple spaces and line breaks
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def lowercase_text(text):
    """Converts text to lowercase."""
    return text.lower()
