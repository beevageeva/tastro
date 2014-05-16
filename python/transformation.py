from generate_source import readImage, showImage, getImageSize
import numpy as np
from math import sqrt

#this is abstract  
#it won't raise NotImplementedError
class Transformation:

	def transform(self, nx, xl, yl, sourceImg, isRgb = False):
		#print("transform in Transformation")
		sourceData = readImage(sourceImg)
		ny = sourceData.shape[0]
		
		#print("imageFile=%s, ny = %d" % (sourceImg, ny))
	
		xs = 2.0 * xl / nx  #size of pixel source in points
		ys = 2.0 * yl / ny 
		if(isRgb):	
			imageData = np.zeros((nx, nx, 3))
		else:	
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

	def getImageMag(self, nx, xl, yl, ny):
		xs = 2.0 * xl / nx  #size of pixel source in points
		ys = 2.0 * yl / ny 
	
		imageMag = np.zeros((ny, ny))
		for i in range(0, nx):
			for j in range(0, nx):
				#pixel -> coordinates in image
				x1 = -float(xl) + i * xs
				x2 = -float(xl) + j * xs
				#identity x1->y1 , x2->y2
				sourcePixel = self.getSourcePixel(x1, x2)
				y1 = sourcePixel[0]
				y2 = sourcePixel[1]
				#find corresponding points in source plane
				i1 = int((y1+yl)/ys)
				i2 = int((y2+yl)/ys) 
				if (i1>=0 and i1<=ny-1) and (i2>=0 and i2<=ny-1):
					imageMag[i1][i2] += 1
		return imageMag		

	def showTransform(self,nx, xl, yl, sourceFilename, withMagMap = False, title=None, imgFullname=None, isRgb = False):
		A = self.transform(nx, xl, yl, sourceFilename, isRgb)
		if(withMagMap):
			from generate_source import show3Images
			imageData = readImage(sourceFilename)
			ny = len(imageData) #assumes a square image
			imageMag = self.getImageMag(nx, xl, yl, ny)
			show3Images(A, imageMag, imageData, title, imgFullname)
		else:
			showImage(A, title, imgFullname)



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
	def makeAnim(self, nx, xl, yl, sourceFilename, endPoint, step, outDir, withMagMap=False, isRgb = False):
		print("DefinedPointTransformation.makeAnim")
		import os.path
		flen = len("%d" % ((endPoint * endPoint) / (step * step)))
		#print("FLEN %d " % flen)
		for i in np.arange(0, endPoint, step):
			for j in np.arange(0, endPoint, step):
				#print("i=%4.2f, j=%4.2f" % (i, j))
				self.x01 = i
				self.x02 = j
				title = "x01=%1.2f, x02=%1.2f" %(self.x01, self.x02)
				#d1 (first digit in base endPoint / step)
				#d2 (second digit in base endPoint / step)
				d1 = self.x01 / step
				d2 = self.x02 / step
				
				imgname = "%d" % (d1 * (endPoint / step) + d2)
				#print("title=%s, imgname(before padding)=%s, d1=%E, d2=%E, base = %E" % (title, imgname, d1, d2, (endPoint / step)))	
				
				for k in range(0, flen - len(imgname)):
					imgname = "0" + imgname

				self.showTransform(nx, xl, yl, sourceFilename, withMagMap, title, os.path.join(outDir, imgname), isRgb)


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
		#print("getSourcePixel(%E, %E) IsothermicSphereTransformation self.01 = %E, self.x02 = %E" % (x1, x2, self.x01, self.x02))
		if x1 == self.x01 and x2 == self.x02:
			d = 0.0000001 #la chapuza
		else:
			d = sqrt((x1 - self.x01)**2 + (x2 - self.x02)**2)
		#print("x1=%E,x2=%E,d=%E" % (x1,x2,d))
		y1 = x1 - (x1 - self.x01)/d
		y2 = x2 - (x2 - self.x02)/d
		return [y1, y2]



class QuadrPertTransformation(DefinedPointTransformation):
	def __init__(self, x01, x02, gamma):
		DefinedPointTransformation.__init__(self, x01, x02)
		self.gamma = gamma


	def makeAnim(self, nx, xl, yl, sourceFilename, endPoint, step, gammaStart, gammaEnd, gammaStep, outDir, withMagMap=False, isRgb = False):
		print("QuadrPertTransformation.makeAnim")
		import os.path
		for k in np.arange(gammaStart, gammaEnd, gammaStep):
			#TODO format %4.3f
			self.gamma = k
			newdir = os.path.join(outDir, ("%4.3f" % k) )
			os.mkdir(newdir)
			DefinedPointTransformation.makeAnim(self, nx, xl, yl, sourceFilename, endPoint, step, newdir, withMagMap, isRgb)


