from textblob import TextBlob
import re
import time

def correct_query(query):
    """Handles the incoming query, performs spell check, and retrieves common docIDs and their details."""
    start = time.time()

    # Split the query into words by non-alphanumeric characters (punctuation, spaces)
    words = re.findall(r'\b\w+\b', query)  # This will match words consisting of letters or digits

    # Create a TextBlob object from the query
    blob = TextBlob(query)

    corrected_query = str(blob.correct())  # Correct the entire query using TextBlob's correct method

    # List to store (original_word, corrected_word) pairs
    word_corrections = []

    # Compare each word in the original query to its corrected version
    for word in words:
        # Create a TextBlob object for each word
        word_blob = TextBlob(word)
        corrected_word = str(word_blob.correct())

        # Only add to word_corrections if the word was actually corrected
        if word != corrected_word:
            word_corrections.append((word, corrected_word))

    print(time.time() - start)
    return corrected_query, word_corrections
