from Lexicon import Lexicon

def sort_and_save_lexicon(input_filename, output_filename):
    # Initialize the Lexicon object
    lexicon = Lexicon()

    # Read the lexicon from the input file
    lexicon.read_from_file(input_filename)

    # Get the lexicon dictionary
    lexicon_dict = lexicon.get_lexicon()

    # Sort the lexicon by word (alphabetically)
    sorted_lexicon = dict(sorted(lexicon_dict.items()))

    # Update the lexicon with the sorted dictionary
    lexicon.word_to_id = sorted_lexicon

    # Write the sorted lexicon back to a new file
    lexicon.write_to_file(output_filename)
