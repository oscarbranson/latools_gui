""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import json
import sys
import os
import ast

import templates.controlsPane as controlsPane

import logging

class RatioStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	
	#@logged
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, ratioWidget, project, links):
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
		ratioWidget : QWidget
			The parent widget for this object. Used mainly for displaying error boxes.
		project : RunningProject
			A reference to the project object which contains all of the information unique to this project,
			including the latools analyse object that the stages will update.
		links : (str, str, str)
			links[0] = The User guide website domain
			links[1] = The web link for reporting an issue
			links[2] = The tooltip for the report issue button
		"""

		self.graphPaneObj = graphPaneObj
		self.progressPaneObj = progressPaneObj
		self.ratioWidget = ratioWidget
		self.project = project
		self.guideDomain = links[0]
		self.reportIssue = links[1]

		# We create a controls pane object which covers the general aspects of the stage's controls pane
		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We import the stage information from a json file
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), 'information/ratioStageInfo.json')
			infoFile = infoFile.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			infoFile = "information/ratioStageInfo.json"

		with open(infoFile, "r") as read_file:
			self.stageInfo = json.load(read_file)
			read_file.close()

		# We set the title and description for the stage

		self.stageControls.setDescription("Ratio Calculation", self.stageInfo["stage_description"])

		# The space for the stage options is provided by the Controls Pane.
		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		self.internal_standardOption = QComboBox()
		self.internal_standardOption.addItem(" ")
		self.standardLabel = QLabel(self.stageInfo["standard_label"])
		self.optionsGrid.addWidget(self.standardLabel, 0, 0)
		self.optionsGrid.addWidget(self.internal_standardOption, 0, 1)
		self.internal_standardOption.activated.connect(self.internal_standardClicked)
		self.internal_standardOption.setToolTip(self.stageInfo["standard_description"])
		self.standardLabel.setToolTip(self.stageInfo["standard_description"])
		self.standardLabel.setMaximumWidth(150)

		self.optionsGrid.setColumnStretch(2,1)

		# We create a button to link to the user guide
		self.guideButton = QPushButton("User guide")
		self.guideButton.clicked.connect(self.userGuide)
		self.stageControls.addDefaultButton(self.guideButton)

		# We create a button to link to the form for reporting an issue
		self.reportButton = QPushButton("Report an issue")
		self.reportButton.clicked.connect(self.reportButtonClick)
		self.stageControls.addDefaultButton(self.reportButton)
		self.reportButton.setToolTip(links[2])

		# We create the apply button for the right-most section of the Controls Pane.
		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)
		self.applyButton.setEnabled(False)

		#log
		self.logger = logging.getLogger(__name__)
		self.logger.info('ratio initialised')

	#@logged
	def pressedApplyButton(self):
		""" Ratios the project data with a given standard when a button is pressed. """

		try:

			# The actual call to the analyse object for this stage is run, using the stage values as parameters
			self.project.eg.ratio(internal_standard=self.internal_standardOption.currentText())

			# Automatically saves the project if it already has a save location
			# self.project.reSave()

			self.graphPaneObj.updateGraph()
			self.progressPaneObj.completedStage(4)

			self.project.importListener.updateRatio()
		except:
			for l in self.project.eg.log:
					self.logger.error(l)
			#logging 
			self.logger.error('Executing stage Ratio with stage variables: [internal_standard]:{}\n['.format( self.internal_standardOption.currentText()))
			
			self.logger.exception("Exception in ratio stage:")
			return

	#@logged
	def updateStageInfo(self):
		""" Updates the stage after data is imported at runtime """

		self.internal_standardOption.clear()
		self.internal_standardOption.addItem(" ")
		for analyte in self.project.eg.analytes:
			self.internal_standardOption.addItem(str(analyte))

	#@logged
	def internal_standardClicked(self):
		""" Only allows the apply button to be activated when an internal standard option has been selected """
		if self.internal_standardOption.currentIndex() != 0:
			self.applyButton.setEnabled(True)
		else:
			self.applyButton.setEnabled(False)

	#@logged
	def loadValues(self):
		""" Loads the values saved in the project, and fills in the stage parameters with them """

		# The stage parameters are stored in project as dictionaries
		params = self.project.getStageParams("ratio")

		# If the stage isn't in the save file, we don't load it.
		if params is None:
			return

		# The stage parameters are applied to the input fields
		self.internal_standardOption.setCurrentText(params.get("internal_standard", " "))
		self.internal_standardClicked()

		# The loading process then activates the stage's apply command
		self.pressedApplyButton()

	#@logged
	def enterPressed(self):
		""" When enter is pressed on this stage """
		if self.applyButton.isEnabled():
			self.pressedApplyButton()

	def userGuide(self):
		""" Opens the online user guide to a particular page for the current stage """
		self.stageControls.userGuide(self.guideDomain + "LAtoolsGUIUserGuide/users/07-ratio.html")

	def reportButtonClick(self):
		""" Links to the online form for reporting an issue """
		self.stageControls.reportIssue(self.reportIssue)

