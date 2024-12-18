import pandas as pd
from tokenize_text import tokenize_text
from Lexicon import Lexicon
from ForwardIndex import ForwardIndex
from hashlib import sha256


def sha_256(data):
    # Compute SHA-256 hash
    hash_value = sha256(data).digest()

    # Extract the first 8 bytes and convert to an integer
    checksum = int.from_bytes(hash_value[:8], byteorder='big')  # Use 'little' if needed

    return checksum


# Read dataset in chunks
chunks = pd.read_csv('files/medium_articles.csv', chunksize=1000)

# Initialize lexicon
lexicon = Lexicon()
lexicon.read_from_file('files/lexicon.bin')

# Initialize forward index
fi = ForwardIndex()

# Iterate over rows
try:
    columns_to_select = [0, 1, 3, 5]
    rowNo = 1
    for chunk in chunks:
        for row in chunk.itertuples(index=False):
            wordIDs = set()
            selected_columns = [row[i] for i in columns_to_select]
            url = row[2]

            # Add each token to forward index
            for column_num, column in enumerate(selected_columns):
                tokenized = tokenize_text(column)
                for token in tokenized:
                    wordID = lexicon.get_word_id(token)
                    if wordID is None:
                        print(token)
                        raise Exception
                    wordIDs.add(wordID)

            # Make entry in forward index
            docID = sha_256(url.encode('utf-8'))
            if docID in fi.get_index().keys():
                print("Duplicate docID")
                continue
            fi.add_document(docID, wordIDs)

            # Keep track of where execution is at
            if rowNo % 50 == 0:
                print(rowNo)
            rowNo += 1
except Exception as e:
    print(e)
    print(rowNo)

# Test forward index
fi.write_to_file('files/forward_index.bin')
fi.read_from_file('files/forward_index.bin')