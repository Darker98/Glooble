import os


class URLMapper:
    def __init__(self):
        self.id_to_offset = {}  # Maps docID to offset

    def read_offsets_from_file(self, offset_file_path):
        """Reads the offset file and populates the id_to_offset hash table."""
        try:
            with open(offset_file_path, 'rb') as file:
                while True:
                    # Read 8 bytes for the docID
                    docID_bytes = file.read(8)
                    if not docID_bytes:  # End of file
                        break

                    docID = int.from_bytes(docID_bytes, byteorder='big')

                    # Read 8 bytes for the offset
                    offset = int.from_bytes(file.read(8), byteorder='big')

                    # Store in the hash table
                    self.id_to_offset[docID] = offset
        except Exception as e:
            print(f"Error reading offset file: {e}")

    def get_details_by_docID(self, docID, file_path):
        """Fetches details (URL, title, tags, authors) by docID using the offset."""
        try:
            offset = self.id_to_offset.get(docID)
            if offset is None:
                return None  # docID not found

            with open(file_path, 'rb') as file:
                # Seek to the offset
                file.seek(offset)

                # Read details
                # Read 2 bytes for URL length
                url_length = int.from_bytes(file.read(2), byteorder='big')
                url = file.read(url_length).decode('utf-8')

                # Read 2 bytes for title length
                title_length = int.from_bytes(file.read(2), byteorder='big')
                title = file.read(title_length).decode('utf-8')

                # Read tags
                num_tags = int.from_bytes(file.read(1), byteorder='big')
                tags = []
                for _ in range(num_tags):
                    tag_length = int.from_bytes(file.read(1), byteorder='big')
                    tag = file.read(tag_length).decode('utf-8')
                    tags.append(tag)
                if num_tags == 0:
                    tags.append("None")

                # Read authors
                num_authors = int.from_bytes(file.read(1), byteorder='big')
                authors = []
                for _ in range(num_authors):
                    author_length = int.from_bytes(file.read(1), byteorder='big')
                    author = file.read(author_length).decode('utf-8')
                    authors.append(author)
                if num_authors == 0:
                    authors.append("Unknown")

                # Read text
                text_length = int.from_bytes(file.read(2), byteorder='big')
                text = file.read(text_length).decode('utf-8')

                return {
                    "url": url,
                    "title": title,
                    "tags": tags,
                    "authors": authors,
                    "text": text
                }
        except Exception as e:
            print(f"Error fetching details for docID {docID}: {e}")
            return None

    def add_entry(self, docID, url, title, tags, authors, text):
        """Adds a new entry to the URL mapper file and stores its offset."""
        try:
            with open('files/url_mapper.bin', 'ab+') as file:
                # Determine the current offset (end of the file)
                file.seek(0, os.SEEK_END)
                offset = file.tell()

                # Encode the URL, title, tags, authors, and text
                url_encoded = url.encode('utf-8')
                title_encoded = title.encode('utf-8')
                tags_encoded = [tag.encode('utf-8') for tag in tags]
                authors_encoded = [author.encode('utf-8') for author in authors]
                text_encoded = text.encode('utf-8')

                # Write URL length and URL
                file.write(len(url_encoded).to_bytes(2, byteorder='big'))
                file.write(url_encoded)

                # Write title length and title
                file.write(len(title_encoded).to_bytes(2, byteorder='big'))
                file.write(title_encoded)

                # Write tags
                file.write(len(tags_encoded).to_bytes(1, byteorder='big'))
                for tag in tags_encoded:
                    file.write(len(tag).to_bytes(1, byteorder='big'))
                    file.write(tag)

                # Write authors
                file.write(len(authors_encoded).to_bytes(1, byteorder='big'))
                for author in authors_encoded:
                    file.write(len(author).to_bytes(1, byteorder='big'))
                    file.write(author)

                # Write text length and text
                file.write(len(text_encoded).to_bytes(2, byteorder='big'))
                file.write(text_encoded)

                # Update the offset mapping
                self.id_to_offset[docID] = offset

            # Update the offset file
            with open('files/offsets.bin', 'ab') as offset_file:
                offset_file.write(docID.to_bytes(8, byteorder='big'))
                offset_file.write(offset.to_bytes(8, byteorder='big'))

        except Exception as e:
            print(f"Error adding entry for docID {docID}: {e}")
