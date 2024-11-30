import struct

class ForwardIndex:
    def __init__(self):
        self.doc_to_wordIDs = {}  # Dictionary to store docID -> list of wordIDs mapping

    def add_document(self, docID, wordIDs):
        """
        Add or update a document in the forward index.

        :param docID: Unique identifier for the document (8 bytes)
        :param wordIDs: List of wordIDs in the document (4 bytes each)
        """
        self.doc_to_wordIDs[docID] = wordIDs

    def get_wordIDs(self, docID):
        """
        Retrieve the list of wordIDs for a given document.

        :param docID: Unique identifier for the document
        :return: List of wordIDs or None if docID doesn't exist
        """
        return self.doc_to_wordIDs.get(docID, None)

    def get_index(self):
        """
        Retrieve the entire forward index.

        :return: Dictionary mapping docID -> list of wordIDs
        """
        return self.doc_to_wordIDs

    def write_to_file(self, filename):
        """
        Write the forward index to a binary file.

        :param filename: File to write the forward index to
        """
        with open(filename, 'wb') as file:
            for docID, wordIDs in self.doc_to_wordIDs.items():
                # Pack the docID (8 bytes) and number of wordIDs (2 bytes)
                data = struct.pack("<QH", docID, len(wordIDs))  # Q = 8-byte unsigned int, H = 2-byte unsigned short

                # Pack all wordIDs (4 bytes each)
                wordID_data = struct.pack(f"<{len(wordIDs)}I", *wordIDs)  # I = 4-byte unsigned int

                # Write the packed data to the file
                file.write(data + wordID_data)

    def read_from_file(self, filename):
        """
        Read the forward index from a binary file.

        :param filename: File to read the forward index from
        """
        with open(filename, 'rb') as file:
            while True:
                # Read the first 10 bytes (docID and word count)
                header_data = file.read(10)  # 8 bytes for docID, 2 bytes for word count
                if not header_data:
                    break  # End of file

                # Unpack docID (8 bytes) and word count (2 bytes)
                docID, word_count = struct.unpack("<QH", header_data)

                # Read the next `word_count * 4` bytes (wordIDs)
                wordID_data = file.read(word_count * 4)
                wordIDs = struct.unpack(f"<{word_count}I", wordID_data)

                # Update the forward index
                self.doc_to_wordIDs[docID] = list(wordIDs)
