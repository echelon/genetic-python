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

	a = GAChromosome([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)

	for gene in a:
		print gene

	print ""

	for gene in a:
		print gene

	print ""

	print a[0]
	print a[1]

	print a[0:4]

	print ""

	print a[0,0]
	print a[0,1]
	print a[0,2]

	print ""

	print a[0,0]
	print a[1,0]
	print a[2,0]

	a[0] = 111

	for gene in a:
		print gene

