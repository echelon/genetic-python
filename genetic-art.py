#!/usr/bin/env python
# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import Image, ImageDraw
import random
import math
import aggdraw
import os
from optparse import OptionParser

from genetic.IndividualCircle import *
from genetic.IndividualPixel import *
from genetic.Population import *

"""
The theory is that evolution isn't just random, but that it intelligently 
preserves valuable information through the cross of the most fit individuals. 
Random mutation is the operator that introduces solutions, but crossing is the 
operator that preserves them. Care must be taken to ensure that evolutionary
algorithms do not become random search. 
"""

def main():
	"""Run the evolutionary algorithm"""
	# Command line options
	parser = OptionParser()
	parser.add_option("-f", "--file", dest = "filename", default = None,
					  help = "Input file to evolve to", metavar = "FILE")
	parser.add_option("-o", "--out", dest = "outputDir", default = "./out",
					  help = "Directory to save output files in", 
					  metavar = "DIR")
	parser.add_option("-i", "--init", dest = "initSize", default = 5,
					  help = "Initial size of the population", 
					  metavar = "SIZE")
	parser.add_option("-s", "--size", dest = "maxSize", default = 20,
					  help = "Maximum size of the population", metavar = "SIZE")
	parser.add_option("-c", "--coding", dest = "codingSeq", default = 20,
					  help = "Number of coding sequences", metavar = "NUM")

	(options, args) = parser.parse_args()

	if not options.filename:
		print "Did not supply -f INPUT FILE. Check the help docs with --help."
		return

	# Begin evolution
	P = Population(options.filename, options.outputDir, 
				   initSize = int(options.initSize), 
				   maxSize = int(options.maxSize),
				   codingSeq = int(options.codingSeq))
	P.runEvolution()

if __name__ == "__main__": main()

