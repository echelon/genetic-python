#!/usr/bin/env python

import Image, ImageDraw
import random
import math
import aggdraw
import os
from optparse import OptionParser

from genetic.GAChromosome import *

class A:
	_var = 1
	_foo = 2
	var = 2

class B(A):
	pass

if __name__ == '__main__':

	ch = GAChromosome(range(60), 10)
	rev = range(1500)
	rev.reverse()
	rev = rev[0:100]
	ch2 = GAChromosome(rev, 10)

	b = ch.cross(ch2)

	for gene in b:
		print gene
