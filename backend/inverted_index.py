import struct
import os


class BarrelReader:
    def __init__(self, num_barrels=44, output_dir="barrels/inverted_index"):
        self.num_barrels = num_barrels  # Number of barrels
        self.output_dir = output_dir  # Directory where barrels and offsets are stored
        self.offsets = {}  # Hash table to store wordID -> (barrel_index, offset) mapping

    def load_offsets(self, offsets_file):
        """Load the offsets metadata into memory."""
        with open(offsets_file, 'rb') as file:
            while True:
                data = file.read(12)  # 4 bytes for wordID, 8 bytes for offset
                if not data:
                    break
                wordID, offset = struct.unpack("<IQ", data)
                self.offsets[wordID] = offset

    def read_docIDs(self, wordID):
        """Retrieve the list of docIDs for the given wordID."""
        if wordID not in self.offsets:
            return None  # WordID not found in metadata

        offset = self.offsets[wordID]
        barrel_index = wordID % self.num_barrels
        barrel_filename = os.path.join(self.output_dir, f"barrel_{barrel_index}.bin")

        with open(barrel_filename, 'rb') as file:
            file.seek(offset)  # Move to the wordID's position
            header_data = file.read(8)  # Read 4 bytes for wordID and 4 bytes for doc count
            wordID_read, doc_count = struct.unpack("<II", header_data)

            if wordID_read != wordID:
                raise ValueError(f"Unexpected wordID read: {wordID_read} (expected: {wordID})")

            docID_data = file.read(doc_count * 8)  # Read the docIDs
            docIDs = struct.unpack(f"<{doc_count}Q", docID_data)
            return list(docIDs)
