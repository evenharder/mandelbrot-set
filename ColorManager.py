from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from decimal import Decimal

def innerPoint(x,y,a,b):
	return (b*x+a*y)/(a+b)

class ColorManager:
	def __init__(self, canvas):
		self.r=0
		self.g=0
		self.b=0
		self.t1=63
		self.t2=127
		self.canvas=canvas
		self.hperiod=1
		self.colorData=StringVar()
		self.updateColorData()

	def setRValue(self, val):
		self.r=int(float(val))
		self.updateColorData()

	def setGValue(self, val):
		self.g=int(float(val))
		self.updateColorData()

	def setBValue(self, val):
		self.b=int(float(val))
		self.updateColorData()

	def updateColorData(self):
		msg=""
		msg+="R : "+str(self.r)+" / "
		msg+="G : "+str(self.g)+" / "
		msg+="B : "+str(self.b)
		self.colorData.set(msg)
		self.repaint()

	def repaint(self):
		self.canvas.delete()
		self.spectrumImage=Image.new('RGB', (100, 20), (0,0,0))
		self.spectrumPixel=self.spectrumImage.load()

		for x in range(100):
			for y in range(20):
				self.spectrumPixel[x,y]=self.getColor(x/25.0*self.hperiod)

		self.imageTk=ImageTk.PhotoImage(self.spectrumImage)
		self.canvas.create_image(0,0,image=self.imageTk, anchor=NW)

	def getColor(self, it):
		hperiod=self.hperiod
		dperiod=4*hperiod
		r=0
		g=0
		b=0
		it=Decimal(it)%dperiod
		it_=Decimal(it)%hperiod
		if it<Decimal(hperiod):
			r=innerPoint(255,Decimal(self.r),it_,hperiod-it_)
			g=innerPoint(255,Decimal(self.g),it_,hperiod-it_)
			b=innerPoint(255,Decimal(self.b),it_,hperiod-it_)
		elif it<Decimal(2*hperiod):
			r=innerPoint(Decimal(self.r),0,it_,hperiod-it_)
			g=innerPoint(Decimal(self.g),0,it_,hperiod-it_)
			b=innerPoint(Decimal(self.b),0,it_,hperiod-it_)
		elif it<Decimal(3*hperiod):
			r=innerPoint(0,255-Decimal(self.r),it_,hperiod-it_)
			g=innerPoint(0,255-Decimal(self.g),it_,hperiod-it_)
			b=innerPoint(0,255-Decimal(self.b),it_,hperiod-it_)
		else:
			r=innerPoint(255-Decimal(self.r),255,it_,hperiod-it_)
			g=innerPoint(255-Decimal(self.g),255,it_,hperiod-it_)
			b=innerPoint(255-Decimal(self.b),255,it_,hperiod-it_)
		return (int(r),int(g),int(b))