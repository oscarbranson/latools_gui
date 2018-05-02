""" This module needs a top level docstring.

"""

import os
import time
import json
import latools as la
import datetime
import re


class RunningProject():
	""" This class is intended to house everything that is specific to one project.

	When a project is created or loaded, this class is what is created or loaded.
	The instance of this class is passed to each stage.
	Currently it just contains a class variable which is later assigned as the la.analyse object.

	Attributes
	----------
		dataDictionary : dict
			A dictionary meant to store var pairs.
			Defined by calls from outside stages' needs.
	"""

	def __init__(self):
		""" Initialise a blank unaltered state.

		Creates tabula rasa project state.
		"""

		# The latools analyse object
		self.eg = None

		# Save file details
		self.folder = None
		self.filePath = None
		self.fileName = None

		# The content of the save file as a list of lines
		self.fileStrings = None

		# The object used to communicate with stages at runtime
		self.importListener = None

	def saveButton(self):
		""" Save overwrites the current save file with the latest file strings """

		# We overwrite the file and write the file strings
		file = open(self.filePath, "w")
		for line in self.fileStrings:
			file.write(line + "\n")
		file.close()
		#print(self.fileName + " saved")
		#self.eg.minimal_export()

	def newFile(self, name, location):
		""" Sets up a new save file, and stores the name and location """

		# Record save file info
		self.fileName = name
		self.folder = location
		self.filePath = location + "/" + name + ".sav"

		# Write a new file with the date and time in the header
		writeFile = open(self.filePath, "w")
		now = datetime.datetime.now()
		nowString = "LAtools save file. Created " + now.strftime("%Y-%m-%d %H:%M")

		# We create a set of blank lines so that we can edit lines by index later
		writeFile.write(nowString + "\n\n\n\n\n\n\n\n\n\n")
		writeFile.close()

		# fileStrings will be a live-updated copy of the save file contents
		self.fileStrings = [nowString, "", "", "", "", "", "", "", "", "", ""]


	def loadFile(self, name, location):
		""" Loads a save file, stores the file info, populates the stage parameters and runs
		the stage function calls """
		self.fileName = name
		self.folder = location
		self.filePath = location + "/" + name + ".sav"

		# Reads the save file to fileStrings
		file = open(self.filePath, "r")
		self.fileStrings = file.read().splitlines()

		# After the first two lines in the save file, the other lines each represent a dictionary of
		# saved parameters for a stage's fields. These dictionaries are passed to the stages for processing
		for i in range(2,9):
			if self.fileStrings[i] != "":
				# The value passed here is a stage index (import = 0, etc)
				self.importListener.loadStage(i - 2)
			else:
				# The first line that is blank is where the focus of stages screen is set
				self.importListener.setStageIndex(i - 2)

				return

		# self.eg = la.reproduce(location + name + ".log")

	def runStage(self, index, parameters):
		""" Here the entries from a stage's parameters are saved to that stage's index in fileStrings """
		self.fileStrings[index + 2] = parameters

	def setImportListener(self, importListener):
		""" Receives the importListener to use to pass info to stages at runtime """
		self.importListener = importListener

	def getStageString(self, index):
		""" Sends the fileString for a particular stage so that it can be processed in the stage """
		return self.fileStrings[index + 2]