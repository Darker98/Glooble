from ForwardIndex import ForwardIndex

# Initialize ForwardIndex and load data
fi = ForwardIndex()
fi.read_from_file('forward_index.bin')  # Replace with the actual path to your file

# Retrieve the forward index
forward_index = fi.get_index()

# Initialize the inverted index
inverted_index = {}

# Build the inverted index
for doc_id, word_ids in forward_index.items():
    for word_id in word_ids:
        if word_id not in inverted_index:
            inverted_index[word_id] = []
        inverted_index[word_id].append(doc_id)

# Print the inverted index
print(inverted_index)