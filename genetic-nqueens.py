#!/usr/bin/env python
# Brandon Thomas Suit
# <http://possibilistic.org>
# <brandon.suit@gmail.com>

import sys
from random import randrange
from math import ceil
from copy import *

##
# Basis board class. This class wraps our NxN matrix,
# provides a helpful interface for a variety of algorithms,
# and keeps things very nice and general/centralized.
# This will be subclassed quite a bit.
#
class Board(object):

	def __init__(self, size = 8, *args, **kwargs):
		"""Set up the chess board for n-queens.
		The default size is 8-queens.
		"""

		super(Board, self).__init__(*args, **kwargs)

		self.size = size
		self.isSolved = False
		self.numQueens = 0

		self.grid = []

		for i in range(self.size):
			cols = []
			for j in range(self.size):
				cols.append(0)
			self.grid.append(cols)

	def placeUnchecked(self, row, col):
		"""This does NOT check if the position
		is under attack.
		"""
		if self.numQueens >= self.size:
			return False

		if self.grid[row][col] != 0:
			return False

		self.grid[row][col] = 1
		self.numQueens += 1
		return True

	def placeChecked(self, row, col):
		"""This does check if the position
		is under attack.
		"""
		# Too many on board
		if self.numQueens >= self.size:
			return False

		# Can't place in an already occupied spot
		if self.grid[row][col] != 0:
			return False

		# Check position
		if not self.rowSafe(row):
			return False
		if not self.colSafe(col):
			return False
		if not self.diagSafe(row, col):
			return False

		# Place
		self.grid[row][col] = 1
		self.numQueens += 1
		return True

	def moveUnchecked(self, row1, col1, row2, col2):
		"""Move a queen. Does not check if the position
		is under attack
		"""

		if not self.isOccupied(row1, col1):
			return False

		if self.isOccupied(row2, col2):
			return False

		self.grid[row1][col1] = 0
		self.grid[row2][col2] = 1
		return True

	def moveChecked(self, row1, col1, row2, col2):
		"""Move a queen. Checks if the new position is
		under attack before moving.
		"""
		if not self.isOccupied(row1, col1):
			return False

		if self.isOccupied(row2, col2):
			return False

		# Temporarily remove piece
		self.remove(row1, col1)

		success = self.placeChecked(row2, col2)

		# Replace on failure
		if not success:
			self.placeUnchecked(row1, col1)

		return success

	def remove(self, row, col):
		"""Remove a queen from the board."""
		if not self.isOccupied(row, col):
			return False

		self.grid[row][col] = 0
		self.numQueens -= 1
		return True

	def isOccupied(self, row, col):
		"""Return true if the square is occupied."""
		return (self.grid[row][col] != 0)

	def isFull(self):
		return (self.numQueens == self.size)

	def rowSafe(self, row):
		"""Return true if the row is safe"""
		for i in range(self.size):
			if self.grid[row][i] != 0:
				return False
		return True

	def colSafe(self, row):
		"""Return true if the column is safe"""
		for i in range(self.size):
			if self.grid[i][col] != 0:
				return False
		return True

	def diagSafe(self, row, col):
		"""Return true if the diagonal is safe"""

		# Check upper left diagonal
		for i in range(self.size):
			rc = row - i
			cc = col - i
			if rc < 0 or cc < 0:
				break
			if self.grid[rc][cc] != 0:
				return False
		# Check upper right diagonal
		for i in range(self.size):
			rc = row - i
			cc = col + i
			if rc < 0 or cc >= self.size:
				break
			if self.grid[rc][cc] != 0:
				return False
		# Check lower left diagonal
		for i in range(self.size):
			rc = row + i
			cc = col - i
			if rc >= self.size or cc < 0:
				break
			if self.grid[rc][cc] != 0:
				return False
		# Check lower right diagonal
		for i in range(self.size):
			rc = row + i
			cc = col + i
			if rc >= self.size or cc >= self.size:
				break
			if self.grid[rc][cc] != 0:
				return False

		return True

	def __str__(self):
		"""Get the string representation of 
		the matrix. This is good for debugging.
		"""
		ret = ""

		for i in range(self.size):
			for j in range(self.size):
				ret += str(self.grid[i][j]) + " "
			ret += "\n"

		return ret

