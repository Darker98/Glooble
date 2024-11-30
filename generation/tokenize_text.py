import contractions
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
import unicodedata

# Function to remove non-ascii characters
def clean_text(word):
    return ''.join(
        c for c in word
        if ord(c) < 128
    )

# Function to remove accents
def remove_accents(input_str):
    """
    Removes accents from characters in the input string.

    :param input_str: The string from which to remove accents
    :return: A string with accents removed
    """
    # Normalize the string to decompose characters into their base form and diacritical marks
    nfkd_form = unicodedata.normalize('NFKD', input_str)

    # Filter out characters that are diacritical marks (non-spacing marks)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def tokenize_text(text):
    stemmer = PorterStemmer()
    tokens = []

    # Step 1: Expand contractions
    expanded_text = contractions.fix(text)

    # Step 2: Tokenize the text
    words = word_tokenize(expanded_text)

    for word in words:
        # Step 3: Split hyphenated words
        if '-' in word:
            parts = word.split('-')
            tokens.extend(parts)  # Add split parts to tokens
        else:
            if word.isdigit() or word.isdecimal():
                continue
            tokens.append(word)

    # Step 4: Store contractions by removing apostrophes
    additional_tokens = []
    for token in word_tokenize(text):
        if "'" in token:
            additional_tokens.append(re.sub(r"'", "", token))  # Remove apostrophe
    tokens.extend(additional_tokens)

    # Step 5: Remove punctuation and handle capitalization
    cleaned_tokens = []
    for i, token in enumerate(tokens):
        # Remove punctuation
        token = re.sub(r'[^\w\s]', '', token)

        cleaned_tokens.append(token)

    # Step 6: Stem the tokens
    stemmed_tokens = [stemmer.stem(token) for token in cleaned_tokens if token]

    # Step 7: Remove non-ASCII and accent characters
    stemmed_tokens = [clean_text(remove_accents(token)) for token in stemmed_tokens]

    return stemmed_tokens