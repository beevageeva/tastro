from generate_source import *

#showImage(rect(10.0, 100.0))
#showImage(circle(30.0, 100.0))
saveImage(rect(10.0, 100.0), "rect")
saveImage(circle(30.0, 100.0), "circle")
#showImage(circles([10.0,20.0,30.0,50.0], 100.0))
A = circles([2.5,5,7.5,10.0], 25.0)
#print("from source generation")
#print(A)
saveImage(A, "circles")
#print("reading saved image")
#B = readImage("circles.png")
#print("from png")
#print(B)
#showImage(B)
