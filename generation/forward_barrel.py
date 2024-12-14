import os
import json
import struct

class ForwardIndexManager:
    def __init__(self, num_buckets=10, output_directory="forward_index_buckets"):
        self.num_buckets = num_buckets
        self.output_directory = output_directory
        self.index_metadata = {}  # Tracks docIDs in each bucket

    def _hash_doc_id(self, doc_id):
        """
        Convert an 8-byte string docID into a numerical hash for modulo operation.
        """
        return sum(byte for byte in doc_id.encode('utf-8'))

    def divide_index_into_buckets(self, document_index):
        os.makedirs(self.output_directory, exist_ok=True)  # Ensure output directory exists

        buckets = [{} for _ in range(self.num_buckets)]

        for doc_id, word_ids in document_index.items():
            hashed_doc_id = self._hash_doc_id(doc_id)
            bucket_index = hashed_doc_id % self.num_buckets  # Assign docID to a bucket
            buckets[bucket_index][doc_id] = word_ids

        for i, bucket in enumerate(buckets):
            bucket_file = f"{self.output_directory}/bucket_{i}.bin"
            self.index_metadata[f"bucket_{i}"] = list(bucket.keys())
            with open(bucket_file, 'wb') as file:
                for doc_id, word_ids in bucket.items():
                    doc_id_bytes = doc_id.encode('utf-8')
                    header = struct.pack(f"<I8s", len(word_ids), doc_id_bytes)  # Serialize header
                    word_data = struct.pack(f"<{len(word_ids)}I", *word_ids)  # Serialize wordIDs
                    file.write(header + word_data)

    def save_metadata(self, filename="index_metadata.json"):
        with open(filename, 'w') as file:
            json.dump(self.index_metadata, file, indent=4)  # Save metadata as JSON

