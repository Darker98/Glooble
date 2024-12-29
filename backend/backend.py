import threading
import socket
import json
import preprocessing
from Lexicon import Lexicon
from inverted_index import BarrelReader

# Define global variables
lexicon = Lexicon()
barrel_reader = BarrelReader()


def process_word(word, result):
    print(word)
    wordID = lexicon.get_word_id(word)
    print(wordID)
    docIDs = barrel_reader.read_docIDs(wordID)

    if docIDs is not None:
        result.append(set(docIDs))  # Append as a set


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
        common_doc_ids = set.intersection(*result)
        return common_doc_ids
    return set()


def start_server(host, port):
    """Starts the backend server to listen for queries."""

    # Initialize hash tables
    lexicon.read_from_file('files/lexicon.bin')
    barrel_reader.load_offsets('barrels/inverted_index/offsets.bin')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client, address = server.accept()
        print(f"Connection from {address}")
        data = client.recv(1024).decode('utf-8')
        if data:
            query = json.loads(data).get('query', '')
            if query:
                common_doc_ids = handle_query(query)
                response = json.dumps({"doc_ids": list(common_doc_ids)})
                client.sendall(response.encode('utf-8'))
        client.close()


if __name__ == "__main__":
    start_server('127.0.0.1', 8080)
