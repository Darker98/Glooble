from Lexicon import Lexicon

lexicon = Lexicon()
lexicon.read_from_file('files/lexicon.bin')
print(lexicon.get_word_id(""))