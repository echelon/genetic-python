# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random
import cPickle as pickle

from GAChromosome import *

class GAIndividual(object):
	# Number of genes
	_initGenes = 0 
	_maxGenes  = 0 

	# Gene length variable?
	_isNumGenesVariable  = False

	# Chromosome length enforcement
	# Set to a number to enforce that length
	_chromoLenChk = False

	# Individual counter
	_counter = 0 

	@classmethod
	def setNumGenes(cls, initGenes, maxGenes = False):
		"""Set the number of genes to be present in this individual. This MUST 
		be called before any individuals are created."""
		cls._initGenes = initGenes
		cls._maxGenes  = maxGenes
		if initGenes == maxGenes or maxGenes == False:
			cls._isNumGenesVariable = False
		else:			
			cls._isNumGenesVariable = True


	def __init__(self, chromo = None, generation = None):
		"""Initialize the individual. The gene will either be random, or bred 
		from others."""
		# Copy in chromosomal data if individual is a successor generation
		if chromo:
			self.generation = generation
			if not self.__class__._chromoLenChk:
				self.chromosome = chromo
			elif len(chromo) == self.__class__._chromoLenChk:
				self.chromosome = chromo
			else:
				raise Exception, "Chromosome length check failed."
		else:
			# Initialize as a member of the P generation
			self.chromosome = self.initChromosome()
			self.generation = 0

		# The heuristic score of this individual
		self.score = None

		# If the maximum score is known, we can keep a record of the percent
		self.scorePercent = None

		# Count of mutations accumulated
		self.mutationCnt = 0

		# Individuals counter
		self.__class__._counter += 1
		self.id = self.__class__._counter

		# Parent data - TODO: cross() is not the best place to do this.
		self.parent1id = 0
		self.parent2id = 0


	@classmethod
	def protoGene(cls):
		"""Return the prototypical gene that is used in both chromosome 
		initialization as well as random chromosome addition."""
		return [0]


	@classmethod
	def initChromosome(cls):
		"""Overloadable helper method used to generate any initial DNA strings 
		that aren't the result of crossover. This forms the initial generation.
		This is especially useful when overriding the base class."""
		chromo = []
		for i in range(cls._initGenes):
			chromo += cls.protoGene()

		return GAChromosome(chromo, len(cls.protoGene()))


	def mutate(self, times = 1):
		"""Basic mutation operator that will mutate one codon at random. This is
		a very basic binary-only representation and will likely be overridden in
		subclasses to provide the desired functionality."""

		while times > 0:
			mpos = random.randint(0, len(self.chromosome)-1)
			self.chromosome[mpos] = random.randint(0, 1)

			self.mutationCnt += 1
			times -= 1


	def cross(self, other, generation = None):
		"""Pass handling of the crossing operator to GAChromosome class and 
		return a new GAIndividual (or subclass)."""
		ret = self.__class__(self.chromosome.cross(other.chromosome), generation)		
		ret.parent1id = self.id
		ret.parent2id = other.id
		return ret

	def evalFitness(self):
		"""The Fitness Evaluation function will rank this individual against a 
		scoring heursitic designed to identify the best solutions. The 
		population controller will use this score to apply selection pressures.

		This function MUST be overridden by the subclass.
		"""
		return self.score


	def getScore(self):
		"""Return the generated score"""
		if type(self.score) == None:
			return False
		return self.score


	def __str__(self):
		"""The representation of the class when printed."""
		return "Individual #" + str(self.id)

	def __len__(self):
		"""Return the length of the chromosome."""
		return len(self.chromosome)

	def saveObjectAs(self, name):
		"""Serialize the object and save it. There is no check to see if it has
		already been saved. Program does not quit on error."""
		#try:
			# Store pickled analysis objects
		f = open(name, "w")
		pickle.dump(self, f, 0) # store serialized ascii
		f.close()

		#except Exception:
		#	# Don't hault the program 
		#	print "***Exception on serializing object!***"


