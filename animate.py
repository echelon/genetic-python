#!/usr/bin/env python
# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import Image
import gifmaker
import os

def main():
	dirname = './out-12'
	files = os.listdir(dirname)
	files.sort(reverse=True)

	count = 0
	seq = []
	for fname in files:
		if count % 10 == 0:
			im = Image.open(dirname+'/'+fname)
			im = im.convert("P") # P or L
			seq.append(im)
		count+= 1

	fp = open("out.gif", "wb")
	gifmaker.makedelta(fp, seq)
	fp.close()

if __name__ == '__main__': main()
