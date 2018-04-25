""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import latools as la
import inspect
import templates.controlsPane as controlsPane

class BackgroundStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, backgroundWidget, project):
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

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We capture the default parameters for this stage's function call
		self.defaultWeightParams = self.stageControls.getDefaultParameters(
			inspect.signature(la.analyse.bkg_calc_weightedmean))

		self.defaultInterParams = self.stageControls.getDefaultParameters(
			inspect.signature(la.analyse.bkg_calc_interp1d))

		# We set the title and description for the stage

		self.stageControls.setDescription("Background Correction", """
			The de-spiked data must now be background-corrected. This involves three steps:
			Signal and background identification.
			Background calculation underlying the signal regions.
			Background subtraction from the signal.""")

		# The space for the stage options is provided by the Controls Pane.
		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		self.methodOption = QComboBox()
		self.methodOption.addItem("bkg_calc_weightedmean")
		self.methodOption.addItem("bkg_calc_interp1d")

		# When methodOption is changed, it calls methodUpdate
		self.methodOption.activated.connect(self.methodUpdate)
		self.optionsGrid.addWidget(QLabel("method"), 0, 0)
		self.optionsGrid.addWidget(self.methodOption, 0, 1)

		# Set up a layout that will only be displayed when bkg_calc_weightedmean is selected
		self.methodWidget1 = QWidget()
		self.methodLayout1 = QGridLayout(self.methodWidget1)

		self.weight_fwhmOption = QLineEdit(self.defaultWeightParams['weight_fwhm'])
		self.methodLayout1.addWidget(QLabel("weight_fwhm"), 0, 0)
		self.methodLayout1.addWidget(self.weight_fwhmOption, 0, 1)

		self.n_minOption = QLineEdit(self.defaultWeightParams['n_min'])
		self.methodLayout1.addWidget(QLabel("n_min"), 0, 2)
		self.methodLayout1.addWidget(self.n_minOption, 0, 3)

		self.n_maxOption = QLineEdit(self.defaultWeightParams['n_max'])
		self.methodLayout1.addWidget(QLabel("n_max"), 0, 4)
		self.methodLayout1.addWidget(self.n_maxOption, 0, 5)

		# Apply the bkg_calc_weightedmean options as default
		self.currentlyMethod1 = True
		self.optionsGrid.addWidget(self.methodWidget1, 1, 0, 1, 2)

		# Set up a layout for when "bkg_calc_interp1d" is selected
		self.methodWidget2 = QWidget()
		self.methodLayout2 = QGridLayout(self.methodWidget2)

		self.kindOption = QLineEdit(self.defaultInterParams['kind'])
		self.methodLayout2.addWidget(QLabel("kind"), 0, 0)
		self.methodLayout2.addWidget(self.kindOption, 0, 1)

		self.n_minOption2 = QLineEdit(self.defaultInterParams['n_min'])
		self.methodLayout2.addWidget(QLabel("n_min"), 0, 2)
		self.methodLayout2.addWidget(self.n_minOption2, 0, 3)

		self.n_maxOption2 = QLineEdit(self.defaultInterParams['n_max'])
		self.methodLayout2.addWidget(QLabel("n_max"), 0, 4)
		self.methodLayout2.addWidget(self.n_maxOption2, 0, 5)

		# Add the universal options
		self.cstepOption = QLineEdit(self.defaultWeightParams['cstep'])
		self.optionsGrid.addWidget(QLabel("cstep"), 2, 0)
		self.optionsGrid.addWidget(self.cstepOption, 2, 1, 1, 1)

		self.bkg_filterOption = QCheckBox("bkg_filter")
		self.optionsGrid.addWidget(self.bkg_filterOption, 3, 0)
		self.bkg_filterOption.setChecked(self.defaultWeightParams['bkg_filter'] == 'True')

		# We set up a click function for the checkbox
		self.bkg_filterOption.stateChanged.connect(self.bkgUpdate)

		# Set up a layout that will only be displayed when bkg_filter is checked
		self.bkgWidget = QWidget()
		self.bkgLayout = QGridLayout(self.bkgWidget)

		self.f_winOption = QLineEdit(self.defaultWeightParams['f_win'])
		self.f_winLabel = QLabel("f_win")
		self.bkgLayout.addWidget(self.f_winLabel, 0, 0)
		self.bkgLayout.addWidget(self.f_winOption, 0, 1)

		self.f_n_limOption = QLineEdit(self.defaultWeightParams['f_n_lim'])
		self.f_n_limLabel = QLabel("f_n_lim")
		self.bkgLayout.addWidget(self.f_n_limLabel, 0, 2)
		self.bkgLayout.addWidget(self.f_n_limOption, 0, 3)

		self.optionsGrid.addWidget(self.bkgWidget, 3, 1)

		self.f_winOption.setVisible(False)
		self.f_n_limOption.setVisible(False)

		# We create the buttons for the right-most section of the Controls Pane.

		self.calcButton = QPushButton("Calculate background")
		self.calcButton.clicked.connect(self.pressedCalcButton)
		self.stageControls.addApplyButton(self.calcButton)

		self.popupButton = QPushButton("Plot in popup")
		self.popupButton.clicked.connect(self.pressedPopupButton)
		self.stageControls.addApplyButton(self.popupButton)

		self.subtractButton = QPushButton("Subtract background")
		self.subtractButton.clicked.connect(self.pressedSubtractButton)
		self.stageControls.addApplyButton(self.subtractButton)
		self.subtractButton.setEnabled(False)


	def pressedCalcButton(self):
		""" Applies a background calculation on the project data when a button is pressed, making sure there are
		no illegal inputs.

		"""

		if (self.currentlyMethod1):

			# We protect against blank or incorrect fields in options
			myweight = None
			if self.weight_fwhmOption.text() != "":
				try:
					myweight = float(self.weight_fwhmOption.text())
				except:
					self.raiseError("The 'weight_fwhm' value must be a floating point number")
					return

			myn_min = 20
			if self.n_minOption.text() != "":
				try:
					myn_min = int(self.n_minOption.text())
				except:
					self.raiseError("The 'n_min' value must be an integer")
					return

			myn_max = None
			if self.n_maxOption.text() != "":
				try:
					myn_max = int(self.n_maxOption.text())
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
				self.project.eg.bkg_calc_weightedmean(analytes=None,
												weight_fwhm=myweight,
												n_min=myn_min,
												n_max=myn_max,
												cstep=mycstep,
												bkg_filter=self.bkg_filterOption.isChecked(),
												f_win=myf_win,
												f_n_lim=myf_n_lim)
			except:
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
				self.raiseError("A problem occurred. There may be a problem with the input values.")
				return

		self.subtractButton.setEnabled(True)

	def pressedPopupButton(self):
		""" Creates a popup for the background calculation when a button is pressed. """
		# TO DO: ADD POPUP FUNCTIONALITY

	def pressedSubtractButton(self):
		""" Subtracts an existing background calculation from the project data when a button is pressed. """
		self.project.eg.bkg_subtract(analytes=None, errtype='stderr', focus_stage='despiked')

		print(list(self.project.eg.data['STD-1'].data.keys()))
		self.graphPaneObj.updateGraph(showRanges=True)

		self.progressPaneObj.setRightEnabled()

	def methodUpdate(self):
		""" Updates the current method. """
		if (self.currentlyMethod1):
			self.methodWidget1.setParent(None)
			self.optionsGrid.addWidget(self.methodWidget2, 1, 0, 1, 2)
		else:
			self.methodWidget2.setParent(None)
			self.optionsGrid.addWidget(self.methodWidget1, 1, 0, 1, 2)
		self.currentlyMethod1 = not self.currentlyMethod1

	def bkgUpdate(self):
		if self.bkg_filterOption.isChecked():
			self.f_winOption.setVisible(True)
			self.f_n_limOption.setVisible(True)
		else:
			self.f_winOption.setVisible(False)
			self.f_n_limOption.setVisible(False)

	def raiseError(self, message):
		errorBox = QMessageBox.critical(self.backgroundWidget, "Error", message, QMessageBox.Ok)