""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import latools as la
import inspect
import templates.controlsPane as controlsPane
import ast
import os

import time

class ImportStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, importStageWidget, project):
		"""
		Initialising creates and customises a Controls Pane for this stage.

		Parameters
		----------
		stageLayout : QVBoxLayout
			The layout for the entire stage screen, that the Controls Pane will be added to.
		graphPaneObj : GraphPane
			A reference to the Graph Pane that will sit at the bottom of the stage screen and display
			updates t the graph, produced by the processing defined in the stage.
		progressPaneObj : ProgressPane
			A reference to the Progress Pane so that the right button can be enabled by completing the stage.
		importStageWidget : QWidget
			A reference to this stage's widget in order to manage popup windows
		project : RunningProject
			A reference to the project object which contains all of the information unique to this project,
			including the latools analyse object that the stages will update.
		"""

		self.graphPaneObj = graphPaneObj
		self.progressPaneObj = progressPaneObj
		self.importStageWidget = importStageWidget
		self.fileLocation = ""
		self.project = project
		self.importListener = None

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We capture the default parameters for this stage's function call
		self.defaultParams = self.stageControls.getDefaultParameters(inspect.signature(la.analyse))

		# We set the title and description for the stage

		self.stageControls.setDescription("Import Data", """
			In this stage you will be importing and configuring all the data required for your analysis session. Specifically, you will:
			<ul>
			<li style="margin-left:-20px;">  Locate the folder containing your sample and standards data</li>
			<li style="margin-left:-20px;">  Select or create a configuration</li>
			<li style="margin-left:-20px;">  Specify your SRM file identifier</li>
			<li style="margin-left:-20px;">  Specify your file extension</li>
			</ul>
			
			<p>Once specified, graph your sample and standard data by clicking APPLY.
			
			""")

		# The space for the stage options is provided by the Controls Pane.
		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		self.findDataButton = QPushButton("Browse")
		self.findDataButton.setMaximumWidth(100)
		self.findDataButton.clicked.connect(self.findDataButtonClicked)
		self.optionsGrid.addWidget(self.findDataButton,0,0)
		self.findDataButton.setToolTip("File path to the directory containing the data files.")

		self.fileLocationLine = QLineEdit("./data/")
		self.optionsGrid.addWidget(self.fileLocationLine, 0, 1)
		self.fileLocationLine.setReadOnly(True)

		self.configOption = QComboBox()
		# The configOption values are added based on the read_latoolscfg values
		for key in dict(la.config.read_latoolscfg()[1]):
			self.configOption.addItem(key)

		self.optionsGrid.addWidget(QLabel("config"), 1,0)
		self.optionsGrid.addWidget(self.configOption, 1,1)
		self.configOption.setToolTip("Configuration for your files.")

		self.srm_identifierOption = QLineEdit(self.defaultParams['srm_identifier'])
		self.optionsGrid.addWidget(QLabel("SRM identifier"), 2, 0)
		self.optionsGrid.addWidget(self.srm_identifierOption, 2, 1)
		self.srm_identifierOption.setToolTip("The string present in the file names of all standards.")

		self.file_extensionOption = QLineEdit(self.defaultParams['extension'])
		self.optionsGrid.addWidget(QLabel("file extension"), 3, 0)
		self.optionsGrid.addWidget(self.file_extensionOption, 3, 1)
		self.file_extensionOption.setToolTip("The file extension used in your data files")

		# We create the button for the right-most section of the Controls Pane.

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		""" Imports data into the project when the apply button is pressed. """

		# The actual call to the analyse object for this stage is run, using the stage values as parameters
		try:
			self.project.eg = la.analyse(data_folder=self.fileLocationLine.text(),
										 config=self.configOption.currentText(),
										 extension=self.file_extensionOption.text(),
										 srm_identifier=self.srm_identifierOption.text(),
										 pbar=self.progressPaneObj.progressUpdater)

			self.graphPaneObj.updateGraph(importing=True)

			self.progressPaneObj.completedStage(0)

			# When the data is imported various stage parameters are updated via the importListener
			if not self.importListener is None:
				self.importListener.dataImported()

			# The data location is recorded to be used as the default savefile location
			self.project.setDataLocation(self.fileLocationLine.text())

			# Automatically saves the project if it already has a save location
			self.project.reSave()
		except:
			print("An error occured")

			errorBox = QMessageBox.critical(self.importStageWidget,
											"Error loading data files",
											"An error occurred while attempting to load the data files. \n" +
											"Please check that the specified data folder contains the correct data files",
											QMessageBox.Ok)

	def findDataButtonClicked(self):
		""" Opens a file dialog to find a file directory for data import when a button is pressed. """

		self.fileLocation = QFileDialog.getExistingDirectory(self.importStageWidget, 'Open file', '/home')
		self.fileLocationLine.setText(self.fileLocation)

	def setImportListener(self, importListener):
		self.importListener = importListener

	def loadValues(self):
		""" Loads the values saved in the project, and fills in the stage parameters with them """

		# The stage parameters are stored in project as dictionaries
		params = self.project.getStageParams("import")

		# The stage parameters are applied to the input fields
		if params is not None:
			self.fileLocationLine.setText(params.get("data_folder", ""))
			self.configOption.setCurrentText(params.get("config", ""))
			self.file_extensionOption.setText(params.get("extension", ""))
			self.srm_identifierOption.setText(params.get("srm_identifier", ""))

		# The loading process then activates the stage's apply command
		self.pressedApplyButton()

	def enterPressed(self):
		""" When enter is pressed on this stage """
		if self.applyButton.isEnabled():
			self.pressedApplyButton()

	def relistConfig(self):
		""" When a new configuration is added the config dropdown box needs to be updated """

		# First each item is removed
		while self.configOption.count() != 0:
			self.configOption.removeItem(0)

		# Items are then readded
		for key in dict(la.config.read_latoolscfg()[1]):
			self.configOption.addItem(key)