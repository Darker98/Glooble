import time
import threading
import preprocessing
import struct
from flask import Flask, request, jsonify
from flask_cors import CORS
from Lexicon import Lexicon
from inverted_index import BarrelReader
from URLMapper import URLMapper
from hashlib import sha256
from max_frequencies_reader import max_frequency_reader, add_max_frequency_entry
from correction import correct_query

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize global variables
lexicon = Lexicon()
barrel_reader = BarrelReader()
url_mapper = URLMapper()
num_barrels = barrel_reader.num_barrels

# Initialize data
lexicon.read_from_file('files/lexicon.bin')
barrel_reader.load_offsets('barrels/inverted_index/offsets.bin')
url_mapper.read_offsets_from_file('files/offsets.bin')
num_documents, max_frequencies = max_frequency_reader('files/max_frequencies.bin')

# Global variable to store sorted_docIDs for the latest query
global_sorted_docIDs = []
previous_query = ""


def sha_256(data):
    # Compute SHA-256 hash
    hash_value = sha256(data.encode('utf-8')).digest()

    # Extract the first 8 bytes and convert to an integer
    checksum = int.from_bytes(hash_value[:8], byteorder='big')  # Use 'little' if needed

    return checksum


def process_word(word, result):
    """Retrieve docIDs for a single word and append as a set of docIDs with their scores."""
    wordID = lexicon.get_word_id(word)
    docIDs_and_scores = barrel_reader.read_docIDs_and_scores(wordID, num_documents, max_frequencies)

    docID_scores = {}  # Dictionary to store cumulative scores for each docID

    for docID, score in docIDs_and_scores:
        if docID is not None:
            if docID not in docID_scores:
                docID_scores[docID] = score
            else:
                docID_scores[docID] += score  # Add the score if docID is repeated

    result.append(docID_scores)  # Append the dictionary of docID => total_score


# Fetch details of each unique docID
def handle_query(query, use_original):
    """Handles the incoming query and retrieves common docIDs and their details."""
    global global_sorted_docIDs  # Access global variable
    word_corrections = []

    # Correct query
    if not use_original:
        query, word_corrections = correct_query(query)

    words = preprocessing.tokenize_text(query)
    threads = []
    result = []

    for word in words:
        thread = threading.Thread(target=process_word, args=(word, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # If we have common docIDs, retrieve their details
    if result:
        # Find common docIDs across all sets
        common_doc_ids = set.intersection(*[set(docID_scores.keys()) for docID_scores in result])

        # Accumulate scores for common docIDs
        docID_final_scores = {}

        for docID_scores in result:
            for docID, score in docID_scores.items():
                if docID in common_doc_ids:
                    if docID not in docID_final_scores:
                        docID_final_scores[docID] = score
                    else:
                        docID_final_scores[docID] += score

        # Sort docIDs by their final accumulated scores
        global_sorted_docIDs = sorted(docID_final_scores.items(), key=lambda x: x[1], reverse=True)

        return global_sorted_docIDs, word_corrections  # Return the sorted docIDs for pagination

    return [], []  # Return an empty list if no common docIDs are found


def add_article(data):
    # Extract data
    text = data.get('text', '')
    title = data.get('title', '')
    authors = data.get('authors', '')
    tags = data.get('tags', '')
    url = data.get('url', '')

    # Preprocess data
    tokens = preprocessing.tokenize_text(text)
    title_tokens = preprocessing.tokenize_text(title)
    authors_tokens = preprocessing.tokenize_text(authors)
    tags_tokens = preprocessing.tokenize_text(tags)

    # Combine tokens for frequency calculation
    all_tokens = tokens + title_tokens + authors_tokens + tags_tokens

    # Get docID
    docID = sha_256(url)

    # Calculate term frequencies and context flags
    term_frequency = {}
    context_flags = {}

    for token in all_tokens:
        term_frequency[token] = term_frequency.get(token, 0) + 1
        if token not in context_flags:
            # Initialize context flags
            context_flags[token] = 0
        # Set flags based on token occurrence
        if token in title_tokens:
            context_flags[token] |= 1 << 0  # Bit 1: title
        if token in tokens:
            context_flags[token] |= 1 << 1  # Bit 2: text
        if token in tags_tokens:
            context_flags[token] |= 1 << 2  # Bit 3: tags
        if token in authors_tokens:
            context_flags[token] |= 1 << 3  # Bit 4: authors

    # Get the maximum frequency
    max_frequency = max(term_frequency.values())

    # Add tokens to lexicon and inverted index
    for word, frequency in term_frequency.items():
        lexicon.add_word(word)
        wordID = lexicon.get_word_id(word)

        # Retrieve the context flag for the current word
        context_flag = context_flags[word]

        barrel_reader.update_barrel_entry(wordID, docID, (docID, context_flag, frequency))

    # Make entry in URL mapper
    url_mapper.add_entry(docID, url, title, tags, authors, text)

    # Add entry in max frequency file
    add_max_frequency_entry(docID, max_frequency)

    # Update lexicon
    lexicon.write_to_file('files/lexicon.bin')

    # Update global variables
    global num_documents
    global max_frequencies
    num_documents += 1
    max_frequencies[docID] = max_frequency


# Return query response with pagination
@app.route('/query', methods=['POST'])
def query():
    """Endpoint to handle search queries."""
    data = request.get_json()
    query_text = data.get('query', '')
    page_number = data.get('page_number', 1)
    use_original = data.get('use_original', False)
    word_corrections = []

    if not query_text:
        return jsonify({"error": "Query cannot be empty"}), 400

    # Process the query and get results
    global global_sorted_docIDs
    global previous_query
    if not global_sorted_docIDs or query_text != previous_query or use_original:
        # New query or if the query is different from the last one
        global_sorted_docIDs, word_corrections = handle_query(query_text, use_original)
        previous_query = query_text

    if global_sorted_docIDs:
        # Calculate the range of docIDs to return for the requested page
        start_index = (page_number - 1) * 14
        end_index = start_index + 14

        # Get the details of the documents in the specified range
        page_docIDs = global_sorted_docIDs[start_index:end_index]

        doc_details = []
        for docID, _ in page_docIDs:
            details = url_mapper.get_details_by_docID(docID, 'files/url_mapper.bin')
            if details:
                doc_details.append(details)

        return jsonify({"results": doc_details,
                        "total_results": len(global_sorted_docIDs),
                        "corrections": word_corrections})
    else:
        return jsonify({"error": "No results found"}), 404


# Define an endpoint for uploading articles
@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Process the request
        data = request.get_json()
        add_article(data)  # Call your function
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
