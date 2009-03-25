# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random
import numpy.linalg

# TODO: New idea for non-complex polygons -
# In adding/removing points, do so on a rotational axis system. Add new points 
# at 175 degrees, 120 degrees, 80 degrees, 60 degrees... etc. They can be far
# out on that line or far in, additionally they can waver left or right--but just
# by a little.

class Polygon:
	"""Representation of polygon shapes for the Evolution application."""
	# Note that these are referenced from 'self' in the methods
	MIN_POINTS = 3
	MAX_POINTS = 4
	MAX_SEP_DENOM = 9

	# Growth transformations
	MIN_GROWTH = 0.3
	MAX_GROWTH = 1.05

	# CLASS COUNTER
	__COUNTER = 0

	def __init__(self, height, width):
		"""Constructor will randomize the polygon."""
		# Dimensions of src image
		self.height = height
		self.width = width

		# Random constants		
		self.maxSep = (height + width) / self.__class__.MAX_SEP_DENOM

		# Anchor points control translation
		self.xAnchor = random.randint(-width, width)
		self.yAnchor = random.randint(-height, height)

		# Each polygon point, relative to the anchor points
		self.xPoints = []
		self.yPoints = []

		if len(self.xPoints) == 0:
			self.initPoints() # Don't perform in copying

		# Other Geometry/LinearAlg operations
		self.xGrowth = random.uniform(self.__class__.MIN_GROWTH,
									  self.__class__.MAX_GROWTH)
		self.yGrowth = random.uniform(self.__class__.MIN_GROWTH,
									  self.__class__.MAX_GROWTH)
		self.rotation = 0	# TODO, probably difficult
		self.affine   = 0	# TODO

		self.__class__.__COUNTER += 1
		self.id = self.__class__.__COUNTER

	def __copy__(self):
		"""Copy constructor. Make sure the lists aren't shallow copied."""
		ret = self.__class__(self.height, self.width)

		ret.xAnchor = self.xAnchor
		ret.yAnchor = self.yAnchor
		ret.xPoints = self.xPoints[:]
		ret.yPoints = self.yPoints[:]

		ret.rotation = self.rotation
		ret.affine   = self.affine
		ret.xGrowth  = self.xGrowth
		ret.yGrowth  = self.yGrowth

		return ret

	def initPoints(self):
		"""Initialize or refresh points."""
		xPoints = []
		yPoints = []
		done = False
		while not done:
			xPoints = []
			yPoints = []
			numPoints = random.randint(self.__class__.MIN_POINTS, 
									   self.__class__.MAX_POINTS)
			numPoints = 3 # TODO TODO TODO TODO - eliminating this variable for testing

			for i in range(numPoints):
				xPoints.append(random.randint(-self.maxSep, self.maxSep))
				yPoints.append(random.randint(-self.maxSep, self.maxSep))

			if self.checkAll(xPoints, yPoints) == -1:
				done = True

		self.xPoints = xPoints
		self.yPoints = yPoints

	def getCords(self):
		"""Return a tuple of (x1, y1, x2, y2...) points in a format suitable for
		use in aggdraw. This takes into account all geometry operations."""
		points = []
		for i in range(len(self.xPoints)):
			points.append(self.xPoints[i]*self.xGrowth+self.xAnchor)
			points.append(self.yPoints[i]*self.yGrowth+self.yAnchor)

		if len(points) > self.__class__.MAX_POINTS*2:
			raise Exception, "Too many points in coordinate system: " + str(points)

		return tuple(points)

	def addPoint(self):
		"""Add a point at a random position as long as the MAX_POINTS threshold 
		has not already been reached."""
		if len(self.xPoints) >= self.__class__.MAX_POINTS:
			return

		# After adding a point, if the the polygon's lines aren't valid, redo
		xPoints = self.xPoints[:]
		yPoints = self.yPoints[:]
		done = False
		randPt = random.randint(0, len(xPoints))
		while not done:
			xPoints = self.xPoints[:]
			yPoints = self.yPoints[:]
			
			randPt = random.randint(0, len(xPoints))
			xPoints.insert(randPt, random.randint(-self.maxSep, self.maxSep))
			yPoints.insert(randPt, random.randint(-self.maxSep, self.maxSep))

			if self.checkPoint(randPt, xPoints, yPoints) == -1:
				done = True

		self.xPoints = xPoints
		self.yPoints = yPoints

	def remPoint(self):
		"""Remove a point from a random position as long as the MIN_POINTS
		threashold has not been reached."""
		if len(self.xPoints) <= self.__class__.MIN_POINTS:
			return

		# After removing a point, if the the polygon's lines aren't valid, redo
		xPoints = self.xPoints[:]
		yPoints = self.yPoints[:]
		done = False
		while not done:
			xPoints = self.xPoints[:]
			yPoints = self.yPoints[:]

			randPt = random.randint(0, len(xPoints)-1)
			xPoints.pop(randPt)
			yPoints.pop(randPt)

			if self.checkAll(xPoints, yPoints) == -1:
				done = True

		self.xPoints = xPoints
		self.yPoints = yPoints

	def mutatePoint(self):
		"""Change the coordinate of one of the points."""
		# TODO: Implement a gray-coding evolution scheme.

		# After mutating a point, if the the polygon's lines aren't valid, redo
		xPoints = self.xPoints[:]
		yPoints = self.yPoints[:]
		done = False
		while not done:
			xPoints = self.xPoints[:]
			yPoints = self.yPoints[:]

			randPt = random.randint(0, len(xPoints)-1)
			xPoints[randPt] = random.randint(-self.maxSep, self.maxSep)
			yPoints[randPt] = random.randint(-self.maxSep, self.maxSep)

			if self.checkPoint(randPt, xPoints, yPoints) == -1:
				done = True

		self.xPoints = xPoints
		self.yPoints = yPoints

	def mutatePoints(self):
		"""Mutate a random number of points."""

		# After mutating a point, if the the polygon's lines aren't valid, redo
		xPoints = self.xPoints[:]
		yPoints = self.yPoints[:]
		done = False
		while not done:
			xPoints = self.xPoints[:]
			yPoints = self.yPoints[:]

			# This might take awhile...
			randNum = random.randint(0, len(xPoints)-1)
			for i in range(randNum):
				randPt = random.randint(0, len(xPoints)-1)
				xPoints[randPt] = random.randint(-self.maxSep, self.maxSep)
				yPoints[randPt] = random.randint(-self.maxSep, self.maxSep)

			if self.checkAll(xPoints, yPoints) == -1:
				done = True

		self.xPoints = xPoints
		self.yPoints = yPoints


	def mutateTranslationSmall(self):
		"""Change the anchor point ever so slightly to translate the object to
		a new point, utilizing a gray coding-like scheme."""
		x = self.xAnchor
		y = self.yAnchor
		self.xAnchor = random.randint(x-5, x+5)
		self.yAnchor = random.randint(y-5, y+5)

	def mutateGrowth(self, which = None):
		"""Change the growth factor of X, Y, or both X and Y."""
		types = ('x', 'y', 'xy')
		if which not in types:
			r = random.randint(0, 2)
			which = types[r]

		if which == 'x':
			self.xGrowth = random.uniform(self.__class__.MIN_GROWTH,
										  self.__class__.MAX_GROWTH)
		elif which == 'y':
			self.yGrowth = random.uniform(self.__class__.MIN_GROWTH,
										  self.__class__.MAX_GROWTH)
		elif which == 'xy':
			self.xGrowth = random.uniform(self.__class__.MIN_GROWTH,
										  self.__class__.MAX_GROWTH)
			self.yGrowth = random.uniform(self.__class__.MIN_GROWTH,
										  self.__class__.MAX_GROWTH)

	def mutateTranslationLarge(self):
		"""Change the anchor point potentially drastically."""
		x = self.xAnchor
		y = self.yAnchor
		self.xAnchor = random.randint(-self.width, self.width)
		self.yAnchor = random.randint(-self.height, self.height)


	def checkPoint(self, pt, xPoints, yPoints):
		return -1 # TODO - works, but slow

		end = len(xPoints)-1
		checkBack = False

		# Lowest point index first
		if pt == 0:
			idx = (0, 0)
			line1 = (xPoints[0], yPoints[0], xPoints[end], yPoints[end])
			line2 = (xPoints[0], yPoints[0], xPoints[1], yPoints[1])
		elif pt == end:
			idx = (0, end-1)
			line1 = (xPoints[0], yPoints[0], xPoints[end], yPoints[end])
			line2 = (xPoints[end-1], yPoints[end-1], xPoints[end], yPoints[end])
		else:
			idx = (pt, pt-1)
			line1 = (xPoints[pt], yPoints[pt], xPoints[pt+1], yPoints[pt+1])
			line2 = (xPoints[pt-1], yPoints[pt-1], xPoints[pt], yPoints[pt])
			checkBack = True
		
		i = 0
		while i < len(xPoints)-1:
			# Don't check the same line
			if i in idx: 
				i+= 1
				continue
			lineChk = (xPoints[i], yPoints[i], xPoints[i+1], yPoints[i+1])

			if self.hasIntersect(line1, lineChk) or \
			   self.hasIntersect(line2, lineChk):
					return False
			i+= 1

		if checkBack:
			lineChk = (xPoints[0], yPoints[0], xPoints[end], yPoints[end])
			if self.hasIntersect(line1, lineChk) or \
			   self.hasIntersect(line2, lineChk):
					return False

		return -1

	@classmethod
	def checkAll(cls, xPoints, yPoints):
		return -1 # TODO - works, but slow
		"""Use linear algebra to determine if any two lines in the polygon 
		cross. Returns -1 if okay, or the index if the polygon is complex."""		
		# Check lines within point range (0, end) against each other
		i = 0
		while i < len(xPoints)-3:				
			j = i+1
			while j < len(xPoints)-1:
				lineA = (xPoints[i], yPoints[i], xPoints[i+1], yPoints[i+1])
				lineB = (xPoints[j], yPoints[j], xPoints[j+1], yPoints[j+1])
				if cls.hasIntersect(lineA, lineB):
					return j+1

				j+= 1
			i+= 1	

		# Check loopback line [0]->[end] against all others in range (0, end)
		end = len(xPoints)-1
		lineA = (xPoints[0], yPoints[0], xPoints[end], yPoints[end])
		while i < len(xPoints)-1:
			lineB = (xPoints[i], yPoints[i], xPoints[i+1], yPoints[i+1])
			if cls.hasIntersect(lineA, lineB):
				return end
			i+= 1

		return -1

	@staticmethod
	def hasIntersect(lineA, lineB):
		"""Use linear algebra to determine if two lines cross. Both inputs are
		4-tuples ordered (x1, y1, x2, y2). Returns true if there is an 
		intersection."""
		# Solution from: http://mathforum.org/library/drmath/view/64379.html

		return False # TODO - works, but slow

		# Line A
		x1 = lineA[0]
		y1 = lineA[1]
		x2 = lineA[2]
		y2 = lineA[3]

		# Line B
		x3 = lineB[0]
		y3 = lineB[1]
		x4 = lineB[2]
		y4 = lineB[3]

		mat1 = [[x1, y1, 1],
				[x2, y2, 1],
				[x3, y3, 1]]

		mat2 = [[x1, y1, 1],
				[x2, y2, 1],
				[x4, y4, 1]]

		det1 = int(numpy.linalg.det(mat1))
		det2 = int(numpy.linalg.det(mat2))

		if det1 == 0 and det2 == 0:
			# Line lies on top of the other.
			return True 
		elif (det1 < 0 and det2 > 0) or (det1 > 0 and det2 < 0):
			# Lines cross each other.
			return True 

		return False

	def __str__(self):
		return "Polygon ID " + str(self.id)
