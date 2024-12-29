from Lexicon import Lexicon
from ForwardIndex import ForwardIndex
from InvertedIndex import InvertedIndex

lexicon = Lexicon()
lexicon.read_from_file('lexicon.bin')

print(lexicon.get_lexicon())