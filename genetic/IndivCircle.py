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

class IndivCircle(GAIndividual):

	# Static parameters that must be set before creating
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

		# Unique parameters
		self.image = None

		self.genesAdd = 0
		self.genesRem = 0

	@classmethod
	def protoGene(cls):
		"""Return the prototypical gene that is used in both chromosome 
		initialization as well as random chromosome addition."""
		poly = Polygon(cls._width, cls._height)
		color = Color()

		return [
			random.randint(0, 255),	# z-index
			color,					# color
			poly					# Polygon
		]
		

	# TODO: Make sure this still works.
	def mutate(self, times = 1):
		"""Overridden mutation operator: randomly mutate the value of one codon,
		with the codon's gene itself selected at random. Can no longer be 
		performed once drawn."""
		if self.image != None:
			return

		# One or more point mutations
		while times > 0:
			mutated = False

			# Remove a gene
			rand = random.randint(0, 5)
			numGenes = self.chromosome.getNumGenes()
			if rand == 0 and self.__class__._isNumGenesVariable:
				if numGenes > self.__class__._initGenes:
					randGenePos = random.randint(0, numGenes-1)
					self.chromosome.pop(randGenePos)
					self.genesRem += 1
					mutated = True

			# Insert a new gene
			rand = random.randint(0, 3)
			numGenes = self.chromosome.getNumGenes()
			if rand == 0 and self.__class__._isNumGenesVariable:
				if numGenes < self.__class__._maxGenes:
					randGenePos = random.randint(0, numGenes)
					self.chromosome.insert(randGenePos, self.protoGene())
					self.genesAdd += 1
					mutated = True

			# Z-index mutation
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			if random.randint(0, 4):
				z = self.chromosome[gene,0]
				r = random.randint(-5, 5)
				z += r
				if z <= 255 and z >= -255:
					self.chromosome[gene,0] = z
				else:
					self.chromosome[gene,0] = z - r
				mutated = True
				self.mutationCnt += 1

			# Color mutation
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			rtype = random.randint(0, 5)
			if rtype == 0:
				self.chromosome[gene,1].mutateSingleSmall()
				mutated = True
				self.mutationCnt += 1
			elif rtype == 1:
				self.chromosome[gene,1].mutateSingleLarge()
				mutated = True
				self.mutationCnt += 1
			elif rtype == 2:
				self.chromosome[gene,1].mutateWholeSmall()
				mutated = True
				self.mutationCnt += 1
			elif rtype == 3:
				self.chromosome[gene,1].mutateWholeLarge()
				mutated = True
				self.mutationCnt += 1

			# Polygon mutation
			gene = random.randint(0, self.chromosome.getNumGenes()-1)
			rtype = random.randint(0, 8)
			if rtype == 0:
				self.chromosome[gene,2].initPoints()
				mutated = True
				self.mutationCnt += 1
			elif rtype == 1:
				self.chromosome[gene,2].addPoint()
				mutated = True
				self.mutationCnt += 1
			elif rtype == 2:
				self.chromosome[gene,2].remPoint()
				mutated = True
				self.mutationCnt += 1
			elif rtype == 3:
				self.chromosome[gene,2].mutatePoint()
				mutated = True
				self.mutationCnt += 1
			elif rtype == 4:
				self.chromosome[gene,2].mutatePoints()
				mutated = True
				self.mutationCnt += 1
			elif rtype == 5:
				self.chromosome[gene,2].mutateTranslationSmall()
				mutated = True
				self.mutationCnt += 1
			elif rtype == 6:
				self.chromosome[gene,2].mutateTranslationLarge()
				mutated = True
				self.mutationCnt += 1
			elif rtype == 7:
				self.chromosome[gene,2].mutateGrowth()
				mutated = True
				self.mutationCnt += 1

			# Force at least one mutation for each loop
			if mutated:
				times -= 1


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
		"""Save the image. There is no check to see if it is already saved."""
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

