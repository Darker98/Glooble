from InvertedIndex import InvertedIndex, BarrelsManager

ii = InvertedIndex()
ii.read_from_file('files/inverted_index.bin')

bm = BarrelsManager()

bm.make_barrels(ii)
