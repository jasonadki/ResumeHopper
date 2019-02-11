from tkinter import filedialog, Toplevel, Button, StringVar, Label

class LoginPage():
	def __init__(self, master):
		self.top = Toplevel(master)
		self.top.geometry("500x100")
		self.top.resizable(0,0)

		self.pdf_path = ''
		self.pdf_text = StringVar()
		self.pdf_text.set(self.pdf_path)

		self.folder_path = ''
		self.folder_text = StringVar()
		self.folder_text.set(self.folder_path)

		self.status = ''
		self.status_text = StringVar()
		self.status_text.set(self.status)




		self.select_resume_button = Button(self.top, text = 'Select Resume Stack', command = self.load_file)
		self.select_folder_button = Button(self.top, text = 'Select Folder Location', command = self.load_directory)
		self.submit_button = Button(self.top, text = 'Submit', command = self.submit)
		self.pdf_label = Label(self.top, textvariable=self.pdf_text, width = 40, borderwidth=2, relief="solid")
		self.folder_label = Label(self.top, textvariable=self.folder_text, width = 40, borderwidth=2, relief="solid")
		self.status_label = Label(self.top, textvariable=self.status_text, fg = 'red')

		self.select_resume_button.grid(row = 0, column = 0, columnspan = 3)
		self.select_folder_button.grid(row = 1, column = 0, columnspan = 3)
		self.submit_button.grid(row = 2, column = 0, columnspan = 3)
		self.pdf_label.grid(row = 0, column = 5, columnspan = 3)
		self.folder_label.grid(row = 1, column = 5, columnspan = 3)
		self.status_label.grid(row = 3, column = 0, columnspan = 3)



	def load_file(self):
		self.pdf_path = filedialog.askopenfilename(filetypes = [("Pdf files", "*.pdf")])
		self.pdf_text.set(self.pdf_path)

	def load_directory(self):
		self.folder_path = filedialog.askdirectory()
		self.folder_text.set(self.folder_path)

	def submit(self):
		# Check to see that both fields have been filed out
		if self.pdf_path == '' or self.folder_path == '':
			self.status_text.set('Incomplete Field!')
		else:
			self.top.destroy()