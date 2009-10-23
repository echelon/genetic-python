# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random
import Image, ImageDraw
import aggdraw
import StringIO

from GAIndividual import *
from GAChromosome import *
from Polygon import *
from Color import *

#
# TODO:
# Change this to a polygon-based system. 
# Add support for addition/subtraction of points
# Ensure points are relative to initial point
# Try to make sure polygons don't overlap themselves - how?


#
# Add/remove points (at any point, not just end)
# Add/remove polygons
# Shift polygon up/down
# Rotate polygon?
# Grow/shrink polygon in 1 or 2D
# Affine translations
#

class IndivPoly(GAIndividual):

	# Must be set before instantiation
	_width  = 0
	_height = 0

	@classmethod
	def setImageSize(cls, width, height):
		"""Set the size of images to be produced, usually to match the target 
		image. This MUST be called before any individuals are created."""
		cls._width  = width
		cls._height = height

	def __init__(self, chromo = None, generation = None):
		"""Initialize the individual. The gene will either be random, or bred 
		from others."""
		super(self.__class__, self).__init__(chromo, generation)

		# Subclass-specific member vars
		self.image = None
		self.genesAdd = 0
		self.genesRem = 0
		self.imported = False # Flag individuals imported from another process

	@classmethod
	def protoGene(cls):
		"""Return the prototypical gene that is used in both chromosome 
		initialization as well as random chromosome addition."""
		poly = Polygon(cls._width, cls._height)
		color = Color()

		return [
			random.randint(0, 255),	# z-index
			color,
			poly
		]
		
	def mutate(self, rate = 1):
		"""Overridden mutation operator: randomly mutate the value of one codon,
		with the codon's gene itself selected at random. Can no longer be 
		performed once drawn."""
		if self.image != None:
			return

		rate = min(rate, 1000) # TODO: Rate hinting not yet implemented.

		# Color mutation - Single Small
		if random.randint(0, 5) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,1].mutateSingleSmall()
			mutated = True
			self.mutationCnt += 1

		# Color mutation - Single Large
		if random.randint(0, 10) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,1].mutateSingleLarge()
			mutated = True
			self.mutationCnt += 5

		# Color mutation - Whole Small
		if random.randint(0, 100) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,1].mutateWholeSmall()
			mutated = True
			self.mutationCnt += 100

		# Color mutation - Whole Large
		if random.randint(0, 1000) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,1].mutateWholeLarge()
			mutated = True
			self.mutationCnt += 5000


		# Polygon Re-init
		if random.randint(0, 10) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,2].initPoints()
			mutated = True
			self.mutationCnt += 100

		# Polygon Add Point
		if random.randint(0, 10) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,2].mutateAddPoint()
			mutated = True
			self.mutationCnt += 10

		# Polygon Remove Point
		if random.randint(0, 7) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,2].mutateRemovePoint()
			mutated = True
			self.mutationCnt += 10
		
		# Polygon Mutate Point
		if random.randint(0, 4) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,2].mutatePoint()
			mutated = True
			self.mutationCnt += 1

		# Polygon Mutate Points
		if random.randint(0, 6) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,2].mutatePoints()
			mutated = True
			self.mutationCnt += 3

		# Polygon Mutate Translation Small
		if random.randint(0, 4) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,2].mutateTranslationSmall()
			mutated = True
			self.mutationCnt += 5

		# Polygon Mutation Translation Large
		if random.randint(0, 10) == 0:
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			self.chromosome[gene,2].mutateTranslationLarge()
			mutated = True
			self.mutationCnt += 10

		# TODO: Mutate Growth removed!

		# TODO: Add/Remove genes

		# TODO: Z-index mutations


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
			raise Exception, "Image for fitness evaluation was not generated"

		pixOrig = target.load()
		pixGen = self.image.load()
		width = self.image.size[0]
		height = self.image.size[1]

		if 0: # Test/debug - run faster with a thumbnail compare
			pixOrig = targetThumb.load()
			imThumb = self.image.resize(targetThumb.size)
			pixGen  = imThumb.load()
			width = imThumb.size[0]
			height = imThumb.size[1]

		# We're using a maximization scoring heuristic 
		score = 0
		for i in range(width):
			for j in range(height):
				# The closer the channels are, the higher the score
				diffR = 255 - abs(pixOrig[i,j][0] - pixGen[i,j][0])
				diffG = 255 - abs(pixOrig[i,j][1] - pixGen[i,j][1])
				diffB = 255 - abs(pixOrig[i,j][2] - pixGen[i,j][2])

				# TODO - test new scoring heuristic
				score += diffR*diffR + diffG*diffG + diffB*diffB 

		self.score = score

		maxScore = width * height * 255.0 * 255.0 * 3 # TODO - test new scoring heuristic.
		self.scorePercent = score / maxScore

		return self.score


	def draw(self):
		"""Generate the image for the first time. Can only be done if there is
		no image that has already been generated (it's called again for unpickled
		objects to regenerate the image object). Note - 
		Aggdraw was the only library that could draw multi-layered transparent 
		shapes from my experience. Both Cairo and PIL failed  at this simple 
		task. PIL is used in conjunction with Agg."""
		if self.image != None:
			return

		self.image = Image.new("RGBA", 
			(self.__class__._width, self.__class__._height), (0,0,0,0))
		dr = aggdraw.Draw(self.image)

		zIndexList = [] # list of z-indexes
		gIndexList = [] # list of gene indexes

		geneIdx = 0
		for gene in self.chromosome: 
			zIndexList.append(gene[0])
			gIndexList.append(geneIdx)
			geneIdx+=1

		while len(zIndexList) > 0:
			zIndexMin = zIndexList.index(min(zIndexList))
			geneIdx = gIndexList[zIndexMin]
			z = self.chromosome[geneIdx,0]
			color = self.chromosome[geneIdx,1]
			poly = self.chromosome[geneIdx,2]

			col = color.getColor()
			cords = poly.getCords()
			brush = aggdraw.Brush(col)

			#dr.ellipse((x, y, x+rad, y+rad), None, brush)
			dr.polygon(cords, None, brush)
			dr.flush()

			if 0: # Debug - draw dot in center of polygon
				center = (poly.xAnchor, poly.yAnchor, poly.xAnchor+5, poly.yAnchor+5)
				dr.ellipse(center, None, aggdraw.Brush((255,0,0,255)))
				dr.flush()

			zIndexList.pop(zIndexMin)
			gIndexList.pop(zIndexMin)

		self.image = self.image.convert("RGB")

	def saveImageAs(self, name):
		"""Save the image to a file. There is no check to see if the file 
		already exists."""
		self.image.save(name)

	def __getstate__(self):
		"""Remove/convert unpickleable objects from the dictionary."""
		dct = self.__dict__.copy()
		# Can't pickle ImageCore objects - convert to string
		del dct['image']
		return dct

	def __setstate__(self, dct):
		"""Restore pickled objects, and convert objects that were serialized
		under a different format."""
		self.__dict__ = dct
		self.image = None
		self.draw() # Regenerate Image

