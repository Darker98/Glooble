from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import preprocessing
from Lexicon import Lexicon
from inverted_index import BarrelReader
from URLMapper import URLMapper

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize global variables
lexicon = Lexicon()
barrel_reader = BarrelReader()
url_mapper = URLMapper()

# Initialize data
lexicon.read_from_file('files/lexicon.bin')
barrel_reader.load_offsets('barrels/inverted_index/offsets.bin')
url_mapper.read_from_file('files/url_mapper.bin')


def process_word(word, result):
    """Retrieve docIDs for a single word and append as a set."""
    wordID = lexicon.get_word_id(word)
    docIDs = barrel_reader.read_docIDs(wordID)

    urls = set()
    for docID in docIDs:
        url = url_mapper.get_url(docID)
        if url is not None:
            urls.add(url)

    if urls is not None:
        result.append(set(urls))  # Append as a set


def handle_query(query):
    """Handles the incoming query and retrieves common docIDs."""
    words = preprocessing.tokenize_text(query)
    threads = []
    result = []

    for word in words:
        thread = threading.Thread(target=process_word, args=(word, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if result:
        common_urls = set.intersection(*result)
        return list(common_urls)  # Convert set to list for JSON serialization
    return []


# Define an endpoint for processing queries
@app.route('/query', methods=['POST'])
def query():
    """Endpoint to handle search queries."""
    data = request.get_json()
    query_text = data.get('query', '')

    if not query_text:
        return jsonify({"error": "Query cannot be empty"}), 400

    # Process the query and get results
    common_urls = handle_query(query_text)
    return jsonify({"urls": common_urls})


# Run the Flask app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
