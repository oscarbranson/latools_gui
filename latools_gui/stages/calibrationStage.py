""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDesktopServices, QIntValidator
from PyQt5.QtCore import QUrl, Qt
import latools as la
import inspect
import templates.controlsPane as controlsPane
import json
import os
import sys
import ast



import logging

class CalibrationStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	#@logged
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, calibrationWidget, project, links):
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
		calibrationWidget : QWidget
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
		self.calibrationWidget = calibrationWidget
		self.project = project
		self.guideDomain = links[0]
		self.reportIssue = links[1]
		self.imported_srms = False

		# We create a controls pane object which covers the general aspects of the stage's controls pane
		self.stageControls = controlsPane.ControlsPane(stageLayout)
		self.srmfile = None
		self.srmList = []
		self.autoApplyButton = False

		# We capture the default parameters for this stage's function call
		self.defaultParams = self.stageControls.getDefaultParameters(inspect.signature(la.analyse.calibrate))

		# We import the stage information from a json file
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), 'information/calibrationStageInfo.json')
			infoFile = infoFile.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			infoFile = "information/calibrationStageInfo.json"

		with open(infoFile, "r") as read_file:
			self.stageInfo = json.load(read_file)
			read_file.close()

		# We set the title and description for the stage

		self.stageControls.setDescription("Calibration", self.stageInfo["stage_description"])

		# The space for the stage options is provided by the Controls Pane.
		self.optionsHBox = QHBoxLayout(self.stageControls.getOptionsWidget())

		# We create a panel on the left for options
		self.optionsLeftWidget = QWidget()
		self.optionsLeft = QGridLayout(self.optionsLeftWidget)
		self.optionsHBox.addWidget(self.optionsLeftWidget)

		# We create an area to hold the SRM list
		self.analytesWidget = QWidget()

		self.scroll = QScrollArea()
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll.setWidgetResizable(True)
		self.scroll.setMinimumWidth(70)

		self.innerWidget = QWidget()
		self.innerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		self.optionsRight = QVBoxLayout(self.innerWidget)
		self.optionsHBox.addWidget(self.scroll)

		self.analytesWidget.scroll = self.scroll

		self.scroll.setWidget(self.innerWidget)

		# We define the stage options and add them to the Controls Pane

		self.drift_correctOption = QCheckBox(self.stageInfo["drift_correct_label"])
		self.drift_correctOption.setChecked(self.defaultParams['drift_correct'] == 'True')
		self.optionsLeft.addWidget(self.drift_correctOption, 0, 0, 1, 2)
		self.drift_correctOption.setToolTip(self.stageInfo["drift_correct_description"])

		self.optionsRight.addWidget(QLabel("<span style=\"color:#779999; font-weight:bold\">" +
									self.stageInfo["standard_label"] + "</span>"))

		#self.zero_interceptOption = QCheckBox(self.stageInfo["zero_intercept_label"])
		#self.zero_interceptOption.setChecked(self.defaultParams['zero_intercept'] == 'True')
		#self.optionsLeft.addWidget(self.zero_interceptOption, 1, 0)
		#self.zero_interceptOption.setToolTip(self.stageInfo["zero_intercept_description"])

		self.n_minLabel = QLabel(self.stageInfo["n_min_label"])
		self.n_minOption = QLineEdit(self.defaultParams['n_min'])
		self.optionsLeft.addWidget(self.n_minLabel, 2, 0)
		self.optionsLeft.addWidget(self.n_minOption, 2, 1)
		self.n_minOption.setToolTip(self.stageInfo["n_min_description"])
		self.n_minLabel.setToolTip(self.stageInfo["n_min_description"])

		self.reloadButton = QPushButton("View SRM table")
		self.reloadButton.clicked.connect(self.pressedReloadButton)
		self.stageControls.addApplyButton(self.reloadButton)
		self.reloadButton.setToolTip(self.stageInfo["srm_button_description"])

		# We create the buttons for the top of the right-most section of the Controls Pane.

		self.defaultButton = QPushButton("Defaults")
		self.defaultButton.clicked.connect(self.defaultButtonPress)
		self.stageControls.addDefaultButton(self.defaultButton)

		# We create a button to link to the user guide
		self.guideButton = QPushButton("User guide")
		self.guideButton.clicked.connect(self.userGuide)
		self.stageControls.addDefaultButton(self.guideButton)

		# We create a button to link to the form for reporting an issue
		self.reportButton = QPushButton("Report an issue")
		self.reportButton.clicked.connect(self.reportButtonClick)
		self.stageControls.addDefaultButton(self.reportButton)
		self.reportButton.setToolTip(links[2])

		# We create the buttons for the bottom of the right-most section of the Controls Pane.

		self.calcButton = QPushButton("Calculate calibration")
		self.calcButton.clicked.connect(self.pressedCalculateButton)
		#self.stageControls.addApplyButton(self.calcButton)

		self.popupButton = QPushButton("Plot in popup")
		self.popupButton.clicked.connect(self.pressedPopupButton)
		self.stageControls.addApplyButton(self.popupButton)
		self.popupButton.setEnabled(False)

		self.applyButton = QPushButton("Apply calibration")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)
		# self.applyButton.setEnabled(False)

		#Logger
		self.logger = logging.getLogger(__name__)
		self.logger.info('initialised calibration')

		#Validation
		self.n_minOption.setValidator(QIntValidator())

	#@logged
	def pressedApplyButton(self):
		""" Calibrates the project data when a button is pressed. """

		# We process each text entry field by converting blank to the value None, and checking for errors
		myn_min = int(self.defaultParams['n_min'])
		if self.n_minOption.text() != "":
			try:
				myn_min = int(self.n_minOption.text())
			except:
				self.raiseError("The 'n_min' value must be an integer")
				return

		srmParam = []
		for srm in self.srmList:
			if srm[0].isChecked():
				srmParam.append(srm[1])

		# The actual call to the analyse object for this stage is run, using the stage values as parameters
		try:
			self.project.eg.calibrate(analytes=None,
								drift_correct=self.drift_correctOption.isChecked(),
								srms_used=srmParam,
								#zero_intercept=self.zero_interceptOption.isChecked(),
								n_min=myn_min)
		except:
			for l in self.project.eg.log:
					self.logger.error(l)
					self.logger.info('Executing stage Calibration with stage variables: [drift_correct]:{}\n[srms_used]:{}\n'
							 '[n_min]:{}\n'.format( self.drift_correctOption.isChecked(),
											srmParam,
											#self.zero_interceptOption.isChecked(),
											myn_min))
			self.logger.exception("Exception occured in calibration stage:")
			self.raiseError("A problem occurred. There may be a problem with the input values.")
			return
		self.graphPaneObj.updateGraph()

		self.popupButton.setEnabled(True)

		self.progressPaneObj.completedStage(5)

		# Automatically saves the project if it already has a save location
		# self.project.reSave()

		# Pop-up button press added to the apply button
		# TO DO: review this.
		if not self.autoApplyButton:
			self.pressedPopupButton()
		self.autoApplyButton = False

	#@logged
	def pressedReloadButton(self):
		""" Performs a reload when the button is pressed. """

		url = QUrl.fromLocalFile(self.srmfile)
		QDesktopServices.openUrl(url)

		print(self.srmfile)

	#@logged
	def updateStageInfo(self):
		""" Updates the stage after data is imported at runtime """

		if not self.imported_srms:

			self.srmfile = self.project.eg.srmfile

			srms = la.helpers.srm.get_defined_srms(self.project.eg.srmfile)

			for i in range(len(srms)):
				self.srmList.append((QCheckBox(srms[i]), srms[i]))
				self.srmList[i][0].setChecked(True)
				self.optionsRight.addWidget(self.srmList[i][0])
			self.optionsRight.addStretch(1)

			self.imported_srms = True

	#@logged
	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.calibrationWidget, "Error", message, QMessageBox.Ok)

	#@logged
	def loadValues(self):
		""" Loads the values saved in the project, and fills in the stage parameters with them """

		# The stage parameters are stored in project as dictionaries
		params = self.project.getStageParams("calibrate")

		# The stage parameters are applied to the input fields
		self.fillValues(params)

		# Setting the srms_used, we get the saved list of strings
		srms = params.get("srms_used", None)
		if srms is not None:

			# All srms are turned off
			for box in self.srmList:
				box[0].setChecked(False)

			# The listed srms are turned on
			for srmString in srms:
				for box in self.srmList:
					if box[1] == srmString:
						box[0].setChecked(True)

		# The loading process then activates the stage's apply command
		self.autoApplyButton = True
		self.pressedApplyButton()

	def fillValues(self, params):
		"""
		Fills the stage parameters from a given dictionary

		Parameters
			----------
			params : dict
				The key-word arguments of the stage call, saved in the lalog file.
		"""

		# The keyword arguments are added to the control fields
		if params is not None:
			self.drift_correctOption.setChecked(params.get("drift_correct", True))
			#self.zero_interceptOption.setChecked(params.get("zero_intercept", True))
			self.n_minOption.setText(str(params.get("n_min", 10)))

	#@logged
	def enterPressed(self):
		""" When enter is pressed on this stage """
		if self.applyButton.isEnabled():
			self.pressedApplyButton()

	#@logged
	def pressedPopupButton(self):
		""" When the user presses the plot in popup button """
		self.graphPaneObj.showAuxGraph(cali=True)

	#@logged
	def pressedCalculateButton(self):
		""" When the user presses the calculate button """
		self.applyButton.setEnabled(True)

	#@logged
	def defaultButtonPress(self):
		""" Returns the option values to their default states """

		params = {
			"drift_correct": self.defaultParams['drift_correct'] == 'True',
			"zero_intercept": self.defaultParams['zero_intercept'] == 'True',
			"n_min": self.defaultParams['n_min']
		}

		for box in self.srmList:
			box[0].setChecked(True)

		self.fillValues(params)

	#@logged
	def ChooseCalibrationButtonPress(self):
		pass

	def userGuide(self):
		""" Opens the online user guide to a particular page for the current stage """
		self.stageControls.userGuide(self.guideDomain + "LAtoolsGUIUserGuide/users/08-calibration.html")

	def updateRatio(self):
		self.popupButton.setEnabled(False)
		#self.applyButton.setEnabled(False)

	def reportButtonClick(self):
		""" Links to the online form for reporting an issue """
		self.stageControls.reportIssue(self.reportIssue)
