import pandas as pd
from hashlib import sha256
import math


def sha_256(data):
    # Compute SHA-256 hash
    hash_value = sha256(data.encode('utf-8')).digest()

    # Extract the first 8 bytes and convert to an integer
    checksum = int.from_bytes(hash_value[:8], byteorder='big')  # Use 'little' if needed

    return checksum


def sanitize_value(value):
    """Convert value to a string if not NaN, otherwise return an empty string."""
    return str(value) if not (value is None or isinstance(value, float) and math.isnan(value)) else ""


# Read dataset in chunks
chunks = pd.read_csv('files/medium_articles.csv', chunksize=1000)

try:
    with open('files/url_mapper.bin', 'wb') as main_file, open('files/offsets.bin', 'wb') as offset_file:
        rowNo = 1
        current_offset = 0  # Track the current offset in the main file

        for chunk in chunks:
            for row in chunk.itertuples(index=False):
                # Sanitize values
                url = sanitize_value(row[2])  # Assuming the URL is in the 3rd column
                title = sanitize_value(row[0])  # Assuming the title is in the 1st column
                tags = sanitize_value(row[5])  # Assuming the tags are in the 6th column
                authors = sanitize_value(row[3])  # Assuming the authors are in the 4th column

                # Calculate docID
                docID = sha_256(url)

                # Track the starting offset of this docID
                offset_file.write(docID.to_bytes(8, byteorder='big'))  # Write docID (8 bytes)
                offset_file.write(current_offset.to_bytes(8, byteorder='big'))  # Write offset (8 bytes)

                # Encode and write URL
                url_encoded = url.encode('utf-8')
                url_length = len(url_encoded)
                main_file.write(url_length.to_bytes(2, byteorder='big'))  # 2 bytes for URL length
                main_file.write(url_encoded)  # URL bytes
                current_offset += 2 + url_length  # Update offset (2 bytes for length + actual URL bytes)

                # Encode and write title
                title_encoded = title.encode('utf-8')
                title_length = len(title_encoded)
                main_file.write(title_length.to_bytes(2, byteorder='big'))  # 2 bytes for title length
                main_file.write(title_encoded)  # Title bytes
                current_offset += 2 + title_length  # Update offset

                # Encode and write tags
                tags_list = tags.split(',') if tags else []  # Split tags by comma
                main_file.write(len(tags_list).to_bytes(1, byteorder='big'))  # 1 byte for number of tags
                current_offset += 1  # Update offset (1 byte for number of tags)

                for tag in tags_list:
                    tag_encoded = tag.strip().encode('utf-8')
                    tag_length = len(tag_encoded)
                    main_file.write(tag_length.to_bytes(1, byteorder='big'))  # 1 byte for tag length
                    main_file.write(tag_encoded)  # Tag bytes
                    current_offset += 1 + tag_length  # Update offset

                # Encode and write authors
                authors_list = authors.split(',') if authors else []  # Split authors by comma
                main_file.write(len(authors_list).to_bytes(1, byteorder='big'))  # 1 byte for number of authors
                current_offset += 1  # Update offset (1 byte for number of authors)

                for author in authors_list:
                    author_encoded = author.strip().encode('utf-8')
                    author_length = len(author_encoded)
                    main_file.write(author_length.to_bytes(1, byteorder='big'))  # 1 byte for author length
                    main_file.write(author_encoded)  # Author bytes
                    current_offset += 1 + author_length  # Update offset

                # Write docID at the end of this entry in the main file
                main_file.write(docID.to_bytes(8, byteorder='big'))  # 8 bytes for docID
                current_offset += 8  # Update offset

                # Progress tracking
                if rowNo % 50 == 0:
                    print(f"Processed {rowNo} rows")
                rowNo += 1

except Exception as e:
    print(f"Error: {e}")
    print(f"Failed at row: {rowNo}")
