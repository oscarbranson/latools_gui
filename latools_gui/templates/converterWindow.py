from PyQt5.QtWidgets import *
import dateutil.parser as dparser
import os
import sys
import json

class ConverterWindow(QWidget):
	""" A popup window, accessed via the import stage, that attempts to convert the user's data into a format
		that can use the DEFAULT configuration.
	"""

	def __init__(self):
		""" Creates the popup window """

		QWidget.__init__(self)
		self.setWindowTitle("Convert data files for import")

		# The parser that is currently running
		self.parser = None

		# A value to record where in the data the converter expects to find the date, based on previous file in the folder
		self.expectedDateLine = None

		# If we're running an integration test, we need to prevent the program from asking for date confirmation
		self.runningTest = False

		# We use a grid layout
		self.mainGrid = QGridLayout(self)

		# We import the section information from a json file
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), 'information/converterInfo.json')
			infoFile = infoFile.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			infoFile = "information/converterInfo.json"

		with open(infoFile, "r") as read_file:
			self.stageInfo = json.load(read_file)
			read_file.close()

		# We make an introduction textbox
		self.intro_text = QTextEdit()
		self.intro_text.setMinimumWidth(660)
		self.intro_text.setFixedHeight(80)
		self.intro_text.setText(self.stageInfo["main_info"])
		self.intro_text.setReadOnly(True)

		self.mainGrid.addWidget(self.intro_text, 0, 0, 1, 4)

		# A type option for choosing between running on a file or a directory
		self.type_label = QLabel("Run conversion on a")
		self.mainGrid.addWidget(self.type_label, 1, 0)

		self.type_combo = QComboBox()
		self.type_combo.activated.connect(self.changed_type)
		self.mainGrid.addWidget(self.type_combo, 1, 1, 1, 2)

		self.type_combo.addItem("file")
		self.type_combo.addItem("folder of files")

		# An option for finding the file to convert
		self.findDataButton = QPushButton(self.stageInfo["find_data_label"])
		self.findDataButton.clicked.connect(self.findDataButtonClicked)
		self.mainGrid.addWidget(self.findDataButton, 2, 0)
		self.findDataButton.setToolTip(self.stageInfo["find_data_description"])

		self.fileLocationLine = QLineEdit()
		self.mainGrid.addWidget(self.fileLocationLine, 2, 1, 1, 3)
		self.fileLocationLine.setReadOnly(True)
		self.fileLocationLine.setToolTip(self.stageInfo["find_data_description"])

		# An option for finding the folder of files to convert
		self.findDirectoryButton = QPushButton(self.stageInfo["find_directory_label"])
		self.findDirectoryButton.clicked.connect(self.findDirectoryButtonClicked)
		self.findDirectoryButton.setToolTip(self.stageInfo["find_directory_description"])

		self.directoryLocationLine = QLineEdit()
		self.directoryLocationLine.setReadOnly(True)
		self.directoryLocationLine.setToolTip(self.stageInfo["find_directory_description"])

		# An option for the converted file's location
		self.exportLocationButton = QPushButton(self.stageInfo["location_label"])
		self.exportLocationButton.clicked.connect(self.exportLocationButtonClicked)
		self.mainGrid.addWidget(self.exportLocationButton, 3, 0)
		self.exportLocationButton.setToolTip(self.stageInfo["location_description"])

		self.exportLocationLine = QLineEdit()
		self.mainGrid.addWidget(self.exportLocationLine, 3, 1, 1, 3)
		self.exportLocationLine.setReadOnly(True)
		self.exportLocationLine.setToolTip(self.stageInfo["location_description"])

		# An option to name the converted file
		self.nameLabel = QLabel("New file name")
		self.mainGrid.addWidget(self.nameLabel, 4, 0)

		self.nameEdit = QLineEdit()
		self.mainGrid.addWidget(self.nameEdit, 4, 1)

		self.nameCSV = QLabel(".csv")
		self.mainGrid.addWidget(self.nameCSV, 4, 2)

		# A button to run the converter
		self.runButton = QPushButton("Convert")
		self.mainGrid.addWidget(self.runButton, 4, 3)
		self.runButton.clicked.connect(self.runConverter)

		# A space to display converter questions
		self.status_text = QTextEdit()
		self.status_text.setFixedHeight(100)
		self.status_text.setReadOnly(True)

		self.mainGrid.addWidget(self.status_text, 5, 0, 1, 4)

		# A checkbox to infer the date from other processed files
		self.infer_date_checkbox = QCheckBox(self.stageInfo["date_label"])
		self.infer_date_checkbox.setToolTip(self.stageInfo["date_description"])
		self.mainGrid.addWidget(self.infer_date_checkbox, 6, 0, 1, 2)
		self.infer_date_checkbox.setEnabled(False)
		self.infer_date_checkbox.setChecked(True)


		# A Yes button to respond to the display text
		# self.yesButton = QPushButton("Yes")
		# self.mainGrid.addWidget(self.yesButton, 6, 3)
		# self.yesButton.clicked.connect(self.yesClicked)
		# self.yesButton.setEnabled(False)

		# A No button to respond to the display text
		# self.noButton = QPushButton("No")
		# self.mainGrid.addWidget(self.noButton, 6, 2)
		# self.noButton.clicked.connect(self.noClicked)
		# self.noButton.setEnabled(False)


	def findDataButtonClicked(self):
		""" Opens a dialog to save a file path to the file location text box """
		loadLocation = QFileDialog.getOpenFileName(self, 'Open file', '/home')
		if loadLocation[0] != '':
			self.fileLocationLine.setText(loadLocation[0])

	def exportLocationButtonClicked(self):
		""" Opens a dialog to save a directory path to the export location text box """
		self.fileLocation = QFileDialog.getExistingDirectory(self, 'Open file', '/home')
		if self.fileLocation != "":
			self.exportLocationLine.setText(self.fileLocation)

	def runConverter(self):
		""" Begins the conversion process """

		# If the file location line is empty we throw an error
		if self.fileLocationLine.text() == "" and self.type_combo.currentText() == "file":
			self.raiseError(
				"You must select a data file to convert")
			return

		# If the file location line is empty we throw an error
		if self.directoryLocationLine.text() == "" and self.type_combo.currentText() != "file":
			self.raiseError(
				"You must select a directory of files to convert")
			return

		# If the export location line is empty we throw an error
		if self.exportLocationLine.text() == "":
			self.raiseError(
				"You must select a directory to export the converted file to.")
			return

		# If the new name line is empty we throw an error
		if self.nameEdit.text() == "" and self.type_combo.currentText() == "file":
			self.raiseError(
				"You must provide a name for the new file.")
			return

		# If we're operating on a file rather than a folder:
		if self.type_combo.currentText() == "file":

			# We check the last characters of the import file to see if it's a csv:
			if self.fileLocationLine.text()[-4:] == ".csv":

				# We run the csv parser
				self.run_csv(self.fileLocationLine.text())

			# If the last characters are txt
			elif self.fileLocationLine.text()[-4:] == ".txt":

				# We run the txt parser, which saves a new csv called latools_temp_data.csv"
				self.run_txt()

			# If the input file is not a csv or txt we don't handle it for now.
			else:
				self.raiseError(
					"Currently only csv and txt files are supported.")
				return
		else:
			# We are now running on a folder of files

			# We attempt to load the input data folder
			try:

				inFile = self.directoryLocationLine.text()

				# We import the stage information from a json file and set the default data folder
				if getattr(sys, 'frozen', False):
					# If the program is running as a bundle, then get the relative directory
					infoFile = os.path.join(os.path.dirname(sys.executable), inFile)
					infoFile = infoFile.replace('\\', '/')

				else:
					# Otherwise the program is running in a normal python environment
					infoFile = inFile

				# File_list is a list of all files found in the given folder
				file_list = os.listdir(inFile)

			except:
				self.converterWindow.raiseError("Unable to open " + self.directoryLocationLine.text())
				return

			for file in file_list:

				# We check each file in the folder and run the converter if it is a .csv or .txt

				if file[-4:] == ".csv":

					# We set simply input the file name and location into the converter option fields as though
					# they were set manually to run on a single file
					self.fileLocationLine.setText(os.path.join(inFile, file))
					self.nameEdit.setText(file[:-4])

					self.run_csv(self.fileLocationLine.text())

					# We set the name and location fields back to blank
					self.nameEdit.setText("")
					self.fileLocationLine.setText("")

				elif file[-4:] == ".txt":
					self.fileLocationLine.setText(os.path.join(inFile, file))
					self.nameEdit.setText(file[:-4])
					self.run_txt()
					self.nameEdit.setText("")
					self.fileLocationLine.setText("")

		# We remove info about where the converter expects to find the date line so that it can be reinitialised
		self.expectedDateLine = None


	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self, "Error", message, QMessageBox.Ok)

	def yesClicked(self):
		""" When the user is asked a question this button can be used to respond. """
		self.questionResult = "Yes"
		# We disable the input buttons
		self.yesButton.setEnabled(False)
		self.noButton.setEnabled(False)
		# We tell the parser to continue
		self.parser.run()

	def noClicked(self):
		""" When the user is asked a question this button can be used to respond. """
		self.questionResult = "No"
		# We disable the input buttons
		self.yesButton.setEnabled(False)
		self.noButton.setEnabled(False)
		# We tell the parser to continue
		self.parser.run()

	def changed_type(self):
		""" Toggles between running on a file or a folder of files. """

		if self.type_combo.currentText() == "file":
			# If running on a file, it hides the folder options and displays the file options
			self.nameEdit.setEnabled(True)
			self.nameLabel.setEnabled(True)
			self.infer_date_checkbox.setEnabled(False)
			self.findDirectoryButton.setParent(None)
			self.directoryLocationLine.setParent(None)
			self.mainGrid.addWidget(self.findDataButton, 2, 0)
			self.mainGrid.addWidget(self.fileLocationLine, 2, 1, 1, 3)

		else:
			# Otherwise it hides the file options and displays the folder options
			self.nameEdit.setEnabled(False)
			self.nameLabel.setEnabled(False)
			self.infer_date_checkbox.setEnabled(True)
			self.findDataButton.setParent(None)
			self.fileLocationLine.setParent(None)
			self.mainGrid.addWidget(self.findDirectoryButton, 2, 0)
			self.mainGrid.addWidget(self.directoryLocationLine, 2, 1, 1, 3)

	def findDirectoryButtonClicked(self):
		""" Opens a file dialog to find a file directory for data import when a button is pressed. """

		fileLocation = QFileDialog.getExistingDirectory(self, 'Open file', '/home')
		if fileLocation != "":
			self.directoryLocationLine.setText(fileLocation)

	def run_csv(self, input):
		""" Runs the converter on a csv file """
		self.parser = Parser_csv(self,
								 input,
								 self.exportLocationLine.text(),
								 self.nameEdit.text())

	def run_txt(self):
		""" runs the converter on a txt file """
		self.parser_txt = Parser_txt(self,
									 self.fileLocationLine.text(),
									 self.exportLocationLine.text(),
									 self.nameEdit.text())

		# For converting a txt file, we first convert the txt to a csv, then run the csv parser on that.
		self.run_csv(self.parser_txt.outPath)
		# We remove the temporary csv file that we made
		os.remove(self.parser_txt.outPath)

