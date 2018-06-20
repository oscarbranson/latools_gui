""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, Qt
import latools as la
import inspect
import templates.controlsPane as controlsPane
import ast

class CalibrationStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, calibrationWidget, project):
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
		self.calibrationWidget = calibrationWidget
		self.project = project

		self.stageControls = controlsPane.ControlsPane(stageLayout)
		self.srmfile = None
		self.srmList = []

		# We capture the default parameters for this stage's function call
		self.defaultParams = self.stageControls.getDefaultParameters(inspect.signature(la.analyse.calibrate))

		# We set the title and description for the stage

		self.stageControls.setDescription("Calibration", """
			Once all your data are normalised to an internal standard, you’re ready to calibrate 
			the data. This is done by creating a calibration curve for each element based on SRMs 
			measured throughout your analysis session, and a table of known SRM values.""")

		# The space for the stage options is provided by the Controls Pane.
		self.optionsHBox = QHBoxLayout(self.stageControls.getOptionsWidget())

		self.optionsLeftWidget = QWidget()
		self.optionsLeft = QGridLayout(self.optionsLeftWidget)
		self.optionsHBox.addWidget(self.optionsLeftWidget)

		self.optionsRightWidget = QScrollArea()
		self.optionsRightWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.optionsRightWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.optionsRightWidget.setWidgetResizable(False)
		self.optionsRightWidget.setMinimumWidth(70)
		self.optionsRight = QVBoxLayout(self.optionsRightWidget)
		self.optionsHBox.addWidget(self.optionsRightWidget)

		# We define the stage options and add them to the Controls Pane

		self.drift_correctOption = QCheckBox("Drift Correction")
		self.drift_correctOption.setChecked(self.defaultParams['drift_correct'] == 'True')
		self.optionsLeft.addWidget(self.drift_correctOption, 0, 0, 1, 2)
		self.drift_correctOption.setToolTip("<qt/>Whether to interpolate calibration paraemters between SRM measurements.")


		self.optionsRight.addWidget(QLabel("srms_used"))

		self.zero_interceptOption = QCheckBox("Force Zero Intercept")
		self.zero_interceptOption.setChecked(self.defaultParams['zero_intercept'] == 'True')
		self.optionsLeft.addWidget(self.zero_interceptOption, 1, 0)
		self.zero_interceptOption.setToolTip("<qt/>Whether to force calibration lines through zero (y = mx) or not (y = mx + c).")


		self.n_minOption = QLineEdit(self.defaultParams['n_min'])
		self.optionsLeft.addWidget(QLabel("Minimum Points"), 2, 0)
		self.optionsLeft.addWidget(self.n_minOption, 2, 1)
		self.n_minOption.setToolTip("<qt/>The minimum number of data points an SRM measurement must have to be included.")

		self.reloadButton = QPushButton("View SRM table")
		self.reloadButton.clicked.connect(self.pressedReloadButton)
		self.stageControls.addApplyButton(self.reloadButton)

		# We create the buttons for the right-most section of the Controls Pane.

		self.calcButton = QPushButton("Calculate calibration")
		self.calcButton.clicked.connect(self.pressedCalculateButton)
		self.stageControls.addApplyButton(self.calcButton)

		self.popupButton = QPushButton("Plot in popup")
		self.popupButton.clicked.connect(self.pressedPopupButton)
		self.stageControls.addApplyButton(self.popupButton)
		# self.popupButton.setEnabled(False)

		self.applyButton = QPushButton("Apply calibration")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)
		self.applyButton.setEnabled(False)

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
								zero_intercept=self.zero_interceptOption.isChecked(),
								n_min=myn_min)
		except:
			self.raiseError("A problem occurred. There may be a problem with the input values.")
			return

		self.graphPaneObj.updateGraph()

		self.progressPaneObj.completedStage(5)

		# Automatically saves the project if it already has a save location
		self.project.reSave()

	def pressedReloadButton(self):
		""" Performs a reload when the button is pressed. """

		url = QUrl.fromLocalFile(self.srmfile)
		QDesktopServices.openUrl(url)

		print(self.srmfile)

	def updateStageInfo(self):
		""" Updates the stage after data is imported at runtime """
		self.srmfile = self.project.eg.srmfile

		srms = la.helpers.srm.get_defined_srms(self.project.eg.srmfile)

		for i in range(len(srms)):
			self.srmList.append((QCheckBox(srms[i]), srms[i]))
			self.srmList[i][0].setChecked(True)
			self.optionsRight.addWidget(self.srmList[i][0])
		self.optionsRight.addStretch(1)

	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.calibrationWidget, "Error", message, QMessageBox.Ok)

	def loadValues(self):
		""" Loads the values saved in the project, and fills in the stage parameters with them """

		# The stage parameters are stored in project as dictionaries
		params = self.project.getStageParams("calibrate")

		# The stage parameters are applied to the input fields
		if params is not None:
			self.drift_correctOption.setChecked(params.get("drift_correct", True))
			self.zero_interceptOption.setChecked(params.get("zero_intercept", True))
			self.n_minOption.setText(str(params.get("n_min", 10)))

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
		self.pressedApplyButton()

	def enterPressed(self):
		""" When enter is pressed on this stage """
		if self.applyButton.isEnabled():
			self.pressedApplyButton()

	def pressedPopupButton(self):
		pass

	def pressedCalculateButton(self):

		self.applyButton.setEnabled(True)

