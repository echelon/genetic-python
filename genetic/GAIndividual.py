# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random

class IndividualGA:
	# Chromosome length
	_chromoLength = 0

	# Number of coding sequences # TODO - remove this
	_codingSeqs = 0

	# Individual counter
	_bredCnt    = 0

	@staticmethod
	def setCodingLen(length):
		"""Set the size of images to be produced, usually to match the target 
		image. This MUST be called before any individuals are created."""
		IndividualGA._codingSeqs = length


	def __init__(self, chromo = None):
		"""Initialize the individual. The gene will either be random, or bred 
		from others."""
		# Copy in chromosomal data if individual is a successor generation
		if chromo and len(chromo) == (self.__class__._chromoLength):
			self.chromosome = chromo
		else:
			# Initialize as a member of the P generation
			self.chromosome = self.initDNA()

		# The heuristic score of this individual
		self.score = None

		# If the maximum score is known, we can keep a record of the percent
		self.scorePercent = None

		# Individuals counter
		self.__class__._bredCnt += 1
		self.breedId = self.__class__._bredCnt


	def initDNA(self):
		"""Overloadable helper method used to generate any initial DNA strings 
		that aren't the result of crossover. This forms the initial generation.
		This is especially useful when overriding the base class."""
		chromo = [0] * self._codingSeqs
		return chromo


	def mutate(self):
		"""Basic mutation operator that will mutate one codon at random. This is
		a very basic binary-only representation and will likely be overridden in
		subclasses to provide the desired functionality."""
		mpos = random.randint(0, len(self.chromosome)-1)
		self.chromosome[mpos] = random.randint(0, 1)
		

	def cross(self, other, muteLower = 5, muteUpper = 15):
		"""Cross this individual with another to produce offspring"""
		half = len(self.chromosome)/2
		usedA = 0
		usedB = 0
		chromo = [0]*len(self.chromosome)
		for i in range(len(self.chromosome)):
			if usedA <= half and random.randint(0,1):
				chromo[i] = self.chromosome[i]
				usedA += 1
			elif usedB <= half:
				chromo[i] = other.chromosome[i]
				usedB += 1
			else:
				chromo[i] = self.chromosome[i]
				usedA += 1

		child = self.__class__(chromo) #TODO : Will this cause problems??

		# TODO: Mutation should be done in Population controller, not cross() method
		mutationCnt = random.randint(muteLower, muteUpper)
		for i in range(mutationCnt):
			child.mutate()
		return child


	def getScore(self):
		"""Return the generated score"""
		if type(self.score) == None:
			return False
		return self.score


	def evalFitness(self):
		"""The Fitness Evaluation function will rank this individual against a 
		scoring heursitic designed to identify the best solutions. The 
		population controller will use this score to apply selection pressures.

		This function MUST be overridden by the subclass.
		"""
		return self.score


	def __str__(self):
		"""The representation of the class when printed."""
		return "Individual #: " + str(self.breedId)

