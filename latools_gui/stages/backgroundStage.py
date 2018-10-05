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

from project.ErrLogger import logged
import logging

class BackgroundStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	#@logged
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, backgroundWidget, project, links):
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
		project : RunningProject
			A reference to the project object which contains all of the information unique to this project,
			including the latools analyse object that the stages will update.
		"""

		self.graphPaneObj = graphPaneObj
		self.progressPaneObj = progressPaneObj
		self.backgroundWidget = backgroundWidget
		self.project = project
		self.guideDomain = links[0]
		self.reportIssue = links[1]

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We capture the default parameters for this stage's function call
		self.defaultWeightParams = self.stageControls.getDefaultParameters(
			inspect.signature(la.analyse.bkg_calc_weightedmean))

		self.defaultInterParams = self.stageControls.getDefaultParameters(
			inspect.signature(la.analyse.bkg_calc_interp1d))

		# We import the stage information from a json file
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), 'information/backgroundStageInfo.json')
			infoFile = infoFile.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			infoFile = "information/backgroundStageInfo.json"

		with open(infoFile, "r") as read_file:
			self.stageInfo = json.load(read_file)
			read_file.close()

		# We set the title and description for the stage

		self.stageControls.setDescription("Background Correction", self.stageInfo["stage_description"])

		# The space for the stage options is provided by the Controls Pane.
		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		self.methodOption = QComboBox()
		self.methodOption.addItem(self.stageInfo["bkg_method_1_label"])
		self.methodOption.addItem(self.stageInfo["bkg_method_2_label"])


		# When methodOption is changed, it calls methodUpdate
		self.methodOption.activated.connect(self.methodUpdate)
		self.optionsGrid.addWidget(QLabel(self.stageInfo["bkg_method_label"]), 0, 0)
		self.optionsGrid.addWidget(self.methodOption, 0, 1)

		# Set up a layout that will only be displayed when bkg_calc_weightedmean is selected
		self.methodWidget1 = QWidget()
		self.methodLayout1 = QGridLayout(self.methodWidget1)

		self.weight_fwhmLabel = QLabel(self.stageInfo["weight_fwhm_label"])
		self.weight_fwhmOption = QLineEdit(self.defaultWeightParams['weight_fwhm'])
		self.methodLayout1.addWidget(self.weight_fwhmLabel, 0, 0)
		self.methodLayout1.addWidget(self.weight_fwhmOption, 0, 1)
		self.weight_fwhmOption.setToolTip(self.stageInfo["weight_fwhm_description"])
		self.weight_fwhmLabel.setToolTip(self.stageInfo["weight_fwhm_description"])
		self.weight_fwhmOption.setPlaceholderText("auto")

		self.n_minLabel = QLabel(self.stageInfo["n_min_label"])
		self.n_minOption = QLineEdit(self.defaultWeightParams['n_min'])
		self.methodLayout1.addWidget(self.n_minLabel, 0, 2)
		self.methodLayout1.addWidget(self.n_minOption, 0, 3)
		self.n_minOption.setToolTip(self.stageInfo["n_min_description"])
		self.n_minLabel.setToolTip(self.stageInfo["n_min_description"])

		self.n_maxLabel = QLabel(self.stageInfo["n_max_label"])
		self.n_maxOption = QLineEdit(self.defaultWeightParams['n_max'])
		self.methodLayout1.addWidget(self.n_maxLabel, 0, 4)
		self.methodLayout1.addWidget(self.n_maxOption, 0, 5)
		self.n_maxOption.setToolTip(self.stageInfo["n_max_description"])
		self.n_maxLabel.setToolTip(self.stageInfo["n_max_description"])


		# Apply the bkg_calc_weightedmean options as default
		self.currentlyMethod1 = True
		self.optionsGrid.addWidget(self.methodWidget1, 1, 0, 1, 2)

		# Set up a layout for when "bkg_calc_interp1d" is selected
		self.methodWidget2 = QWidget()
		self.methodLayout2 = QGridLayout(self.methodWidget2)

		self.kind_label = QLabel(self.stageInfo["kind_label"])
		self.kindOption = QLineEdit(self.defaultInterParams['kind'])
		self.methodLayout2.addWidget(self.kind_label, 0, 0)
		self.methodLayout2.addWidget(self.kindOption, 0, 1)
		self.kindOption.setToolTip(self.stageInfo["kind_description"])
		self.kind_label.setToolTip(self.stageInfo["kind_description"])

		self.n_min2Label = QLabel(self.stageInfo["n_min_label"])
		self.n_minOption2 = QLineEdit(self.defaultInterParams['n_min'])
		self.methodLayout2.addWidget(self.n_min2Label, 0, 2)
		self.methodLayout2.addWidget(self.n_minOption2, 0, 3)
		self.n_minOption2.setToolTip(self.stageInfo["n_min_description"])
		self.n_min2Label.setToolTip(self.stageInfo["n_min_description"])

		self.n_max2Label = QLabel(self.stageInfo["n_max_label"])
		self.n_maxOption2 = QLineEdit(self.defaultInterParams['n_max'])
		self.methodLayout2.addWidget(self.n_max2Label, 0, 4)
		self.methodLayout2.addWidget(self.n_maxOption2, 0, 5)
		self.n_maxOption2.setToolTip(self.stageInfo["n_max_description"])
		self.n_max2Label.setToolTip(self.stageInfo["n_max_description"])

		# Add the universal options
		self.cstepLabel = QLabel(self.stageInfo["cstep_label"])
		self.cstepOption = QLineEdit(self.defaultWeightParams['cstep'])
		self.optionsGrid.addWidget(self.cstepLabel, 2, 0)
		self.optionsGrid.addWidget(self.cstepOption, 2, 1, 1, 1)
		self.cstepOption.setToolTip(self.stageInfo["cstep_description"])
		self.cstepLabel.setToolTip(self.stageInfo["cstep_description"])
		self.cstepOption.setPlaceholderText("auto")

		self.bkg_filterOption = QCheckBox(self.stageInfo["bkg_filter_label"])
		self.optionsGrid.addWidget(self.bkg_filterOption, 3, 0)
		self.bkg_filterOption.setChecked(self.defaultWeightParams['bkg_filter'] == 'True')
		self.bkg_filterOption.setToolTip(self.stageInfo["bkg_filter_description"])

		# We set up a click function for the checkbox
		self.bkg_filterOption.stateChanged.connect(self.bkgUpdate)

		# Set up a layout that will only be displayed when bkg_filter is checked
		self.bkgWidget = QWidget()
		self.bkgLayout = QGridLayout(self.bkgWidget)

		self.f_winOption = QLineEdit(self.defaultWeightParams['f_win'])
		self.f_winLabel = QLabel(self.stageInfo["f_win_label"])
		self.bkgLayout.addWidget(self.f_winLabel, 0, 0)
		self.bkgLayout.addWidget(self.f_winOption, 0, 1)
		self.f_winOption.setToolTip(self.stageInfo["f_win_description"])
		self.f_winLabel.setToolTip(self.stageInfo["f_win_description"])

		self.f_n_limOption = QLineEdit(self.defaultWeightParams['f_n_lim'])
		self.f_n_limLabel = QLabel(self.stageInfo["f_n_lim_label"])
		self.bkgLayout.addWidget(self.f_n_limLabel, 0, 2)
		self.bkgLayout.addWidget(self.f_n_limOption, 0, 3)
		self.f_n_limOption.setToolTip(self.stageInfo["f_n_lim_description"])
		self.f_n_limLabel.setToolTip(self.stageInfo["f_n_lim_description"])

		self.optionsGrid.addWidget(self.bkgWidget, 3, 1)

		self.f_winOption.setEnabled(False)
		self.f_n_limOption.setEnabled(False)

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

		# We create the buttons for the right-most section of the Controls Pane.

		self.calcButton = QPushButton("Calculate background")
		self.calcButton.clicked.connect(self.pressedCalcButton)
		self.stageControls.addApplyButton(self.calcButton)

		self.popupButton = QPushButton("Plot in popup")
		self.popupButton.clicked.connect(self.pressedPopupButton)
		self.stageControls.addApplyButton(self.popupButton)
		self.popupButton.setEnabled(False)

		self.subtractButton = QPushButton("Subtract background")
		self.subtractButton.clicked.connect(self.pressedSubtractButton)
		self.stageControls.addApplyButton(self.subtractButton)
		self.subtractButton.setEnabled(False)
		self.subtractButton.setToolTip(self.stageInfo["subtract_button_description"])

		#Logging
		self.logger = logging.getLogger(__name__)
		self.logger.info('Background initialised')

		#Validation
		self.weight_fwhmOption.setValidator(QDoubleValidator())
		self.n_minOption.setValidator(QIntValidator())
		self.n_maxOption.setValidator(QIntValidator())
		self.cstepOption.setValidator(QDoubleValidator())
		self.f_winOption.setValidator(QIntValidator())
		self.f_n_limOption.setValidator(QIntValidator())
		self.kindOption.setValidator(QIntValidator())
		self.n_minOption2.setValidator(QIntValidator())
		self.n_maxOption2.setValidator(QIntValidator())

	#@logged
	def pressedCalcButton(self):
		""" Applies a background calculation on the project data when a button is pressed, making sure there are
		no illegal inputs.

		"""
			    
		# There are two different calculation methods for this stage
		if (self.currentlyMethod1):

			# We process each text entry field by converting blank to the value None, and checking for errors
			myweight = None
			if self.weight_fwhmOption.text() != "":
				try:
					myweight = float(self.weight_fwhmOption.text())
				except:
					self.logger.exception("Invalid value")
					self.raiseError("The 'weight_fwhm' value must be a floating point number")
					return

			myn_min = 20
			if self.n_minOption.text() != "":
				try:
					myn_min = int(self.n_minOption.text())
				except:
					self.logger.exception("Invalid value")
					self.raiseError("The 'n_min' value must be an integer")
					return

			myn_max = None
			if self.n_maxOption.text() != "":
				try:
					myn_max = int(self.n_maxOption.text())
				except:
					self.logger.exception("Invalid value")
					self.raiseError("The 'n_max' value must be an integer")
					return

			mycstep = None
			if self.cstepOption.text() != "":
				try:
					mycstep = float(self.cstepOption.text())
				except:
					self.logger.exception("Invalid value")
					self.raiseError("The 'cstep' value must be a floating point number")
					return

			myf_win = 7
			if self.f_winOption.text() != "":
				try:
					myf_win = int(self.f_winOption.text())
				except:
					self.logger.exception("Invalid value")
					self.raiseError("The 'f_win' value must be an integer")
					return

			myf_n_lim = 3
			if self.f_n_limOption.text() != "":
				try:
					myf_n_lim = int(self.f_n_limOption.text())
				except:
					self.logger.exception("Invalid value")
					self.raiseError("The 'f_n_lim' value must be an integer")
					return

			# The actual call to the analyse object for this stage is run, using the stage values as parameters
			try:
				# logging 
				self.logger.info('Executing stage Import with stage variables: [weight_fwhm]:{}\n[n_min]:{}\n[n_max]:'
								 '{}\n[cstep]:{}\n[bkg_filter]:{}\n[f_win]:{}\n[f_n_lim]:{}\n'.format( myweight,
																								     myn_min,
																								     myn_max,
																								     mycstep,
																								     self.bkg_filterOption.isChecked(),
																								     myf_win,
																								     myf_n_lim))
				
				self.project.eg.bkg_calc_weightedmean(analytes=None,
								      weight_fwhm=myweight,
								      n_min=myn_min,
								      n_max=myn_max,
								      cstep=mycstep,
								      bkg_filter=self.bkg_filterOption.isChecked(),
								      f_win=myf_win,
								      f_n_lim=myf_n_lim)
			except:
				self.logger.exception("Exception in background stage:")
				self.raiseError("A problem occurred. There may be a problem with the input values.")
				return
		else:

			# We protect against blank or incorrect fields in options
			myKind = 1
			if self.kindOption.text() != "":
				try:
					myKind = int(self.kindOption.text())
				except:
					self.raiseError("The 'kind' value must be an integer")
					return

			myn_min2 = 10
			if self.n_minOption2.text() != "":
				try:
					myn_min2 = int(self.n_minOption2.text())
				except:
					self.raiseError("The 'n_min' value must be an integer")
					return

			myn_max2 = None
			if self.n_maxOption2.text() != "":
				try:
					myn_max2 = int(self.n_maxOption2.text())
				except:
					self.raiseError("The 'n_max' value must be an integer")
					return

			mycstep = None
			if self.cstepOption.text() != "":
				try:
					mycstep = float(self.cstepOption.text())
				except:
					self.raiseError("The 'cstep' value must be a floating point number")
					return

			myf_win = 7
			if self.f_winOption.text() != "":
				try:
					myf_win = int(self.f_winOption.text())
				except:
					self.raiseError("The 'f_win' value must be an integer")
					return

			myf_n_lim = 3
			if self.f_n_limOption.text() != "":
				try:
					myf_n_lim = int(self.f_n_limOption.text())
				except:
					self.raiseError("The 'f_n_lim' value must be an integer")
					return

			try:
				self.project.eg.bkg_calc_interp1d(analytes=None,
											kind=myKind,
											n_min=myn_min2,
											n_max=myn_max2,
											cstep=mycstep,
											bkg_filter=self.bkg_filterOption.isChecked(),
											f_win=myf_win,
											f_n_lim=myf_n_lim)
			except:
				self.logger.exception("Exception in background stage:")
				self.raiseError("A problem occurred. There may be a problem with the input values.")
				return

		self.graphPaneObj.updateBkg()

		# The background calculation is now complete, and can now be subtracted and plotted
		self.subtractButton.setEnabled(True)
		self.popupButton.setEnabled(True)

		# Automatically saves the project if it already has a save location
		# self.project.reSave()

	#@logged
	def pressedPopupButton(self):
		""" Creates a popup for the background calculation when a button is pressed. """

		self.graphPaneObj.showAuxGraph(bkg=True)

	#@logged
	def pressedSubtractButton(self):
		""" Subtracts an existing background calculation from the project data when a button is pressed. """
		self.project.eg.bkg_subtract(analytes=None, errtype='stderr', focus_stage='despiked')
		self.graphPaneObj.updateGraph()
		self.progressPaneObj.completedStage(3)

	#@logged
	def methodUpdate(self):
		""" Updates the current method. """

		if self.methodOption.currentText() == self.stageInfo["bkg_method_1_label"]:
			self.methodWidget2.setParent(None)
			self.optionsGrid.addWidget(self.methodWidget1, 1, 0, 1, 2)
			self.currentlyMethod1 = True
		else:
			self.methodWidget1.setParent(None)
			self.optionsGrid.addWidget(self.methodWidget2, 1, 0, 1, 2)
			self.currentlyMethod1 = False

	#@logged
	def bkgUpdate(self):
		""" Hides the last two input fields unless the bkg_filter button is ticked """
		if self.bkg_filterOption.isChecked():
			self.f_winOption.setEnabled(True)
			self.f_n_limOption.setEnabled(True)
		else:
			self.f_winOption.setEnabled(False)
			self.f_n_limOption.setEnabled(False)

	#@logged
	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.backgroundWidget, "Error", message, QMessageBox.Ok)

	#@logged
	def resetButtons(self):
		self.popupButton.setEnabled(False)
		self.subtractButton.setEnabled(False)

	#@logged
	def loadValues(self):
		""" Loads the values saved in the project, and fills in the stage parameters with them """

		# The stage parameters are stored in project as dictionaries
		params = self.project.getStageParams("bkg_calc_weightedmean")

		# The stage parameters are applied to the input fields
		# bkg_calc_weightedmean, or bkg_calc_interp1d will be in stageParams dictionary, but not both.
		# We define all stage values based on which entry exists (ie. was performed most recently)
		if params is not None:
			self.methodOption.setCurrentText("bkg_calc_weightedmean")

			self.weight_fwhmOption.setText(str(params.get("weight_fwhm", "")))
			self.n_minOption.setText(str(params.get("n_min", 20)))
			self.n_maxOption.setText(str(params.get("n_max", "")))

			self.cstepOption.setText(str(params.get("cstep", "")))
			self.bkg_filterOption.setChecked(params.get("bkg_filter", False))
			self.f_winOption.setText(str(params.get("f_win", 7)))
			self.f_n_limOption.setText(str(params.get("f_n_lim", 3)))

		else:
			params = self.project.getStageParams("bkg_calc_interp1d")
			if params is not None:
				self.methodOption.setCurrentText("bkg_calc_interp1d")

				self.kindOption.setText(str(params.get("kind", 1)))
				self.n_minOption2.setText(str(params.get("n_min", 10)))
				self.n_maxOption2.setText(str(params.get("n_max", "")))

				self.cstepOption.setText(str(params.get("cstep", "")))
				self.bkg_filterOption.setChecked(params.get("bkg_filter", False))
				self.f_winOption.setText(str(params.get("f_win", 7)))
				self.f_n_limOption.setText(str(params.get("f_n_lim", 3)))

				self.methodUpdate()

		# The loading process then activates the stage's apply command
		self.pressedCalcButton()
		self.pressedSubtractButton()

	#@logged
	def enterPressed(self):
		""" When enter is pressed on this stage """
		if self.subtractButton.isEnabled():
			self.pressedSubtractButton()

	#@logged
	def defaultButtonPress(self):

		self.methodOption.setCurrentText(self.stageInfo["bkg_method_1_label"])

		self.weight_fwhmOption.setText(self.defaultWeightParams['weight_fwhm'])
		self.n_minOption.setText(self.defaultWeightParams['n_min'])
		self.n_maxOption.setText(self.defaultWeightParams['n_max'])

		self.cstepOption.setText(self.defaultWeightParams['cstep'])
		self.bkg_filterOption.setChecked(self.defaultWeightParams['bkg_filter'] == 'True')
		self.f_winOption.setText(self.defaultWeightParams['f_win'])
		self.f_n_limOption.setText(self.defaultWeightParams['f_n_lim'])

		self.kindOption.setText(self.defaultInterParams['kind'])
		self.n_minOption2.setText(self.defaultInterParams['n_min'])
		self.n_maxOption2.setText(self.defaultInterParams['n_max'])

		self.methodUpdate()
		self.bkgUpdate()

	def userGuide(self):
		""" Opens the online user guide to a particular page for the current stage """
		self.stageControls.userGuide(self.guideDomain + "LAtoolsGUIUserGuide/users/06-background.html")

	def reportButtonClick(self):
		""" Links to the online form for reporting an issue """
		self.stageControls.reportIssue(self.reportIssue)
