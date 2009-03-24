# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random
from copy import copy

class Polygon:
	"""Representation of polygon shapes for the Evolution application."""
	# Note that these are referenced from 'self' in the methods
	MIN_POINTS = 3
	MAX_POINTS = 3
	MAX_SEP_DENOM = 4

	def __init__(self, height, width):
		"""Constructor"""
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
		self.rotation = 0	# TODO
		self.affine   = 0	# TODO
		self.growthX  = 0	# TODO
		self.growthY  = 0	# TODO

	def __copy__(self):
		"""Copy constructor."""
		ret = self.__class__(self.height, self.width)

		ret.xAnchor = self.xAnchor
		ret.yAnchor = self.yAnchor
		ret.xPoints = copy(self.xPoints)
		ret.yPoints = copy(self.yPoints)

		ret.rotation = self.rotation
		ret.affine   = self.affine
		ret.growthX  = self.growthX
		ret.growthY  = self.growthY

		return ret

	def initPoints(self):
		"""Initialize or refresh points."""
		numPoints = random.randint(self.__class__.MIN_POINTS, 
								   self.__class__.MAX_POINTS)

		self.xPoints = []
		self.yPoints = []
		for i in range(numPoints):
			self.xPoints.append(random.randint(-self.maxSep, self.maxSep))
			self.yPoints.append(random.randint(-self.maxSep, self.maxSep))

	def getCords(self):
		"""Return a tuple of x1, y1, x2, y2... points in a format suitable for 
		use in aggdraw. This takes into account all geometry operations."""
		points = []
		for i in range(len(self.xPoints)):
			points.append(self.xPoints[i]+self.xAnchor)
			points.append(self.yPoints[i]+self.yAnchor)

		if len(points) > self.__class__.MAX_POINTS*2:
			raise Exception, "Too many points in coordinate system: " + str(points)

		return tuple(points)

	def addPoint(self):
		"""Add a point at a random position as long as the MAX_POINTS threshold 
		has not already been reached."""
		if len(self.xPoints) >= self.__class__.MAX_POINTS:
			return
		randPt = random.randint(0, len(self.xPoints))
		self.xPoints.insert(randPt, random.randint(-self.maxSep, self.maxSep))
		self.yPoints.insert(randPt, random.randint(-self.maxSep, self.maxSep))

	def remPoint(self):
		"""Remove a point from a random position as long as the MIN_POINTS
		threashold has not been reached."""
		if len(self.xPoints) <= self.__class__.MIN_POINTS:
			return
		randPt = random.randint(0, len(self.xPoints)-1)
		self.xPoints.pop(randPt)
		self.yPoints.pop(randPt)

	def mutatePoint(self):
		"""Change the coordinate of one of the points."""
		# TODO: Implement a gray-coding evolution scheme.
		randPt = random.randint(0, len(self.xPoints)-1)
		self.xPoints[randPt] = random.randint(-self.maxSep, self.maxSep)
		self.yPoints[randPt] = random.randint(-self.maxSep, self.maxSep)

	def mutatePoints(self):
		"""Mutate a random number of points."""
		randNum = random.randint(0, len(self.xPoints)-1)
		for i in range(randNum):
			randPt = random.randint(0, len(self.xPoints)-1)
			self.xPoints[randPt] = random.randint(-self.maxSep, self.maxSep)
			self.yPoints[randPt] = random.randint(-self.maxSep, self.maxSep)

	def mutateTranslationSmall(self):
		"""Change the anchor point ever so slightly to translate the object to
		a new point, utilizing a gray coding-like scheme."""
		x = self.xAnchor
		y = self.yAnchor
		self.xAnchor = random.randint(x-5, x+5)
		self.yAnchor = random.randint(y-5, y+5)

	def mutateTranslationLarge(self):
		"""Change the anchor point potentially drastically."""
		x = self.xAnchor
		y = self.yAnchor
		self.xAnchor = random.randint(-self.width, self.width)
		self.yAnchor = random.randint(-self.height, self.height)
