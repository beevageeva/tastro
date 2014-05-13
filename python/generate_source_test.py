from generate_source import *



def generateImage(shapeType, saveToFile=True):
	if shapeType == "circle":
		A = circle(30.0, 100.0)
	elif shapeType == "circles":
		A = circles([5.0,10.0,20.0,25.0], 100.0)
	elif shapeType == "rect":
		A = rect(10.0, 100.0)
	if saveToFile:
		saveImage(A, shapeType)
		#this saves the matplot figure
		#showImage(A, shapeType, shapeType + ".png")
	else:
		showImage(A, shapeType)



def testSaveImages():
	A = circles([5,10,20,25.0], 100.0)
	print("from source generation")
	print(A)
	saveImage(A, "test-circles")
	print("reading saved image")
	B = readImage("test-circles.png")
	print("from png")
	print(B)
	showImage(B)


generateImage("circles")
showImage(readImage("circles.png"))
