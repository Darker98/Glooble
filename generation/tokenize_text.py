import spacy
from nltk.tokenize import word_tokenize
import re
import unicodedata
import inflect


# Load spaCy model for lemmatization
nlp = spacy.load("en_core_web_sm")

# Initialize inflect engine for number-to-word conversion
p = inflect.engine()

# Define stopwords to remove
custom_stopwords = {"and", "or", "the", "a", "an", "in", "of", "on", "at", "for", "is", "was", "it", "with", "as",
                    "by", "to", "from", "that", "this", "these", "those", "been", "be", "has", "have", "will",
                    "can", "could", "would", "should", "do", "did", "done", "i", "you", "we", "he", "she", "they",
                    "them", "us", "about"}


# Function to remove non-ASCII characters
def clean_text(word):
    return ''.join(
        c for c in word
        if ord(c) < 128
    )


# Function to remove accents
def remove_accents(input_str):
    # Normalize the string to decompose characters into their base form and diacritical marks
    nfkd_form = unicodedata.normalize('NFKD', input_str)

    # Filter out characters that are diacritical marks (non-spacing marks)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


def tokenize_text(text):
    tokens = []

    # Ensure input is a string; convert non-string to empty string
    if not isinstance(text, str):
        text = ""

    # Step 1: Tokenize the text
    words = word_tokenize(text)

    for word in words:
        # Step 2: Convert numbers to words and remove numbers
        if word.isdigit():
            try:
                word = p.number_to_words(word)
            except:
                continue

        # Step 3: Split hyphenated words
        if '-' in word:
            parts = word.split('-')
            tokens.extend(parts)  # Add split parts to tokens
        else:
            if word.isdecimal():
                continue
            tokens.append(word)

    # Step 4: Remove punctuation and handle capitalization
    cleaned_tokens = []
    for token in tokens:
        # Remove punctuation
        token = re.sub(r'[^\w\s]', '', token)
        token = token.lower()
        cleaned_tokens.append(token)

    # Step 5: Remove non-ASCII characters and normalize accent characters
    cleaned_tokens = [clean_text(remove_accents(token)) for token in cleaned_tokens if token]

    # Step 6: Lemmatize tokens using spaCy
    lemmatized_tokens = []
    doc = nlp(' '.join(cleaned_tokens))
    for token in doc:
        # Step 7: Remove stopwords
        if token.text not in custom_stopwords:
            # Truncate long words to 30 characters
            truncated_lemma = token.lemma_[:30] if len(token.lemma_) > 30 else token.lemma_

            lemmatized_tokens.append(truncated_lemma)

    return lemmatized_tokens
