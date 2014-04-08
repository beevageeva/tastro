from generate_source import readImage, showImage
import numpy as np
from math import sqrt

#this is abstract  
#it won't raise NotImplementedError
class Transformation:

	def transform(self, nx, xl, yl, sourceImg):
		sourceData = readImage(sourceImg)
		ny = sourceData.shape[0]
		
		#print("imageFile=%s, ny = %d" % (sourceImg, ny))
	
		xs = 2.0 * xl / nx  #size of pixel source in points
		ys = 2.0 * yl / ny 
	
		imageData = np.zeros((nx, nx))
		for i in range(0, nx):
			for j in range(0, nx):
				#pixel -> coordinates in image
				x1 = -float(xl) + i * xs
				x2 = -float(xl) + j * xs
				#identity x1->y1 , x2->y2
				sourcePixel = self.getSourcePixel(x1, x2)
				y1 = sourcePixel[0]
				y2 = sourcePixel[1]
				#find corresponding points in image space
				i1 = int((y1+yl)/ys)
				i2 = int((y2+yl)/ys) 
				if (i1>=0 and i1<=ny-1) and (i2>=0 and i2<=ny-1):
					imageData[i][j] = sourceData[i1][i2] 
		return imageData		



class IdentityTransformation(Transformation):
	
	def getSourcePixel(self, x1, x2):
		return [x1, x2]
		


#this is abstract
#it won't raise NotImplementedError
class DefinedPointTransformation(Transformation):
	def __init__(self, x01, x02):
		self.x01 = x01
		self.x02 = x02

	#outDir must exist
	def makeAnim(self, nx, xl, yl, sourceFilename, endPoint, step, outDir):
		import os.path
		flen = len("%d" % ((endPoint * endPoint) / (step * step)))
		print("FLEN %d " % flen)
		for i in np.arange(0, endPoint, step):
			for j in np.arange(0, endPoint, step):
				print("i=%4.2f, j=%4.2f" % (i, j))
				self.x01 = i
				self.x02 = j
				title = "x01=%1.2f, x02=%1.2f" %(self.x01, self.x02)
				#d1 (first digit in base endPoint / step)
				#d2 (second digit in base endPoint / step)
				d1 = self.x01 / step
				d2 = self.x02 / step
				
				imgname = "%d" % (d1 * (endPoint / step) + d2)
				print("title=%s, imgname(before padding)=%s, d1=%E, d2=%E, base = %E" % (title, imgname, d1, d2, (endPoint / step)))	
				
				for k in range(0, flen - len(imgname)):
					imgname = "0" + imgname
				A = self.transform(nx, xl, yl, sourceFilename)
				showImage(A, title, os.path.join(outDir, imgname))

class SimpleLensTransformation(DefinedPointTransformation):

	def getSourcePixel(self, x1, x2):
		#print("x01 = %E, x02 = %E" % (x01, x02))
		if x1 == self.x01 and x2 == self.x02:
			d = 0.0000001 #la chapuza
		else:
			d = (x1 - self.x01)**2 + (x2 - self.x02)**2
		#print("x1=%E,x2=%E,d=%E" % (x1,x2,d))
		y1 = x1 - (x1 - self.x01)/d
		y2 = x2 - (x2 - self.x02)/d
		return [y1, y2]


class IsothermicSphereTransformation(DefinedPointTransformation):

	def getSourcePixel(self, x1, x2):
		#print("x01 = %E, x02 = %E" % (x01, x02))
		if x1 == self.x01 and x2 == self.x02:
			d = 0.0000001 #la chapuza
		else:
			d = sqrt((x1 - self.x01)**2 + (x2 - self.x02)**2)
		#print("x1=%E,x2=%E,d=%E" % (x1,x2,d))
		y1 = x1 - (x1 - self.x01)/d
		y2 = x2 - (x2 - self.x02)/d
		return [y1, y2]



class QuadrPertTransformation(DefinedPointTransformation):
	def __init__(self, cls, x01, x02, gamma):
		DefinedPointTransformation.__init__(self, x01, x02)
		self.cls = cls
		self.gamma = gamma

	
	def getSourcePixel(self, x1, x2):
		sres =  self.cls.getSourcePixel(self, x1, x2)
		#print("getSourcePixel %E" % self.gamma)
		return [(1.0 - self.gamma ) * sres[0], (1.0 + self.gamma) * sres[1]]

	def makeAnim(self, nx, xl, yl, sourceFilename, endPoint, step, gammaStart, gammaEnd, gammaStep, outDir):
		import os.path
		for k in np.arange(gammaStart, gammaEnd, gammaStep):
			#TODO format %4.3f
			self.gamma = k
			newdir = os.path.join(outDir, ("%4.3f" % k) )
			os.mkdir(newdir)
			DefinedPointTransformation.makeAnim(self, nx, xl, yl, sourceFilename, endPoint, step, newdir)


class QuadrPertLensTransformation(QuadrPertTransformation, SimpleLensTransformation):
	
	def __init__(self, x01, x02, gamma):
		QuadrPertTransformation.__init__(self, SimpleLensTransformation, x01, x02, gamma)

	
class QuadrPertSphereTransformation(QuadrPertTransformation, IsothermicSphereTransformation):
	
	def __init__(self, x01, x02, gamma):
		QuadrPertTransformation.__init__(self, IsothermicSphereTransformation, x01, x02, gamma)
		
