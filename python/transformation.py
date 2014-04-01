class IdentityTransformation:
	
	def getSourcePixel(self, x1, x2):
		return [x1, x2]
		
def getSourcePixelSimple(x01, x02, x1, x2):
	#print("x01 = %E, x02 = %E" % (x01, x02))
	if x1 == x01 and x2 == x02:
		d = 0.0000001 #la chapuza
	else:
		d = (x1 - x01)**2 + (x2 - x02)**2
	#print("x1=%E,x2=%E,d=%E" % (x1,x2,d))
	y1 = x1 - (x1 - x01)/d
	y2 = x2 - (x2 - x02)/d
	return [y1, y2]


class SimpleLensTransformation:
	
	def __init__(x01, x02):
		self.x01 = x01
		self.x02 = x02

	
	def getSourcePixel(x1, x2):
		return getSourcePixelSimple(self.x01, self.x02, x1, x2)


class QuadrPertLensTransformation:
	
	def __init__(x01, x02, gamma):
		self.x01 = x01
		self.x02 = x02
		self.gamma = gamma

	
	def getSourcePixel(x1, x2):
		sres =  getSourcePixelSimple(self.x01, self.x02, x1, x2)
		return [(1.0 - gamma ) * sres[0], (1.0 + gamma) * sres[1]]

		
