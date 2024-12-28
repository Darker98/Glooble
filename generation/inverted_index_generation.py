from ForwardIndex import ForwardIndex
from InvertedIndex import InvertedIndex

# Initialize ForwardIndex and load data
fi = ForwardIndex()
fi.read_from_file('files/forward_index.bin')  # Replace with the actual path to your file

# Retrieve the forward index
forward_index = fi.get_index()

# Initialize the inverted index
inverted_index = InvertedIndex()

# Build the inverted index
inverted_index.build_from_forward_index(forward_index)

inverted_index.write_to_file('files/inverted_index.bin', 'files/max_frequencies.bin')
