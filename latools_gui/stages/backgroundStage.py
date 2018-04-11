""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys

import templates.controlsPane as controlsPane

class BackgroundStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	def __init__(self, stageLayout, graphPaneObj, navigationPaneObj, project):
		"""
		Initialising creates and customises a Controls Pane for this stage.

		Parameters
		----------
		stageLayout : QVBoxLayout
			The layout for the entire stage screen, that the Controls Pane will be added to.
		graphPaneObj : GraphPane
			A reference to the Graph Pane that will sit at the bottom of the stage screen and display
			updates t the graph, produced by the processing defined in the stage.
		navigationPaneObj : NavigationPane
			A reference to the Navigation Pane so that the right button can be enabled by completing the stage.
		project : RunningProject
			A reference to the project object which contains all of the information unique to this project,
			including the latools analyse object that the stages will update.
		"""

		self.graphPaneObj = graphPaneObj
		self.navigationPaneObj = navigationPaneObj
		self.project = project

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We set the title and description for the stage

		self.stageControls.setTitle("Background Correction")

		self.stageControls.setDescription("""
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

		self.weight_fwhmOption = QLineEdit()
		self.methodLayout1.addWidget(QLabel("weight_fwhm"), 0, 0)
		self.methodLayout1.addWidget(self.weight_fwhmOption, 0, 1)

		self.n_minOption = QLineEdit("20")
		self.methodLayout1.addWidget(QLabel("n_min"), 0, 2)
		self.methodLayout1.addWidget(self.n_minOption, 0, 3)

		self.n_maxOption = QLineEdit()
		self.methodLayout1.addWidget(QLabel("n_max"), 0, 4)
		self.methodLayout1.addWidget(self.n_maxOption, 0, 5)

		# Apply the bkg_calc_weightedmean options as default
		self.currentlyMethod1 = True
		self.optionsGrid.addWidget(self.methodWidget1, 1, 0, 1, 2)

		# Set up a layout for when "bkg_calc_interp1d" is selected
		self.methodWidget2 = QWidget()
		self.methodLayout2 = QGridLayout(self.methodWidget2)

		self.kindOption = QLineEdit("1")
		self.methodLayout2.addWidget(QLabel("kind"), 0, 0)
		self.methodLayout2.addWidget(self.kindOption, 0, 1)

		self.n_minOption2 = QLineEdit("10")
		self.methodLayout2.addWidget(QLabel("n_min"), 0, 2)
		self.methodLayout2.addWidget(self.n_minOption2, 0, 3)

		self.n_maxOption2 = QLineEdit()
		self.methodLayout2.addWidget(QLabel("n_max"), 0, 4)
		self.methodLayout2.addWidget(self.n_maxOption2, 0, 5)

		# Add the universal options
		self.cstepOption = QLineEdit()
		self.optionsGrid.addWidget(QLabel("cstep"), 2, 0)
		self.optionsGrid.addWidget(self.cstepOption, 2, 1, 1, 1)

		self.bkg_filterOption = QCheckBox("bkg_filter")
		self.optionsGrid.addWidget(self.bkg_filterOption, 3, 0)

		# We set up a click function for the checkbox
		self.bkg_filterOption.stateChanged.connect(self.bkgUpdate)

		# Set up a layout that will only be displayed when bkg_filter is checked
		self.bkgWidget = QWidget()
		self.bkgLayout = QGridLayout(self.bkgWidget)

		self.f_winOption = QLineEdit("7")
		self.bkgLayout.addWidget(QLabel("f_win"), 0, 0)
		self.bkgLayout.addWidget(self.f_winOption, 0, 1)

		self.f_n_limOption = QLineEdit("3")
		self.bkgLayout.addWidget(QLabel("f_n_lim"), 0, 2)
		self.bkgLayout.addWidget(self.f_n_limOption, 0, 3)

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

		if (self.currentlyMethod1):

			# We protect against blank or incorrect fields in options
			myweight = None
			if self.weight_fwhmOption.text() != "":
				myweight = float(self.weight_fwhmOption.text())

			myn_min = 20
			if self.n_minOption.text() != "":
				myn_min = int(self.n_minOption.text())

			myn_max = None
			if self.n_maxOption.text() != "":
				myn_max = int(self.n_maxOption.text())

			mycstep = None
			if self.cstepOption.text() != "":
				mycstep = float(self.cstepOption.text())

			myf_win = 7
			if self.f_winOption.text() != "":
				myf_win = int(self.f_winOption.text())

			myf_n_lim = 3
			if self.f_n_limOption.text() != "":
				myf_n_lim = int(self.f_n_limOption.text())

			self.project.eg.bkg_calc_weightedmean(analytes=None,
												weight_fwhm=myweight,
												n_min=myn_min,
												n_max=myn_max,
												cstep=mycstep,
												bkg_filter=self.bkg_filterOption.isChecked(),
												f_win=myf_win,
												f_n_lim=myf_n_lim)
		else:

			# We protect against blank or incorrect fields in options
			myKind = 1
			if self.kindOption.text() != "":
				myKind = int(self.kindOption.text())

			myn_min2 = 10
			if self.n_minOption2.text() != "":
				myn_min2 = int(self.n_minOption2.text())

			myn_max2 = None
			if self.n_maxOption2.text() != "":
				myn_max2 = int(self.n_maxOption2.text())

			mycstep = None
			if self.cstepOption.text() != "":
				mycstep = float(self.cstepOption.text())

			myf_win = 7
			if self.f_winOption.text() != "":
				myf_win = int(self.f_winOption.text())

			myf_n_lim = 3
			if self.f_n_limOption.text() != "":
				myf_n_lim = int(self.f_n_limOption.text())

			self.project.eg.bkg_calc_interp1d(analytes=None,
											kind=myKind,
											n_min=myn_min2,
											n_max=myn_max2,
											cstep=mycstep,
											bkg_filter=self.bkg_filterOption.isChecked(),
											f_win=myf_win,
											f_n_lim=myf_n_lim)

		self.navigationPaneObj.setRightEnabled()
		self.subtractButton.setEnabled(True)

	def pressedPopupButton(self):
		# TO DO: ADD POPUP FUNCTIONALITY
		self.navigationPaneObj.setRightEnabled()

	def pressedSubtractButton(self):
		self.project.eg.bkg_subtract(analytes=None, errtype='stderr', focus='despiked')
		self.subtractButton.setEnabled(False)

	def methodUpdate(self):
		if (self.currentlyMethod1):
			self.methodWidget1.setParent(None)
			self.optionsGrid.addWidget(self.methodWidget2, 1, 0, 1, 2)
		else:
			self.methodWidget2.setParent(None)
			self.optionsGrid.addWidget(self.methodWidget1, 1, 0, 1, 2)
		self.currentlyMethod1 = not self.currentlyMethod1

	def bkgUpdate(self):
		if (self.bkg_filterOption.isChecked()):
			self.optionsGrid.addWidget(self.bkgWidget, 3, 1, 1, 2)
		else:
			self.bkgWidget.setParent(None)
