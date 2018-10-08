""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import latools as la
import inspect
import templates.controlsPane as controlsPane
import json
import ast
import sys
import os

import logging

class DespikingStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	#@logged
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, despikingWidget, project, links):
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
		despikingWidget : QWidget
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
		self.despikingWidget = despikingWidget
		self.project = project
		self.guideDomain = links[0]
		self.reportIssue = links[1]

		# We create a controls pane object which covers the general aspects of the stage's controls pane
		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We capture the default parameters for this stage's function call
		self.defaultParams = self.stageControls.getDefaultParameters(inspect.signature(la.analyse.despike))

		# We import the stage information from a json file
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), 'information/despikeStageInfo.json')
			infoFile = infoFile.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			infoFile = "information/despikeStageInfo.json"

		with open(infoFile, "r") as read_file:
			self.stageInfo = json.load(read_file)
			read_file.close()

		# We set the title and description for the stage

		self.stageControls.setDescription("Data De-spiking", self.stageInfo["stage_description"])

		# The space for the stage options is provided by the Controls Pane.

		self.optionsGrid = QHBoxLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		# We make two despiking option areas, called pane1 and pane2

		# We create the first pane of options
		self.pane1VWidget = QWidget()
		self.pane1VLayout = QVBoxLayout(self.pane1VWidget)
		self.exponentialLabel = QLabel(self.stageInfo["despike_1"])
		self.pane1VLayout.addWidget(self.exponentialLabel)

		self.pane1Frame = QFrame()
		self.pane1Frame.setFrameShape(QFrame.StyledPanel)
		self.pane1Frame.setFrameShadow(QFrame.Raised)

		self.pane1Layout = QGridLayout(self.pane1Frame)
		self.pane1VLayout.addWidget(self.pane1Frame)

		self.pane1VLayout.addStretch(1)

		self.optionsGrid.addWidget(self.pane1VWidget)

		# We add the exp decay option
		self.pane1expdecayOption = QCheckBox(self.stageInfo["exp_decay_label"])
		self.pane1expdecayOption.setChecked(self.defaultParams['expdecay_despiker'] == 'True')
		self.pane1Layout.addWidget(self.pane1expdecayOption, 0, 0, 1, 0)
		self.pane1expdecayOption.setToolTip(self.stageInfo["exp_decay_description"])

		# We add the exponent option
		self.pane1ExponentLabel = QLabel(self.stageInfo["exponent_label"])
		self.pane1Exponent = QLineEdit(self.defaultParams['exponent'])
		self.pane1Layout.addWidget(self.pane1ExponentLabel, 1, 0)
		self.pane1Layout.addWidget(self.pane1Exponent, 1, 1)
		self.pane1Exponent.setToolTip(self.stageInfo["exponent_description"])
		self.pane1ExponentLabel.setToolTip(self.stageInfo["exponent_description"])
		self.pane1Exponent.setPlaceholderText("auto")

		#self.pane1Maxiter = QLineEdit(self.defaultParams('maxiter'))
		#self.pane1Layout.addWidget(QLabel("maxiter"), 2, 0)
		#self.pane1Layout.addWidget(self.pane1Maxiter, 2, 1)

		# Second pane

		self.pane2VWidget = QWidget()
		self.pane2VLayout = QVBoxLayout(self.pane2VWidget)
		self.noiseLabel = QLabel(self.stageInfo["despike_2"])
		self.pane2VLayout.addWidget(self.noiseLabel)

		self.pane2Frame = QFrame()
		self.pane2Frame.setFrameShape(QFrame.StyledPanel)
		self.pane2Frame.setFrameShadow(QFrame.Raised)

		self.pane2Layout = QGridLayout(self.pane2Frame)
		self.pane2VLayout.addWidget(self.pane2Frame)
		self.pane2VLayout.addStretch(1)

		self.optionsGrid.addWidget(self.pane2VWidget)

		# We create the noise option
		self.pane2NoiseOption = QCheckBox(self.stageInfo["noise_label"])
		self.pane2NoiseOption.setChecked(self.defaultParams['noise_despiker'] == 'True')
		self.pane2Layout.addWidget(self.pane2NoiseOption, 0, 0, 1, 0)
		self.pane2NoiseOption.setToolTip(self.stageInfo["noise_description"])

		# We create the win option
		self.winLabel = QLabel(self.stageInfo["win_label"])
		self.pane2win = QLineEdit(self.defaultParams['win'])
		self.pane2Layout.addWidget(self.winLabel, 1, 0)
		self.pane2Layout.addWidget(self.pane2win, 1, 1)
		self.pane2win.setToolTip(self.stageInfo["win_description"])
		self.winLabel.setToolTip(self.stageInfo["win_description"])

		# We create the nlim option
		self.nlimLabel = QLabel(self.stageInfo["nlim_label"])
		self.pane2nlim = QLineEdit(self.defaultParams['nlim']) #nlim
		self.pane2Layout.addWidget(self.nlimLabel, 2, 0)
		self.pane2Layout.addWidget(self.pane2nlim, 2, 1)
		self.pane2nlim.setToolTip(self.stageInfo["nlim_description"])
		self.nlimLabel.setToolTip(self.stageInfo["nlim_description"])

		# We create the maxiter option
		self.maxiterLabel = QLabel(self.stageInfo["maxiter_label"])
		self.pane2Maxiter = QLineEdit(self.defaultParams['maxiter'])
		self.pane2Layout.addWidget(self.maxiterLabel, 3, 0)
		self.pane2Layout.addWidget(self.pane2Maxiter, 3, 1)
		self.pane2Maxiter.setToolTip(self.stageInfo["maxiter_description"])
		self.maxiterLabel.setToolTip(self.stageInfo["maxiter_description"])

		# We create a reset to default button
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

		# We create the button for the right-most section of the Controls Pane.

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

		self.pane1Exponent.setValidator(QDoubleValidator())
		self.pane2win.setValidator(QDoubleValidator())
		self.pane2nlim.setValidator(QDoubleValidator())
		self.pane2Maxiter.setValidator(QIntValidator())
		
		self.logger=logging.getLogger(__name__)
		self.logger.info('Initialised despiking stage')

	#@logged
	def pressedApplyButton(self):
		""" Applies a despiking filter to the project data when a button is pressed. """

		# We process each text entry field by converting blank to the value None, and checking for errors
		localExponent = None
		self.logger.info('Pressed button')
		if (self.pane1Exponent.text() != ""):
			try:
				localExponent = float(self.pane1Exponent.text())
			except:
				self.logger.exception("value fail")
				self.raiseError("The exponent value must be a floating point number")
				return

		localWin = 3
		if (self.pane2win.text() != ""):
			try:
				localWin = float(self.pane2win.text())
			except:
				self.logger.exception("value fail")
				self.raiseError("The 'win' value must be a floating point number")
				return

		localNlim = 12.0
		if (self.pane2nlim.text() != ""):
			try:
				localNlim = float(self.pane2nlim.text())
			except:
				self.logger.exception("value fail")
				self.raiseError("The 'nlim' value must be a floating point number")
				return

		localMaxiter = 4
		if (self.pane2Maxiter.text() != ""):
			try:
				localMaxiter = int(self.pane2Maxiter.text())
			except:
				self.logger.exception("value fail")
				self.raiseError("The 'maxiter' value must be an integer")
				return

		# The actual call to the analyse object for this stage is run, using the stage values as parameters
		try:
			self.project.eg.despike(expdecay_despiker=self.pane1expdecayOption.isChecked(),
								exponent=localExponent,
								noise_despiker=self.pane2NoiseOption.isChecked(),
								win=localWin,
								nlim=localNlim,
								exponentplot=False,
								maxiter=localMaxiter)
		except:
			for l in self.eg.log:
				self.logger.error(self.eg.log(l))
			self.logger.error('Executing despiking stage with stage variables: [expdecay_despiker]:'
							 '{}\n[exponent]:{}\n[noise_despiker]:{}\n[win]:{}\n[nlim]:{}\n[maxiter]'
							 ':{}\n'.format( self.pane1expdecayOption.isChecked(),
											 localExponent,
											 self.pane2NoiseOption.isChecked(),
											 localWin,
											 localNlim,
											 localMaxiter))
			self.logger.exception("Problem occured in despiking stage:")
			self.raiseError("A problem occurred. There may be a problem with the input values.")
			return

		# If the exponential decay despiker is applied without specifying the 'exponent' option, the automatically
		# calculated value is provided to the exponent textbox.
		if self.pane1expdecayOption.isChecked():
			try :
				self.pane1Exponent.setText(str(self.project.eg.expdecay_coef[0]))
			except:
				pass
				#self.raiseError("A problem has occured with your exponent. Please check that the value is correct")
				#return

		self.graphPaneObj.updateGraph()
		self.progressPaneObj.completedStage(1)

		# Automatically saves the project if it already has a save location
		# self.project.reSave()

	#@logged
	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.despikingWidget, "Error", message, QMessageBox.Ok)

	#@logged
	def loadValues(self):
		""" Loads the values saved in the project, and fills in the stage parameters with them """

		# The stage parameters are stored in project as dictionaries
		params = self.project.getStageParams("despike")

		# The stage parameters are applied to the input fields
		self.fillValues(params)

		# The loading process then activates the stage's apply command
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
			self.pane1expdecayOption.setChecked(params.get("expdecay_despiker", False))
			self.pane1Exponent.setText(str(params.get("exponent", "")))
			self.pane2NoiseOption.setChecked(params.get("noise_despiker", True))
			self.pane2win.setText(str(params.get("win", "")))
			self.pane2nlim.setText(str(params.get("nlim", "")))
			# exponentplot value?
			self.pane2Maxiter.setText(str(params.get("maxiter", 4)))

	#@logged
	def enterPressed(self):
		""" When enter is pressed on this stage """
		if self.applyButton.isEnabled():
			self.pressedApplyButton()

	#@logged
	def defaultButtonPress(self):
		""" Returns the option values to their default states """
		params = {
			"expdecay_despiker": self.defaultParams['expdecay_despiker'] == 'True',
			"exponent": self.defaultParams["exponent"],
			"noise_despiker": self.defaultParams['noise_despiker'] == 'True',
			"win": self.defaultParams['win'],
			"nlim": self.defaultParams['nlim'],
			"maxiter": self.defaultParams['maxiter']
		}
		self.fillValues(params)

	def userGuide(self):
		""" Opens the online user guide to a particular page for the current stage """
		self.stageControls.userGuide(self.guideDomain + "LAtoolsGUIUserGuide/users/04-data-despiking.html")

	def reportButtonClick(self):
		""" Links to the online form for reporting an issue """
		self.stageControls.reportIssue(self.reportIssue)