class Parser_csv:
	"""
	A parser that searches through a user's data file, looking for indications of data fields that latools
	works with. It asks the user for some input, then saves the data into a format that can use the DEFAULT
	configuration.
	"""
	def __init__(self, converterWindow, inFile, outLocation, outName):
		"""
		Parameters
		----------
		converterWindow : ConverterWindow
			A reference to the window running the show, so that responses to questions can be gathered.
		inFile : str
			The filepath of the data file to process
		outLocation : str
			The directory to save the converted file to
		outName : str
			The name of the converted file
		"""

		self.converterWindow = converterWindow

		# Determines if we are currently in the middle of questioning the user about the date
		self.dateQuestioning = False

		# Keeps track of which date option the user is currently being questioned about
		self.dateQuestionIndex = 0

		self.inFile = inFile
		self.outLocation = outLocation
		self.outName = outName

		# We attempt to load the input data file
		try:

			# We import the stage information from a json file and set the default data folder
			if getattr(sys, 'frozen', False):
				# If the program is running as a bundle, then get the relative directory
				infoFile = os.path.join(os.path.dirname(sys.executable), inFile)
				infoFile = infoFile.replace('\\', '/')

			else:
				# Otherwise the program is running in a normal python environment
				infoFile = inFile

			with open(infoFile, "r") as file:
				self.lines = file.read().splitlines()
				file.close()

		except:
			self.converterWindow.raiseError("Unable to open " + inFile)
			return

		# Pre-processing of the lines. Currently this just removes trailing commas
		# ** Could also get it to remove empty cells if that is useful **
		self.clean_lines()

		# We want to find the correct column count for this data to us in parsing things later
		self.col_count = self.get_column_count()

		# Lines that we determine are the actual ablation data (numbers)
		self.table_rows = []

		# Lines that are not ablation data numbers
		self.other_rows = []

		# A list of possible dates to question the user about
		self.possible_dates = []

		# We run a parser to put each row of the file into table_rows or other_rows
		self.get_table_rows()

		# We run a process that finds possible dates in other_rows
		self.get_date()

		# The user is then asked to confirm the date and time
		self.date = self.confirm_date()

		# We use a parser to find the header row
		self.header_row = self.get_header_row()

		# We fix the analyte names so that they are in the form of letters then numbers (Al27 instead of 27Al)
		self.fix_analyte_names()

		# The list of lines that will be exported
		self.out_lines = []

		# We format the lines for export, then export the new file
		self.create_formatted()
		self.output()

		# A success message is displayed in the window's status box.
		self.converterWindow.status_text.setText(
			"Data conversion completed successfully. <br> The converted file has been saved in: " +
			self.outLocation + "<br>Please check that the date and time text is accurate.")

	def get_column_count(self):
		"""
		We run a parser to find the number of columns in the ablation data.
		This is based on finding a certain number of rows with a consistent number of columns.
		** This function could be changed to finding the column count of all rows and then taking the mode of the
		result, if that is more consistent. **
		"""

		# The number of consecutive rows with the same column count before we confirm that to be the
		# column count for that file.
		COUNT_THRESHOLD = 10

		# How many consecutive consistent column numbers we are currently on
		count = 0
		cols = 0

		for row in self.lines:

			# We split the row into csv cells
			splits = row.split(",")

			# We're looking for a table with more than two columns
			if len(splits) > 2:

				# If this col count was different to the last:
				if count == 0:
					# Set the new column count
					cols = len(splits)
					# We now have 1 consistent consecutive column
					count += 1
					continue

			# If this row's column count is the same as last row's
			if count != 0:
				if len(splits) > 2 and cols == len(splits):
					count += 1
				else:
					count = 0

			# If we have a number of consecutive rows with the same col count (> 2) we return this.
			if count > COUNT_THRESHOLD:
				return cols

		# Otherwise there was a problem and we return 0
		return 0

	def get_table_rows(self):
		""" We divide the file's lines up into table rows or other rows.
			Currently the criteria for this is that the row has a number of cells that is the same as
			the column count that was determined above, and that each cell has a number in it.
		"""
		for row in self.lines:

			# We split the line up into csv cells
			split = row.split(",")
			table_row = False

			# If the line has the correct number of columns
			if len(split) == self.col_count:

				table_row = True

				# We try to convert each cell to a float. Any failures result in the row not being considered a
				# data row
				for value in split:
					try:
						float(value)
					except:
						table_row = False
						break

			# The line is either put into the table or other.
			if table_row:
				self.table_rows.append(row)
			else:
				self.other_rows.append(row)

	def get_date(self):
		""" We run a fuzzy date finder over all non-table rows.
			It has a tendency to find extra dates, so we put them all in a list and ask the user to confirm
			the correct one.
		"""
		for row in self.other_rows:
			try:
				date = dparser.parse(row, fuzzy=True)
				# If the date makes some amount of sense we add it to the possible dates list
				if date.year > 1950 and date.year < 2100:
					self.possible_dates.append(date)
			except:
				pass

	def get_header_row(self):
		""" To find the header row we look for a row with the right column count, and where each cell except for
			the first one (typically Time) has an appropriate length for an analyte string, and either begins or
			ends with a digit.
		"""
		for row in self.other_rows:

			# We split the row up into csv cells
			splits = row.split(",")

			# If the row has the appropriate columns count
			if len(splits) == self.col_count:
				header = True

				# We check each cell except for the first one which will generally be "time" in some format
				for value in splits[1:]:

					# We define an appropriate string length for an analyte as between 2 and 5 characters
					if len(value) > 1 and len(value) < 6:

						# If either the first or last character is a digit, we consider this value a potential
						# analyte name.
						try:
							int(value[-1])
						except:
							try:
								int(value[0])
							except:
								header = False
								break
					else:
						header = False
						break

				# If every cell (except the first one) passes the analyte test, we consider that row the header
				if header:
					return row

		# Otherwise we didn't find a header and return an empty string
		return ""

	def format_date(self, date):
		""" Formats the datetime object into the string value that the DEFAULT configuration looks for. """
		return date.strftime('%b %d %Y  %I:%M:%S ') + date.strftime('%p').lower()

	def get_date_line(self, date):
		""" Writes out the date line that the DEFAULT configuration is used to dealing with. """
		dateLine = self.format_date(date)
		return "Acquired      : " + dateLine + " using AcqMethod OB102915.m"

	def clean_lines(self):
		""" Pre-processing of the input file lines """

		for i in range(len(self.lines)):

			# Currently we just remove trailing commas
			if len(self.lines[i]) > 0 and self.lines[i][-1] == ",":
				self.lines[i] = self.lines[i][0:-1]

	def confirm_date(self):
		""" Displays a question about the date in the window's status textbox, and enables the yes/no buttons """

		# If we're running integration tests, we don't ask for the user to confirmt the date
		if self.converterWindow.runningTest:
			return self.possible_dates[0]

		# If we are infering the date, we check if we have a previous value
		if self.converterWindow.expectedDateLine is not None and self.converterWindow.infer_date_checkbox.isChecked():

			expected_length = self.converterWindow.expectedDateLine[0]
			expected_value = self.converterWindow.expectedDateLine[1]

			# If the length of the list of potential dates in the original is the same as this file,
			# we use that as confirmation to go ahead and use the date index from the first file.
			if expected_length == len(self.possible_dates):
				return self.possible_dates[expected_value]

		while True:
			# We ask the user about each potential date that was found by the fuzzy-matcher
			reply = QMessageBox.question(self.converterWindow, 'Message',
										 str(len(self.possible_dates)) + " possible date(s) found<br>" +
										 "in file: " + self.outName + "<br>"
										"Checking date option number: " + str(self.dateQuestionIndex + 1) +
										"<br>Is the date in the data file: <br>" +
										 self.format_date(self.possible_dates[self.dateQuestionIndex]) + " ?",
										 QMessageBox.Yes | QMessageBox.No,
										 QMessageBox.Yes)

			if reply == QMessageBox.No:
				# If they say no we ask about the next one
				self.dateQuestionIndex += 1
			else:
				# If they say yes we save that date as correct
				self.converterWindow.expectedDateLine = (len(self.possible_dates), self.dateQuestionIndex)
				return self.possible_dates[self.dateQuestionIndex]

	def fix_analyte_names(self):
		""" We put analyte names in the header line into "Al27" format """

		new_header = ""
		begin_col = 1
		# We split the row into csv cells
		splits = self.header_row.split(",")

		# On the off chance that the first column is not Time, we check if it is an analyte name.
		# This is based on a length of 2-5 characters with either the first or last a digit.
		if len(splits[0]) > 1 and len(splits[0]) < 6 and (splits[0][0].isdigit() or splits[0][-1].isdigit()):
			begin_col = 0

		# The first column is understood to generally be time.
		if begin_col == 1:
			new_header += "Time [Sec],"

		# For each cell we gather the letters and numbers separately, then write them out as letters then numbers.
		for s in splits[begin_col:]:
			chars = ''.join([i for i in s if not i.isdigit()])
			nums = ''.join([i for i in s if i.isdigit()])
			new_header += chars + nums + ","

		# We drop the last comma that our loop added.
		self.header_row = new_header[0:-1]

	def create_formatted(self):
		""" Writes out the converted file lines into the format that the DEFAULT configuration accepts """
		new = []

		# We add two blank rows then the formatted date line
		new.append("-")
		new.append("-")
		new.append(self.get_date_line(self.date))

		# Then the header row
		new.append(self.header_row)

		# Then the ablation data rows
		new = new + self.table_rows

		# For each line we need to add a newline character to the end.
		for line in new:
			self.out_lines.append(line + "\n")

	def output(self):
		""" Saves the new file content to a csv file """

		outPath = os.path.join(self.outLocation, self.outName + ".csv")

		# We import the stage information from a json file and set the default data folder
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), outPath)
			infoFile = infoFile.replace('\\', '/')

		else:
			# Otherwise the program is running in a normal python environment
			infoFile = outPath

		with open(infoFile, "w") as out:
			out.writelines(self.out_lines)
			out.close()


