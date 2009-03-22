# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random
import Image, ImageDraw

from IndividualGA import *

# This algorithm to evolve an image pixel by pixel is slow and can be 
# done much quicker in a general backwards search from the original image
# to zero pixels. The reason why this is possible is because this type of
# representation does not build upon other dependencies within the solution,
# that is, each pixel is unique and self-contained.

class IndividualPixel(IndividualGA):
	# Chromosome length
	_chromoLength = 0

	# Individual counter
	_bredCnt    = 0

	# Static parameters that must be set before creating
	__width  = 0
	__height = 0

	@staticmethod
	def setCodingLen(length):
		"""NO EFFECT"""
		pass

	@staticmethod
	def setImageSize(width, height):
		"""Set the size of images to be produced, usually to match the target 
		image. This MUST be called before any individuals are created."""
		IndividualPixel.__width  = width
		IndividualPixel.__height = height
		IndividualPixel._chromoLength = width * height * 3


	def __init__(self, chromo = None):
		"""Initialize the individual. The gene will either be random, or bred 
		from others."""
		IndividualGA.__init__(self, chromo)

		# Unique parameters
		self.image = None


	def initDNA(self):
		"""Overloadable helper method used to generate any initial DNA strings 
		that aren't the result of crossover. This forms the initial generation.
		This is especially useful when overriding the base class."""
		chromo = [0, 0, 0] * self.__width * self.__height

		return chromo


	def mutate(self):
		"""Overridden mutation operator: randomly mutate the value of one codon,
		with the codon's gene itself selected at random. Can no longer be 
		performed once drawn."""
		if self.image != None:
			return

		mpos = random.randint(0, len(self.chromosome)-1)
		self.chromosome[mpos] = random.randint(0, 255)


	def evalFitness(self, target, targetThumb):
		"""The Fitness Evaluation function will rank this individual against a 
		scoring heursitic designed to identify the best solutions. The 
		population controller will use this score to apply selection pressures.

		This function is designed to Maximize the score.
		"""
		# Don't recompute
		if type(self.score) == int:
			return self.score

		if self.image == None:
			print "IMAGE NOT GENERATED"
			return False

		# Too costly to calculate for a fullsize image
		imThumb = self.image.resize(targetThumb.size)
		pixOrig = targetThumb.load()
		pixGen  = None
		pixGen  = imThumb.load()

		# We're using a maximization scoring heuristic 
		score = 0
		width = imThumb.size[0]
		height = imThumb.size[1]
		for i in range(width): # TODO
			for j in range(height):
				# The closer the channels are, the higher the score
				diffR = 255 - abs(pixOrig[i,j][0] - pixGen[i,j][0])
				diffG = 255 - abs(pixOrig[i,j][1] - pixGen[i,j][1])
				diffB = 255 - abs(pixOrig[i,j][2] - pixGen[i,j][2])

				score += diffR + diffG + diffB

		self.score = score

		maxScore = width * height * 255.0
		self.scorePercent = score / maxScore

		return self.score


	def __str__(self):
		"""The representation of the class when printed."""
		return IndividualGA.__str__(self, chromo)


	####################################################
	############# CLASS-SPECIFIC FUNCTIONS #############
	####################################################

	def draw(self):
		""" Draw the image for the first time. Can only be done once."""
		if self.image != None:
			return

		self.image = Image.new("RGB", 
			(self.__width, self.__height), (0,0,0))

		pix = self.image.load()

		for i in range(self.__width):
			for j in range(self.__height):
				offset = (j*self.__width + i)*3


				rgb = (self.chromosome[offset+0],
					   self.chromosome[offset+1],
					   self.chromosome[offset+2])

				pix[i,j] = rgb

		self.image = self.image.convert("RGB")

	def saveAs(self, name):
		"""Save the image.
		There is no check to see if it is already saved."""
		self.image.save(name)

