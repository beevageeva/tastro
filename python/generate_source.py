import pylab as plt
import numpy as np
from math import sqrt


def rect(li, lo):
	a = np.zeros((lo, lo))
	i = int(0.5 * (lo - li))
	for j in range(i, lo - i):
		for k in range(i, li  + 0.5 * lo):
			a[j][k] = 1
	return a


def circle(r, l):
	a = np.zeros((2 * l, 2 * l))
	for j in range(l - r, l + r):
		b = abs(l - j)
		q = int(sqrt(r ** 2 - b**2))
		for k in range(l-q, l+q):
			a[j][k] = 1
	return a
	


def showImage(A):
	plt.figure(1)
	plt.imshow(A, interpolation='nearest')
	plt.grid(True)
	plt.draw()
	plt.show()

#showImage(rect(10, 100))
showImage(circle(10, 100))
