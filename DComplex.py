from decimal import Decimal

class DComplex:
	def __init__(self, real, imag):
		#the type of real and imag are Decimal
		self.real=Decimal(real)
		self.imag=Decimal(imag)

	def __add__(self, dcomp): #overrides + operator
		n_real=self.real+dcomp.real
		n_imag=self.imag+dcomp.imag
		return DComplex(n_real, n_imag)

	def __mul__(self, dcomp): #overrides * operator
		n_real=self.real*dcomp.real-self.imag*dcomp.imag
		n_imag=self.real*dcomp.imag+self.imag*dcomp.real
		return DComplex(n_real, n_imag)

	def sq(self): 
		return self.real*self.real+self.imag*self.imag

	def __str__(self):
		return "({0},{1})".format(self.real, self.imag)

	def ln(self):
		return self.sq().ln()/2
