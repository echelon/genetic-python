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

from genetic.IndivPoly import *
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
	group.add_option("-f", "--file", dest = "filename", 
					  default = None,
					  help = "Input file to evolve to", metavar = "FILE")
	group.add_option("-o", "--outImg", dest = "imgOutputDir", 
					  default = "./out",
					  help = "Directory to save output images in", 
					  metavar = "DIR")
	group.add_option("-p", "--outObj", dest = "objOutputDir", 
					  default = "./obj",
					  help = "Directory to save serialized objects in", 
					  metavar = "DIR")
	group.add_option("-z", "--loadObjs", dest = "loadObjs", 
					  default = False,
					  help = "Load objects from a previous generation?", 
					  metavar = "True")
	parser.add_option_group(group)

	# Individual Options
	group = OptionGroup(parser, "Individual Options",
						"These options affect how individuals evolve")
	group.add_option("-i", "--iGenes", dest = "initGenes", 
					  default = 5,
					  help = "Initial number of genes", metavar = "NUM")
	group.add_option("-m", "--mGenes", dest = "maxGenes", 
					  default = 60,
					  help = "Maximum number of genes", metavar = "NUM")
	group.add_option("-x", "--iMutation", dest = "initMutate", 
					  default = 5,
					  help = "Number of mutations for initial generation", 
					  metavar = "NUM")
	parser.add_option_group(group)

	# Population Options
	group = OptionGroup(parser, "Population Options",
						"These options affect the population dynamics")
	group.add_option("-s", "--iSize", dest = "initSize", 
					  default = 5,
					  help = "Initial size of the population", metavar = "SIZE")
	group.add_option("-l", "--mSize", dest = "maxSize", 
					  default = 40,
					  help = "Maximum size of the population", metavar = "SIZE")
	parser.add_option_group(group)

	# Get args
	(options, args) = parser.parse_args()

	if not options.filename:
		print "Did not supply -f INPUT FILE. Check the help docs with --help."
		return

	print "DEBUG - NUMBER OF GENES SET STATIC!"
	genes = int(options.initGenes)

	# Begin evolution
	P = Population("TODO",
				   options.filename, 
				   options.imgOutputDir, 
				   options.objOutputDir, 
				   loadObjs   = bool(options.loadObjs),
				   initSize	  = int(options.initSize), 
				   maxSize	  = int(options.maxSize),
				   initGenes  = genes,
				   maxGenes	  = genes,
				   initMutate = int(options.initMutate))

	P.runEvolution()

if __name__ == "__main__": main()

