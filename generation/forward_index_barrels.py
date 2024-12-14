from ForwardIndex import ForwardIndex, BarrelsManager

fi = ForwardIndex()
fi.read_from_file('files/forward_index.bin')

bm = BarrelsManager()

bm.make_barrels(fi)
