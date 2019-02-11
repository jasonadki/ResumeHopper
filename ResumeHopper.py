from tkinter import *

from LoginPage import LoginPage

import PIL.Image
from PIL import Image, ImageTk
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from pdf2image import convert_from_path
import os
from datetime import datetime
import time

class MainWindow():
	def __init__(self, master):



		self.master = master
		self.master.withdraw()
		self.master.title("Resume Hopper")

		self.rootWidth, self.rootHeight = 1000, 700

		self.master.geometry(f"{self.rootWidth}x{self.rootHeight}")
		self.master.resizable(0,0)



		# Greeted With Login Page to grab directories
		self.LP = LoginPage(self.master)
		self.master.wait_window(self.LP.top)
		self.master.deiconify()
		self.pdf_path = self.LP.pdf_path
		self.folder_path = self.LP.folder_path

		# Check to see that both fields from previous screen were entered
		if self.pdf_path == '' or self.folder_path == '':
			self.master.destroy()

		# Save the department folders and position types
		self.departments = [dI for dI in os.listdir(self.folder_path) if os.path.isdir(os.path.join(self.folder_path,dI))]

		self.posType = ['FullTime', 'Internship']


		# Keep track of what page you are viewing
		self.index = 0

		# Set the two Frames. First will be the page display, Second will have the controls
		self.topFrame = Frame(self.master, borderwidth=2, height = self.rootHeight*.9, relief="solid")
		self.bottomFrame = Frame(self.master, borderwidth=2, height = self.rootHeight*.1, relief="solid", bg = '#e24848')

		# Create internal containers for the bottom frame
		self.container1 = Frame(self.bottomFrame, relief="solid", bg = '#e24848')
		self.container2 = Frame(self.bottomFrame, relief="solid", bg = '#e24848')
		self.container3 = Frame(self.bottomFrame, relief="solid", bg = '#e24848')



		# Set the string variables returned from radio buttons
		self.nameVar = StringVar()
		self.nameVar.set('')
		self.depVar = StringVar()
		self.depVar.set(self.departments[0])
		self.posVar = StringVar()
		self.posVar.set(self.posType[0])

		# Covert pdf to list of images
		self.convertedImages = convert_from_path(self.pdf_path)
		self.numberOfPages = len(self.convertedImages)

		# Create lists that will hold the output values
		self.namesResult = ['' for i in range(self.numberOfPages)]
		self.departmentsResult = ['' for i in range(self.numberOfPages)]
		self.typesResult = ['' for i in range(self.numberOfPages)]


		# Grab first image and crop to top 50%
		self.im = self.convertedImages[0]
		self.im = self.im.crop((0, 0, self.im.size[0], self.im.size[1] * .5))

		# Create canvas and set initial image
		self.canvas = Canvas(self.topFrame, borderwidth = 1)
		self.im = self.im.resize((1000, 600))
		self.tk_im = ImageTk.PhotoImage(self.im)
		self.canvas.create_image(0, 0, anchor = "nw", image = self.tk_im)
		self.canvas.configure(bg = 'green')
		self.canvas.pack(expand = True, fill = 'both')

		# Create Name Entry and Submit Button
		self.NameEntry = Entry(self.container1, textvariable = self.nameVar).pack(anchor = 'center')
		self.submitButton = Button(self.bottomFrame, text="Submit", command = self.finish)		



		# Create Department Radio Buttons
		for dep in self.departments:
			self.button = Radiobutton(self.container2, text = dep, variable = self.depVar, value = dep, width = 15, borderwidth = 1).pack()

		# Create position type Radio Buttons
		for t in self.posType:
			self.button = Radiobutton(self.container3, text = t, variable = self.posVar, value = t, width = 15, borderwidth = 1).pack()



		self.leftButton = Button(self.topFrame, anchor = W, command = self.pageLeft)
		self.leftButton.configure(width = 5, height = 20, bg = '#d9dadb',  activebackground = "#33B5E5", relief = FLAT)
		self.button1_window = self.canvas.create_window(5, 200, anchor=W, window=self.leftButton)

		self.rightButton = Button(self.topFrame, anchor = E, command = self.pageRight)
		self.rightButton.configure(width = 5, height = 20, bg = '#d9dadb',  activebackground = "#33B5E5", relief = FLAT)
		self.button2_window = self.canvas.create_window(990, 200, anchor=E, window=self.rightButton)



		self.topFrame.pack(side="top", expand=True, fill="both")
		self.bottomFrame.pack(side="bottom", expand=True, fill="both")
		self.container1.pack(side = 'left', expand = True, fill = 'both')
		self.container2.pack(side = 'left', expand = True, fill = 'both')
		self.container3.pack(side = 'left', expand = True, fill = 'both')




	def finish(self):
		# Need to grab info from the last page
		self.addResumeInfo(self.index)

		fullPdf = PdfFileReader(open(self.pdf_path, "rb"))

		for i in range(fullPdf.numPages):
			if self.departmentsResult[i] != 'None' and self.typesResult[i] != 'None' and self.namesResult[i] != '':

				# Create the file name with path
				fileName = self.folder_path + '/' + self.departmentsResult[i] + '/' + self.typesResult[i] + '/' + self.namesResult[i] +  datetime.today().strftime('%Y%m%d') + '.pdf'

				
				output = PdfFileWriter()
				output.addPage(fullPdf.getPage(i))
				with open(fileName, 'wb') as outputStream:
					output.write(outputStream)

		self.master.destroy()


	def displayResume(self, pageNum):
		self.im = self.convertedImages[pageNum]
		self.im = self.im.crop((0, 0, self.im.size[0], self.im.size[1] * .5))
		self.im = self.im.resize((1000, 600))
		self.tk_im = ImageTk.PhotoImage(self.im)
		self.canvas.create_image(0, 0, anchor = "nw", image = self.tk_im)
		self.topFrame.pack(side="top", expand=True, fill="both")


	def addResumeInfo(self, pageNum):
		self.namesResult[pageNum] = self.nameVar.get()
		self.departmentsResult[pageNum] = self.depVar.get()
		self.typesResult[pageNum] = self.posVar.get()


	def resetEntries(self, pageNum):
		self.nameVar.set(self.namesResult[pageNum])

		if self.departmentsResult[pageNum] == '':
			self.depVar.set(None)
		else:
			self.depVar.set(self.departmentsResult[pageNum])

		if self.typesResult[pageNum] == '':
			self.posVar.set(None)
		else:
			self.posVar.set(self.typesResult[pageNum])


	def checkForLastPage(self, pageNum):
		if pageNum == self.numberOfPages - 1:
			self.canvas.delete(self.button2_window)
			self.submitButton.pack(side = RIGHT)
		else:
			self.button2_window = self.canvas.create_window(990, 200, anchor=E, window=self.rightButton)
			self.submitButton.pack_forget()

	def checkForFirstPage(self, pageNum):
		if pageNum == 0:
			self.canvas.delete(self.button1_window)
		else:
			self.button1_window = self.canvas.create_window(5, 200, anchor=W, window=self.leftButton)



	def pageRight(self):
		self.addResumeInfo(self.index)
		self.index = min(self.numberOfPages - 1, self.index + 1)
		self.displayResume(self.index)
		self.resetEntries(self.index)
		self.checkForFirstPage(self.index)
		self.checkForLastPage(self.index)

	def pageLeft(self):
		self.addResumeInfo(self.index)
		self.index = max(0, self.index - 1)
		self.displayResume(self.index)
		self.resetEntries(self.index)
		self.checkForFirstPage(self.index)
		self.checkForLastPage(self.index)




root = Tk()
my_gui = MainWindow(root)
root.mainloop()


