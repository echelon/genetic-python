# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random
import Image, ImageDraw
import aggdraw

from IndividualGA import *

#
# TODO:
# Add expression depth for the circles - normally circles are drawn one
# right after the other in a layer, but this can force us into local 
# extrema very quickly. To combat this, allow a gene to change its expression
# order (level) by adding a new parameter to each gene. - might want to clean
# up the TODO sections/refactor before adding this.
#

class IndividualCircle(IndividualGA):
	# Chromosome length
	_chromoLength = 0

	# Number of coding sequences
	_codingSeqs = 0

	# Individual counter
	_bredCnt    = 0

	# Static parameters that must be set before creating
	__width  = 0
	__height = 0

	geneParamCnt = 8 # TODO - refactor this

	@staticmethod
	def setCodingLen(length):
		"""Set the size of images to be produced, usually to match the target 
		image. This MUST be called before any individuals are created."""
		IndividualCircle._codingSeqs = length
		IndividualCircle._chromoLength = \
			self.__class__._codingSeqs * self.__class__.geneParamCnt

	@staticmethod
	def setImageSize(width, height):
		"""Set the size of images to be produced, usually to match the target 
		image. This MUST be called before any individuals are created."""
		IndividualCircle.__width  = width
		IndividualCircle.__height = height


	def __init__(self, chromo = None):
		"""Initialize the individual. The gene will either be random, or bred 
		from others."""
		IndividualGA.__init__(self, chromo)

		# Unique parameters
		self.image = None
		self.geneParamCnt = 8 # TODO: REFACTOR THIS!


	def initDNA(self):
		"""Overloadable helper method used to generate any initial DNA strings 
		that aren't the result of crossover. This forms the initial generation.
		This is especially useful when overriding the base class."""
		chromo = [
				0,		# Radius
				-5000,	# x cord - don't initate in a predictable corner,
				-5000,	# y cord   because that will affect evolution
				0,		# z-index
				127,	# r channel - neutral values 
				127,	# g channel
				127,	# b channel
				127		# a channel
			] * self._codingSeqs

		return chromo


	def mutate(self):
		"""Overridden mutation operator: randomly mutate the value of one codon,
		with the codon's gene itself selected at random. Can no longer be 
		performed once drawn."""
		if self.image != None:
			return

		mpos = random.randint(0, len(self.chromosome)-1)
		mtype = mpos % len(self.chromosome)

		if mtype == 0:
			# TODO: Make maximum radius size a function of image size
			self.chromosome[mpos] = random.randint(0, 3000)   # radius
		elif mtype in (1, 2, 3):
			maxCord = max(IndividualCircle.__width, IndividualCircle.__height)*2
			self.chromosome[mpos] = random.randint(-maxCord, maxCord) # x, y, z
		else:
			self.chromosome[mpos] = random.randint(0, 255)	  # rgba vals


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
		buf = "INDIVIDUAL:\n"
		for i in range(0, len(self.chromosome), self.geneParamCnt): # TODO - refactor this
			buf += ": radius (" + str(self.chromosome[i+0]) + ")"
			buf += " position (" + str(self.chromosome[i+1]) + \
				   "," + str(self.chromosome[i+2]) + \
				   "," + str(self.chromosome[i+3]) + ")"
			buf += " color (R:" + str(self.chromosome[i+4]) + \
				   " G:" + str(self.chromosome[i+5])+ \
				   " B:" + str(self.chromosome[i+6])+ \
				   " A:" + str(self.chromosome[i+7])+ ")"
			buf += "\n"
		buf += "\n"
		return buf


	####################################################
	############# CLASS-SPECIFIC FUNCTIONS #############
	####################################################

	def draw(self):
		""" Draw the image for the first time. Can only be done once.
		Note - Aggdraw was the only library that could draw multi-layered
		transparent shapes from my experience. Both Cairo and PIL failed 
		at this simple task. PIL is used in conjunction with Agg."""
		if self.image != None:
			return

		self.image = Image.new("RGBA", 
			(self.__class__.__width, self.__class__.__height), (0,0,0,0))
		dr = aggdraw.Draw(self.image)

		zList = [] # list of z-indexes
		cList = [] # list of chromosome index points

		# TODO - remove geneParamCnt
		for i in range(0, len(self.chromosome), self.geneParamCnt): 
			# don't waste CPU drawing invisible (via alpha channel) images
			if self.chromosome[i+7] is 0:				
				continue

			zList.append(self.chromosome[i+3])
			cList.append(i)

		while len(zList) > 0:
			zIndexMin = zList.index(min(zList))
			i = cList[zIndexMin]
			rad = self.chromosome[i]
			x = self.chromosome[i+1]
			y = self.chromosome[i+2]
			z = self.chromosome[i+3]
			r = self.chromosome[i+4]
			g = self.chromosome[i+5]
			b = self.chromosome[i+6]
			a = self.chromosome[i+7]
			col = (r, g, b, a)
			brush = aggdraw.Brush(col)
			dr.ellipse((x, y, x+rad, y+rad), None, brush)
			dr.flush()

			cList.pop(zIndexMin)
			zList.pop(zIndexMin)

		self.image = self.image.convert("RGB")

	def saveAs(self, name):
		"""Save the image.
		There is no check to see if it is already saved."""
		self.image.save(name)

