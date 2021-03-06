#!/usr/bin/env python2.6
# Copyright 2009 Brandon Thomas Suit
# <http://possibilistic.org>
# Licensed under the LGPL3.

import random

class Polygon(object):
	"""Representation of polygon shapes for the Evolution application."""
	# Note that these are referenced from 'self' in the methods
	MIN_POINTS = 3
	MAX_POINTS = 7
	MAX_SEP_DENOM = 5 # XXX TODO REMOVE

	# Growth transformations
	MIN_GROWTH = 0.8
	MAX_GROWTH = 1.2

	def __init__(self, height, width):
		"""Constructor will randomize the polygon."""
		# Dimensions of src image
		self.height = height
		self.width = width

		# Random constants		
		self.maxSep = (height + width) / self.__class__.MAX_SEP_DENOM # TODO XXX REMOVE

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
		
		numPoints = random.randint(self.__class__.MIN_POINTS, 
								   self.__class__.MAX_POINTS)

		for i in range(numPoints):
			xPoints.append(random.randint(-self.maxSep, self.maxSep))
			yPoints.append(random.randint(-self.maxSep, self.maxSep))

		self.xPoints = xPoints
		self.yPoints = yPoints

	def getCords(self):
		"""Return a tuple of (x1, y1, x2, y2...) points in a format suitable for
		use in aggdraw. This takes into account all geometry operations."""
		points = []
		for i in range(len(self.xPoints)):
			points.append(int(self.xPoints[i]*self.xGrowth+self.xAnchor))
			points.append(int(self.yPoints[i]*self.yGrowth+self.yAnchor))

		if len(points) > self.__class__.MAX_POINTS*2:
			raise Exception, "Too many points in coordinate system: " + \
					str(points)

		return tuple(points)

	def mutateAddPoint(self):
		"""Add a point at a random position as long as the MAX_POINTS threshold 
		has not already been reached."""
		if len(self.xPoints) >= self.__class__.MAX_POINTS:
			return
		
		randPt = random.randint(0, len(self.xPoints))
		self.xPoints.insert(randPt, random.randint(-self.maxSep, self.maxSep))
		self.yPoints.insert(randPt, random.randint(-self.maxSep, self.maxSep))

	def mutateRemovePoint(self):
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
		self.xAnchor = random.randint(x-20, x+20)
		self.yAnchor = random.randint(y-20, y+20)

	def mutateTranslationLarge(self):
		"""Change the anchor point potentially drastically."""
		self.xAnchor = random.randint(-self.width, self.width)
		self.yAnchor = random.randint(-self.height, self.height)

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


