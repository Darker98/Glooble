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
    def __init__(self, num_buckets=10, output_directory="barrels/forward_index"):
        self.num_buckets = num_buckets
        self.output_directory = output_directory
        self.index_metadata = {}  # Tracks docIDs in each bucket

    def divide_index_into_buckets(self, document_index):
        os.makedirs(self.output_directory, exist_ok=True)  # Ensure output directory exists

        buckets = [{} for _ in range(self.num_buckets)]

        for doc_id, word_ids in document_index.items():
            bucket_index = doc_id % self.num_buckets  # Assign docID to a bucket
            buckets[bucket_index][doc_id] = word_ids

        for i, bucket in enumerate(buckets):
            bucket_file = f"{self.output_directory}/bucket_{i}.bin"
            with open(bucket_file, 'wb') as file:
                for doc_id, word_ids in bucket.items():
                    doc_id_bytes = doc_id.encode('utf-8')
                    header = struct.pack(f"<I8s", len(word_ids), doc_id_bytes)  # Serialize header
                    word_data = struct.pack(f"<{len(word_ids)}I", *word_ids)  # Serialize wordIDs
                    file.write(header + word_data)
