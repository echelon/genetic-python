#!/usr/bin/env python2.6

import os
import sys
import time
from optparse import *

# TODO README XXX
"""
This code is terrible. 
	* It's not really GA
	* It's not really GP
	* Individuals can live forever.
		* On that note, the algo reaches local maxima and never leaves

	* The code itself sucks. It's disorganized, barely comprehensible. 
		* Too complex...

I need to write a generic GA/GP that I can use in the future, but I also
am very short on time...

	* I want to be able to use this in my algorithm heatmap research project
	* Forget OO for a minute-- just model the basics of evolution in GA and GP
	  then attach these to what ever objects I design for each project.

Multicore:
	* Some cores can have differential ability. Make this easy:		
		* Some cores can evolve at a faster rate
		* Some cores can select a different heuristic function

	c1 = Core {
		grayscale heuristic func {}
		evolve quickly
		high level of import
		high level of export
	}

	c2 = {
		YUV heuristic func {}
		evolve slowly
		low level of import
		low level of export
	}
	c3 = {
		threshold heuristic func {}
		evolve very quickly
		high level of import
		low level of export
	}

"""

def getArgs():

	# Default Values
	imgOutputDir = "./output/images"
	objOutputDir = "./output/state"
	loadObjs = False

	initSize = 10 # (Population)
	maxSize  = 20
	initGenes = 50
	maxGenes  = 100

	initMutate = 200 # Mutations to start with
	#initMutate = 1

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
					  default = imgOutputDir,
					  help = "Directory to save output images in", 
					  metavar = "DIR")
	group.add_option("-p", "--outObj", dest = "objOutputDir", 
					  default = objOutputDir,
					  help = "Directory to save serialized objects in", 
					  metavar = "DIR")
	group.add_option("-z", "--loadObjs", dest = "loadObjs", 
					  default = loadObjs,
					  help = "Load objects from a previous generation?", 
					  metavar = "True")
	parser.add_option_group(group)

	# Individual Options
	group = OptionGroup(parser, "Individual Options",
						"These options affect how individuals evolve")
	group.add_option("-i", "--iGenes", dest = "initGenes", 
					  default = initGenes,
					  help = "Initial number of genes", metavar = "NUM")
	group.add_option("-m", "--mGenes", dest = "maxGenes", 
					  default = maxGenes,
					  help = "Maximum number of genes", metavar = "NUM")
	group.add_option("-x", "--iMutation", dest = "initMutate", 
					  default = initMutate,
					  help = "Number of mutations for initial generation", 
					  metavar = "NUM")
	parser.add_option_group(group)

	# Population Options
	group = OptionGroup(parser, "Population Options",
						"These options affect the population dynamics")
	group.add_option("-s", "--iSize", dest = "initSize", 
					  default = initSize,
					  help = "Initial size of the population", metavar = "SIZE")
	group.add_option("-l", "--mSize", dest = "maxSize", 
					  default = maxSize,
					  help = "Maximum size of the population", metavar = "SIZE")
	parser.add_option_group(group)

	# Get args
	(options, args) = parser.parse_args()
	return options

def main():

	options = getArgs()

	if not options.filename:
		print "Did not supply -f INPUT FILE. Check --help."
		return

	processes = 0
	while processes < 8:
		pid = os.fork()
		processes += 1
		if not pid:
			# Child
			import genetic.Population
			p = genetic.Population.Population("Population %d" % processes,
						   options.filename, 
						   options.imgOutputDir, 
						   options.objOutputDir, 
						   loadObjs   = bool(options.loadObjs),
						   initSize	  = int(options.initSize), 
						   maxSize	  = int(options.maxSize),
						   initGenes  = int(options.initGenes),
						   maxGenes	  = int(options.maxGenes),
						   initMutate = int(options.initMutate))
	
			p.runEvolution()
			sys.exit(0)

	# Parent reaches this point
	try:
		while 1:
			time.sleep(100) 
	except KeyboardInterrupt:
		print "\nEnd of genetic algorithm"

if __name__ == "__main__": main()


