import os
from transformation import *
from common import createFolder
import numpy as np
from generate_source import showImage


#X image , Y source

#transformType = "identity" 
#transformType = "simple_lens" 
#transformType = "simple_lens_quadr_pert" 
#transformType = "isothermic_sphere" 
transformType = "isothermic_sphere_quadr_pert" 


#nx = 1000 #number of points of the image
nx = 200 #number of points of the image
#xl, yl depends on problem geometry
#xl = 8 #2*xl = number of matrix image elements (points) of a pixel (image plan)
#yl = 4 #2*yl = number of matrix image elements (points) of a pixel (source plan)
xl = 4
yl = 1


transformation = None

if transformType == "identity":
	transformation = IdentityTransformation()

elif transformType == "simple_lens":
	x01 = 0.25
	x02 = 1 
	transformation = SimpleLensTransformation(x01,x02)	
elif transformType == "simple_lens_quadr_pert":
	x01 = 0.25
	x02 = 1 
	gamma = 0.5 #this must be between [0.1 .. 0.7]
	transformation = QuadrPertLensTransformation(x01, x02, gamma) 
elif transformType == "isothermic_sphere":
	x01 = 0.25
	x02 = 1 
	transformation = IsothermicSphereTransformation(x01, x02) 
elif transformType == "isothermic_sphere_quadr_pert":
	x01 = 0.25
	x02 = 1 
	gamma = -0.5 #this must be between [0.1 .. 0.7]
	transformation = QuadrPertSphereTransformation(x01, x02, gamma) 
	

#save image to file
#showImage(transformation.transform(nx, xl, yl, "circles.png"), "Circles", "isoth.png")
#print image on screen
showImage(transformation.transform(nx, xl, yl, "circles.png"), "Circles") 
			
#folderBasename = "imgSimpleLens"
#folderBasename = "imgIsothSph"
#transformation.makeAnim(nx,xl,yl,"circles.png", 1, 0.05, createFolder(folderBasename))

#folderBasename = "imgQuadPertLens"
#folderBasename = "imgQuadPertSphereNegGamma"
#for a range
#transformation.makeAnim(nx,xl,yl,"circles.png", 1, 0.05, 0.1, 0.7, 0.01, createFolder(folderBasename))
#just for one gamma value 0.1 (the step) here can be any value except 0!
#transformation.makeAnim(nx,xl,yl,"circles.png", 1, 0.05, 0.7, 0.701, 0.1, createFolder(folderBasename))
#transformation.makeAnim(nx,xl,yl,"circles.png", 2, 0.05, -0.6, -0.599, 0.1, createFolder(folderBasename))


