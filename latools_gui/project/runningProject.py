""" This module needs a top level docstring.

"""

import ast
from PyQt5.QtWidgets import *

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

	def __init__(self, mainWidget):
		""" Initialise a blank unaltered state.

		Creates tabula rasa project state.
		"""
		self.mainWidget = mainWidget

		# The latools analyse object
		self.eg = None

		# Save file details
		self.folder = None
		self.fileName = None
		self.hasSaved = False
		self.dataLocation = None
		self.recentProjects = None

		# The object used to communicate with stages at runtime
		self.importListener = None

		# The information taken from the log file used when loading
		self.stageParams = {}
		self.lastStage = 0

	def saveProject(self):
		""" Save overwrites the current save file with the latest file strings """

		if not self.hasSaved:

			location = '/home'
			if self.dataLocation is not None:
				location = self.dataLocation

			dialogLocaton = QFileDialog.getExistingDirectory(self.mainWidget, 'Open file', location)
			print(dialogLocaton)
			# If cancel was not pressed, set the location
			if dialogLocaton != '':
				self.folder = dialogLocaton
				self.hasSaved = True
			else:
				return
		self.recentProjects.updateLocation(self.fileName, self.folder)
		if self.eg is None:
			return

		if self.folder is not None:
			self.eg.save_log(self.folder)
		else:
			print("failed to save")

	def newFile(self, name, location = None):
		""" Sets up a new save file, and stores the name and location """

		# Record save file info
		self.fileName = name
		if location is not None:
			self.folder = location
			self.hasSaved = True

	def loadFile(self, name, location):
		""" Loads a save file, stores the file info, populates the stage parameters and runs
		the stage function calls """
		self.fileName = name
		self.folder = location
		self.hasSaved = True

		# We open the log file and split into lines
		logName = location + "/analysis.lalog"
		logFile = open(logName, "r")
		logFileStrings = logFile.read().splitlines()

		# Each line is checked for a characteristic indicating a particular stage's parameter list
		# The line is then cropped to only the section resembling a dictionary of parameters.
		# This is then cast to an actual dictionary and saved.
		# The lastStage value is then updated to find the last completed stage
		for line in logFileStrings:
			if "__init__ :: args=() kwargs=" in line:
				subLine = line.replace("__init__ :: args=() kwargs=", "")
				self.stageParams["import"] = ast.literal_eval(subLine)
				self.updateLastStage(0)

			if "despike :: args=() kwargs=" in line:
				subLine = line.replace("despike :: args=() kwargs=", "")
				self.stageParams["despike"] = ast.literal_eval(subLine)
				self.updateLastStage(1)

			if "autorange :: args=() kwargs=" in line:
				subLine = line.replace("autorange :: args=() kwargs=", "")
				self.stageParams["autorange"] = ast.literal_eval(subLine)
				self.updateLastStage(2)

			if "bkg_calc_weightedmean :: args=() kwargs=" in line:
				subLine = line.replace("bkg_calc_weightedmean :: args=() kwargs=", "")
				self.stageParams["bkg_calc_weightedmean"] = ast.literal_eval(subLine)
				# We remove any past instances of bkg_calc_interp1d calls
				self.stageParams.pop("bkg_calc_interp1d", None)
				self.updateLastStage(2)

			if "bkg_calc_interp1d :: args=() kwargs=" in line:
				subLine = line.replace("bkg_calc_interp1d :: args=() kwargs=", "")
				self.stageParams["bkg_calc_interp1d"] = ast.literal_eval(subLine)
				# We remove any past instances of bkg_calc_weightedmean calls
				self.stageParams.pop("bkg_calc_weightedmean", None)
				self.updateLastStage(2)

			if "bkg_subtract :: args=() kwargs=" in line:
				subLine = line.replace("bkg_subtract :: args=() kwargs=", "")
				self.stageParams["bkg_subtract"] = ast.literal_eval(subLine)
				self.updateLastStage(3)

			if "ratio :: args=() kwargs=" in line:
				subLine = line.replace("ratio :: args=() kwargs=", "")
				self.stageParams["ratio"] = ast.literal_eval(subLine)
				print(self.stageParams["ratio"])
				self.updateLastStage(4)

			if "calibrate :: args=() kwargs=" in line:
				subLine = line.replace("calibrate :: args=() kwargs=", "")
				self.stageParams["calibrate"] = ast.literal_eval(subLine)
				self.updateLastStage(5)

		# Any parameters that are listed as None are replaced with an empty string, so that they
		# can be input into the stage parameter textboxes.
		for stage in self.stageParams.keys():
			for key in self.stageParams[stage].keys():
				if self.stageParams[stage][key] is None:
					self.stageParams[stage][key] = ""

		#reply = QMessageBox.information(self.mainWidget, 'Information',
		#							 "Loading project", QMessageBox.Ok, QMessageBox.Ok)

		# The completed stages are loaded
		for i in range(self.lastStage + 1):
			self.importListener.loadStage(i)

		# Load the stage after the last completed stage
		self.importListener.setStageIndex(self.lastStage + 1)

	def setImportListener(self, importListener):
		""" Receives the importListener to use to pass info to stages at runtime """
		self.importListener = importListener

	def getStageParams(self, stage):
		# If the stage doesn't exist as a key, return None
		return self.stageParams.get(stage, None)

	def updateLastStage(self, i):
		if i > self.lastStage:
			self.lastStage = i

	def setDataLocation(self, location):
		self.dataLocation = location

	def reSave(self):
		if self.hasSaved:
			self.saveProject()

	def addRecentProjects(self, recents):
		self.recentProjects = recents