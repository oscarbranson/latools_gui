""" This is the main module that builds all aspects of the latools program and runs the GUI."""

print("LAtools is currently loading. Please wait. This may take several minutes.")

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QKeyEvent, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
import sys
import os
import latools as la
import json
import zipfile

# Import the templates
from templates import titleScreen
from templates import graphPane
from templates import progressPane
from templates import stageTabs

# Import the stage files
from stages import importStage
from stages import despikingStage
from stages import autorangeStage
from stages import backgroundStage
from stages import ratioStage
from stages import calibrationStage
from stages import filteringStage
from stages import exportStage

from project import runningProject

import logging
import logging.config


# List of stages
STAGES = ["Import","De-Spiking","Autorange","Background","Ratio","Calibration","Filtering", "Export"]



class MainWindow(QMainWindow):
	"""
	The main GUI window. All of the GUI functionality is built through this class.
	"""

	def __init__(self):
		""" The initialisation method creates the window and then runs the UI initialisation. """

		super().__init__()
		
		# Determines where the offset for where the window appears on the screen.
		# Moves the window x pixels to the right, and y pixels down
		self.move(100, 0)
		self.setWindowTitle("LAtools")
		
		# We move on to build the UI
		self.initUI()

	def initUI(self):
		""" Creates instances of all screens and stages of the program, and controls movement between them. """

		self.mainWidget = QWidget()
		self.setCentralWidget(self.mainWidget)

		# We import the user guide location information from a json file
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), 'information/guiInfo.json')
			infoFile = infoFile.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			infoFile = "information/guiInfo.json"

		with open(infoFile, "r") as read_file:
			self.guiInfo = json.load(read_file)
			read_file.close()

		self.links = (self.guiInfo["user_guide_domain"],
					  self.guiInfo["report_issue_link"],
					  self.guiInfo["report_issue_description"])
		#self.userGuideDomain = self.links[0]

		# principalLayout is a vertical box that runs down the entire window
		self.principalLayout = QVBoxLayout(self.mainWidget)

		# The file menu is produced here
		self.initFileMenu()

		# mainStack moves between views that occupy the entire window
		self.mainStack = QStackedWidget()

		# Add the mainStack to the principalLayout
		self.principalLayout.addWidget(self.mainStack)

		# We create an instance of a Running Project to store in one place all of the analysis that will be
		# performed in this project
		self.project = runningProject.RunningProject(self.mainWidget)

		# Here we create a title screen object from the file in templates
		self.titleScreenObj = titleScreen.TitleScreen(self.mainStack, self.project, self.links)
		self.project.addRecentProjects(self.titleScreenObj.recentProjects)

		# And it is added to the mainstack in position 0.
		self.mainStack.addWidget(self.titleScreenObj.getPane())

		# We create a widget for the stages and add this to the main stack
		self.stageTabsWidget = QWidget()
		self.stagesLayout = QVBoxLayout(self.stageTabsWidget)
		self.mainStack.addWidget(self.stageTabsWidget)

		# The stageTabs object is created
		self.stageTabs = stageTabs.StageTabs(STAGES, self.stagesLayout)

		# The layout for each stage is stored in a list, which is passed to the stageTabs object
		self.stageLayouts = []

		# For each stage, we make a widget, a layout for the widget, and add the layout to the list.
		self.importStageWidget = QWidget()
		self.importStageLayout = QVBoxLayout(self.importStageWidget)
		self.stageLayouts.append(self.importStageLayout)

		self.despikingStageWidget = QWidget()
		self.despikingStageLayout = QVBoxLayout(self.despikingStageWidget)
		self.stageLayouts.append(self.despikingStageLayout)

		self.autorangeStageWidget = QWidget()
		self.autorangeStageLayout = QVBoxLayout(self.autorangeStageWidget)
		self.stageLayouts.append(self.autorangeStageLayout)

		self.backgroundStageWidget = QWidget()
		self.backgroundStageLayout = QVBoxLayout(self.backgroundStageWidget)
		self.stageLayouts.append(self.backgroundStageLayout)

		self.ratioStageWidget = QWidget()
		self.ratioStageLayout = QVBoxLayout(self.ratioStageWidget)
		self.stageLayouts.append(self.ratioStageLayout)

		self.calibrationStageWidget = QWidget()
		self.calibrationStageLayout = QVBoxLayout(self.calibrationStageWidget)
		self.stageLayouts.append(self.calibrationStageLayout)

		self.filteringStageWidget = QWidget()
		self.filteringStageLayout = QVBoxLayout(self.filteringStageWidget)
		self.stageLayouts.append(self.filteringStageLayout)

		self.exportStageWidget = QWidget()
		self.exportStageLayout = QVBoxLayout(self.exportStageWidget)
		self.stageLayouts.append(self.exportStageLayout)

		# All of the stage layouts are passed to the stageTabs, to be placed in tabs
		self.stageTabs.passStageLayouts(self.stageLayouts)

		# Here we define the graph pane, so that it could be passed to the controls pane.
		# However, we want it to sit below the controls, so it's not added to the layout yet.
		self.graphPaneObj = graphPane.GraphPane(self.project)

		# We create the progress pane object but will add it to the stages layout later
		self.progressPaneObj = progressPane.ProgressPane(STAGES, self.graphPaneObj, self.project, self.stageTabs)

		# The stage objects are then created. Their content will populate the tabs
		self.importStageObj = importStage.ImportStage(self.importStageLayout,
													  self.graphPaneObj,
													  self.progressPaneObj,
													  self.importStageWidget,
													  self.project,
													  self.links)

		self.despikingStageObj = despikingStage.DespikingStage(self.despikingStageLayout,
															   self.graphPaneObj,
															   self.progressPaneObj,
															   self.despikingStageWidget,
															   self.project,
															   self.links)

		self.autorangeStageObj = autorangeStage.AutorangeStage(self.autorangeStageLayout,
															   self.graphPaneObj,
															   self.progressPaneObj,
															   self.autorangeStageWidget,
															   self.project,
															   self.links)

		self.backgroundStageObj = backgroundStage.BackgroundStage(self.backgroundStageLayout,
																  self.graphPaneObj,
																  self.progressPaneObj,
																  self.backgroundStageWidget,
																  self.project,
																  self.links)

		self.ratioStageObj = ratioStage.RatioStage(self.ratioStageLayout,
												   self.graphPaneObj,
												   self.progressPaneObj,
												   self.ratioStageWidget,
												   self.project,
												   self.links)

		self.calibrationStageObj = calibrationStage.CalibrationStage(self.calibrationStageLayout,
																	 self.graphPaneObj,
																	 self.progressPaneObj,
																	 self.calibrationStageWidget,
																	 self.project,
																	 self.links)

		self.filteringStageObj = filteringStage.FilteringStage(self.filteringStageLayout,
															   self.graphPaneObj,
															   self.project,
															   self.links)

		self.exportStageObj = exportStage.ExportStage(self.exportStageLayout,
													  self.graphPaneObj,
													  self.progressPaneObj,
													  self.exportStageWidget,
													  self.project,
													  self.links,
													  self)

		# ImportListener handles all interaction between stages at run time.
		self.importListener = ImportListener(self.importStageObj,
											self.despikingStageObj,
											self.autorangeStageObj,
											self.backgroundStageObj,
											self.ratioStageObj,
											self.calibrationStageObj,
											self.filteringStageObj,
											self.exportStageObj,
											self.progressPaneObj,
											self.graphPaneObj,
											self.titleScreenObj,
											self.stageTabs,
											self)
		self.importStageObj.setImportListener(self.importListener)
		self.titleScreenObj.setImportListener(self.importListener)
		self.project.setImportListener(self.importListener)

		# Finally, we call methods on the progressPane and graphPane object to add them to the layout.
		self.progressPaneObj.addToLayout(self.stagesLayout)
		self.graphPaneObj.addToLayout(self.stagesLayout)

		# This bool is used to avoid having to confirm quitting twice in a row
		self.quitting = False

		# The config window is a popup window that is recorded here so that it is not destroyed after being created.
		self.configWindow = None
	
	def keyPressEvent(self, event):
		"""
		Keypress events are handled here

		Parameters
		----------
		event : Event
			The type of event that has just occured. We are looking for a key press type
		"""
		if type(event) == QKeyEvent:

			# Pressing the enter key will attempt to press the main activation button on the stages and title screen
			if event.key() == Qt.Key_Return:
				# The stages are alerted of the keypress via the Import Listener
				self.importListener.enterPressed(main=self.mainStack.currentIndex(),
												 stage=self.stageTabs.tabs.currentIndex())
	
	def initFileMenu(self):
		""" Builds and displays the file menu"""

		saveFile = QAction(QIcon('save.png'), 'Save', self)
		saveFile.setShortcut('Ctrl+S')
		saveFile.setStatusTip('Save your project')
		saveFile.triggered.connect(self.saveButton)

		#exportFile = QAction(QIcon('export.png'), 'Export', self)
		#exportFile.setShortcut('Ctrl+E')
		#exportFile.setStatusTip('Export your data')
		#exportFile.triggered.connect(self.exportButton)

		# loadFile = QAction(QIcon('open.png'), 'Load', self)
		# #loadFile.setShortcut('Ctrl+L')
		# loadFile.setStatusTip('Load File')
		# # loadFile.triggered.connect()

		# exitAct = QAction(QIcon('exit.png'), 'Exit', self)
		# exitAct.setShortcut('Ctrl+Q')
		# exitAct.setStatusTip('Exit application')
		# exitAct.triggered.connect(qApp.quit)

		# A file option for zipping the error log
		saveLog = QAction(QIcon('export.png'), 'Export error logs', self)
		saveLog.setShortcut('Ctrl+E')
		saveLog.setStatusTip("Saves a zip folder of your error logs to the LAtools directory")
		saveLog.triggered.connect(self.zipLogs)

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(saveFile)
		fileMenu.addAction(saveLog)
		# fileMenu.addAction(loadFile)
		# fileMenu.addAction(exportFile)
		# fileMenu.addAction(exitAct)

		makeConfig = QAction(QIcon('open.png'), 'Make', self)
		makeConfig.setStatusTip('Make a new configuration')
		makeConfig.triggered.connect(self.makeConfig)

		configMenu = menubar.addMenu('&Configuration')
		configMenu.addAction(makeConfig)

		guideMenu = QAction(QIcon('help.png'), 'User Guide', self)
		guideMenu.setStatusTip('Read the user guide')
		guideMenu.triggered.connect(self.helpButton)

		helpMenu = menubar.addMenu('&User Guide')
		helpMenu.addAction(guideMenu)
	
	def saveButton(self):
		""" Runs the save command on the current running project """
		self.project.saveProject()
	
	def exportButton(self):
		""" Runs the export command on the current running project """
		if self.project.eg is not None:
			self.project.eg.trace_plots()
			infoBox = QMessageBox.information(self.mainWidget, "Export",
											   "Your data plots have been saved as pdfs in the reports folder " +
											   "created on import",
											   QMessageBox.Ok)

	def zipLogs(self):
		""" Runs the command to zip the error logs and save them to the LAtools directory """

		try:
			if getattr(sys, 'frozen', False):
				# If the program is running as a bundle, then get the relative directory
				logFolder = os.path.join(os.path.dirname(sys.executable), "logs/")
				logFolder = logFolder.replace('\\', '/')

				parentFolder = os.path.dirname(sys.executable)
				parentFolder = parentFolder.replace('\\', '/')
				outputZip = os.path.join(parentFolder, 'Logs.zip')
			else:
				# Otherwise the program is running in a normal python environment
				logFolder = "logs/"
				outputZip = 'Logs.zip'

			# We create an empty zip folder
			zipf = zipfile.ZipFile(outputZip, 'w', zipfile.ZIP_DEFLATED)

			# The folder is filled with the files in the logs directory
			self.zipdir(logFolder, zipf)

			# The zip file is saved
			zipf.close()

			infoBox = QMessageBox.information(self.mainWidget, "Export logs",
											  "Your error log files have been saved to 'Logs.zip' in the LAtools directory",
											  QMessageBox.Ok)
		except:
			infoBox = QMessageBox.information(self.mainWidget, "Export logs",
											  "An error was encountered when attempting to save the error log files.",
											  QMessageBox.Ok)

	def zipdir(self, path, ziph):
		"""
		Takes a new zip file and fills it with the contents of the path directory

		Parameters
		----------
		path : str
			The filepath of the folder we're zipping
		ziph : ZipFile
			The handle for the zipfile we're creating
		"""
		for root, dirs, files in os.walk(path):
			for file in files:
				ziph.write(os.path.join(root, file))

	#@logged
	def closeEvent(self, event):
		"""
		Attempting to close the window is handled here.
		This function is automatically called as part of the functionality of a QT Main Window

		Parameters
		----------
		event : Event
			The close event (we don't need this)
		"""

		# If we are not on the title page...
		if self.mainStack.currentIndex() != 0 and not self.quitting:
			self.quitting = True

			# A popup message is created to ask to save the project
			reply = QMessageBox.question(self, 'Message',
										"Would you like to save before quitting?", QMessageBox.Yes |
										QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

			if reply == QMessageBox.Yes:
				# If yes is selected the project is saved, then closed
				self.project.saveProject()
				event.accept()
			elif reply == QMessageBox.No:
				# If no, the project is closed
				event.accept()
			else:
				# If cancel, the event is ignored
				self.quitting = False
				event.ignore()

	def makeConfig(self):
		""" Displays the New Configuration popup window """
		self.configWindow = ConfigWindow(self.importStageObj)
		self.configWindow.show()

	def setProjectTitle(self, title):
		"""
		Updates the program window with the project title

		Parameters
		----------
		title : str
			The project title to update the main window with
		"""
		self.setWindowTitle("LAtools - " + title)

	def helpButton(self):
		""" Opens the online user guide """
		url = QUrl(self.links[0] + "LAtoolsGUIUserGuide/index.html")
		QDesktopServices.openUrl(url)


class ConfigWindow(QWidget):
	""" A popup window, accessed via the file menu, that allows the user to define a new configuration for LAtools """

	def __init__(self, importStage):
		""" Creates the popup window

		Parameters
		----------
		importStage : ImportStage
			A reference to the import stage
		"""

		QWidget.__init__(self)
		self.setWindowTitle("Create new configuration")

		# We use a bool to determine if the chosen configuration name is acceptable
		self.nameOK = False
		self.importStage = importStage

		# The location of the config guide
		self.guideLocation = "https://latools.readthedocs.io/en/latest/users/configuration/index.html"

		# We use a grid layout
		self.configGrid = QGridLayout(self)

		# The name field
		self.configGrid.addWidget(QLabel("Configuration name:"), 0, 0)
		self.configName = QLineEdit()
		self.configGrid.addWidget(self.configName, 0, 1)
		self.configName.setFixedWidth(250)
		self.configName.cursorPositionChanged.connect(self.nameEdited)

		# The data format field and browse button
		self.configGrid.addWidget(QLabel("dataformat:"), 1, 0)
		self.configData = QLineEdit()
		self.configGrid.addWidget(self.configData, 1, 1)
		self.configData.setEnabled(False)

		self.configDataButton = QPushButton("Browse")
		self.configDataButton.clicked.connect(self.dataClicked)
		self.configGrid.addWidget(self.configDataButton, 1, 3)

		# The srm file field and browse button
		self.configGrid.addWidget(QLabel("srmfile:"), 2, 0)
		self.configSrm = QLineEdit()
		self.configGrid.addWidget(self.configSrm, 2, 1)
		self.configSrm.setEnabled(False)

		self.configSrmButton = QPushButton("Browse")
		self.configSrmButton.clicked.connect(self.srmClicked)
		self.configGrid.addWidget(self.configSrmButton, 2, 3)

		# The activation button, which is disabled until there is acceptable input parameters
		self.applyButton = QPushButton("Create configuration")
		self.applyButton.setEnabled(False)
		self.configGrid.addWidget(self.applyButton, 4, 3)
		self.applyButton.clicked.connect(self.applyClicked)

		# The guide button that links to info about creating a configuration
		self.guideButton = QPushButton("Configuration Guide")
		self.guideButton.clicked.connect(self.guideButtonClick)
		self.configGrid.addWidget(self.guideButton, 0, 3)

		# A text box that displays the current configurations
		self.configPrint = QTextEdit()

		# The content for the text box is derived from a list of current configurations
		configStr = "Current LAtools configurations:\n\n"
		for key in dict(la.config.read_latoolscfg()[1]):
			configStr = configStr + key + "\n"
		self.configPrint.setText(configStr)

		# The text box is displayed and disabled
		self.configGrid.addWidget(self.configPrint, 5, 0, 1, 4)
		self.configPrint.setEnabled(False)

	def dataClicked(self):
		""" The browse button for the data field """
		location = QFileDialog.getOpenFileName(self, 'Open file', '/home')
		self.configData.setText(location[0])
		self.nameEdited()

	def srmClicked(self):
		""" The browse button for the srm field """
		location = QFileDialog.getOpenFileName(self, 'Open file', '/home')
		self.configSrm.setText(location[0])
		self.nameEdited()

	def applyClicked(self):
		""" Creates the new configuration when the apply button is pressed """

		# The latools function is called
		la.config.create(self.configName.text(),
						 srmfile=self.configSrm.text(),
						 dataformat=self.configData.text(),
						 base_on='DEFAULT', make_default=False)

		# The text box is updated
		configStr = "Current LAtools configurations:\n\n"
		for key in dict(la.config.read_latoolscfg()[1]):
			configStr = configStr + key + "\n"
		self.configPrint.setText(configStr)

		# An info box informs the user that a configuration has been created
		infoBox = QMessageBox.information(self,
										"Configuration added",
										"Configuration added",
										QMessageBox.Ok)

		# The dropdown in the import stage is relisted to include the new configuration
		self.importStage.relistConfig()
		# The apply button is then disabled to avoid creating the config twice
		self.applyButton.setEnabled(False)

	def nameEdited(self):
		""" Called whenever the name field is edited. Determines when the apply button can be enabled """
		self.nameOK = self.configName.text() != ""
		# Can be extended to disallow certain characters in the name field
		self.applyButton.setEnabled(self.nameOK and self.configData.text() != "" and self.configSrm.text() != "")

	def guideButtonClick(self):
		""" Link to online user guide """
		url = QUrl(self.guideLocation)
		QDesktopServices.openUrl(url)

class ImportListener():
	""" Handles the passing of information between modules during runtime """

	def __init__(self,
				 importStage,
				 despikingStage,
				 autorangeStage,
				 backgroundStage,
				 ratioStage,
				 calibrationStage,
				 filteringStage,
				 exportStage,
				 progressPane,
				 graphPane,
				 titleScreen,
				 stageTabs,
				 mainWindow):
		"""
		This object passes information between stages at run time. The parameters are threrefore a reference to
		every object and stage that may need information passed to it at run time.
		"""

		# References to each object are saved
		self.importStage = importStage
		self.despikingStage = despikingStage
		self.autorangeStage = autorangeStage
		self.backgroundStage = backgroundStage
		self.ratioStage = ratioStage
		self.calibrationStage = calibrationStage
		self.filteringStage = filteringStage
		self.exportStage = exportStage
		self.progressPane = progressPane
		self.graphPane = graphPane
		self.titleScreen = titleScreen
		self.stageTabs = stageTabs
		self.mainWindow = mainWindow

		# Stages are stored in a list so that we can access them by index
		self.stageObjects = [self.importStage,
							 self.despikingStage,
							 self.autorangeStage,
							 self.backgroundStage,
							 self.ratioStage,
							 self.calibrationStage,
							 self.filteringStage,
							 self.exportStage]

	def dataImported(self):
		""" When data is first imported in the Import Stage, several fields can be updated in later
		stages which require info from that data """
		self.autorangeStage.updateStageInfo()
		self.ratioStage.updateStageInfo()
		self.calibrationStage.updateStageInfo()
		self.filteringStage.updateStageInfo()
		self.exportStage.updateStageInfo()
		self.backgroundStage.resetButtons()

	def setTitle(self, title):
		"""
		Adds the project title to the name of the program's window

		Parameters
		----------
		title : str
			The project title
		"""
		self.mainWindow.setProjectTitle(title)

	def setStageIndex(self, index):
		"""
		Jumps to a particular stage when loading a project

		Parameters
		----------
		index : int
			The index of the stage to jump to
		"""
		self.stageTabs.setStage(index)

	def loadStage(self, index):
		"""
		Tells a stage to load the saved stage parameter info, based on an identifying stage index

		Parameters
		----------
		index : int
			The index of the stage to load
		"""
		self.stageObjects[index].loadValues()
		self.progressPane.progressUpdater.reset()

	def enterPressed(self, main, stage):
		"""
		Determines which screen the enter command should be sent to

		Parameters
		----------
		main : int
			0 = we're on the title screen, 1 = we're currently in the analysis stages
		stage : int
			The index of the stage we're currently in
		"""
		if main == 0:
			self.titleScreen.enterPressed()
		elif main == 1:
			# If we are on the stages screen, the command is sent to the indexed stage
			self.stageObjects[stage].enterPressed()

	def loadFilters(self, filters, filterOnOff):
		"""
		The filter information from the save file which is currently being loaded is sent to the filtering stage

		Parameters
		----------
		filters : list
			The filter calls that need to be loaded
		filterOnOff : list
			The filter on or off calls that need to be loaded
		"""
		self.filteringStage.stageControls.loadFilters(filters, filterOnOff)

	def makeConfiguration(self):
		""" Displays the make new configuration pop-up window """
		self.mainWindow.configWindow = ConfigWindow(self.importStage)
		self.mainWindow.configWindow.show()

	def updateExport(self, stage=""):
		"""
		When an analysis stage is completed we update the export stage so that the most recent focus stage is known

		Parameters
		----------
		stage : str
			The stage that has been completed. We only need this info for particular stages
		"""
		self.exportStage.updateFocus(stage)
	
	def updateRatio(self):
		"""
		When the user goes back and changes the ratio stage after completing the calibration stage,
		the calibration stage needs to know about it, to reset.
		"""
		self.calibrationStage.updateRatio()

	def blockReImport(self):
		"""
		After a certain point in the analysis the user cannot go back and reimport data, because the amount of
		things that would need to be reset gets too complicated. It's easier for them to start a new project.
		"""
		self.importStage.blockReImport()

# This is where the GUI is actually created and run.
# Autodocs executes side effects when it imports modules to be read. Therefore the GUI must be created and
# run in a conditional that only accepts the main routine.
if __name__ == '__main__':

	# Set the appropriate file paths to write logs to
	if getattr(sys, 'frozen', False):
		# If the program is running as a bundle, then get the relative directory
		logFile = os.path.join(os.path.dirname(sys.executable), 'logs/log.log')
		logFile = logFile.replace('\\', '/')

		errorFile = os.path.join(os.path.dirname(sys.executable), 'logs/error.log')
		errorFile = errorFile.replace('\\', '/')
	else:
		# Otherwise the program is running in a normal python environment
		logFile = "logs/log.log"
		errorFile = "logs/error.log"

	# Define logger configuration
	logger = logging.getLogger(__name__)
	logging.config.dictConfig({
		'version': 1,
		'formatters': {
			'stdFormatter': {
				'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
			},
		},
		'handlers': { #Debug log currently not used
			#'loghandler': {
			#	'level': 'DEBUG',
			#	'class': 'logging.handlers.TimedRotatingFileHandler',
			#	'formatter': 'stdFormatter',
			#	'filename': logFile,
			#	'when': 'midnight',
			#	'backupCount': 2
			#},
			'errhandler': {
				'level': 'ERROR',
				'class': 'logging.FileHandler',
				'formatter': 'stdFormatter',
				'filename': errorFile
			},
		},
		'loggers': {
			'': {
				'handlers': ['errhandler'],
				'level': 'DEBUG',
				'propagate': True
			},
		},

	})

	# Actually run the application here
	app = QApplication([])
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())
