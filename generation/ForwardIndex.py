import struct
import os


class ForwardIndex:
    def __init__(self):
        self.doc_to_wordIDs = {}  # Dictionary to store docID -> list of word data

    def add_document(self, docID, word_data, max_frequency):
        """
        Add a document to the forward index.
        :param docID: Unique 8-byte integer identifier for the document.
        :param word_data: List of tuples (wordID, context_flags, frequency).
        :param max_frequency: Maximum frequency of any word in the document.
        """
        self.doc_to_wordIDs[docID] = (word_data, max_frequency)

    def get_document(self, docID):
        return self.doc_to_wordIDs.get(docID, None)

    def get_index(self):
        return self.doc_to_wordIDs

    def write_to_file(self, filename):
        with open(filename, 'wb') as file:
            for docID, (word_data, max_frequency) in self.doc_to_wordIDs.items():
                # Pack docID (8 bytes) and number of word entries (2 bytes)
                header = struct.pack("<QH", docID, len(word_data))

                # Pack word data (4-byte wordID, 1-byte context_flags, 2-byte frequency each)
                word_entries = b''.join(struct.pack("<IBH", wordID, context_flags, frequency)
                                        for wordID, context_flags, frequency in word_data)

                # Pack max_frequency (2 bytes)
                max_freq_data = struct.pack("<H", max_frequency)

                # Write all data to file
                file.write(header + word_entries + max_freq_data)

    def read_from_file(self, filename):
        with open(filename, 'rb') as file:
            while True:
                # Read the header (docID and word count)
                header = file.read(10)  # 8 bytes docID + 2 bytes word count
                if not header:
                    break
                docID, word_count = struct.unpack("<QH", header)

                # Read all word data
                word_data = []
                for _ in range(word_count):
                    word_entry = file.read(7)  # 4 bytes wordID, 1 byte context_flags, 2 bytes frequency
                    wordID, context_flags, frequency = struct.unpack("<IBH", word_entry)
                    word_data.append((wordID, context_flags, frequency))

                # Read max_frequency (2 bytes)
                max_frequency = struct.unpack("<H", file.read(2))[0]

                # Add to index
                self.doc_to_wordIDs[docID] = (word_data, max_frequency)


class BarrelsManager:
    def __init__(self, num_barrels=38, output_directory="barrels/forward_index"):
        self.num_barrels = num_barrels
        self.output_directory = output_directory
        self.offsets = {}  # Tracks docID -> offset

    def make_barrels(self, index):
        os.makedirs(self.output_directory, exist_ok=True)  # Ensure output directory exists
        buckets = [{} for _ in range(self.num_barrels)]
        self.offsets = {}  # Initialize metadata for all documents

        # Divide documents into buckets
        for docID, (word_data, max_frequency) in index.get_index().items():
            bucket_index = docID % self.num_barrels  # Assign docID to a bucket
            buckets[bucket_index][docID] = (word_data, max_frequency)

        # Write buckets to files and track offsets
        for i, bucket in enumerate(buckets):
            bucket_file = f"{self.output_directory}/bucket_{i}.bin"

            with open(bucket_file, 'wb') as file:
                offset = 0
                for docID, (word_data, max_frequency) in bucket.items():
                    # Serialize data
                    header = struct.pack("<QH", docID, len(word_data))
                    word_entries = b''.join(struct.pack("<IBH", wordID, context_flags, frequency)
                                            for wordID, context_flags, frequency in word_data)
                    max_freq_data = struct.pack("<H", max_frequency)

                    # Write to file
                    file.write(header + word_entries + max_freq_data)

                    # Record offset in metadata
                    self.offsets[docID] = offset  # Store only the offset

                    # Update offset
                    offset += len(header) + len(word_entries) + len(max_freq_data)

        # Write all offsets to a single metadata file
        metadata_file = f"{self.output_directory}/offsets.bin"
        with open(metadata_file, 'wb') as meta_file:
            for docID, offset in self.offsets.items():
                # Pack docID (8 bytes) and offset (4 bytes)
                meta_file.write(struct.pack("<QI", docID, offset))

    def load_metadata(self, metadata_file):
        self.offsets = {}
        with open(metadata_file, 'rb') as meta_file:
            while True:
                meta_data = meta_file.read(12)  # 8 bytes docID + 4 bytes offset
                if not meta_data:
                    break
                docID, offset = struct.unpack("<QI", meta_data)
                self.offsets[docID] = offset

    def get_document(self, docID):
        if docID not in self.offsets:
            raise KeyError("Document not found.")

        # Determine the bucket dynamically based on docID
        bucket_index = docID % self.num_barrels
        bucket_file = f"{self.output_directory}/bucket_{bucket_index}.bin"

        # Read the document data
        with open(bucket_file, 'rb') as file:
            file.seek(self.offsets[docID])
            header = file.read(10)  # 8 bytes docID + 2 bytes word_count
            _, word_count = struct.unpack("<QH", header)

            word_data = [struct.unpack("<IBH", file.read(7)) for _ in range(word_count)]
            max_frequency = struct.unpack("<H", file.read(2))[0]

            return word_data, max_frequency
