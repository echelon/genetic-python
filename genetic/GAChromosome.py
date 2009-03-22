# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random

"""
GAChromosome is a Genetic Algorithm data structure that provides easy access 
to chromosome data, length, and a method of subindexing by property. A 
crossover breeding mechanism is also provided. Mutation, fitness, and other 
operators are assumed to be controlled by another system or class.
"""

# TODO: Allow crossover between two differently-sized chromosomes
# TODO: Allow crossover between more than two chromosomes (multiparty genetics)
# TODO: More support for variable length GA's. Check for extra non-gene codons though
# TODO: Make GAGene a property for __init__(chromo) and return it from accessors when
# numProps > 1. This will allow zero-based indexing and propertyName-based indexing,
# as well as add support for type checking

class GAChromosome:

	def __init__(self, chromo = None, numPropsPerGene = 0):
		"""Initialize a chromosome accessor from a list"""
		# Copy chromosome from a list
		self.chromosome = chromo

		# Number of properties per gene
		self.numProps = numPropsPerGene

		# For iteration
		self.iterIndex = 0

	def __len__(self):
		"""The length of the chromosome"""
		return len(self.chromosome)

	def __getitem__(self, key):
		"""Access the chromosome array at an index directly via Ch[0], or 
		provide access to a computed prop index if the key is a tuple: Ch[5,1].
		eg Ch[gene, property]."""
		# Index or Slice global accessor
		if type(key) == int or type(key) == slice:
			return self.chromosome[key]

		# ParamNumber,GeneNumber based accessor
		if type(key) == tuple and self.numProps > 1:
			i = key[0]*self.numProps + key[1]
			return self.chromosome[i]

	def __setitem__(self, key, val):
		"""Assign the chromosome array at an index directly via Ch[0], or 
		provide access to a computed prop index if the key is a tuple: Ch[5,1].
		eg Ch[gene, property]."""
		# Index or Slice global mutator (slice throws exception)
		if type(key) == int or type(key) == slice:
			self.chromosome[key] = val
			return

		# ParamNumber,GeneNumber based mutator
		if type(key) == tuple and self.numProps > 1:
			i = key[0]*self.numProps + key[1]
			self.chromosome[i] = val
			return

	def __str__(self):
		"""Return the string representation of the object."""
		ret = ""
		ret += str(self.__class__.__name__) + " length: " + str(len(self))
		if self.numProps > 0:
			ret += " properties: " + str(self.numProps)
		else:
			ret += ". No properties."
		return ret

	def cross(self, other):
		"""Cross this chromosome with another to produce offspring"""
		usedA = 0
		usedB = 0
		half = len(self.chromosome)/2
		chromo = [0]*len(self.chromosome)
		for i in range(len(self.chromosome)):
			if usedA < half and random.randint(0, 1):
				chromo[i] = self.chromosome[i]
				usedA += 1
			elif usedB < half:
				chromo[i] = other.chromosome[i]
				usedB += 1
			else:
				chromo[i] = self.chromosome[i]
				usedA += 1

		return self.__class__(chromo, self.numProps)

	def __iter__(self):
		"""Return a chromosome iterator."""
		self.iterIndex = 0 # refresh in case Chromo.next() was called prior
		return self

	def next(self):
		"""Get the next gene. Will return a list of size numProps if set."""
		if self.iterIndex > len(self.chromosome)-1:
			self.iterIndex = 0
			raise StopIteration

		# Return non-property based chromosomes as values
		if self.numProps <= 1:
			ret = self.chromosome[self.iterIndex]
			self.iterIndex += 1
			return ret

		# Return each gene inside a list
		ret = self.chromosome[self.iterIndex : self.iterIndex+self.numProps]
		self.iterIndex += self.numProps
		return ret
		

	def getNumGenes(self):
		"""Return number of genes"""
		if self.numProps > 0:
			if len(self.chromosome)%self.numProps:
				raise Exception, "There is an uneven number of codons per gene."
			return len(self.chromosome)/self.numProps
		return 0

	#def getNumProps(self):
	#	"""Return number of properties per gene"""
	#	return self.numProps

