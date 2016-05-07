from decimal import *
from tkinter import *
from tkinter.ttk import *
import sys
import queue
from PIL import Image, ImageTk

from IterationCalculator import *
from ColorManager import *
from MandelbrotData import *
from DComplex import *

CALC_ABORTED="Stop Calculation"
TK_TERMINATED="Terminate tk"
CALC_FINISHED="Calculation Finished"
INVALID_ENTRY="Invalid Entry"

canvas_width=400
canvas_height=400

class GUI:
	isDead=False
	def __init__(self):
		
		#Tk
		self.root=Tk()
		self.root.title("Mandelbrot Set Plotting")

		#Tk image
		self.image=Image.new('RGB', (canvas_width, canvas_height), (0, 0, 0))
		self.imageTk=ImageTk.PhotoImage(self.image)

		self.pixel=self.image.load()

		#Tk/Canvas
		self.canvas=Canvas(self.root, width=canvas_width, height=canvas_height)
		self.canvas.pack()

		#Tk/PanedWindow
		self.mainFrame=Frame(self.root)
		self.mainFrame.pack()

		#TK/PanedWindow/valueFrame
		self.valueFrame=LabelFrame(self.mainFrame, text="Inputs")
		self.valueFrame.grid(row=1, column=1, sticky=(N,S))

		self.xLabel=Label(self.valueFrame, text="Real coordinate :")
		self.xLabel.grid(row=1, column=1, sticky=(N,E,W,S))

		self.xEntry=Entry(self.valueFrame, width=5, justify=CENTER)
		self.xEntry.insert(INSERT, 0)
		self.xEntry.grid(row=1, column=2, sticky=(N,E,W,S))

		self.yLabel=Label(self.valueFrame, text="Imag coordinate : ")
		self.yLabel.grid(row=2, column=1, sticky=(N,E,W,S))
		self.yEntry=Entry(self.valueFrame, width=5, justify=CENTER)
		self.yEntry.insert(INSERT, 0)
		self.yEntry.grid(row=2, column=2, sticky=(N,E,W,S))

		self.wLabel=Label(self.valueFrame, text="Width Value : ")
		self.wLabel.grid(row=3, column=1, sticky=(N,E,W,S))
		self.wEntry=Entry(self.valueFrame, width=5, justify=CENTER)
		self.wEntry.insert(INSERT, 2)
		self.wEntry.grid(row=3, column=2, sticky=(N,E,W,S))

		self.hLabel=Label(self.valueFrame, text="Height Value : ")
		self.hLabel.grid(row=4, column=1, sticky=(N,E,W,S))
		self.hEntry=Entry(self.valueFrame, width=5, justify=CENTER)
		self.hEntry.insert(INSERT, 2)
		self.hEntry.grid(row=4, column=2, sticky=(N,E,W,S))

		self.itLabel=Label(self.valueFrame, text="Iterations : ")
		self.itLabel.grid(row=5, column=1, sticky=(N,E,W,S))
		self.itEntry=Entry(self.valueFrame, width=5, justify=CENTER)
		self.itEntry.insert(INSERT, 50)
		self.itEntry.grid(row=5, column=2, sticky=(N,E,W,S))

		#Tk/PanedWindow/colorFrame
		self.colorFrame=LabelFrame(self.mainFrame, text="Options")
		self.colorFrame.grid(row=1, column=2, sticky=(N,E,W,S))

		self.spectrum=Canvas(self.colorFrame, width=100, height=20)
		self.colorManager=ColorManager(self.spectrum)

		#I don't know why, but it exactly requires 269 pixels
		self.rLabel = Label(self.colorFrame, text="R")
		self.rLabel.grid(row=1, column=1, sticky=(N,E,W,S))
		self.rScale = Scale(self.colorFrame,
                            orient=HORIZONTAL, length=269, from_=0, to=255,
                            command=self.colorManager.setRValue)
		self.rScale.grid(row=1, column=2, sticky=(N,E,W,S))

		self.gLabel = Label(self.colorFrame, text="G")
		self.gLabel.grid(row=2, column=1, sticky=(N,E,W,S))
		self.gScale = Scale(self.colorFrame,
                            orient=HORIZONTAL, length=269, from_=0, to=255,
                            command=self.colorManager.setGValue)
		self.gScale.grid(row=2, column=2, sticky=(N,E,W,S))

		self.bLabel = Label(self.colorFrame, text="B")
		self.bLabel.grid(row=3, column=1, sticky=(N,E,W,S))
		self.bScale = Scale(self.colorFrame,
                            orient=HORIZONTAL, length=269, from_=0, to=255,
                            command=self.colorManager.setBValue)
		self.bScale.grid(row=3, column=2, sticky=(N,E,W,S))

		self.infoLabel=Label(self.colorFrame, anchor=CENTER, 
			textvariable=self.colorManager.colorData)
		self.infoLabel.grid(row=4, column=1, columnspan=2, sticky=(N,E,W,S))

		self.spectrum.grid(row=5, column=1, columnspan=2)

		self.smoothButtonVar=IntVar()
		self.smoothButton=Checkbutton(self.colorFrame, text="Apply Smoothing",
			variable=self.smoothButtonVar, command=self.checkSmoothButton)
		self.smoothButton.grid(row=6, column=1, columnspan=2, sticky=(N,E,W,S))
		#Tk/PanedWindow/commandFrame

		self.commandFrame=LabelFrame(self.mainFrame, text="Commands")
		self.commandFrame.grid(row=1, column=3, sticky=(N,E,W,S))

		self.generateButton=Button(self.commandFrame, text="Generate", command=self.generateMandelbrot)
		self.generateButton.grid(row=1, column=1, columnspan=2, sticky=(N,E,W,S))
		
		self.abortButton=Button(self.commandFrame, text="Abort", command=self.abortIterCalc, state="disabled")
		self.abortButton.grid(row=2, column=1, columnspan=2, sticky=(N,E,W,S))

		self.exportButton=Button(self.commandFrame, text="Export", command=self.exportMandelbrot, state=DISABLED)
		self.exportButton.grid(row=3, column=1, columnspan=2, sticky=(N,E,W,S))
		
		self.exportFormat=StringVar()
		self.exportAsBMPButton=Radiobutton(self.commandFrame, text="BMP", variable=self.exportFormat, value="BMP", state="disabled")
		self.exportAsBMPButton.grid(row=4, column=1, columnspan=2, sticky=(N,E,W,S))
		self.exportAsPNGButton=Radiobutton(self.commandFrame, text="PNG", variable=self.exportFormat, value="PNG", state="disabled")
		self.exportAsPNGButton.grid(row=5, column=1, columnspan=2, sticky=(N,E,W,S))
		self.exportAsJPGButton=Radiobutton(self.commandFrame, text="JPEG", variable=self.exportFormat, value="JPEG", state="disabled")
		self.exportAsJPGButton.grid(row=6, column=1, columnspan=2, sticky=(N,E,W,S))
		self.exportFormat.set("BMP")

		#tk/Progressbar
		self.progressbarFrame=LabelFrame(self.root, text="Calculation Progress")
		self.progressbar=Progressbar(self.progressbarFrame, orient="horizontal", 
			length=canvas_width, value=0, maximum=canvas_width, mode="determinate")
		self.progressbar.pack()
		self.progressbarFrame.pack()
		
		self.mandelbrot=MandelbrotData(canvas_width, canvas_height)
		self.mandelbrot.initiateArray(canvas_width, canvas_height, Decimal(-1), Decimal(1), Decimal(2)/400, Decimal(2)/400)
		
		self.isMandelbrotDrawn=False
		self.root.protocol("WM_DELETE_WINDOW", self.terminateTk)
		self.root.mainloop()

	def abortIterCalc(self):
		self.checkIterCalc(CALC_ABORTED)

	def terminateTk(self):
		self.checkIterCalc(TK_TERMINATED)

	def checkIterCalc(self, message):
		try:
			self.queue.put(message)
			if message==TK_TERMINATED:
				self.isDead=True
			self.iterCalc.is_alive()
		except AttributeError:
			if message==TK_TERMINATED:
				self.exitProtocol()
		else:
			if message==TK_TERMINATED:
				self.delIterCalc(message)

	def delIterCalc(self, message):
		if self.iterCalc.is_alive():
			self.root.after(50, lambda: self.delIterCalc(message))
		else:
			del self.iterCalc
			self.exitProtocol()

	def exitProtocol(self):
		self.root.destroy()
		sys.exit()
		
	def generateMandelbrot(self):
		self.disableComponents()
		
		self.queue=queue.Queue()
		self.root.after(50, self.checkQueue)
		self.mandelbrot.count=0
		try:
			self.resize()
			self.getNewValue()
		except (InvalidOperation, ValueError, AssertionError):
			self.queue.put(INVALID_ENTRY)
			self.enableComponents()
			return

	def resize(self):
		base_real=0
		base_imag=0
		unit_real=0
		unit_imag=0
		try:
			base_real=Decimal(self.xEntry.get())
		except InvalidOperation:
			self.createErrorTk("Invalid expression on real coordinate or more.")
			raise

		try:
			base_imag=Decimal(self.yEntry.get())
		except InvalidOperation:
			self.createErrorTk("Invalid expression on imaginary coordinate or more.")
			raise

		try:
			unit_real=Decimal(self.wEntry.get())/Decimal(canvas_width)
			assert unit_real>Decimal(0)
		except InvalidOperation:
			self.createErrorTk("Invalid expression on width.")
			raise
		except AssertionError:
			self.createErrorTk("Non-positive value on width.")
			raise

		try:
			unit_imag=Decimal(self.hEntry.get())/Decimal(canvas_height)
			assert unit_real>Decimal(0)
		except InvalidOperation:
			self.createErrorTk("Invalid expression on height.")
			raise
		except AssertionError:
			self.createErrorTk("Non-positive value on height.")
			raise
		
		self.mandelbrot.initiateArray(canvas_width, canvas_height, base_real-canvas_width*unit_real/2, base_imag+canvas_height*unit_imag/2, unit_real, unit_imag)

	def createErrorTk(self, message):
		warningTk=Tk()
		warningTk.title("Error")
		warningLabel=Label(warningTk, text=message)
		warningLabel.pack()

	def getNewValue(self):
		iteration=0
		try:
			iteration=int(self.itEntry.get())
			assert iteration>0
		except (ValueError, InvalidOperation):
			self.createErrorTk("Invalid expression on iteration.")
			raise
		except AssertionError:
			self.createErrorTk("Non-positive value on iteration.")
			raise

		self.iterCalc=IterationCalculator(self.queue, self.mandelbrot, iteration, 
			self.progressbar, canvas_width, canvas_height)

		self.iterCalc.start()

	def checkQueue(self):
		try:
			msg=self.queue.get(0)
			if msg==INVALID_ENTRY:
				return
			if msg==CALC_FINISHED:
				self.draw()
				self.isMandelbrotDrawn=True
			if msg is not TK_TERMINATED:
				self.enableComponents()
				self.progressbar.stop()

		except queue.Empty:
			self.root.after(50, self.checkQueue)

	def draw(self):
		self.recolor()
		self.imageTk=ImageTk.PhotoImage(self.image)
		self.canvas.create_image(0,0,image=self.imageTk, anchor=NW)
		self.root.update();
		self.progressbar["value"]=0
		self.mandelbrot.count=0

	def recolor(self):
		for y in range(canvas_height):
			for x in range(canvas_width):
				self.pixel[x,y]=self.colorManager.getColor(self.mandelbrot.currentMandelbrot[x][y])

	def disableComponents(self):
		self.xEntry.state(["disabled"])
		self.yEntry.state(["disabled"])
		self.wEntry.state(["disabled"])
		self.hEntry.state(["disabled"])
		self.itEntry.state(["disabled"])

		self.rScale.state(["disabled"])
		self.bScale.state(["disabled"])
		self.gScale.state(["disabled"])
		self.smoothButton.state(["disabled"])

		self.generateButton.state(["disabled"])
		self.abortButton.state(["!disabled"])
		self.exportButton.state(["disabled"])
		
		self.exportAsBMPButton.state(["disabled"])
		self.exportAsPNGButton.state(["disabled"])
		self.exportAsJPGButton.state(["disabled"])

	def enableComponents(self):
		self.xEntry.state(["!disabled"])
		self.yEntry.state(["!disabled"])
		self.wEntry.state(["!disabled"])
		self.hEntry.state(["!disabled"])
		self.itEntry.state(["!disabled"])

		self.rScale.state(["!disabled"])
		self.bScale.state(["!disabled"])
		self.gScale.state(["!disabled"])
		self.smoothButton.state(["!disabled"])

		self.generateButton.state(["!disabled"])
		self.abortButton.state(["disabled"])

		if self.isMandelbrotDrawn:
			self.exportButton.state(["!disabled"])
			self.exportAsBMPButton.state(["!disabled"])
			self.exportAsPNGButton.state(["!disabled"])
			self.exportAsJPGButton.state(["!disabled"])
		else:
			self.exportButton.state(["disabled"])
			self.exportAsBMPButton.state(["disabled"])
			self.exportAsPNGButton.state(["disabled"])
			self.exportAsJPGButton.state(["disabled"])

	def exportMandelbrot(self):
		self.image.save("mandelbrot."+self.exportFormat.get())

	def checkSmoothButton(self):
		if self.smoothButtonVar.get()==1:
			self.mandelbrot.applySmoothing=True
		else:
			self.mandelbrot.applySmoothing=False
