import struct


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
