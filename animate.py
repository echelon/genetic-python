#!/usr/bin/env python
# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import Image
import gifmaker
import os
import sys

def main():
	if len(sys.argv) < 2:
		print "usage: animate.py inputdir [skip]"
		sys.exit()
	dirname = sys.argv[1]

	outfileL = "./outL.gif"
	outfileP = "./outP.gif"

	skip = 0
	if len(sys.argv) > 2:
		skip = int(sys.argv[2])

	makeGif(dirname, outfileL, skip, "L")
	makeGif(dirname, outfileP, skip, "P")


def makeGif(inputdir, outfile, skip = 10, colorMode = "P", reverse=False):
	files = os.listdir(inputdir)
	files.sort(reverse=reverse)
	count = 0
	seq = []
	for fname in files:
		if skip > 1 and count % skip != 0:
			count+= 1
			continue
		im = Image.open(inputdir+'/'+fname)
		im = im.convert(colorMode) # P or L
		seq.append(im)
		count+= 1

	fp = open(outfile, "wb")
	gifmaker.makedelta(fp, seq)
	fp.close()

if __name__ == '__main__': main()
