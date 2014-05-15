import os
from transformation import *
from common import createFolder
import numpy as np
from generate_source import showImage
import matplotlib.pyplot as plt


#X image , Y source

#transformType = "identity" 
#transformType = "simple_lens" 
#transformType = "simple_lens_quadr_pert" 
#transformType = "isothermic_sphere" 
#transformType = "isothermic_sphere_quadr_pert" 
transformType = "binary_system" 


nx = 30000 #number of points of the image
#nx = 200 #number of points of the image
#xl, yl depends on problem geometry
#xl = 8 #2*xl = number of matrix image elements (points) of a pixel (image plan)
#yl = 4 #2*yl = number of matrix image elements (points) of a pixel (source plan)
xl = 1 
yl = 0.00025

#imgFilename = "circle.png"
imgFilename = "circles.png"

transformation = None

if transformType == "identity":
	transformation = IdentityTransformation()

elif transformType == "simple_lens":
	x01 = 0
	x02 = 0
	transformation = SimpleLensTransformation(x01,x02)	
elif transformType == "simple_lens_quadr_pert":
	x01 = 0.5
	x02 = 0 
	gamma = 0.5 #this must be between [0.1 .. 0.7]
	transformation = QuadrPertLensTransformation(x01, x02, gamma) 
elif transformType == "isothermic_sphere":
	x01 = 0.5
	x02 = 1 
	transformation = IsothermicSphereTransformation(x01, x02) 
elif transformType == "isothermic_sphere_quadr_pert":
	x01 = 0.8
	x02 = 0.8
	gamma = -0.5 #this must be between [0.1 .. 0.7]
	transformation = QuadrPertSphereTransformation(x01, x02, gamma) 
elif transformType == "binary_system":
	#k = 10 ** (-3)
	#a = 1.2
	#k = 0.1
	#a = 1.5
	#k = 0.01
	#k = 0.5
	#k = 1
	#a = 1.5
	#nature planet
	k = 7.6 * 10 ** (-5)
	#k = 7.6 * 10 ** (-4)
	a = 1.61
	transformation = BinarySystemTransformation(k, a)

#def getCurveImplicit(theta, u0, imageArray):
#	n = len(imageArray) - 1
#	#y,x=np.ogrid[-n / 2: n/2 + 1, -n / 2: n/2 + 1]
#	y,x=np.ogrid[0: n, 0: n]
#	#print("u0 * (np.cos(theta) + np.sin(theta) * np.tan(theta))")
#	#print(u0 * (np.cos(theta) + np.sin(theta) * np.tan(theta)))
#	#delta = 0.5
#	delta = 5
#	#delta = 50
#	#mask = np.absolute(y - np.tan(theta) * x - u0 * (np.cos(theta) + np.sin(theta) * np.tan(theta))) < delta
#	mask = y - np.tan(theta) * x + u0 * (np.cos(theta) + np.sin(theta) * np.tan(theta)) < delta
#	#mask = np.absolute(n * (y - np.tan(theta) * x - u0 * (np.cos(theta) + np.sin(theta) * np.tan(theta)))) < delta
#	#print("mask.shape")
#	#print(mask.shape)
#	return [imageArray[mask], mask]
	

def getCurve(theta, u0, imageArray):
	mask = np.zeros(imageArray.shape)
	n = len(imageArray) - 1
	print("u0 * (np.cos(theta) + np.sin(theta) * np.tan(theta))")
	print(u0 * (np.cos(theta) + np.sin(theta) * np.tan(theta)))
	for xval in range(0,n+1):
		#yval =  int(n * abs(np.tan(theta) * xval + u0 * (np.cos(theta) + np.sin(theta) * np.tan(theta)))) #scaled?
		yval =  int(abs(np.tan(theta) * xval + u0 * (np.cos(theta) + np.sin(theta) * np.tan(theta))))
		#print("xval=%d,yval=%d" % (xval,yval))
		if (yval>=0) and (yval<=n):
			mask[xval][yval]  = 1
	mask = mask.astype(bool)
	#print("mask.shape")
	#print(mask.shape)
	return [imageArray[mask], mask]




def transformImage(saveToFile = False, withMagMap = False):
	title = "%s_%s" % (transformType, imgFilename[:-4])
	if(saveToFile):
		transformation.showTransform(nx, xl, yl, imgFilename, withMagMap, title, title+".png")
	else:
		transformation.showTransform(nx, xl, yl, imgFilename, withMagMap, title)



def getImageMag(ny):
	print("image mag")
	title = "%s_mag" % (transformType)	
	from datetime import datetime
	print(datetime.now())
	imageMag = transformation.getImageMag(nx, xl, yl, ny)
	print(datetime.now())
	#np.set_printoptions(threshold=np.nan)
	#print(imageMag)
	#hor projection
	#plt.plot(range(0, imageMag.shape[0]), imageMag[int(0.5 * imageMag.shape[0]),:])
	#vert projection
	#plt.plot(range(0, imageMag.shape[1]), imageMag[:,int(0.5 * imageMag.shape[0])])
	#for binary systems plot on the curve y = tan(theta) * x + u0 * (cos(theta) + sin(theta) * tan(theta))
	u0 = 0.359
	theta = 2.756 #radians
	
	res = getCurve(theta, u0, imageMag)
	#np.set_printoptions(threshold='nan')
	#print(res[0].shape)	
	#print(res[1].shape)	
	plt.plot(range(0, len(res[0])), res[0])
	plt.figure(2)
	#make a different image and plot the other on top
	curveIm = np.ones(imageMag.shape)
	curveIm[res[1]]	= 0
	plt.imshow(curveIm)
	plt.imshow(imageMag, alpha=0.5)
	#change directly imageMag array
	#imageMag[res[1]] = -1
	#plot image
	#plt.imshow(imageMag)


	plt.draw()
	plt.show()

			

def createAnimation():
	withMagMap = True
	endX01X02 = 4
	stepX01X02 = 0.1
	folderBasename = "img_%s_%s" % (transformType, imgFilename[:-4])
	if(isinstance(transformation, QuadrPertTransformation)):
		#for a range
		#startGamma = 0.6
		#endGamma = 0.71
		#stepGamma = 0.05
#		#negative gamma
		startGamma = -0.7
		endGamma = 0.7
		stepGamma = 0.1
#		#only one point
#		#just for one gamma value 0.1 (the step) here can be any value except 0!
#		startGamma = -0.6
#		endGamma = -0.599
#		stepGamma = 0.1
		transformation.makeAnim(nx,xl,yl,imgFilename, endX01X02, stepX01X02, startGamma, endGamma, stepGamma, createFolder(folderBasename), withMagMap)
	else:
		transformation.makeAnim(nx,xl,yl,imgFilename, endX01X02, stepX01X02, createFolder(folderBasename), withMagMap)


#save to file and NO mag Map
#transformImage(True)
#save to file with mag Map
#transformImage(True, True)
#NO save to file, with mag map
#transformImage(False, True)
#NO save to file, NO mag map
#transformImage()
#this creates an animation see withMagMap in function impl to set either to show the magnification map supeposed on the source image
#createAnimation()
getImageMag(100)
#transformation.showTransform(nx, xl, yl, "circles.png", True)
#transformation.makeAnim(nx, xl, yl, ny, startK, endK, stepK, outDir)
#transformation.makeAnim(nx, xl, yl, 1000, 1, 7.6 * 10 ** (-5), -0.1, createFolder("outBS"))

