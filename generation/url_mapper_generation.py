import pandas as pd
from hashlib import sha256


def sha_256(data):
    # Compute SHA-256 hash
    hash_value = sha256(data.encode('utf-8')).digest()

    # Extract the first 8 bytes and convert to an integer
    checksum = int.from_bytes(hash_value[:8], byteorder='big')  # Use 'little' if needed

    return checksum


# Read dataset in chunks
chunks = pd.read_csv('files/medium_articles.csv', chunksize=1000)


# Iterate over rows
try:
    with open('files/url_mapper.bin', 'wb') as file:
        rowNo = 1
        for chunk in chunks:
            for row in chunk.itertuples(index=False):
                url = row[2]  # Assuming the URL is in the 3rd column
                docID = sha_256(url)

                # Encode URL in UTF-8
                url_encoded = url.encode('utf-8')
                url_length = len(url_encoded)

                # Write 2 bytes for URL length
                file.write(url_length.to_bytes(2, byteorder='big'))

                # Write the URL bytes
                file.write(url_encoded)

                # Write 8 bytes for the docID
                file.write(docID.to_bytes(8, byteorder='big'))

                # Keep track of where execution is at
                if rowNo % 50 == 0:
                    print(rowNo)
                rowNo += 1
except Exception as e:
    print(f"Error: {e}")
    print(f"Failed at row: {rowNo}")
