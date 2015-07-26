import tkinter as tk # GUI
import field as fld
import sys

# Prevent the user from resizing the window.
tk.Tk().resizable(width=False, height=False)

"""Used to validate the entry fields, which can only contain numeric characters.
Zero length strings are also permitted."""
def validateEntryField(newText) :
	return newText.isdigit() or len(newText)==0

"""This class represents the main application."""
class Application(tk.Frame) :
	def __init__(self, master=None) :
		tk.Frame.__init__(self, master)
		self.master.title("Python - The Travelling Salesman Problem")
		self.build()
		self.grid()
		
	def build(self) :
		# Has the user specified their own dimensions for the field?
		if ( (len(sys.argv) >= 2) and (min(int(sys.argv[1]), int(sys.argv[2])) > 0) ) : # If they have, and if the values are legal...
			self.field = fld.Field(int(sys.argv[1]), int(sys.argv[2])) # ...use those dimensions.
		else : # Otherwise...
			self.field = fld.Field() # ...use the default dimensions.
		# The field (canvas) packs itself  - see field.py
		
		self.validateFunc = self.register(validateEntryField)
		
		
		tk.Label(self,text='Number of cities\n(minimum of 4):',justify=tk.CENTER).grid(row=1,column=0)
		self.nodeCount = tk.StringVar(value=20)
		self.nodeCountEntry = tk.Entry(self,justify=tk.CENTER,textvariable=self.nodeCount,validate='key',validatecommand=(self.validateFunc,'%P'))
		self.nodeCountEntry.grid(row=2,column=0)
		self.genBtn = tk.Button(self, text='Generate', command=self.genClick)
		self.genBtn.grid(row=3, column=0)
		
		tk.Label(self,text='Milliseconds between swaps:\n',justify=tk.CENTER).grid(row=1,column=1)
		self.swapInterval = tk.StringVar(value=100)
		self.swapIntervalEntry = tk.Entry(self,justify=tk.CENTER,textvariable=self.swapInterval,validate='key',validatecommand=(self.validateFunc,'%P'))
		self.swapIntervalEntry.grid(row=2,column=1)
		self.isSwapping = tk.IntVar()
		self.stepBtn = tk.Checkbutton(self, text='Toggle swapping', variable=self.isSwapping)
		self.stepBtn.grid(row=3, column=1)
		
	def genClick(self) :
		self.nodeCount.set(max(int(self.nodeCount.get()), 4)) # Permit a minimum node count of four.
		self.field.generateNodes(int(self.nodeCount.get()) )
			
	def tick(self) :
		if (self.isSwapping.get()) :
			self.isSwapping.set( self.field.randomSwap() ) # If no shorter distance could be found after a number of attempts, disable the swapping automatically. This prevents infinite loops.
		
		interval = self.swapInterval.get()
		if len(interval) > 0 and int(interval) > 0 :
			self.after(int(interval),self.tick)
		else : # If the interval is set to zero or the entry area is empty...
			self.after(1,self.tick) # ...just update once every millisecond.

if __name__ == '__main__' :
	app = Application()
	app.after(100,app.tick) # tick() will continuously invoke itself as part of the main loop.
	app.mainloop()