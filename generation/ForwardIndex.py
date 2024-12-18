import struct
import os


class ForwardIndex:
    def __init__(self):
        self.doc_to_wordIDs = {}  # Dictionary to store docID -> list of wordIDs mapping

    def add_document(self, docID, wordIDs):
        self.doc_to_wordIDs[docID] = wordIDs

    def get_wordIDs(self, docID):
        return self.doc_to_wordIDs.get(docID, None)

    def get_index(self):
        return self.doc_to_wordIDs

    def write_to_file(self, filename):
        with open(filename, 'wb') as file:
            for docID, wordIDs in self.doc_to_wordIDs.items():
                # Pack the docID (8 bytes) and number of wordIDs (2 bytes)
                data = struct.pack("<QH", docID, len(wordIDs))  # Q = 8-byte unsigned int, H = 2-byte unsigned short

                # Pack all wordIDs (4 bytes each)
                wordID_data = struct.pack(f"<{len(wordIDs)}I", *wordIDs)  # I = 4-byte unsigned int

                # Write the packed data to the file
                file.write(data + wordID_data)

    def read_from_file(self, filename):
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


class BarrelsManager:
    def __init__(self, num_barrels=22, output_directory="barrels/forward_index"):
        self.num_barrels = num_barrels
        self.output_directory = output_directory
        self.offsets = {}  # Tracks bucket offsets: {bucket_index: {docID: offset}}

    def make_barrels(self, index):
        os.makedirs(self.output_directory, exist_ok=True)  # Ensure output directory exists

        buckets = [{} for _ in range(self.num_barrels)]
        self.offsets = {i: {} for i in range(self.num_barrels)}  # Initialize metadata

        # Divide documents into buckets
        for doc_id, word_ids in index.get_index().items():
            bucket_index = doc_id % self.num_barrels  # Assign docID to a bucket
            buckets[bucket_index][doc_id] = word_ids

        # Write buckets to files and track offsets
        for i, bucket in enumerate(buckets):
            bucket_file = f"{self.output_directory}/bucket_{i}.bin"
            self.offsets[i] = {}  # Initialize metadata for this bucket

            with open(bucket_file, 'wb') as file:
                offset = 0  # Start at the beginning of the file
                for doc_id, word_ids in bucket.items():
                    # Serialize data
                    header = struct.pack(f"<QH", doc_id, len(word_ids))  # Serialize header
                    word_data = struct.pack(f"<{len(word_ids)}I", *word_ids)  # Serialize wordIDs

                    # Write to file
                    file.write(header + word_data)

                    # Record offset in metadata
                    self.offsets[i][doc_id] = offset

                    # Update offset (header + wordIDs size)
                    offset += len(header) + len(word_data)

            # Save metadata for this bucket to a file
            metadata_file = f"{self.output_directory}/offsets.bin"
            with open(metadata_file, 'wb') as meta_file:
                for doc_id, doc_offset in self.offsets[i].items():
                    meta_file.write(struct.pack("<QQ", doc_id, doc_offset))  # Serialize docID and offset

    def get_document(self, doc_id):
        """Retrieve a document using its docID."""
        # Determine the bucket
        bucket_index = doc_id % self.num_barrels
        bucket_file = f"{self.output_directory}/bucket_{bucket_index}.bin"
        metadata_file = f"{self.output_directory}/metadata.bin"

        # Load metadata for the bucket
        offsets = {}
        with open(metadata_file, 'rb') as meta_file:
            while True:
                meta_data = meta_file.read(16)  # 8 bytes for docID, 8 bytes for offset
                if not meta_data:
                    break
                meta_doc_id, meta_offset = struct.unpack("<QQ", meta_data)
                offsets[meta_doc_id] = meta_offset

        # Find the offset for the requested docID
        if doc_id not in offsets:
            raise Exception  # docID not found

        # Seek to the offset in the bucket file and read the data
        with open(bucket_file, 'rb') as file:
            file.seek(offsets[doc_id])
            header = file.read(10)  # Read header (8 bytes for docID, 2 bytes for word count)
            _, word_count = struct.unpack("<QH", header)

            # Read the wordIDs
            word_data = file.read(word_count * 4)
            word_ids = struct.unpack(f"<{word_count}I", word_data)

            return list(word_ids)
