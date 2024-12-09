import pandas as pd
import nltk
from tokenize_text import tokenize_text
from Lexicon import Lexicon
from sorting import sort_and_save_lexicon

# Read dataset in chunks
chunks = pd.read_csv('articles_sample.csv', nrows = 100)

lexicon = Lexicon()

# Iterate over rows
columns_to_select = [0, 1, 3, 5]
#for chunk in chunks:
for row in chunks.itertuples(index=False):
    selected_columns = [row[i] for i in columns_to_select]
    for column_num, column in enumerate(selected_columns):
        tokenized = tokenize_text(column)
        for token in tokenized:
            lexicon.add_word(token)

lexicon.write_to_file('lexicon.bin')
sort_and_save_lexicon('lexicon.bin', 'lexicon.bin')