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
transformType = "isothermic_sphere_quadr_pert" 


nx = 1000 #number of points of the image
#nx = 200 #number of points of the image
#xl, yl depends on problem geometry
#xl = 8 #2*xl = number of matrix image elements (points) of a pixel (image plan)
#yl = 4 #2*yl = number of matrix image elements (points) of a pixel (source plan)
xl = 4
yl = 1

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
	x01 = 0.25
	x02 = 1 
	gamma = -0.5 #this must be between [0.1 .. 0.7]
	transformation = QuadrPertSphereTransformation(x01, x02, gamma) 
	

def transformImage(saveToFile = False):
	title = "%s_%s" % (transformType, imgFilename[:-4])
	if(saveToFile):
		showImage(transformation.transform(nx, xl, yl, imgFilename), title, title+".png")
	else:
		showImage(transformation.transform(nx, xl, yl, imgFilename), title)



def getImageMag():
	print("image mag")
	title = "%s_%s" % (transformType, imgFilename[:-4])	
	showImage(transformation.transform(nx, xl, yl, imgFilename), title)
	imageMag = transformation.getImageMag(nx, xl, yl, imgFilename)
	#np.set_printoptions(threshold=np.nan)
	#print(imageMag)
	#hor projection
	#plt.plot(range(0, imageMag.shape[0]), imageMag[int(0.5 * imageMag.shape[0]),:])
	#hvert projection
	plt.plot(range(0, imageMag.shape[1]), imageMag[:,int(0.5 * imageMag.shape[0])])
	plt.draw()
	plt.show()

			

def createAnimation():
	endX01X02 = 2
	stepX01X02 = 0.1
	folderBasename = "img_%s_%s" % (transformType, imgFilename[:-4])
	if(isinstance(transformation, QuadrPertTransformation)):
		#for a range
		startGamma = 0.6
		endGamma = 0.71
		stepGamma = 0.05
#		#negative gamma
#		startGamma = -0.7
#		endGamma = -0.1
#		stepGamma = 0.01
#		#only one point
#		#just for one gamma value 0.1 (the step) here can be any value except 0!
#		startGamma = -0.6
#		endGamma = -0.599
#		stepGamma = 0.1
		transformation.makeAnim(nx,xl,yl,imgFilename, endX01X02, stepX01X02, startGamma, endGamma, stepGamma, createFolder(folderBasename))
	else:
		transformation.makeAnim(nx,xl,yl,imgFilename, endX01X02, stepX01X02, createFolder(folderBasename))



#transformImage(True)
createAnimation()
#getImageMag()


