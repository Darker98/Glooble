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


def sha_256(data):
    # Compute SHA-256 hash
    hash_value = sha256(data).digest()

    # Extract the first 8 bytes and convert to an integer
    checksum = int.from_bytes(hash_value[:8], byteorder='big')  # Use 'little' if needed

    return checksum


def process_word(word, result):
    """Retrieve docIDs for a single word and append as a set."""
    wordID = lexicon.get_word_id(word)
    docIDs = barrel_reader.read_docIDs(wordID)

    unique_doc_IDs = set()
    for docID in docIDs:
        if docID is not None:
            unique_doc_IDs.add(docID)

    if unique_doc_IDs is not None:
        result.append(set(unique_doc_IDs))  # Append as a set


# Fetch details of each unique docID
def handle_query(query):
    """Handles the incoming query and retrieves common docIDs and their details."""
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
        common_doc_ids = set.intersection(*result)

        # Fetch the details (URL, title, tags, authors) for each docID
        doc_details = []
        for docID in common_doc_ids:
            details = url_mapper.get_details_by_docID(docID, 'files/url_mapper.bin')
            if details:
                doc_details.append(details)

        return doc_details  # Return list of documents' details as JSON-serializable list

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


# Return query response
@app.route('/query', methods=['POST'])
def query():
    """Endpoint to handle search queries."""
    data = request.get_json()
    query_text = data.get('query', '')

    if not query_text:
        return jsonify({"error": "Query cannot be empty"}), 400

    # Process the query and get results
    doc_details = handle_query(query_text)
    if doc_details:
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
