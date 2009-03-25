# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random
from copy import copy

"""
GAChromosome is a Genetic Algorithm Data Structure that provides easy access 
to chromosome data, length, and a method of subindexing by property. A 
crossover breeding mechanism is also provided. Mutation, fitness, and other 
operators are assumed to be controlled by another system or class.

Usage:

	ch = GAChromosome(range(100), 10)

	print ch 			# info
	print len(ch)		# '100'

	for gene in ch:		# Iteration example
		print gene		# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] on first iter, etc...

	while len(ch) > 0:	# Pop example
		print ch.pop()	# [99, 98, 97, 96, 95, 94, 93, 92, 91, 90], [89,...

	print len			# '0'

	ch = GAChromosome(range(100), 10)

	while len(ch) > 0:	# Dequeue example 
		print ch.pop(0)	# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, etc...

"""

# TODO: Fix distribution issues in crossover between two differently-sized chromosomes
# TODO: Allow crossover between more than two chromosomes (multiparty genetics)
# TODO: More support for variable length GA's. Check for extra non-gene codons though
# TODO: Make GAGene a property for __init__(chromo) and return it from accessors when
# numProps > 1. This will allow zero-based indexing and propertyName-based indexing,
# as well as add support for type checking

class GAChromosome:

	def __init__(self, chromo = None, numPropsPerGene = 0):
		"""Initialize a chromosome accessor from a list"""
		# Copy chromosome from a list
		if type(chromo) == list:
			self.chromosome = chromo[:]

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
		eg Ch[gene, property]. Any set property is COPIED."""
		# Index or Slice global mutator (slice throws exception)
		if type(key) == int or type(key) == slice:
			self.chromosome[key] = copy(val)
			return

		# ParamNumber,GeneNumber based mutator
		if type(key) == tuple and self.numProps > 1:
			i = key[0]*self.numProps + key[1]
			self.chromosome[i] = copy(val)
			return

	def __str__(self):
		"""Return the string representation of the object."""
		ret = ""
		ret += str(self.__class__.__name__) + " length: " + str(len(self))
		if self.numProps > 1:
			ret += " properties: " + str(self.numProps)
		else:
			ret += ". No properties."
		return ret

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
		
	def pop(self, geneOffset = False):
		"""Remove a gene from the chromosome."""
		# List-only (Non-gene) based chromosome
		if self.numProps < 2:
			if type(geneOffset) == bool:
				return self.chromosome.pop()
			return self.chromosome.pop(geneOffset)

		# Gene-based chromosome (has properties)
		# Determine starting pop position
		popPos = 0
		lastGenePos = len(self.chromosome) - self.numProps
		if type(geneOffset) == bool:
			if len(self.chromosome) < self.numProps:
				raise IndexError, "Not enough data to pop"
			popPos = lastGenePos
		elif type(geneOffset) == int:
			popPos = geneOffset*self.numProps
			if popPos < 0 or popPos > lastGenePos:
				raise IndexError, "Pop location is out of bounds"

		gene = self.chromosome[popPos : popPos+self.numProps]

		for i in range(self.numProps):
			self.chromosome.pop(popPos)

		return gene

	def insert(self, geneOffset, gene):
		"""Insert a gene into the chromosome at the location specified. Contents
		are COPIED."""
		offset = geneOffset

		# Prepare for gene-based chromosome (which have properties)
		if self.numProps > 1:
			if type(gene) != list:
				raise Exception, "Inserted gene must be of type list."
			if len(gene) != self.numProps:
				raise Exception, "Inserted gene doesn't match size reqs."

			offset = geneOffset * self.numProps

		# This handles gene and non-gene based chromosomes
		# Seems to work even with negative offsets!
		before = self.chromosome[:offset]
		after  = self.chromosome[offset:]
		self.chromosome = before + copy(gene) + after

	def cross(self, other):
		"""Cross this chromosome with another to produce offspring. This method
		supports crossing parents of equal length or creating a child from two
		parents of different length, with a result length somewhere between the
		two parents."""
		lenA = len(self.chromosome)
		lenB = len(other.chromosome)
		# Use the old equal-parts cross algorithm, which tries to correct any 
		# bias that exists in the random number generator (with respect to 
		# child constitution, not the distribution of order!). This will only
		# work for equal parent lengths, otherwise use the new algorithm
		if lenA == lenB:
			usedA = 0
			usedB = 0
			half = len(self.chromosome)/2
			chromo = [0]*len(self.chromosome)
			for i in range(len(self.chromosome)):
				if usedA < half and random.randint(0, 1):
					chromo[i] = copy(self.chromosome[i])
					usedA += 1
				elif usedB < half:
					chromo[i] = copy(other.chromosome[i])
					usedB += 1
				else:
					chromo[i] = copy(self.chromosome[i])
					usedA += 1

			return self.__class__(chromo, self.numProps)

		# The parents are of unequal length, so we're going to create a child
		# chromosome of length somewhere between min and max. This algorithm
		# doesn't ensure equal contribution or account for RNG bias. Mark TODO.

		minChromo = min(len(self.chromosome), len(other.chromosome))
		maxChromo = max(len(self.chromosome), len(other.chromosome))
		childChromoLen = random.randint(minChromo, maxChromo)

		remove = childChromoLen % self.numProps
		childChromoLen -= remove

		chromo = [0] *childChromoLen
		usedA = 0
		usedB = 0

		# TODO:
		#useA = lenA/2 # equal sizes = equal contribution
		#useB = lenB/2
		#if lenA < lenB:
		#	useA = max(lenA/2, len(chromo)-lenB/2)
		#	useB = max(lenB/2, len(chromo)-lenA/2)
		"""
		len(parA) = 3  || CONTRIBUTE:
		len(parB) = 9  || parA	parB
		==============================*self.numProps
		len(child) = 3 || 1xor2	1xor2	# For uneven output, one contribs more at random
		len(child) = 4 || 2		2
		len(child) = 5 || 2xor3	2xor3	# For uneven output, one contribs more at random
		len(child) = 6 || 3		3
		len(child) = 7 || 3		4		# For input<half, one gives all, the other fills in
		len(child) = 8 || 3		5		# For input<half, one gives all, the other fills in
		len(child) = 9 || 3		6		# For input<half, one gives all, the other fills in

		we need to keep each gene intact, unless there is some change
		"""

		for i in range(len(chromo)):
			if random.randint(0, 1) and i < lenA:
				chromo[i] = copy(self.chromosome[i])
				usedA += 1
			elif i < lenB:
				chromo[i] = copy(other.chromosome[i])
				usedB += 1
			else:
				chromo[i] = copy(self.chromosome[i])
				usedA += 1

		return self.__class__(chromo, self.numProps)


	def getNumGenes(self):
		"""Return number of genes"""
		if self.numProps > 0:
			if len(self.chromosome)%self.numProps:
				raise Exception, "There is an uneven number of codons per gene."
			return len(self.chromosome)/self.numProps
		return 0

	def getNumProps(self):
		"""Return number of properties per gene"""
		return self.numProps