##
# Defines the interface for Complete-State Boards
# These boards will not need to have queens added
# or removed, only moved. A heuristic will probably
# subclass these.
#
class CompleteBoard(Board):

	def __init__(self, size = 8, startType = 0, *args, **kwargs):
		"""Set up the chess board for n-queens.
		The default size is 8-queens.
		"""
		super(CompleteBoard, self).__init__(size, *args, **kwargs)

		# Init the board to n-queens
		for i in range(size):
			# All placed in first column
			if startType == 0:
				x = 0
			# ALl placed in a random column
			elif startType == 1:
				x = randrange(0, size-1)
			# All placed diagonal
			else:
				x = i
			self.grid[i][x] = 1

		self.numQueens = size
		self.heuristic = self.numUnderAttack()

	def numUnderAttack(self):
		"""This is our heuristic function for complete-state
		representations of the problem. It returns the number
		of attacking pairs of queens.
		"""
		attacking = 0

		rowCount = [0]*self.size
		colCount = [0]*self.size

		numDiags = self.size * 2 -1

		diags1 = [0]*numDiags
		diags2 = [0]*numDiags

		# Check diagonals
		# This was annoying to figure out...
		for row in range(self.size):

			# There's an index for each diagonal
			# Both positive, and negative slopes
			for col in range(self.size):
				diag1 = col - row + (self.size - 1) # Scores negative-slope diagonals
				diag2 = (col - self.size + 1) + row + (self.size - 1) # positive-slope diagonals

				if self.grid[row][col] != 0:
					diags1[diag1] += 1
					diags2[diag2] += 1

		# Check laterals
		for i in range(self.size):
			for j in range(self.size):
				if self.grid[i][j]:
					rowCount[i] += 1
					colCount[j] += 1

		# Score laterals
		for i in range(self.size):
			if rowCount[i] > 1:
				attacking += rowCount[i]
			if colCount[i] > 1:
				attacking += colCount[i]

		# Score diagonals
		for i in range(numDiags):
			if diags1[i] > 1:
				attacking += diags1[i]
			if diags2[i] > 1:
				attacking += diags2[i]

		return attacking

	# Override
	def remove(self, row, col):
		return False

	# Override
	def placeChecked(self, row, col): 
		return False

	# Override
	def placeUnchecked(self, row, col):
		return False

	# Override
	def __str__(self):
		"""Provide heuristic information with output"""
		ret = super(CompleteBoard, self).__str__()
		ret += "\nh = " + str(self.numUnderAttack()) + "\n"

		return ret

##
# BoardNodes are used for non-local searches. We'll model 
# what was in the book, for the most part.
#
class BoardNode(object):
	
	def __init__(self, board, parent = None, children = ()):

		# leaving out: action, path-cost
		# adding: children pointers (necessary?)
		self.board = board
		self.parent = parent
		self.children = children
		self.depth = 0

		# correct depth
		if self.parent:
			self.depth = self.parent.depth + 1
			

	def isSolved(self):
		"""Is the node solved?"""
		return self.board.isSolved		


##
# This solves N-Queens utilizing Genetic Algorithms
# When run from the command line, there are four distinct options:
#	"python nqueens_genetic.py [populationSize, [numQueens, [mutationDistrib, [mutationRate]]]]
#
#	* populationSize is the gene pool size.
#	* numQueens is the board size
# 	* mutationDistrib is the probability of mutations occuring in an individual
#	* mutationRate is the probability of multiple point mutations occuring
#
# Both mutationDistrib and mutationRate should be supplied as integers (inverse ratio)
#
class Genetic(CompleteBoard):

	def __init__(self, size = 8, startType = 1, *args, **kwargs):
		"""This is the Genetic Algorithm-based solver"""

		super(Genetic, self).__init__(size, startType, *args, **kwargs)

		self.mutations = 0

	def score(self):
		return self.numUnderAttack()

	def getRow(self, row):
		"""Get all the queens in the row"""
		return deepcopy(self.grid[row])

	def setRow(self, rownum, rowdata):
		"""This is an unchecked operation"""
		self.grid[rownum] = deepcopy(rowdata)

