import os
import struct


def add_max_frequency_entry(docID, max_frequency, file_path='files/max_frequencies.bin'):
    """
    Adds a new max_freq entry for a given docID and updates the total document count.

    :param docID: The document ID (int).
    :param max_frequency: The maximum term frequency in the document (int).
    :param file_path: Path to the max_frequencies file.
    """
    try:
        if not os.path.exists(file_path):
            # Create the file and initialize the total document count
            with open(file_path, 'wb') as file:
                file.write(struct.pack("<I", 0))  # Initial total_documents count

        # Read current total_documents
        with open(file_path, 'rb+') as file:
            total_documents = struct.unpack("<I", file.read(4))[0]
            total_documents += 1

            # Move the cursor back to update the total_documents
            file.seek(0)
            file.write(struct.pack("<I", total_documents))

            # Append the new docID and max_frequency at the end of the file
            file.seek(0, os.SEEK_END)
            file.write(struct.pack("<QH", docID, max_frequency))

    except Exception as e:
        print(f"Error adding max frequency entry: {e}")


def max_frequency_reader(file_path):
    """
    Reads the max_frequencies file and returns the total number of documents and a hash table
    of docIDs against their max frequencies.

    :param file_path: Path to the max_frequencies file.
    :return: A tuple containing:
             - total_documents (int): Total number of unique docIDs.
             - doc_max_freq (dict): A dictionary mapping docID (int) to max frequency (int).
    """
    doc_max_freq = {}

    with open(file_path, 'rb') as file:
        # Read the first 4 bytes to get the total number of unique docIDs
        total_documents = struct.unpack("<I", file.read(4))[0]

        # Read the rest of the file
        while True:
            data = file.read(10)  # 8 bytes for docID, 2 bytes for max frequency
            if len(data) != 10:
                break
            # Unpack the docID and max frequency
            docID, max_freq = struct.unpack("<QH", data)
            doc_max_freq[docID] = max_freq

    return total_documents, doc_max_freq
