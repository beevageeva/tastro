import os
from generate_source import *
from transformation import *
from common import createFolder
import numpy as np



#X image , Y source

#transformType = "identity" 
transformType = "simple_lens" 
#transformType = "simple_lens_quadr_pert" 


#nx = 1000 #number of pixels of the image
nx = 200 #number of pixels of the image
#xl, yl depends on problem geometry
#xl = 8 #number of matrix image elements (points) of a pixel (image plan)
#yl = 4 #number of matrix image elements (points) of a pixel (source plan)
xl = 4
yl = 1


transformation = None

if transformType == "identity":
	transformation = IdentityTransformation()

elif transformType == "simple_lens" 
	transformation = SimpleLensTransformation(0,0)	
elif transformType == "simple_lens_quadr_pert":
	transformation = QuadPertLensTransformation(0,0,0.1) 


def transform(sourceImg):
	sourceData = readImage(sourceImg)
	ny = sourceData.shape[0]
	
	#print("imageFile=%s, ny = %d" % (sourceImg, ny))

	xs = 2.0 * xl / nx 
	ys = 2.0 * yl / ny 

	imageData = np.zeros((nx, nx))
	for i in range(0, nx):
		for j in range(0, nx):
			#pixel -> coordinates in image
			x1 = -float(xl) + i * xs
			x2 = -float(xl) + j * xs
			#identity x1->y1 , x2->y2
			sourcePixel = transformation.getSourcePixel(x1, x2)
			y1 = sourcePixel[0]
			y2 = sourcePixel[1]
			#find corresponding points in image space
			i1 = int((y1+yl)/ys)
			i2 = int((y2+yl)/ys) 
			if (i1>=0 and i1<=ny-1) and (i2>=0 and i2<=ny-1):
				imageData[i][j] = sourceData[i1][i2] 
	return imageData		
			



def makeSimpleLensAnim(outFolderBase, endPoint):
	#x01 = 0
	#x02 = 1
	#saveImage(transform("circles.png"), "circles-transformed")
	#saveImage(transform("rect.png"), "rect-transformed")
	#saveImage(transform("circle.png"), "circle-transformed")
	
	
	outDir = createFolder(outFolderBase)
	#outDir2 = createFolder("imgSimpleLensBN")
	
	
	flen = len("%d" % (endPoint * endPoint * 100))
	print("FLEN %d " % flen)
	for x01 in np.arange(0, endPoint, 0.05):
		for x02 in np.arange(0, endPoint, 0.05):
			title = "x01=%1.2f, x02=%1.2f" %(x01, x02)
			print(title)	
			imgname = "%d" % ((x01 * nx + x02) * 100)
			for i in range(0, flen - len(imgname)):
				imgname = "0" + imgname
			A = transform("circles.png")
			showImage(A, title, os.path.join(outDir, imgname))
			#saveImage(A, os.path.join(outDir2, imgname))
	
def makeQuadrPertAnim(imgFolderBase, endPoint):
	x01 = 0
	x02 = 1
	gamma = 0.1
	showImage(transform("circles.png"))
	


#makeSimpleLensAnim("imgSimpleLens", 1)
makeQuadrPertAnim("imgQuadPert", 1)