##
# Population container
#
class Population:

	def __init__(self, size = 12, queens = 8, mutateRate = 2, mutateDistrib = 2):
		
		self.generation = 0
		self.size = size
		self.queens = queens
		self.mutateRate = mutateRate
		self.mutateDistrib = mutateDistrib
		self.population = []

		# Init the population
		for i in range(size):
			x = Genetic(queens)
			self.population.append(x)

		self.sort()

	def sort(self):
		temp = None
		for i in range(self.size):
			for j in range(self.size):
				if (self.population[i].score() < self.population[j].score()):
					temp = self.population[i]
					self.population[i] = self.population[j]
					self.population[j] = temp

	def evolve(self):
		"""Evolve a new generation."""

		self.sort()

		newPopulation = []

		# Top performing 1/4th of individuals may survive - 33% chance
		for i in range(self.size/4):
			chance = randrange(0, 2)
			if chance == 0:
				newPopulation.append(deepcopy(self.population[i]))

		# Breed the top individuals until gene pool is filled.
		while len(newPopulation) < self.size:
			a = randrange(0, self.size/2)
			b = randrange(0, self.size/2)
			if a == b:
				# We can't produce asexually
				continue

			children = self.cross(self.population[a], self.population[b])
			newPopulation.append(children[0])
			newPopulation.append(children[1])

		# Trim any extras
		if len(newPopulation) > self.size:
			newPopulation = newPopulation[0:self.size]

		# Mutate individuals

		for i in range(len(newPopulation)):
			# 50% probability of mutation
			newPopulation[i].mutations = 0
			if randrange(0, self.mutateDistrib) == 0:
				newPopulation[i] = self.mutate(newPopulation[i])

		self.population = newPopulation
		self.generation += 1
		self.sort()

	def cross(self, a, b):
		"""Produce a cross of A and B"""

		x = deepcopy(a)
		y = deepcopy(b)

		splice = randrange(self.queens - self.queens/2, self.queens - self.queens/4)

		for row in range(splice):
			xr = a.getRow(row)
			yr = b.getRow(row)

			x.setRow(row, yr)
			y.setRow(row, xr)

		return (x, y)


	def mutate(self, x):
		"""Produce a mutant of X"""

		mutant = deepcopy(x)
		#mutate = randrange(1, int(ceil(float(self.queens)/2))) # A low number of mutations to perform
		mutate = randrange(1, self.mutateRate)

		mutant.mutations = mutate
		while mutate > 0:
			randrow = randrange(0, self.queens)
			randcol = randrange(0, self.queens)
			col = [0]*self.queens
			col[randcol] = 1

			mutant.grid[randrow] = col

			mutate =- 1

		return mutant

	def __str__(self):
		ret = "==== GENETIC ALGORITHM N-QUEENS ====\n\n"
		ret += "queens:\t\t\t" + str(self.queens) + "\n"
		ret += "population:\t\t" + str(self.size) + "\n"
		ret += "mutation distribution:\t" + str(self.mutateDistrib) + " (an inverse weight)\n"
		ret += "mutation rate:\t\t" + str(self.mutateRate) + " (an inverse weight)\n"
		ret += "reproduction rate/bias:\t FIXED\n\n"
		ret += "GENERATION " + str(self.generation) + "\n"

		for i in range(len(self.population)):
			ret += "h("+str(i)+") = "+ str(self.population[i].score())
			ret += "\tm = " +str(self.population[i].mutations) + "\n"

		ret += "\nBEST INDIVIDUAL\n" + str(self.population[0]) + "\n"

		return ret

##
# Main
#
if __name__ == '__main__':
	print "n-queens Genetic Algorithm"

	if len(sys.argv) < 2:
		print "Call as: " + sys.argv[0] + " [popSize, [numQueens, [mutDistrib, [mutRate]]]]"
		sys.exit()

	print ""

	reproductionRate = 4
	mutationRate     = 4
	mutationDistrib  = 4
	populationSize   = 12
	numQueens		 = 8

	if len(sys.argv) > 1:
		populationSize = int(sys.argv[1])

	if len(sys.argv) > 2:
		numQueens = int(sys.argv[2])

	if len(sys.argv) > 3:
		mutationDistrib = int(sys.argv[3])

	if len(sys.argv) > 4:
		mutationRate = int(sys.argv[4])

	p = Population(size = populationSize, queens = numQueens, mutateRate = mutationRate, mutateDistrib = mutationDistrib)

	while p.population[0].score() != 0:

		print str(p) + "\n"
		p.evolve()

	print "Solved!\n"
	print str(p) + "\n"
