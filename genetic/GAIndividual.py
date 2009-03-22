# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random

from GAIndividual import *

class GAIndividual(object):
	# Number of genes
	_numGenes = 0 

	# Chromosome length enforcement
	# Set to a number to enforce that length
	_chromoLenChk = False

	# Individual counter
	_counter = 0 

	@classmethod
	def setNumGenes(cls, num):
		"""Set the number of genes to be present in this individual. This MUST be 
		called before any individuals are created."""
		cls._numGenes = num


	def __init__(self, chromo = None):
		"""Initialize the individual. The gene will either be random, or bred 
		from others."""
		# Copy in chromosomal data if individual is a successor generation
		if chromo:
			if not self.__class__._chromoLenChk:
				self.chromosome = chromo
			elif len(chromo) == self.__class__._chromoLenChk:
				self.chromosome = chromo
			else:
				raise Exception, "Chromosome length check failed."
		else:
			# Initialize as a member of the P generation
			self.chromosome = self.initDNA()

		# The heuristic score of this individual
		self.score = None

		# If the maximum score is known, we can keep a record of the percent
		self.scorePercent = None

		# Count of mutations accumulated
		self.mutationCnt = 0

		# Individuals counter
		self.__class__._counter += 1
		self.id = self.__class__._counter


	@classmethod
	def initDNA(cls):
		"""Overloadable helper method used to generate any initial DNA strings 
		that aren't the result of crossover. This forms the initial generation.
		This is especially useful when overriding the base class."""
		chromo = [0] * cls._numGenes
		return chromo


	def mutate(self, times = 1):
		"""Basic mutation operator that will mutate one codon at random. This is
		a very basic binary-only representation and will likely be overridden in
		subclasses to provide the desired functionality."""

		while times > 0:
			mpos = random.randint(0, len(self.chromosome)-1)
			self.chromosome[mpos] = random.randint(0, 1)

			self.mutationCnt += 1
			times -= 1


	def cross(self, other):
		"""Pass handling of the crossing operator to GAChromosome class and 
		return a new GAIndividual (or subclass)."""
		return self.__class__(self.chromosome.cross(other.chromosome))		


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
		return "Individual #: " + str(self.id)

	def __len__(self):
		"""Return the length of the chromosome."""
		return len(self.chromosome)

