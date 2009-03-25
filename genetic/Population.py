# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import Image, ImageDraw
import random
import math
import os
import cPickle as pickle

from GAIndividual import *
from IndivCircle import * 

# TODO: Population should be generic. make PopCircle, PopPixel, etc.
# TODO: Better way to track improvement/percentGain statistics. New class? Graphing?

# TODO: Huge project for mathematical proving/better heuristics/rates ->
# Track historical mutations in codons and cross points, also taking into account
# variable lengths and a possible expansion to GP's that will allow us to build a 
# model for crossover potential and mutation rate statistics
#

#
#
#
# TODO/ README/ FIXME
# If I get back and evolution hasn't changed much (currently below 2.6%), then
# implement variable-length GA's and a much more dynamic generation mutation 
# scheme
#
#
#

class Population:

	def __init__(self, targetImage, imgOutputDir = "./out", objOutputDir = "./obj",
				 loadObjs = False, initSize = 5, maxSize = 20, initGenes = 5, 
				 maxGenes = 30, initMutate = 5):
		"""Initialize the target and the population"""

		# Target to approximate
		self.target = Image.open(targetImage)
		self.targetThumb = self.target.resize(
			(self.target.size[0]/4,
			self.target.size[1]/4)
		)

		# Directory to save evolution result images to
		self.imgOutputDir = "./out"
		if imgOutputDir:
			self.imgOutputDir = imgOutputDir

		# Directory to save evolution result objects to
		self.objOutputDir = "./obj"
		if objOutputDir:
			self.objOutputDir = objOutputDir

		# Evolution Population
		self.indivs = []
		self.generation = 0
		self.improvement = 0

		# Individual gene counts / Population sizes
		self.initGenes = initGenes
		self.maxGenes  = maxGenes
		self.initSize = initSize
		self.maxSize  = maxSize
		self.initMutate = initMutate

		# Prep individual class
		IndivCircle.setNumGenes(initGenes, maxGenes)
		IndivCircle.setImageSize(self.target.size[0], self.target.size[1])

		# Load individuals from a previous run?
		# New individuals will also be generated.
		if loadObjs:
			self.indivs = self.loadObjs()

		# Generate initial population - if smaller than eventual size limit,
		# it will grow in subseqent generations. If set larger (an unwise 
		# waste of CPU), it will be culled in evolution to the eventual size.
		size = self.maxSize
		if initSize:
			size = self.initSize

		for i in range(size):
			indiv = IndivCircle()
			for x in range(initMutate):
				indiv.mutate()
			indiv.draw()
			indiv.evalFitness(self.target, self.targetThumb)
			self.indivs.append(indiv)


	def runEvolution(self):
		"""Evolutionary main loop. This adjusts the population to 
		scale to the fitness function."""

		topScore = 0
		lastTopScore = 0
	
		# Run Each Generation
		while(topScore < 9999999999999): 
			lastTopScore = topScore
			self.generation += 1

			# Dynamic evolution - best first.
			topIndex = 1
			for i in range(20):
				iParentA = random.randint(0, topIndex)
				iParentB = random.randint(0, topIndex)
				while iParentA == iParentB:
					iParentB = random.randint(0, topIndex)

				child = self.indivs[iParentA].cross(self.indivs[iParentB], self.generation)	
				child.mutate(topIndex) 
				child.draw()
				child.evalFitness(self.target, self.targetThumb)
				self.indivs.append(child)

				# Increse breeding index size, but don't include bad individuals
				topIndex = min(topIndex+1, self.maxSize-1, len(self.indivs)-1) 


			# Sort by performance, and cull the straglers
			self.indivs.sort(self.scoreCmp)
			worst = self.indivs[-1:1]
			print self
			self.indivs = self.indivs[0:self.maxSize]

			# Update Top Score
			if topScore < self.indivs[0].getScore():
				topScore = self.indivs[0].getScore()

			self.improvement = topScore - lastTopScore

			# Save image
			fname = self.imgOutputDir + "/score-"+str(topScore)+".png"
			if not os.path.isfile(fname):
				self.indivs[0].saveImageAs(fname)

			# Pickle object
			fname = self.objOutputDir + "/score-"+str(topScore)+".pkl"
			if not os.path.isfile(fname):
				self.indivs[0].saveObjectAs(fname)


	def loadObjs(self, directory = None, limit = 10, reverse = True):
		"""Use the Pickler to load the Individual objects located in the 
		files of the directory. Limit and sort order are supported."""
		if not directory:
			directory = self.objOutputDir

		files = os.listdir(directory)
		files.sort(reverse=reverse)
		count = 0
		objs = []
		for fname in files:
			if count >= limit:
				break
			path = directory+'/'+fname
			size = os.path.getsize(path)
			if size == 0:
				continue
			f = open(path, 'r')
			obj = pickle.load(f)
			objs.append(obj)
			f.close()
			count += 1
		return objs


	def __str__(self):
		"""Represent the generation's statistics. Used for tracking the 
		evolutionary improvement and performance as well as debugging."""
		ret = ""
		ret += "\tGENERATION " + str(self.generation)
		ret += " (improved " + str(self.improvement) + ")\n\n"
		ret += "gen\tid\tgenes\tmut\tadd\trem\tP1/P2\t\tscore (percent)\n"
		for i in range(len(self.indivs)-1): # TODO: Only show the top 10
			indiv = self.indivs[i]
			gen = indiv.generation
			if gen == self.generation:
				ret+= "New\t"
			else:
				ago = self.generation - gen
				ret+= str(ago) + " Ago\t"
 			ret += str(indiv.id) + "\t"
			ret += str(indiv.chromosome.getNumGenes()) + "\t"
			ret += str(indiv.mutationCnt) + "\t"
			ret += str(indiv.genesAdd) + "\t"
			ret += str(indiv.genesRem) + "\t"
			ret += str(indiv.parent1id) + "/"
			ret += str(indiv.parent2id) + "\t\t"
			ret += str(indiv.getScore()) + " (" 
			ret += "%.04f" % indiv.scorePercent + "%)\t"
			if i >= self.maxSize:
				ret += "*d"
			ret += "\n"
		ret += "\nParams: InitSize: " + str(self.initSize)
		ret += " MaxSize: " + str(self.maxSize)
		ret += " InitGenes: " + str(self.initGenes)
		ret += " MaxGenes: " + str(self.maxGenes)
		ret += " InitMutate: " + str(self.initMutate) + "\n"
		ret += "\tGENERATION " + str(self.generation)
		ret += " (improved " + str(self.improvement) + ")\n"
		return ret


	def scoreCmp(self, a, b):
		"""Score comparison callback, a maximization comparator"""
		if a.getScore() < b.getScore():
			return 1
		elif a.getScore() == b.getScore():
			return 0
		else:
			return -1

