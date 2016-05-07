from DComplex import *

class MandelbrotData:
	applySmoothing=False

	def __init__(self, width, height):
		self.initiateArray(width, height, 0, 0, 0, 0)
		self.count=0

	def initiateArray(self, width, height, base_real, base_imag, unit_real, unit_imag):
		self.currentComplex=[[DComplex(0,0) for x in range(width)] for y in range(height)]
		self.currentBaseComplex=[[DComplex(base_real+unit_real*x, base_imag-unit_imag*y) for y in range(width)] for x in range(height)]
		self.currentMandelbrot=[[-1 for x in range(width)] for y in range(height)]

	def performMandelbrot(self, x, y):
		z=self.currentComplex[x][y]
		z=z*z+self.currentBaseComplex[x][y]
		self.currentComplex[x][y]=z

	def isMandelbrot(self, x, y):
		if self.applySmoothing:
			return self.currentComplex[x][y].sq()>=Decimal(2**4)
		else:
			return self.currentComplex[x][y].sq()>=Decimal(4)

	
