import spacy
from nltk.tokenize import word_tokenize
import re
import unicodedata
import inflect


# Load spaCy model for lemmatization
nlp = spacy.load("en_core_web_sm")

# Initialize inflect engine for number-to-word conversion
p = inflect.engine()


# Function to remove non-ASCII characters
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
    tokens = []
    custom_stopwords = {"and", "or", "the", "a", "an", "in", "of", "on", "at", "for", "is", "was", "it", "with", "as",
                        "by", "to", "from", "that", "this", "these", "those", "been", "be", "has", "have", "will",
                        "can", "could", "would", "should", "do", "did", "done", "i", "you", "we", "he", "she", "they",
                        "them", "us", "about"}

    # Ensure input is a string; convert non-string to empty string
    if not isinstance(text, str):
        text = ""

    # Step 1: Tokenize the text
    words = word_tokenize(text)

    for word in words:
        # Step 2: Convert numbers to words and remove numbers
        if word.isdigit():
            number_word = p.number_to_words(word)
            tokens.append(number_word)
        else:
            # Step 3: Split hyphenated words
            if '-' in word:
                parts = word.split('-')
                tokens.extend(parts)  # Add split parts to tokens
            else:
                if word.isdecimal:
                    continue
                tokens.append(word)

    # Step 4: Remove punctuation and handle capitalization
    cleaned_tokens = []
    for token in tokens:
        # Remove punctuation
        token = re.sub(r'[^\w\s]', '', token)

        cleaned_tokens.append(token)

    # Step 5: Remove non-ASCII and accent characters
    cleaned_tokens = [clean_text(remove_accents(token)) for token in cleaned_tokens if token]

    # Step 6: Lemmatize tokens using spaCy
    lemmatized_tokens = []
    doc = nlp(' '.join(cleaned_tokens))
    for token in doc:
        # Step 7: Remove stopwords
        if token not in custom_stopwords:
            lemmatized_tokens.append(token.lemma_)

    return lemmatized_tokens
