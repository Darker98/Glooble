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
from max_frequencies_reader import max_frequency_reader

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
    hash_value = sha256(data).digest()

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
def handle_query(query):
    """Handles the incoming query and retrieves common docIDs and their details."""
    global global_sorted_docIDs  # Access global variable
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

        return global_sorted_docIDs  # Return the sorted docIDs for pagination

    return []  # Return an empty list if no common docIDs are found


def add_article(data):
    # Extract data
    text = data.get('text', '')
    title = data.get('title', '')
    authors = data.get('authors', '')
    tags = data.get('tags', '')
    url = data.get('url', '')

    # Preprocess data
    tokens = preprocessing.tokenize_text(text)
    tokens.extend(preprocessing.tokenize_text(title))
    tokens.extend(preprocessing.tokenize_text(authors))
    tokens.extend(preprocessing.tokenize_text(tags))

    # Get docID
    docID = sha_256(url)

    # Add tokens to lexicon and inverted index
    for word in tokens:
        lexicon.add_word(word)
        wordID = lexicon.get_word_id(word)

        offset = barrel_reader.get_wordID_offset(wordID)

        # If wordID is new
        if offset == -1:
            barrel_num = wordID % num_barrels
            max_offset = barrel_reader.get_max_offset(barrel_num)

            # Make new entry in barrel
            with open(f'barrels/inverted_index/barrel_{barrel_num}.bin', 'ab') as file:
                data = struct.pack("<II", wordID, 1)  # I = unsigned int
                docID_data = struct.pack(f"<Q", docID)  # Q = unsigned long long
                file.write(data + docID_data)

            # Make new entry in offsets file
            barrel_reader.offsets[wordID] = max_offset + 12
            with open('barrels/inverted_index/offsets.bin', 'ab') as meta_file:
                meta_file.write(struct.pack("<IQ", wordID, barrel_reader.get_wordID_offset(wordID)))

        # Update barrel and offsets
        else:
            barrel_reader.update_barrel_entry(wordID, docID)

    # Make entry in url mapper
    url_mapper.add_entry(docID, url)


# Return query response with pagination
@app.route('/query', methods=['POST'])
def query():
    """Endpoint to handle search queries."""
    data = request.get_json()
    query_text = data.get('query', '')
    page_number = data.get('page_number', 1)

    if not query_text:
        return jsonify({"error": "Query cannot be empty"}), 400

    # Process the query and get results
    global global_sorted_docIDs
    global previous_query
    if not global_sorted_docIDs or query_text != previous_query:
        # New query or if the query is different from the last one
        global_sorted_docIDs = handle_query(query_text)
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

        return jsonify({"results": doc_details})
    else:
        return jsonify({"error": "No results found"}), 404


# Define an endpoint for adding articles
@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()

    add_article(data)


# Run the Flask app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
