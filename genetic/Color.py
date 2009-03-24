# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random

class Color:
	"""Representation of colors for the Evolution application."""
	MIN_ALPHA = 20
	MAX_ALPHA = 60

	def __init__(self):
		self.r = random.randint(0, 255)
		self.g = random.randint(0, 255)
		self.b = random.randint(0, 255)
		self.a = random.randint(self.__class__.MIN_ALPHA, 
								self.__class__.MAX_ALPHA)

	def __copy__(self):
		"""Copy constructor."""
		ret = self.__class__()
		ret.r = self.r
		ret.g = self.g
		ret.b = self.b
		ret.a = self.a
		return ret

	def mutateSingleSmall(self):
		"""Change the color value slightly."""
		which = random.randint(0, 3)
		r = random.randint(-10, 10) + self.r
		g = random.randint(-10, 10) + self.g
		b = random.randint(-10, 10) + self.b
		a = random.randint(-10, 10) + self.a
		
		if which == 0 and r >= 0 and r <= 255: 
			self.r = r
		if which == 1 and g >= 0 and g <= 255: 
			self.g = g
		if which == 2 and b >= 0 and b <= 255: 
			self.b = b
		if which == 3 and \
			a >= self.__class__.MIN_ALPHA and \
			a <= self.__class__.MAX_ALPHA: 
				self.a = a

	def mutateSingleLarge(self):
		"""Large-scale mutation"""
		which = random.randint(0, 3)
		if which == 0:
			self.r = random.randint(0, 255)
		elif which == 1:
			self.g = random.randint(0, 255)
		elif which == 2:
			self.b = random.randint(0, 255)
		else:
			self.a = random.randint(self.__class__.MIN_ALPHA, 
									self.__class__.MAX_ALPHA)

	def mutateWholeSmall(self):
		"""Change the color value slightly."""
		r = random.randint(-10, 10) + self.r
		g = random.randint(-10, 10) + self.g
		b = random.randint(-10, 10) + self.b
		a = random.randint(-10, 10) + self.a
		
		if r >= 0 and r <= 255: 
			self.r = r
		if g >= 0 and g <= 255: 
			self.g = g
		if b >= 0 and b <= 255: 
			self.b = b
		if a >= self.__class__.MIN_ALPHA and \
			a<= self.__class__.MAX_ALPHA: 
				self.a = a

	def mutateWholeLarge(self):
		"""Large-scale mutation"""
		self.r = random.randint(0, 255)
		self.g = random.randint(0, 255)
		self.b = random.randint(0, 255)
		self.a = random.randint(self.__class__.MIN_ALPHA, 
								self.__class__.MAX_ALPHA)

	def getColor(self):
		"""Return in an aggdraw friendly format."""
		return (self.r, self.g, self.b, self.a)


