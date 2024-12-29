import struct
import os


class BarrelReader:
    def __init__(self, num_barrels=60, output_dir="barrels/inverted_index"):
        self.num_barrels = num_barrels  # Number of barrels
        self.output_dir = output_dir  # Directory where barrels and offsets are stored
        self.offsets = {}  # Hash table to store wordID -> (barrel_index, offset) mapping

    def load_offsets(self, offsets_file):
        """Load the offsets metadata into memory."""
        with open(offsets_file, 'rb') as file:
            while True:
                data = file.read(8)  # 4 bytes for wordID, 4 bytes for offset
                if not data:
                    break
                wordID, offset = struct.unpack("<II", data)
                self.offsets[wordID] = offset

    def read_docIDs_and_scores(self, wordID, total_docs, max_frequencies):
        """
        Retrieve the list of docIDs and calculate their scores for the given wordID.
        """
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

            # Calculate the number of documents containing the word
            num_docs_with_word = doc_count

            docIDs_and_scores = []

            for _ in range(doc_count):
                entry_data = file.read(11)  # 8 bytes docID, 1 byte context flags, 2 bytes frequency
                docID, context_flags, frequency = struct.unpack("<QBH", entry_data)

                # Determine context weight based on context flags
                context_weight = 1  # Default context weight for text only
                if context_flags & 0b0001:  # Title
                    context_weight = 3
                elif context_flags & 0b0010:  # Text
                    context_weight = 1
                elif context_flags & 0b0100:  # Tags
                    context_weight = 2
                elif context_flags & 0b1000:  # Authors
                    context_weight = 2

                # Calculate the score
                max_freq = max_frequencies.get(docID, 1)  # Avoid division by zero
                score = (
                    (frequency / max_freq) *
                    (total_docs / (1 + num_docs_with_word)) *
                    context_weight
                )

                # Append the docID and its score to the result list
                docIDs_and_scores.append((docID, score))

        return docIDs_and_scores

    def get_wordID_offset(self, wordID):
        if wordID in self.offsets.keys():
            return self.offsets[wordID]
        return -1

    def update_barrel_entry(self, wordID, new_doc_ID, word_data):
        """
        Update or append an entry for a wordID in the appropriate barrel and recalculate offsets.
        """
        barrel_index = wordID % self.num_barrels
        barrel_filename = os.path.join(self.output_dir, f"barrel_{barrel_index}.bin")
        offsets_file = os.path.join(self.output_dir, "offsets.bin")

        # Load the entire barrel into memory
        barrel_data = {}
        with open(barrel_filename, 'rb') as file:
            while True:
                header = file.read(8)  # 4 bytes wordID, 4 bytes doc count
                if not header:
                    break
                curr_wordID, doc_count = struct.unpack("<II", header)
                entries = [
                    struct.unpack("<QBH", file.read(11))
                    for _ in range(doc_count)
                ]
                barrel_data[curr_wordID] = entries

        # Modify or add the entry for the given wordID
        if wordID in barrel_data:
            # Update the existing wordID entry
            existing_entries = barrel_data[wordID]
            for i, (docID, _, _) in enumerate(existing_entries):
                if docID == new_doc_ID:
                    existing_entries[i] = word_data  # Update the document data
                    break
            else:
                existing_entries.append(word_data)  # Add new document data
        else:
            # Add a new wordID entry
            barrel_data[wordID] = [word_data]

        # Recalculate offsets and write back the updated barrel
        new_offsets = {}
        with open(barrel_filename, 'wb') as file:
            offset = 0
            for curr_wordID, entries in sorted(barrel_data.items()):
                # Write header: wordID and number of entries
                header = struct.pack("<II", curr_wordID, len(entries))
                file.write(header)
                offset += len(header)

                # Write document entries
                for entry in entries:
                    doc_entry = struct.pack("<QBH", *entry)
                    file.write(doc_entry)
                    offset += len(doc_entry)

                # Update the offsets for the current wordID
                new_offsets[curr_wordID] = offset - len(header) - len(entries) * 11

        # Merge new offsets with the in-memory offsets
        self.offsets.update(new_offsets)

        # Write the updated offsets to the offsets.bin file
        with open(offsets_file, 'wb') as file:
            for curr_wordID, word_offset in sorted(self.offsets.items()):
                file.write(struct.pack("<II", curr_wordID, word_offset))

