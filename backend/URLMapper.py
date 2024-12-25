class URLMapper:
    def __init__(self):
        self.id_to_url = {}

    def get_url(self, docID):
        return self.id_to_url.get(docID, None)

    def read_from_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                while True:
                    # Read 2 bytes for the URL length
                    length_bytes = file.read(2)
                    if not length_bytes:  # End of file
                        break

                    url_length = int.from_bytes(length_bytes, byteorder='big')

                    # Read the URL of `url_length` bytes
                    url = file.read(url_length).decode('utf-8')

                    # Read 8 bytes for the docID
                    docID = int.from_bytes(file.read(8), byteorder='big')

                    # Store in the hash table
                    self.id_to_url[docID] = url
        except Exception as e:
            print(f"Error reading from file: {e}")
