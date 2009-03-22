# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import Image, ImageDraw
import random
import math
import os

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

	def __init__(self, targetImage, outputDir = "./out",
		initSize = 5, maxSize = 20, numGenes = 20, 
		initMutate = 50): # TODO: Fixed length genes -> variable length
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
		self.generation = 0
		self.improvement = 0

		# Maximum population size
		self.maxSize = maxSize
		self.initSize = initSize

		# Prep individual class
		IndivCircle.setNumGenes(numGenes)
		IndivCircle.setImageSize(self.target.size[0], self.target.size[1])

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

			# Index of top 20% of population
			topFifth = int(math.ceil(len(self.indivs)*0.2))
			if topFifth < 4:
				topFifth = len(self.indivs)

			# Top 20% Parents - Single Mutation
			for i in range(5):
				iParentA = random.randint(0, topFifth-1)
				iParentB = random.randint(0, topFifth-1)
				while iParentA == iParentB:
					iParentB = random.randint(0, topFifth-1)
				child = self.indivs[iParentA].cross(self.indivs[iParentB])	
				child.mutate(1) 
				child.draw()
				child.evalFitness(self.target, self.targetThumb)
				self.indivs.append(child)


			# Top 20% Parents - Low Mutation
			for i in range(5):
				iParentA = random.randint(0, topFifth-1)
				iParentB = random.randint(0, topFifth-1)
				while iParentA == iParentB:
					iParentB = random.randint(0, topFifth-1)
				mutateLo = 0
				mutateHi = int(len(self.indivs[0]) * 0.09)
				child = self.indivs[iParentA].cross(self.indivs[iParentB])
				child.mutate(random.randint(mutateLo, mutateHi)) 
					# TODO: An error last time - mutation was left out, but we had really
					# results. Was this omission the cause?
				child.draw()
				child.evalFitness(self.target, self.targetThumb)
				self.indivs.append(child)


			# Top 20% Parents - High Mutation
			for i in range(5):
				iParentA = random.randint(0, topFifth-1)
				iParentB = random.randint(0, topFifth-1)
				while iParentA == iParentB:
					iParentB = random.randint(0, topFifth-1)
				mutateLo = int(len(self.indivs[0]) * 0.1)
				mutateHi = int(len(self.indivs[0]) * 0.5)
				child = self.indivs[iParentA].cross(self.indivs[iParentB])
				child.mutate(random.randint(mutateLo, mutateHi))
				child.draw()
				child.evalFitness(self.target, self.targetThumb)
				self.indivs.append(child)

			# Random Parents - Single Mutation
			for i in range(5):
				iParentA = random.randint(0, len(self.indivs)-1)
				iParentB = random.randint(0, len(self.indivs)-1)
				while iParentA == iParentB:
					iParentB = random.randint(0, len(self.indivs)-1)
				child = self.indivs[iParentA].cross(self.indivs[iParentB])				
				child.mutate(1)
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
				mutateHi = int(len(self.indivs[0]) * 0.09)
				child = self.indivs[iParentA].cross(self.indivs[iParentB])				
				child.mutate(random.randint(mutateLo, mutateHi))
				child.draw()
				child.evalFitness(self.target, self.targetThumb)
				self.indivs.append(child)

			# Random Parents - High Mutation
			for i in range(5):
				iParentA = random.randint(0, len(self.indivs)-1)
				iParentB = random.randint(0, len(self.indivs)-1)
				while iParentA == iParentB:
					iParentB = random.randint(0, len(self.indivs)-1)
				mutateLo = int(len(self.indivs[0]) * 0.1)
				mutateHi = int(len(self.indivs[0]) * 0.5)
				child = self.indivs[iParentA].cross(self.indivs[iParentB])
				child.mutate(random.randint(mutateLo, mutateHi))
				child.draw()
				child.evalFitness(self.target, self.targetThumb)
				self.indivs.append(child)

			# Sort by performance, and cull the straglers
			self.indivs.sort(self.scoreCmp)
			worst = self.indivs[-1:1]
			self.indivs = self.indivs[0:self.maxSize]

			# Update Top Score
			if topScore < self.indivs[0].getScore():
				topScore = self.indivs[0].getScore()

			self.improvement = topScore - lastTopScore

			# Print Status
			print self

			# Save image
			fname = self.outputDir + "/score-"+str(topScore)+".png"
			if not os.path.isfile(fname):
				self.indivs[0].saveAs(fname)


	def __str__(self):
		"""Represent the generation's statistics. Used for tracking the 
		evolutionary improvement and performance as well as debugging."""
		ret  = "\tGENERATION " + str(self.generation)
		ret += " (improved " + str(self.improvement) + ")\n\n"
		ret += "id\tgenes\tmutations score\t\tpercent\n"
		for indiv in self.indivs[0:10]: # Only show the top 10
 			ret += str(indiv.id) + "\t"
			ret += str(indiv.chromosome.getNumGenes()) + "\t"
			ret += str(indiv.mutationCnt) + "\t"
			ret += str(indiv.getScore()) + "\t\t" 
			ret += "%.04f" % indiv.scorePercent
			ret += "\n"
		ret += "\nParams: InitSize: " + str(self.initSize)
		ret += " MaxSize: " + str(self.maxSize) + "\n"
		return ret


	def scoreCmp(self, a, b):
		"""Score comparison callback, a maximization comparator"""
		if a.getScore() < b.getScore():
			return 1
		elif a.getScore() == b.getScore():
			return 0
		else:
			return -1