class Parser_txt:
	"""
		A parser that converts a text file into a csv file that can be processed by Parser_csv.
		Currently this is a bit more specific than the csv parser, due to a lack of example txt files to
		work with, but it works on general principles.
	"""
	def __init__(self, converterWindow, inFile, outLocation, outName):
		"""
		Parameters
		----------
		converterWindow : ConverterWindow
			A reference to the window running the show, so that responses to questions can be gathered.
		inFile : str
			The filepath of the data file to process
		outLocation : str
			The directory to save the converted file to
		outName : str
			The name of the converted file
		"""
		self.converterWindow = converterWindow
		self.inFile = inFile
		self.outLocation = outLocation
		self.outName = outName

		# The parser produces a temporary csv file that will be sent to Parser_csv, and deleted afterwards.
		self.outPath = os.path.join(self.outLocation, "latools_temp_data.csv")

		try:

			# We import the stage information from a json file and set the default data folder
			if getattr(sys, 'frozen', False):
				# If the program is running as a bundle, then get the relative directory
				infoFile = os.path.join(os.path.dirname(sys.executable), inFile)
				infoFile = infoFile.replace('\\', '/')

			else:
				# Otherwise the program is running in a normal python environment
				infoFile = inFile

			with open(infoFile, "r") as file:
				self.lines = file.read().splitlines()
				file.close()

		except:
			self.converterWindow.raiseError("Unable to open " + inFile)
			return

		# We split the file contents into comma-separated cells
		self.commas = self.clean_lines()

		# We define rows of data that are either in the table (ablation numbers) or other
		self.table_rows = []
		self.other_rows = []

		# We list possible headers. This section could be extended to ask the user if the header row is not clear.
		self.possible_headers = []

		# We try to determine the number of columns in the ablation data
		self.col_count = self.get_column_count()

		# We split the file up into rows of ablation numbers and other
		self.get_table_rows()

		# We find and process the header line into an acceptable format for the csv parser
		self.find_possible_headers()

		# We save the temporary csv file for Parser_csv to run
		self.write_csv()


	def clean_lines(self):
		""" Currently the parser has only been tested on tab-separated txt files.
			It converts all tabs to commas, then splits the lines into comma-separated cells, then removes empty cells.
		"""
		commas = []

		for row in self.lines:
			# We replace tab characters with commas
			new = row.replace("	", ",")

			# TO DO: replace other white-space characters with commas
			# new = new.replace("	", ",")

			# We make csv cells from the row
			splits = new.split(",")
			new = ""

			# We ignore cells that are empty or "-"
			# TO DO: add other cells we should ignore. This is only really important for the ablation data table.
			# The table should just be cells of numbers after this process.
			for cell in splits:
				if len(cell) != 0 and cell != "-":
					new += cell + ","
			# We remember to drop the last comma that we added to the end of the row in our loop above.
			commas.append(new[0:-1])

		return commas

	def find_possible_headers(self):
		""" Finds the header row by looking through non-table rows and finding values that look like analyte
			names. If the number of these analyte names found is appropriate for the data table the header row
			is added to a list of possibilities.
			Currently on all tests this process finds one correct option, but if new examples fail, the user could
			be asked to determine the header row, as they are questioned about the date in Parser_csv.
		"""
		# For each non-data row
		for row in self.other_rows:

			# We make a new list of analyte names, with the first column being time.
			new = ['Time']

			# The row is split into csv cells
			split = row.split(",")
			for cell in split:

				# The USC data example has analyte names such as Na23(LR)
				# We get rid of the brackets and what they contain by splitting based on those characters
				# into "bits".
				# Other text elements that needed to be ignored could be added here too.
				new_cell = cell.replace("(", ",").replace(")", ",")
				cell_split = new_cell.split(",")

				# For each bit of the cell we are looking for something that resembles an analyte name
				for bit in cell_split:

					# We look for strings between 3 and 5 characters long
					if len(bit) > 2 and len(bit) < 6:

						# We make a copy where we convert all letters to "C" and all numbers to "N"
						dummy = ""
						for char in bit:
							if char.isdigit():
								dummy += "N"
							elif char.isalpha():
								dummy += "C"

						# We then look for instances of CNN or NNC.
						# For example 'Al27' would be "CCNN" and would be a match for the "CNN" string.
						if 'CNN' in dummy or 'NNC' in dummy:
							# If the bit of the cell looks like an analyte we add it to the list
							new.append(bit)

			# Once we have gone through all of the cells in a row, and added any analyte names that we came across
			# to the new list. If that list is the appropriate length to be a header for the data table, then
			# We add it to the possible_headers list.
			if len(new) == self.col_count:
				self.possible_headers.append(new)

	def get_column_count(self):
		"""
		We run a parser to find the number of columns in the ablation data.
		This is based on finding a certain number of rows with a consistent number of columns.
		** This function could be changed to finding the column count of all rows and then taking the mode of the
		result, if that is more consistent. **
		"""

		# The number of consecutive rows with the same column count before we confirm that to be the
		# column count for that file.
		COUNT_THRESHOLD = 10

		# How many consecutive consistent column numbers we are currently on
		count = 0
		cols = 0

		for row in self.commas:

			# We split the row into csv cells
			splits = row.split(",")

			# We're looking for a table with more than two columns
			if len(splits) > 2:

				# If this col count was different to the last:
				if count == 0:
					# Set the new column count
					cols = len(splits)
					# We now have 1 consistent consecutive column
					count += 1
					continue

			# If this row's column count is the same as last row's
			if count != 0:
				if len(splits) > 2 and cols == len(splits):
					count += 1
				else:
					count = 0

			# If we have a number of consecutive rows with the same col count (> 2) we return this.
			if count > COUNT_THRESHOLD:
				return cols

		# Otherwise there was a problem and we return 0
		return 0

	def get_table_rows(self):
		""" We divide the file's lines up into table rows or other rows.
			Currently the criteria for this is that the row has a number of cells that is the same as
			the column count that was determined above, and that each cell has a number in it.
		"""
		for row in self.commas:

			# We split the line up into csv cells
			split = row.split(",")
			table_row = False

			# If the line has the correct number of columns
			if len(split) == self.col_count:

				table_row = True

				# We try to convert each cell to a float. Any failures result in the row not being considered a
				# data row
				for value in split:
					try:
						float(value)
					except:
						table_row = False
						break

			# The line is either put into the table or other.
			if table_row:
				self.table_rows.append(row)
			else:
				self.other_rows.append(row)

	def write_csv(self):
		""" We take our comma-separated rows and the header row and save them into a new csv file
			for Parser_csv to process.
		"""
		new_lines = []

		# We currently add all possible header rows to the csv file.
		for line in self.possible_headers:

			# We stick the header row values together with commas
			h_line = ""
			for cell in line:
				h_line += cell + ","
			# The last character in the line we make a newline instead of the last comma from the loop
			new_lines.append(h_line[0:-1] + "\n")

		# We add all of the comma-separated lines
		for line in self.commas:
			new_lines.append(line + "\n")

		# We import the stage information from a json file and set the default data folder
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), self.outPath)
			infoFile = infoFile.replace('\\', '/')

		else:
			# Otherwise the program is running in a normal python environment
			infoFile = self.outPath

		with open(infoFile, "w") as out:
			out.writelines(new_lines)
			out.close()



