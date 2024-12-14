import struct
import os


class InvertedIndex:
    def __init__(self):
        self.word_to_docIDs = {}  # Dictionary to store wordID -> list of docIDs mapping

    def build_from_forward_index(self, forward_index):
        docNo = 1
        for docID, wordIDs in forward_index.items():
            for wordID in wordIDs:
                if wordID not in self.word_to_docIDs:
                    self.word_to_docIDs[wordID] = []
                self.word_to_docIDs[wordID].append(docID)

            if docNo % 50 == 0:
                print(docNo)
            docNo += 1

    def get_docIDs(self, wordID):
        return self.word_to_docIDs.get(wordID, None)

    def get_index(self):
        return self.word_to_docIDs

    def write_to_file(self, filename):
        with open(filename, 'wb') as file:
            for wordID, docIDs in self.word_to_docIDs.items():
                # Pack the wordID (4 bytes) and number of docIDs (2 bytes)
                data = struct.pack("<II", wordID, len(docIDs))  # I = 4-byte unsigned int

                # Pack all docIDs (8 bytes each)
                docID_data = struct.pack(f"<{len(docIDs)}Q", *docIDs)  # Q = 8-byte unsigned int

                # Write the packed data to the file
                file.write(data + docID_data)

    def read_from_file(self, filename):
        with open(filename, 'rb') as file:
            while True:
                # Read the first 8 bytes (wordID and doc count)
                header_data = file.read(8)  # 4 bytes for wordID, 4 bytes for doc count
                if not header_data:
                    break  # End of file

                # Unpack wordID (4 bytes) and doc count (4 bytes)
                wordID, doc_count = struct.unpack("<II", header_data)

                # Read the next `doc_count * 8` bytes (docIDs)
                docID_data = file.read(doc_count * 8)
                docIDs = struct.unpack(f"<{doc_count}Q", docID_data)

                # Update the inverted index
                self.word_to_docIDs[wordID] = list(docIDs)


class BarrelsManager:
    def __init__(self, num_barrels=44, output_dir="barrels/inverted_index"):
        self.num_barrels = num_barrels  # Number of barrels
        self.output_dir = output_dir  # Directory to store barrels
        self.offsets = {}  # Mapping of barrels to their wordID ranges or hashes

    def make_barrels(self, index):
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure the output directory exists

        # Initialize barrels (as dictionaries for now)
        barrels = [{} for _ in range(self.num_barrels)]
        self.offsets = {i: {} for i in range(self.num_barrels)}  # Initialize metadata

        # Assign wordIDs to barrels
        for wordID, docIDs in index.get_index().items():
            barrel_index = wordID % self.num_barrels  # Example: hash-based assignment
            barrels[barrel_index][wordID] = docIDs

        # Write each barrel to a file
        for i, barrel in enumerate(barrels):
            barrel_filename = f"{self.output_dir}/barrel_{i}.bin"
            self.offsets[i] = {}

            with open(barrel_filename, 'wb') as file:
                offset = 0
                for wordID, docIDs in barrel.items():
                    # Serialize and write wordID and its docIDs
                    data = struct.pack("<II", wordID, len(docIDs))  # I = unsigned int
                    docID_data = struct.pack(f"<{len(docIDs)}Q", *docIDs)  # Q = unsigned long long
                    file.write(data + docID_data)

                    self.offsets[i][wordID] = offset

                    offset += len(data) + len(docID_data)

            # Save metadata for this bucket to a file
            metadata_file = f"{self.output_dir}/offsets.bin"
            with open(metadata_file, 'wb') as meta_file:
                for word_id, word_offset in self.offsets[i].items():
                    meta_file.write(struct.pack("<IQ", word_id, word_offset))  # Serialize docID and offset