class QuadrPertLensTransformation(QuadrPertTransformation):
	

	def getSourcePixel(self, x1, x2):
		#print("getSourcePixel(%E, %E) QuadrPertTransformation self.01 = %E, self.x02 = %E, self.gamma = %E" % (x1, x2, self.x01, self.x02, self.gamma))
		if x1 == self.x01 and x2 == self.x02:
			d = 0.0000001 #la chapuza
		else:
			d = (x1 - self.x01)**2 + (x2 - self.x02)**2
		#print("x1=%E,x2=%E,d=%E" % (x1,x2,d))
		y1 =  (x1 - self.x01)/d
		y2 =  (x2 - self.x02)/d
		#print("getSourcePixel %E" % self.gamma)
		return [(1.0 - self.gamma ) * x1 - y1, (1.0 + self.gamma) * x2 - y2]

	
class QuadrPertSphereTransformation(QuadrPertTransformation):
		
	def getSourcePixel(self, x1, x2):
		#print("getSourcePixel(%E, %E) IsothermicSphereTransformation self.01 = %E, self.x02 = %E" % (x1, x2, self.x01, self.x02))
		if x1 == self.x01 and x2 == self.x02:
			d = 0.0000001 #la chapuza
		else:
			d = sqrt((x1 - self.x01)**2 + (x2 - self.x02)**2)
		#print("x1=%E,x2=%E,d=%E" % (x1,x2,d))
		y1 = (x1 - self.x01)/d
		y2 =  (x2 - self.x02)/d
		return [(1.0 - self.gamma ) * x1 - y1, (1.0 + self.gamma) * x2 - y2]



class BinarySystemTransformation(Transformation):
	#k = M1/M2
	def __init__(self, k, a):
		self.eps1 = k / (k+1.0)	
		self.eps2 = 1 / (k+1.0)	
		self.x11 = -self.eps2 * a
		self.x12 = 0.0
		self.x21 = self.eps1 * a
		self.x22 = 0.0

	
	def setK(self, k):
		#get a 
		a =  self.x21 / self.eps1
		self.eps1 = k / (k+1.0)	
		self.eps2 = 1 / (k+1.0)	
		self.x11 = -self.eps2 * a
		self.x21 = self.eps1 * a
		


	def getSourcePixel(self, x1, x2):
		d1 = 0
		d2 = 0
		if x1 == self.x11 and x2 == self.x12:
			d1 = 0.0000001 #la chapuza
		else:
			d1 = (x1 - self.x11)**2 + (x2 - self.x12)**2
		if x1 == self.x21 and x2 == self.x22:
			d2 = 0.0000001 #la chapuza
		else:	
			d2 = (x1 - self.x21)**2 + (x2 - self.x22)**2
		#print("x11=%E,x12=%E,x21=%E,x22=%E,x1=%E,x2=%E,d1=%E,d2=%E,%s,%s" % (self.x11, self.x12, self.x21,self.x22,x1,x2,d1,d2, ( x1 == self.x11), ( x2 == self.x12)))
		y1 = x1 - self.eps1 *  (x1 - self.x11)/d1 - self.eps2 * (x1 - self.x21) / d2
		y2 = x2 - self.eps1 *  (x2 - self.x12)/d1 - self.eps2 * (x2 - self.x22) / d2
		#print("getSourcePixel %E" % self.gamma)
		return [y1, y2]

	#outDir must exist
	def makeAnim(self, nx, xl, yl, ny, startK, endK, stepK, outDir):
		print("BinarySystemTransformation.makeAnim")
		import os.path
		print(((endK - startK) / stepK))
		flen = len("%d" % ((endK - startK) / stepK))
		print("FLEN %d " % flen)
		npoints = int((endK - startK)/stepK)
		for k in np.linspace(startK, endK, npoints):
			#print("i=%4.2f, j=%4.2f" % (i, j))
			self.setK(k)
			title = "k=%1.6f" %(k)
			imgname = "%d" % abs(k / stepK)
			#print("title=%s, imgname(before padding)=%s, d1=%E, d2=%E, base = %E" % (title, imgname, d1, d2, (endPoint / step)))	
			
			for i in range(0, flen - len(imgname)):
				imgname = "0" + imgname
			imgFile = os.path.join(outDir, imgname)
			imageMag = self.getImageMag(nx, xl, yl, ny)
			showImage(imageMag, title, imgFile)
