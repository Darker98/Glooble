import pandas as pd
from tokenize_text import tokenize_text
from Lexicon import Lexicon
from ForwardIndex import ForwardIndex
from hashlib import sha256


def sha_256(data):
    hash_value = sha256(data).digest()
    return int.from_bytes(hash_value[:8], byteorder='big')  # Use 'little' if needed


# Read dataset in chunks
chunks = pd.read_csv('files/medium_articles.csv', chunksize=1000)

# Initialize lexicon
lexicon = Lexicon()
lexicon.read_from_file('files/lexicon.bin')

# Initialize forward index
fi = ForwardIndex()

# Correct column-to-flag mapping
column_flags = {
    0: 1,  # Title: bit 0
    1: 2,  # Text: bit 1
    5: 4,  # Tags: bit 2
    3: 8,  # Authors: bit 3
}

rowNo = 1

for chunk in chunks:
    for row in chunk.itertuples(index=False):
        word_data = {}
        url = row[2]

        # Iterate through the relevant columns
        for column_num, context_flag in column_flags.items():
            column = row[column_num]
            tokenized = tokenize_text(column)

            for token in tokenized:
                wordID = lexicon.get_word_id(token)
                if wordID is None:
                    raise Exception(f"Word not found in lexicon: {token}")

                if wordID in word_data:
                    word_data[wordID][1] |= context_flag  # Update context_flag (bitwise OR)
                    word_data[wordID][2] += 1  # Increment frequency
                else:
                    word_data[wordID] = [wordID, context_flag, 1]  # New entry

        # Prepare word_data and max_frequency
        doc_word_data = list(word_data.values())
        max_frequency = max(freq for _, _, freq in doc_word_data)

        # Add to forward index
        docID = sha_256(url.encode('utf-8'))
        if docID in fi.get_index():
            print("Duplicate docID")
            continue
        fi.add_document(docID, doc_word_data, max_frequency)

        # Keep track of execution progress
        if rowNo % 50 == 0:
            print(f"Processed {rowNo} rows")
        rowNo += 1

# Write forward index to file
fi.write_to_file('files/forward_index.bin')

# Test reading forward index
fi.read_from_file('files/forward_index.bin')
