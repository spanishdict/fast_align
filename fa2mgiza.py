# Converts Fast Align output into MGIZA output format
# Usage: `python fa2mgiza.py corpus.bi alignments.sym alignments.en-es alignments.es-en`

import sys
from itertools import izip

corpus = open(sys.argv[1]) # /bi/ corpus
aligns = open(sys.argv[2]) # symmetrized file
scoresENES = open(sys.argv[3]) # .en-es
scoresESEN = open(sys.argv[4]) # .es-en
outENES = open(sys.argv[2] + '.en-es.mgiza', 'w+')
outESEN = open(sys.argv[2] + '.es-en.mgiza', 'w+')

def parens(v):
	return '({ ' + ' '.join(v) + '})'

def alignSent(src, trgLn, aligns, d):
	remaining = [1] * trgLn
	m = []
	for x in src:
		m.append([])
	for a in aligns:
		if d:
			s, t = [int(v) for v in a.split('-')]
		else:
			t, s = [int(v) for v in a.split('-')]
		remaining[t] = 0
		m[s].append(str(t+1)+' ')
	n = []
	for i in range(0, trgLn):
		if remaining[i] > 0:
			n.append(str(i+1)+' ')
	for i in range(len(m)-1, -1, -1):
		src.insert(i+1, parens(m[i]))
	src.insert(0, "NULL")
	src.insert(1, parens(n))
	return ' '.join(src)

def doLang(i, src0, trg0, alignments, d, score, outF):
	src = src0.split(' ')
	trg = trg0.split(' ')
	srcLn = len(src)
	trgLn = len(trg)
	outF.write('# Sentence pair (' + str(i) + ') source length ' + str(srcLn) + ' target length ' + str(trgLn) + ' alignment score : ' + score + '\n')
	outF.write(trg0 + '\n')
	outF.write(alignSent(src, trgLn, alignments, d) + '\n')

def doErr(outF):
	outF.write('# Sentence pair ERR\n')
	outF.write('# Sentence pair ERR\n')
	outF.write('# Sentence pair ERR\n')

test = ""
i = 0
for c, a, senes, sesen in izip(corpus, aligns, scoresENES, scoresESEN):
	i = i + 1
	if i % 100000 == 0:
		print 'line ' + str(i)
	aa = a[:-1]
	if len(aa) < 1:
		doErr(outENES)
		doErr(outESEN)
		continue
	alignments = aa.split(' ')
	scoreENES = senes[:-1].split(' /// ')[1]
	scoreESEN = sesen[:-1].split(' /// ')[1]
	en0, es0 = c[:-1].split(' ||| ')
	doLang(i, en0, es0, alignments, True, scoreENES, outENES)
	doLang(i, es0, en0, alignments, False, scoreESEN, outESEN)
outENES.close()