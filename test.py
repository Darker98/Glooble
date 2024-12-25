import time
from generation.tokenize_text import tokenize_text
from generation.Lexicon import Lexicon
from backend.Lexicon import HashTable

sum = 0
for i in range(100):
    start_time = time.time()
    lexicon = Lexicon()
    lexicon.read_from_file('generation/files/lexicon.bin')
    for word in tokenize_text("this is some sample text to check operation"):
        lexicon.get_word_id(word)
    sum += time.time() - start_time
print(sum/100)

sum = 0
for i in range(100):
    start_time = time.time()
    lexicon = HashTable()
    lexicon.read_from_file("generation/files/lexicon.bin")
    for word in tokenize_text("this is some sample text to check operation"):
        lexicon.get_word_id(word)
    sum += time.time() - start_time
print(sum/100)
