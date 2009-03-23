# Genetic Art application.
# Copyright 2009 Brandon Thomas 
# <http://possibilistic.org>

import random
import Image, ImageDraw
import aggdraw

from GAIndividual import *
from GAChromosome import *

#
# TODO:
# Add expression depth for the circles - normally circles are drawn one
# right after the other in a layer, but this can force us into local 
# extrema very quickly. To combat this, allow a gene to change its expression
# order (level) by adding a new parameter to each gene. - might want to clean
# up the TODO sections/refactor before adding this.
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


	def __init__(self, chromo = None):
		"""Initialize the individual. The gene will either be random, or bred 
		from others."""
		super(self.__class__, self).__init__(chromo)

		# Unique parameters
		self.image = None

	@classmethod
	def protoGene(cls):
		"""Return the prototypical gene that is used in both chromosome 
		initialization as well as random chromosome addition."""
		return [
				0,		# Radius
				-5000,	# x cord - don't initate in a predictable corner,
				-5000,	# y cord   because that will affect evolution
				0,		# z-index
				127,	# r channel - neutral values 
				127,	# g channel
				127,	# b channel
				127		# a channel
		]


	# TODO: Make sure this still works.
	def mutate(self, times = 1):
		"""Overridden mutation operator: randomly mutate the value of one codon,
		with the codon's gene itself selected at random. Can no longer be 
		performed once drawn."""
		if self.image != None:
			return

		while times > 0:
			xtype = random.randint(0,4)
			numGenes = self.chromosome.getNumGenes()

			# Remove a gene
			if xtype == 0 and self.__class__._isNumGenesVariable:
				if numGenes > self.__class__._initGenes:
					randGenePos = random.randint(0, numGenes-1)
					self.chromosome.pop(randGenePos)
					return
				
			# Insert a new gene
			elif xtype == 1 and self.__class__._isNumGenesVariable:
				if numGenes < self.__class__._maxGenes:
					randGenePos = random.randint(0, numGenes)
					self.chromosome.insert(randGenePos, self.protoGene())
					return
				
			# Else, Normal point mutation
			mpos = random.randint(0, len(self.chromosome)-1)
			mtype = mpos % len(self.chromosome)

			if mtype == 0:
				# TODO: Make maximum radius size a function of image size
				self.chromosome[mpos] = random.randint(0, 3000)   # radius
			elif mtype in (1, 2, 3):
				maxCord = max(self.__class__._width, self.__class__._height)*2
				self.chromosome[mpos] = random.randint(-maxCord, maxCord) # x, y, z
			else:
				self.chromosome[mpos] = random.randint(0, 255)	  # rgba vals

			self.mutationCnt += 1
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
			(self.__class__._width, self.__class__._height), (0,0,0,0))
		dr = aggdraw.Draw(self.image)

		zIndexList = [] # list of z-indexes
		gIndexList = [] # list of gene indexes

		geneIdx = 0
		for gene in self.chromosome: 
			# don't waste CPU drawing invisible (via alpha channel) images
			if gene[7] is 0:	
				geneIdx+=1			
				continue

			zIndexList.append(gene[3])
			gIndexList.append(geneIdx)
			geneIdx+=1

		while len(zIndexList) > 0:
			zIndexMin = zIndexList.index(min(zIndexList))
			geneIdx = gIndexList[zIndexMin]
			rad = self.chromosome[geneIdx,0]
			x = self.chromosome[geneIdx,1]
			y = self.chromosome[geneIdx,2]
			z = self.chromosome[geneIdx,3]
			r = self.chromosome[geneIdx,4]
			g = self.chromosome[geneIdx,5]
			b = self.chromosome[geneIdx,6]
			a = self.chromosome[geneIdx,7]
			col = (r, g, b, a)
			brush = aggdraw.Brush(col)
			dr.ellipse((x, y, x+rad, y+rad), None, brush)
			dr.flush()

			zIndexList.pop(zIndexMin)
			gIndexList.pop(zIndexMin)

		self.image = self.image.convert("RGB")

	def saveAs(self, name):
		"""Save the image.
		There is no check to see if it is already saved."""
		self.image.save(name)

