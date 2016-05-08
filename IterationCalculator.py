from threading import Thread
import queue
from decimal import Decimal

CALC_ABORTED="Stop Calculation"
TK_TERMINATED="Terminate tk"
CALC_FINISHED="Calculation Finished"
INVALID_ENTRY="Invalid Entry"

class IterationCalculator(Thread):

	d_ln_2=Decimal(2).ln()
	max_nu=0
	def __init__(self, queue, mandelbrot, iteration, progressbar, w, h):
		Thread.__init__(self)
		self.queue=queue
		self.m=mandelbrot
		self.iteration=iteration
		self.progressbar=progressbar
		self.countLimit=w
		self.rangeLimit=h

	def smoothing(self, x, y, it):
		if it<self.iteration:
			log_zn=self.m.currentComplex[x][y].sq().ln()/2
			nu=((log_zn/(2*self.d_ln_2)).ln()/self.d_ln_2)
			self.m.currentMandelbrot[x][y] += (-nu)
			self.max_nu=max(self.max_nu, nu)
		pass
	
	def run(self):
		self.max_nu=0
		while self.m.count<self.countLimit:
			if self.m.count<self.countLimit:
				for y in range(self.rangeLimit):
					x=self.m.count

					for i in range(self.iteration):
						if not self.queue.empty():
							break
						if self.m.currentMandelbrot[x][y]<=-1:
							if self.m.isMandelbrot(x,y):
								self.m.currentMandelbrot[x][y]=i
								if self.m.applySmoothing:
									self.smoothing(x,y,i)
								break
							self.m.performMandelbrot(x,y)

				if not self.queue.empty():
					break
				self.m.count+=1
				print(self.m.count)
				self.progressbar["value"]=self.m.count
				#self.progressbar["text"]=str(self.m.count*100//self.rangeLimit)+"%"
			else:
				break

		if not self.queue.empty():
			return
		self.queue.put_nowait(CALC_FINISHED)
		print(str(self.max_nu))