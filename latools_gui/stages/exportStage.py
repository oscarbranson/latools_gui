""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import latools as la
import logging
import templates.controlsPane as controlsPane
import os
import sys
import json

class ExportStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	#@logged
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, exportStageWidget, project, guideDomain):
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
		exportStageWidget : QWidget
			A reference to this stage's widget in order to manage popup windows
		project : RunningProject
			A reference to the project object which contains all of the information unique to this project,
			including the latools analyse object that the stages will update.
		"""
		self.logger = logging.getLogger(__name__)
		self.logger.info('Initialised import stage!')

		self.graphPaneObj = graphPaneObj
		self.progressPaneObj = progressPaneObj
		self.exportStageWidget = exportStageWidget
		self.project = project
		self.guideDomain = guideDomain
		self.defaultDataFolder = ""

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We import the stage information from a json file and set the default data folder
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), 'information/importStageInfo.json')
			infoFile = infoFile.replace('\\', '/')

			#self.defaultDataFolder = os.path.join(os.path.dirname(sys.executable), "./data/")
			#self.defaultDataFolder = self.defaultDataFolder.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			infoFile = "information/exportStageInfo.json"
			#self.defaultDataFolder = "./data/"

		with open(infoFile, "r") as read_file:
			self.stageInfo = json.load(read_file)
			read_file.close()

		self.stageControls.setDescription("Export Reports", self.stageInfo["stage_description"])

		# The space for the stage options is provided by the Controls Pane.
		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		# A button to find the export folder's filepath
		self.locationButton = QPushButton(self.stageInfo["location_label"])
		self.locationButton.setMaximumWidth(100)
		self.locationButton.clicked.connect(self.locationButtonClicked)
		self.optionsGrid.addWidget(self.locationButton, 0, 0)
		self.locationButton.setToolTip(self.stageInfo["location_description"])

		# A line to display the currently selected folder path
		self.fileLocationLine = QLineEdit(self.defaultDataFolder)
		self.optionsGrid.addWidget(self.fileLocationLine, 0, 1)
		self.fileLocationLine.setReadOnly(True)
		self.fileLocationLine.setToolTip(self.stageInfo["location_description"])

		# We create the export button for the right-most section of the Controls Pane.
		self.exportButton = QPushButton("Export")
		self.exportButton.clicked.connect(self.pressedExportButton)
		self.stageControls.addApplyButton(self.exportButton)


	def locationButtonClicked(self):
		""" Opens a file dialog to find a file directory for data export when the button is pressed. """

		self.fileLocation = QFileDialog.getExistingDirectory(self.exportStageWidget, 'Open file', '/home')
		self.fileLocationLine.setText(self.fileLocation)

	def enterPressed(self):
		""" When enter is pressed on this stage """
		pass

	def updateStageInfo(self):
		""" When the data is imported, we set the default export location to the imported data folder """
		self.defaultDataFolder = self.project.dataLocation
		self.fileLocationLine.setText(self.defaultDataFolder)

	def pressedExportButton(self):
		print("export button pressed")

