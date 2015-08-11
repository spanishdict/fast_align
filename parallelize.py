import sys
from itertools import izip

outf = open(sys.argv[3], 'w+')
with open(sys.argv[1]) as src, open(sys.argv[2]) as trg:
	for x, y in izip(src, trg):
		outf.write(x.strip() + " ||| " +  y.strip() + '\n')
outf.close()
