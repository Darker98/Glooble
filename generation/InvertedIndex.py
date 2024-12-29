import struct
import os


class InvertedIndex:
    def __init__(self):
        # Dictionary to store wordID -> list of tuples (docID, context_flags, frequency)
        self.word_to_docIDs = {}
        # Dictionary to store docID -> max frequency
        self.doc_max_frequencies = {}

    def build_from_forward_index(self, forward_index):
        docNo = 1
        for docID, (word_data, max_frequency) in forward_index.items():
            self.doc_max_frequencies[docID] = max_frequency  # Store the max frequency for the document
            for wordID, context_flags, frequency in word_data:
                if wordID not in self.word_to_docIDs:
                    self.word_to_docIDs[wordID] = []
                self.word_to_docIDs[wordID].append((docID, context_flags, frequency))

            if docNo % 50 == 0:
                print(docNo)
            docNo += 1

    def get_docIDs(self, wordID):
        return self.word_to_docIDs.get(wordID, None)

    def get_index(self):
        return self.word_to_docIDs

    def write_to_file(self, index_filename, max_freq_filename):
        # Write the inverted index to a file
        with open(index_filename, 'wb') as file:
            for wordID, doc_data in self.word_to_docIDs.items():
                # Pack the wordID (4 bytes) and number of docIDs (4 bytes)
                header = struct.pack("<II", wordID, len(doc_data))

                # Pack all docID data (8 bytes docID, 1 byte context_flags, 2 bytes frequency)
                doc_entries = b''.join(
                    struct.pack("<QBH", docID, context_flags, frequency)
                    for docID, context_flags, frequency in doc_data
                )

                # Write the packed data to the file
                file.write(header + doc_entries)

        # Write the max frequencies to a separate file
        with open(max_freq_filename, 'wb') as max_file:
            for docID, max_frequency in self.doc_max_frequencies.items():
                # Pack docID (8 bytes) and max frequency (2 bytes)
                max_file.write(struct.pack("<QH", docID, max_frequency))

    def read_from_file(self, index_filename, max_freq_filename):
        # Read the inverted index from a file
        with open(index_filename, 'rb') as file:
            while True:
                # Read the first 8 bytes (wordID and doc count)
                header_data = file.read(8)  # 4 bytes wordID, 4 bytes doc count
                if not header_data:
                    break  # End of file

                # Unpack wordID (4 bytes) and doc count (4 bytes)
                wordID, doc_count = struct.unpack("<II", header_data)

                # Read the next `doc_count * 11` bytes (docID, context_flags, frequency)
                doc_entries = file.read(doc_count * 11)
                doc_data = [
                    struct.unpack("<QBH", doc_entries[i:i + 11])
                    for i in range(0, len(doc_entries), 11)
                ]

                # Update the inverted index
                self.word_to_docIDs[wordID] = doc_data

        # Read the max frequencies from a separate file
        self.doc_max_frequencies = {}
        with open(max_freq_filename, 'rb') as max_file:
            while True:
                max_data = max_file.read(10)  # 8 bytes docID, 2 bytes max frequency
                if not max_data:
                    break
                docID, max_frequency = struct.unpack("<QH", max_data)
                self.doc_max_frequencies[docID] = max_frequency


class BarrelsManager:
    def __init__(self, num_barrels=60, output_dir="barrels/inverted_index"):
        self.num_barrels = num_barrels  # Number of barrels
        self.output_dir = output_dir  # Directory to store barrels
        self.offsets = {}  # Mapping of barrels to their wordID ranges or offsets

    def make_barrels(self, index):
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure the output directory exists

        # Initialize barrels (as dictionaries for now)
        barrels = [{} for _ in range(self.num_barrels)]
        self.offsets = {i: {} for i in range(self.num_barrels)}  # Initialize metadata
        doc_max_freq = {}

        # Assign wordIDs to barrels and track max frequencies per docID
        for wordID, doc_data in index.get_index().items():
            barrel_index = wordID % self.num_barrels  # Example: hash-based assignment
            barrels[barrel_index][wordID] = doc_data
            for docID, _, frequency in doc_data:
                doc_max_freq[docID] = max(doc_max_freq.get(docID, 0), frequency)

        # Write each barrel to a file and store offsets
        for i, barrel in enumerate(barrels):
            barrel_filename = f"{self.output_dir}/barrel_{i}.bin"
            self.offsets[i] = {}

            with open(barrel_filename, 'wb') as file:
                offset = 0
                for wordID, doc_data in barrel.items():
                    # Serialize and write wordID and its doc data
                    header = struct.pack("<II", wordID, len(doc_data))  # 4 bytes wordID, 4 bytes doc count
                    doc_entries = b''.join(
                        struct.pack("<QBH", docID, context_flags, frequency)
                        for docID, context_flags, frequency in doc_data
                    )
                    file.write(header + doc_entries)

                    self.offsets[i][wordID] = offset

                    offset += len(header) + len(doc_entries)

        # Write offsets to a metadata file
        metadata_file = f"{self.output_dir}/offsets.bin"
        with open(metadata_file, 'wb') as meta_file:
            for barrel_index, offsets in self.offsets.items():
                for wordID, word_offset in offsets.items():
                    # Serialize wordID (4 bytes) and offset (4 bytes)
                    meta_file.write(struct.pack("<II", wordID, word_offset))  # wordID and 4-byte offset

        # Write max frequencies to a separate file
        self.write_max_frequencies(doc_max_freq)

    def write_max_frequencies(self, doc_max_freq):
        max_frequencies_file = f"{self.output_dir}/max_frequencies.bin"
        unique_doc_count = len(doc_max_freq)  # Calculate the total number of unique docIDs

        with open(max_frequencies_file, 'wb') as file:
            # Write the total number of unique docIDs (4 bytes)
            file.write(struct.pack("<I", unique_doc_count))

            # Write each docID and its max frequency
            for docID, max_freq in doc_max_freq.items():
                # 8 bytes for docID, 2 bytes for max frequency
                file.write(struct.pack("<QH", docID, max_freq))
