#import pylab as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from math import sqrt
from random import random


def rect(li, lo):
	a = np.zeros((2*lo, 2*lo))
	ccolor = random()
	for j in range(int(lo - li) , int(lo + li) + 1):
		for k in range(int(lo -li),  int(lo + li) + 1):
			a[j][k] = ccolor
	return a


def circle(r, l):
	a = np.zeros((2 * l, 2 * l))
	ccolor = random()
	for j in range(int(l - r), int(l + r)+1):
		b = abs(l - j)
		q = sqrt(r ** 2 - b**2)
		for k in range(int(l-q), int(l+q)+1):
			a[j][k] =  ccolor
	return a
	
#now r is an array
def circles(r, l):
	if(not hasattr(r, "__len__") or (len(r)==0)):
		print("r must be an array with at least 1 elem")
		sys.exit()
	r = sorted(r, reverse=True)
	if(r[0]>l):
		print("out circle radius %(4.3f)  cannot be bigger than l (%4.3f)" % (r[0], l))
		sys.exit()
	a = np.zeros((2 * l, 2 * l))
	ccolor = []
	for i in range(0, len(r)):
		ccolor.append(random())
	for j in range(int(l - r[0]), int(l + r[0])+1):
		b = abs(l - j)
		q = sqrt(r[0] ** 2 - b**2)
		for k in range(int(l-q), int(l+q)+1):
			found = False
			index = 0
			#see in what circle the point is : this is not the fast way..
			for i in range(1, len(r)):
				#print("b**2 = %4.2f, (l - k)**2 = %4.2f, sum %4.2f, r[%d]**2 = %4.2f" % (b**2, (l-k)**2, b**2 + (l-k)**2,i, r[i] ** 2))
				#print("b = %4.2f, l - k = %4.2f, r[%d] = %4.2f" % (b, (l-k), i, r[i]))
				if((l-k)**2 + b**2 <= r[i] ** 2):
					index = i
				else:
					found = True
				if(found):
					break
			#print("Found i = %d" % index)
			a[j][k] =  ccolor[index]
	#print("result")
	#print(a)
	return a
	
#filename should contain extension
def readImage(filename):
	extension = filename[-4:]	
	if(extension == ".png"):
		#native
		img=mpimg.imread(filename)
	else:
		#use PIL
		import Image
		img = Image.open(filename).getdata() 
	return img

def getImageSize(filename):
	import Image
	return Image.open(filename).size



#filename should not contain extension
#I want always png
def saveImage(A, filename):
	import Image
	A = (A*255).astype('uint8')
	im = Image.fromarray(A)
	im.save("%s.png" % filename)

#saveFilename should contain extension
def showImage(A, title=None, saveFilename=None):
	plt.figure(1)
	#plt.imshow(A, interpolation='nearest')
	#antialiasing	
	plt.imshow(A)
	plt.grid()
	if(title):
		plt.title(title)
	if(saveFilename):
		plt.savefig(saveFilename)
	else:
		plt.draw()
		plt.show()



