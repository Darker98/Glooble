import pandas as pd
import nltk
from tokenize_text import tokenize_text
from Lexicon import Lexicon
from sorting import sort_and_save_lexicon


# Read dataset in chunks
chunks = pd.read_csv('files/medium_articles.csv', chunksize=1000)

lexicon = Lexicon()

# Iterate over rows
try:
    columns_to_select = [0, 1, 3, 5]
    rowNo = 1
    for chunk in chunks:
        for row in chunk.itertuples(index=False):
            selected_columns = [row[i] for i in columns_to_select]
            for column_num, column in enumerate(selected_columns):
                tokenized = tokenize_text(column)
                for token in tokenized:
                    lexicon.add_word(token)

            # Keep track of which row execution is at
            if rowNo % 50 == 0:
                print(rowNo)
            rowNo += 1
except:
    print(rowNo)

lexicon.write_to_file('lexicon.bin')
sort_and_save_lexicon('files/lexicon.bin', 'files/lexicon.bin')

lexicon = Lexicon()
lexicon.read_from_file('lexicon.bin')
print((lexicon.get_lexicon()))
