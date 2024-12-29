from spellchecker import SpellChecker
import re


def handle_query(query):
    """Handles the incoming query, performs spell check, and retrieves common docIDs and their details."""
    # Split the query into words by non-alphanumeric characters (punctuation, spaces)
    words = re.findall(r'\b\w+\b', query)  # This will match words consisting of letters or digits

    spell = SpellChecker()
    misspelled = spell.unknown(words)  # Find words that are misspelled

    corrected_pairs = []

    for word in misspelled:
        corrected_word = spell.correction(word)  # Get the most likely correction
        corrected_pairs.append((word, corrected_word))  # Append the pair to the list

    return corrected_pairs


print(handle_query("seach engiee queri documetn"))