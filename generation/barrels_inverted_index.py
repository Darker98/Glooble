import os
import json
import struct

class BarrelManager:
    def _init_(self, num_barrels=10, output_dir="barrels"):
        self.num_barrels = num_barrels  # Number of barrels
        self.output_dir = output_dir  # Directory to store barrels
        self.pointers = {}  # Mapping of barrels to their wordID ranges or hashes

    def split_into_barrels(self, word_to_docIDs):
        """
        Split the inverted index into barrels and save them as separate files.
        :param word_to_docIDs: The inverted index (wordID -> list of docIDs).
        """
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure the output directory exists

        # Initialize barrels (as dictionaries for now)
        barrels = [{} for _ in range(self.num_barrels)]

        # Assign wordIDs to barrels
        for wordID, docIDs in word_to_docIDs.items():
            barrel_index = wordID % self.num_barrels  # Example: hash-based assignment
            barrels[barrel_index][wordID] = docIDs

        # Write each barrel to a file
        for i, barrel in enumerate(barrels):
            barrel_filename = f"{self.output_dir}/barrel_{i}.bin"
            self.pointers[f"barrel_{i}"] = list(barrel.keys())  # Keep track of the wordIDs in this barrel
            with open(barrel_filename, 'wb') as file:
                for wordID, docIDs in barrel.items():
                    # Serialize and write wordID and its docIDs
                    data = struct.pack("<IH", wordID, len(docIDs))  # I = unsigned int, H = unsigned short
                    docID_data = struct.pack(f"<{len(docIDs)}Q", *docIDs)  # Q = unsigned long long
                    file.write(data + docID_data)

    def save_pointers(self, filename="pointers.json"):
        """
        Save the pointers list to a file.
        :param filename: File to save the pointers list.
        """
        with open(filename, 'w') as file:
            json.dump(self.pointers, file, indent=4)
