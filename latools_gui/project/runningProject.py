""" Defines and records details from the currently running project """

import ast
from PyQt5.QtWidgets import *
import os
# from project.ErrLogger import logged Disused

class RunningProject():
	"""
	An object that defines and records all the details from the currently running project, and handles
	the saving and loading.
	"""
	#@logged
	def __init__(self, mainWidget):
		"""
		Initialises a blank project state

		Parameters
		----------
		mainWidget : MainWindow
			The main window created in latoolsgui
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

		# A reference to the Progress Bar, used for occasional resetting
		self.progressBar = None

	#@logged
	def saveProject(self):
		""" Save overwrites the current save file with the latest file strings """

		# If the project hasn't been saved before it will not have a save file location
		if not self.hasSaved:

			# The location of the specified data folder is used as a default save location, if there is one.
			location = '/home'
			if self.dataLocation is not None:
				location = self.dataLocation

			# A browse dialog that specifies the save folder location
			dialogLocaton = QFileDialog.getExistingDirectory(self.mainWidget, 'Open file', location)

			# If cancel was not pressed, set the location
			if dialogLocaton != '':
				self.folder = dialogLocaton
				self.hasSaved = True
				self.recentProjects.updateLocation(self.fileName, self.folder)
			else:
				return

		# If a project hasn't been started yet, a blank file is used as a save file
		if self.eg is None and self.folder is not None:
			file = open(self.folder + "/" + self.fileName + ".lalog", 'w')
			return

		# Otherwise the project is saved in the save folder location
		if self.folder is not None:
			self.eg.save_log(self.folder, self.fileName + ".lalog")
		else:
			print("failed to save")

	def newFile(self, name, location = None):
		"""
		Sets up a new save file, and stores the name and location

		Parameters
		----------
		name : str
			The name of the project
		location : str
			The file location for the save file
		"""

		# Record save file info
		self.fileName = name
		if location is not None:
			self.folder = location
			self.hasSaved = True

	#@logged
	def loadFile(self, name, location, progress=None):
		"""
		Loads a save file, stores the file info, populates the stage parameters and runs
		the stage function calls

		Parameters
		----------
		name : str
			The name of the project
		location : str
			The file location for the save file
		progress : ProgressBar
			The progress bar object that will be used in this project
		"""
		self.fileName = name
		self.folder = location
		self.hasSaved = True

		# A list of filter calls in the lalog file
		self.filters = []

		# A list of filter on and off calls in the lalog file
		self.filterOnOff = []

		# We open the log file and split into lines
		logName = os.path.join(location, name + ".lalog")
		logFile = open(logName, "r")
		logFileStrings = logFile.read().splitlines()

		if len(logFileStrings) == 0:
			return

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
				self.updateLastStage(4)

			if "calibrate :: args=() kwargs=" in line:
				subLine = line.replace("calibrate :: args=() kwargs=", "")
				self.stageParams["calibrate"] = ast.literal_eval(subLine)
				self.updateLastStage(5)

			if "filter_threshold :: args=() kwargs=" in line:
				subLine = line.replace("filter_threshold :: args=() kwargs=", "")
				self.filters.append(("filter_threshold", ast.literal_eval(subLine)))

			if "filter_threshold_percentile :: args=() kwargs=" in line:
				subLine = line.replace("filter_threshold_percentile :: args=() kwargs=", "")
				self.filters.append(("filter_threshold_percentile", ast.literal_eval(subLine)))

			if "filter_gradient_threshold :: args=() kwargs=" in line:
				subLine = line.replace("filter_gradient_threshold :: args=() kwargs=", "")
				self.filters.append(("filter_gradient_threshold", ast.literal_eval(subLine)))

			if "filter_trim :: args=() kwargs=" in line:
				subLine = line.replace("filter_trim :: args=() kwargs=", "")
				self.filters.append(("filter_trim", ast.literal_eval(subLine)))

			if "filter_correlation :: args=() kwargs=" in line:
				subLine = line.replace("filter_correlation :: args=() kwargs=", "")
				self.filters.append(("filter_correlation", ast.literal_eval(subLine)))

			if "filter_defragment :: args=() kwargs=" in line:
				subLine = line.replace("filter_defragment :: args=() kwargs=", "")
				self.filters.append(("filter_defragment", ast.literal_eval(subLine)))

			if "filter_exclude_downhole :: args=() kwargs=" in line:
				subLine = line.replace("filter_exclude_downhole :: args=() kwargs=", "")
				self.filters.append(("filter_exclude_downhole", ast.literal_eval(subLine)))

			if "filter_clustering :: args=() kwargs=" in line:
				subLine = line.replace("filter_clustering :: args=() kwargs=", "")
				self.filters.append(("filter_clustering", ast.literal_eval(subLine)))

			if "optimise_signal :: args=() kwargs=" in line:
				subLine = line.replace("optimise_signal :: args=() kwargs=", "")
				self.filters.append(("optimise_signal", ast.literal_eval(subLine)))

			if "filter_on :: args=" in line:
				subLine = line.replace("filter_on :: args=", "").replace(" kwargs={}", "")
				self.filterOnOff.append(("filter_on", ast.literal_eval(subLine)))

			if "filter_off :: args=" in line:
				subLine = line.replace("filter_off :: args=", "").replace(" kwargs={}", "")
				self.filterOnOff.append(("filter_off", ast.literal_eval(subLine)))

		# Any parameters that are listed as None are replaced with an empty string, so that they
		# can be input into the stage parameter textboxes.
		for stage in self.stageParams.keys():
			for key in self.stageParams[stage].keys():
				if self.stageParams[stage][key] is None:
					self.stageParams[stage][key] = ""

		# Set up loading bar
		if progress is not None:
			bar = progress.set(self.lastStage + 1, "loading stages")

		# The completed stages are loaded
		for i in range(self.lastStage + 1):
			self.importListener.loadStage(i)
			if progress is not None:
				bar.update()

		# The filters are loaded
		if len(self.filters) != 0:
			self.importListener.loadFilters(self.filters, self.filterOnOff)

		# We reset the progress bar after the last stage call is run
		if progress is not None:
			bar.reset()

		# Load the stage after the last completed stage
		self.importListener.setStageIndex(self.lastStage + 1)

	def setImportListener(self, importListener):
		"""
		Receives the importListener to use to pass info to stages at runtime

		Parameters
		----------
		importListener : ImportListener
			The object that manages communication between different program elements at run time.
		"""
		self.importListener = importListener

	def getStageParams(self, stage):
		"""
		Passes the keyword arguments that have been loaded as a dict for the requested stage

		Parameters
		----------
		stage : str
			The name of the stage to return the parameters for
		"""
		# If the stage doesn't exist as a key, return None
		return self.stageParams.get(stage, None)

	def updateLastStage(self, i):
		"""
		A quick function for updating the 'last stage' if the provided index is greater

		Parameters
		----------
		i : int
			The index of the current stage.
		"""
		if i > self.lastStage:
			self.lastStage = i

	def setDataLocation(self, location):
		"""
		Saves the location of the specified data folder

		Parameters
		----------
		location : str
			The location of the specified data folder
		"""
		self.dataLocation = location

	def reSave(self):
		"""
		Only saves the project if it already has a save file location. Used when stage apply buttons are pressed
		This has currently been deactivated so as not to save when the user hasn't specified to.
		"""
		if self.hasSaved:
			self.saveProject()

	def addRecentProjects(self, recents):
		""" saves a reference to the recentProjects object, which manages and displays the recent projects

		Parameters
		----------
		recents : RecentProjects
			An object that handles updating, displaying and saving the list of recent projects
		"""
		self.recentProjects = recents
