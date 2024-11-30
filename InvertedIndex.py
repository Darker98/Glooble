class InvertedIndex:
    def __init__(self):
        self.word_to_docIDs = {}  # Dictionary to store wordID -> list of docIDs mapping

    def build_from_forward_index(self, forward_index):
        """
        Build the inverted index from a given forward index.

        :param forward_index: Dictionary mapping docID -> list of wordIDs
        """
        for docID, wordIDs in forward_index.items():
            for wordID in wordIDs:
                if wordID not in self.word_to_docIDs:
                    self.word_to_docIDs[wordID] = []
                self.word_to_docIDs[wordID].append(docID)

    def get_docIDs(self, wordID):
        """
        Retrieve the list of docIDs for a given wordID.

        :param wordID: Unique identifier for the word
        :return: List of docIDs or None if wordID doesn't exist
        """
        return self.word_to_docIDs.get(wordID, None)

    def get_index(self):
        """
        Retrieve the entire inverted index.

        :return: Dictionary mapping wordID -> list of docIDs
        """
        return self.word_to_docIDs

    def write_to_file(self, filename):
        """
        Write the inverted index to a binary file.

        :param filename: File to write the inverted index to
        """
        with open(filename, 'wb') as file:
            for wordID, docIDs in self.word_to_docIDs.items():
                # Pack the wordID (4 bytes) and number of docIDs (2 bytes)
                data = struct.pack("<IH", wordID, len(docIDs))  # I = 4-byte unsigned int, H = 2-byte unsigned short

                # Pack all docIDs (8 bytes each)
                docID_data = struct.pack(f"<{len(docIDs)}Q", *docIDs)  # Q = 8-byte unsigned int

                # Write the packed data to the file
                file.write(data + docID_data)

    def read_from_file(self, filename):
        """
        Read the inverted index from a binary file.

        :param filename: File to read the inverted index from
        """
        with open(filename, 'rb') as file:
            while True:
                # Read the first 6 bytes (wordID and doc count)
                header_data = file.read(6)  # 4 bytes for wordID, 2 bytes for doc count
                if not header_data:
                    break  # End of file

                # Unpack wordID (4 bytes) and doc count (2 bytes)
                wordID, doc_count = struct.unpack("<IH", header_data)

                # Read the next `doc_count * 8` bytes (docIDs)
                docID_data = file.read(doc_count * 8)
                docIDs = struct.unpack(f"<{doc_count}Q", docID_data)

                # Update the inverted index
                self.word_to_docIDs[wordID] = list(docIDs)
