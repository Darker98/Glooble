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

    def get_wordID_offset(self, wordID):
        if wordID in self.offsets.keys():
            return self.offsets[wordID]
        return -1

    def get_max_offset(self, barrel_number):
        barrel_offsets = []
        for wordID in self.offsets.keys():
            if wordID % self.num_barrels == barrel_number:
                barrel_offsets.append(self.offsets[wordID])
        return max(barrel_offsets)

    def update_barrel_entry(self, wordID, new_docID):
        # Step 1: Locate the barrel and offset for the given wordID
        offset = self.get_wordID_offset(wordID)
        if offset == -1:
            raise ValueError(f"wordID {wordID} not found in the offsets metadata.")

        barrel_index = wordID % self.num_barrels
        barrel_filename = os.path.join(self.output_dir, f"barrel_{barrel_index}.bin")

        # Step 2: Read the existing entry
        with open(barrel_filename, 'rb') as file:
            file.seek(offset)
            header_data = file.read(8)  # Read 4 bytes for wordID and 4 bytes for doc count
            wordID_read, doc_count = struct.unpack("<II", header_data)

            if wordID_read != wordID:
                raise ValueError(f"Unexpected wordID read: {wordID_read} (expected: {wordID})")

            docID_data = file.read(doc_count * 8)  # Read the docIDs
            docIDs = list(struct.unpack(f"<{doc_count}Q", docID_data))

        # Step 3: Modify the entry
        if new_docID not in docIDs:
            docIDs.append(new_docID)

        # Step 4: Reconstruct the barrel
        new_barrel_data = []
        new_barrel_offsets = {}  # Store updated offsets for the specific barrel
        current_offset = 0

        with open(barrel_filename, 'rb') as file:
            while True:
                header_data = file.read(8)
                if not header_data:
                    break

                old_wordID, doc_count = struct.unpack("<II", header_data)
                docID_data = file.read(doc_count * 8)
                if old_wordID == wordID:
                    # Use the updated docIDs for this wordID
                    updated_data = struct.pack("<II", old_wordID, len(docIDs))
                    updated_docID_data = struct.pack(f"<{len(docIDs)}Q", *docIDs)
                    new_barrel_data.append(updated_data + updated_docID_data)
                else:
                    new_barrel_data.append(header_data + docID_data)

                # Record the offset for this wordID in the specific barrel
                new_barrel_offsets[old_wordID] = current_offset
                current_offset += len(new_barrel_data[-1])

        # Step 5: Write the reconstructed barrel
        with open(barrel_filename, 'wb') as file:
            for entry in new_barrel_data:
                file.write(entry)

        # Step 6: Update the offsets metadata for this barrel only
        metadata_file = os.path.join(self.output_dir, "offsets.bin")
        with open(metadata_file, 'r+b') as meta_file:
            while True:
                data = meta_file.read(12)  # 4 bytes for wordID, 8 bytes for offset
                if not data:
                    break

                existing_wordID, existing_offset = struct.unpack("<IQ", data)
                if existing_wordID in new_barrel_offsets:
                    # Update the offset for this wordID
                    updated_offset = new_barrel_offsets[existing_wordID]
                    meta_file.seek(-12, os.SEEK_CUR)  # Move back to overwrite
                    meta_file.write(struct.pack("<IQ", existing_wordID, updated_offset))

        self.load_offsets('barrels/inverted_index/offsets.bin')