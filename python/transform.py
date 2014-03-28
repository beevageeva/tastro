from generate_source import *


#X image , Y source

transformType = "simple_lens"


#nx = 1000 #number of pixels of the image
nx = 200 #number of pixels of the image
#xl, yl depends on problem geometry
#xl = 8 #number of matrix image elements (points) of a pixel (image plan)
#yl = 4 #number of matrix image elements (points) of a pixel (source plan)
xl = 1
yl = 1


if transformType == "identity":

	def getSourcePixel(x1, x2):
		return [x1, x2]

elif transformType == "simple_lens":
	x01= 0.0
	x02 = 0.25
	def getSourcePixel(x1, x2):
		if x1 == x01 and x2 == x02:
			d = 0.0000001 #la chapuza
		else:
			d = (x1 - x01)**2 + (x2 - x02)**2
		#print("x1=%E,x2=%E,d=%E" % (x1,x2,d))
		y1 = x1 - (x1 - x01)/d
		y2 = x2 - (x2 - x02)/d
		return [y1, y2]
		


def transform(sourceImg):
	sourceData = readImage(sourceImg)
	ny = sourceData.shape[0]
	
	print("imageFile=%s, ny = %d" % (sourceImg, ny))

	xs = 2.0 * xl / nx 
	ys = 2.0 * yl / ny 

	imageData = np.zeros((nx, nx))
	for i in range(0, nx):
		for j in range(0, nx):
			#pixel -> coordinates in image
			x1 = -float(xl) + i * xs
			x2 = -float(xl) + j * xs
			#identity x1->y1 , x2->y2
			sourcePixel = getSourcePixel(x1, x2)
			y1 = sourcePixel[0]
			y2 = sourcePixel[1]
			#find corresponding points in image space
			i1 = int((y1+yl)/ys)
			i2 = int((y2+yl)/ys) 
			if (i1>=0 and i1<=ny-1) and (i2>=0 and i2<=ny-1):
				imageData[i][j] = sourceData[i1][i2] 
	return imageData		
			

saveImage(transform("circles.png"), "circles-transformed")
saveImage(transform("rect.png"), "rect-transformed")
saveImage(transform("circle.png"), "circle-transformed")


