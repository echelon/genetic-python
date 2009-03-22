#!/usr/bin/env python
# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import Image, ImageDraw
import random
import math
import aggdraw
import os
from optparse import *

from genetic.IndivCircle import *
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
	formatter = IndentedHelpFormatter(indent_increment=4, max_help_position=40, width=80)
	parser = OptionParser(usage="%prog -f INFILE -o OUTDIR [other opts]", 
						  version="%prog 0.1", formatter=formatter)

	# File options
	group = OptionGroup(parser, "File and Directory Options")
	group.add_option("-f", "--file", dest = "filename", default = None,
					  help = "Input file to evolve to", metavar = "FILE")
	group.add_option("-o", "--out", dest = "outputDir", default = "./out",
					  help = "Directory to save output files in", 
					  metavar = "DIR")
	parser.add_option_group(group)

	# Individual Options
	group = OptionGroup(parser, "Individual Options",
						"These options affect how individuals evolve")
	group.add_option("-g", "--genes", dest = "numGenes", default = 20,
					  help = "Number of genes", metavar = "NUM")
	group.add_option("-m", "--iMutation", dest = "initMutate", default = 50,
					  help = "Number of mutations for initial generation", 
					  metavar = "NUM")
	parser.add_option_group(group)

	# Population Options
	group = OptionGroup(parser, "Population Options",
						"These options affect the population dynamics")
	group.add_option("-i", "--iSize", dest = "initSize", default = 5,
					  help = "Initial size of the population", 
					  metavar = "SIZE")
	group.add_option("-s", "--mSize", dest = "maxSize", default = 20,
					  help = "Maximum size of the population", metavar = "SIZE")
	parser.add_option_group(group)

	# Get args
	(options, args) = parser.parse_args()

	if not options.filename:
		print "Did not supply -f INPUT FILE. Check the help docs with --help."
		return

	# Begin evolution
	P = Population(options.filename, options.outputDir, 
				   initSize = int(options.initSize), 
				   maxSize = int(options.maxSize),
				   numGenes = int(options.numGenes),
				   initMutate = int(options.initMutate))
	P.runEvolution()

if __name__ == "__main__": main()
