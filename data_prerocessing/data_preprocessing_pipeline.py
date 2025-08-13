from data_prerocessing.data_clean import remove_special_chars, lowercase_text
from data_prerocessing.data_stopwords import remove_stopwords
from data_prerocessing.data_lemma import lemmatize_text


def clean_text_pipeline(text, remove_sw=True, do_lemmatize=True):
    """
    Runs full cleaning pipeline: lowercase -> remove special chars -> stopwords removal -> lemmatization
    """
    text = lowercase_text(text)
    text = remove_special_chars(text)
    if remove_sw:
        text = remove_stopwords(text)
    if do_lemmatize:
        text = lemmatize_text(text)
    return text
