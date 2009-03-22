# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import Image, ImageDraw
import random
import math
import os

from IndividualGA import *
from IndividualCircle import * # TODO: Population should be generic. make PopulationCircle
from IndividualPixel import *

class Population:
	children = 10

	def __init__(self, targetImage, outputDir = "./out",
		initSize = 5, maxSize = 20, codingSeq = 20):
		"""Initialize the target and the population"""

		# Target to approximate
		self.target = Image.open(targetImage)
		self.targetThumb = self.target.resize(
			(self.target.size[0]/4,
			self.target.size[1]/4)
		)

		# Directory to save evolution result images to
		self.outputDir = "./out"
		if outputDir:
			self.outputDir = outputDir

		# Evolution Population
		self.indivs = []

		# Maximum population size
		self.maxSize = maxSize
		self.initSize = initSize

		# Prep individual class
		IndividualPixel.setCodingLen(codingSeq)
		IndividualPixel.setImageSize(self.target.size[0], self.target.size[1])

		# Generate initial population - if smaller than eventual size limit,
		# it will grow in subseqent generations. If set larger (an unwise 
		# waste of CPU), it will be culled in evolution to the eventual size.
		size = self.maxSize
		if initSize:
			size = self.initSize

		for i in range(size):
			#indiv = IndividualCircle()
			indiv = IndividualPixel()
			for x in range(50):
				indiv.mutate()
			indiv.draw()
			indiv.evalFitness(self.target, self.targetThumb)
			self.indivs.append(indiv)

	def runEvolution(self):
		"""Evolutionary main loop. This adjusts the population to 
		scale to the fitness function."""

		topScore = 0
		lastTopScore = 0
		topIndiv = None
		generation = 0
	
		# Run Each Generation
		while(topScore < 9999999999999): 
			lastTopScore = topScore
			generation += 1

			# Index of top 20% of population
			topFifth = int(math.ceil(len(self.indivs)*0.2))
			if topFifth < 4:
				topFifth = len(self.indivs)

			# Top 20% Parents - Low Mutation
			for i in range(5):
				iParentA = random.randint(0, topFifth-1)
				iParentB = random.randint(0, topFifth-1)
				while iParentA == iParentB:
					iParentB = random.randint(0, topFifth-1)
				mutateLo = 0
				mutateHi = int(IndividualCircle._chromoLength * 0.009)
				#mutateHi = int(IndividualCircle._codingSeqs * 0.09)
				child = self.indivs[iParentA].cross(
					self.indivs[iParentB], mutateLo, mutateHi)
				child.draw()
				child.evalFitness(self.target, self.targetThumb)
				self.indivs.append(child)


			# Top 20% Parents - High Mutation
			for i in range(5):
				iParentA = random.randint(0, topFifth-1)
				iParentB = random.randint(0, topFifth-1)
				while iParentA == iParentB:
					iParentB = random.randint(0, topFifth-1)
				#mutateLo = int(IndividualCircle._codingSeqs * 0.1)
				#mutateHi = int(IndividualCircle._codingSeqs * 0.5)
				mutateLo = int(IndividualCircle._chromoLength * 0.1)
				mutateHi = int(IndividualCircle._chromoLength * 0.5)
				child = self.indivs[iParentA].cross(
					self.indivs[iParentB], mutateLo, mutateHi)
				child.draw()
				child.evalFitness(self.target, self.targetThumb)
				self.indivs.append(child)

			# Random Parents - Low Mutation
			for i in range(5):
				iParentA = random.randint(0, len(self.indivs)-1)
				iParentB = random.randint(0, len(self.indivs)-1)
				while iParentA == iParentB:
					iParentB = random.randint(0, len(self.indivs)-1)
				mutateLo = 0
				mutateHi = int(IndividualCircle._chromoLength * 0.009)
				#mutateHi = int(IndividualCircle._codingSeqs * 0.09)
				child = self.indivs[iParentA].cross(
					self.indivs[iParentB], mutateLo, mutateHi)
				child.draw()
				child.evalFitness(self.target, self.targetThumb)
				self.indivs.append(child)

			# Random Parents - High Mutation
			for i in range(5):
				iParentA = random.randint(0, len(self.indivs)-1)
				iParentB = random.randint(0, len(self.indivs)-1)
				while iParentA == iParentB:
					iParentB = random.randint(0, len(self.indivs)-1)
				#mutateLo = int(IndividualCircle._codingSeqs * 0.1)
				#mutateHi = int(IndividualCircle._codingSeqs * 0.5)
				mutateLo = int(IndividualCircle._chromoLength * 0.1)
				mutateHi = int(IndividualCircle._chromoLength * 0.5)
				child = self.indivs[iParentA].cross(
					self.indivs[iParentB], mutateLo, mutateHi)
				child.draw()
				child.evalFitness(self.target, self.targetThumb)
				self.indivs.append(child)

			# Kill off straglers
			self.indivs.sort(self.scoreCmp)
			self.indivs = self.indivs[0:self.maxSize]

			# Update Top Score
			if topScore < self.indivs[0].getScore():
				topScore = self.indivs[0].getScore()

			# Print Status
			self.printGen(generation) # TODO remove param
			improvement = topScore - lastTopScore
			print "Improvement: " + str(improvement)

			# Save image
			fname = self.outputDir + "/score-"+str(topScore)+".png"
			if not os.path.isfile(fname):
				self.indivs[0].saveAs(fname)


	def printGen(self, generation = 0):
		"""Print the generation's statistics. Used for tracking the 
		evolutionary improvement and performance as well as debugging."""
		print "GENERATION " + str(generation) + ", init size: " + \
			  str(self.initSize) + ", max size: " + str(self.maxSize)
		print "score\t\tindividual\tpercent"
		for indiv in self.indivs:
			print str(indiv.getScore()) + ":\t" + str(indiv.breedId) + \
				  "\t\t%.04f" % indiv.scorePercent
			

	def scoreCmp(self, a, b):
		"""Score comparison callback"""
		if a.getScore() < b.getScore():
			return 1
		elif a.getScore() == b.getScore():
			return 0
		else:
			return -1
