import struct


class Lexicon:
    def __init__(self):
        self.word_to_id = {}  # Dictionary to store word -> unique ID mapping
        self.id_to_word = {}  # Dictionary for reverse lookup
        self.current_id = 0    # Starting ID for words

    def add_word(self, word):
        if word not in self.word_to_id:
            self.word_to_id[word] = self.current_id
            self.id_to_word[self.current_id] = word
            self.current_id += 1  # Increment ID for the next word

    def get_word_id(self, word):
        return self.word_to_id.get(word, None)

    def get_word(self, wordID):
        return self.id_to_word.get(wordID, None)

    def get_lexicon(self):
        return self.word_to_id

    def write_to_file(self, filename):
        with open(filename, 'wb') as file:
            for word, word_id in self.word_to_id.items():
                word_length = len(word)

                data = struct.pack(f"<B{word_length}sI", word_length, word.encode('utf-8', errors='remove'), word_id)
                file.write(data)

    def read_from_file(self, filename):
        with open(filename, 'rb') as file:
            while True:
                # Read 1 byte for the word length
                length_data = file.read(1)
                if not length_data:
                    break  # End of file

                # Unpack the word length
                word_length = struct.unpack("<B", length_data)[0]

                # Read the word and 4 bytes for the ID
                word_data = file.read(word_length)
                id_data = file.read(4)

                # Unpack the word and ID
                try:
                    word = word_data.decode('utf-8')
                    prev_word = word
                except UnicodeDecodeError as e:
                    # Print the byte sequence that caused the error
                    print(f"Error at byte position {e.start}-{e.end}: {word[e.start:e.end]}")
                    print(prev_word)

                word_id = struct.unpack("<I", id_data)[0]

                # Reconstruct the dictionaries
                self.word_to_id[word] = word_id
                self.id_to_word[word_id] = word

                # Update the current ID (optional, useful for adding new words after reading)
                self.current_id = max(self.current_id, word_id + 1)