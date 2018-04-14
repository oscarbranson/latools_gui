""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

import templates.controlsPane as controlsPane

class RatioStage():
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

		self.stageControls.setDescription("Ratio Calculation", """
			Next, you must normalise your data to an internal standard
			The internal standard is specified during data import, but can also be changed 
			here by specifying internal_standard in ratio(). In this case, the internal 
			standard is Ca43, so all analytes are divided by Ca43.""")

		# The space for the stage options is provided by the Controls Pane.
		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		self.internal_standardOption = QComboBox()
		self.internal_standardOption.addItem("None")
		self.optionsGrid.addWidget(QLabel("internal_standard"), 0, 0)
		self.optionsGrid.addWidget(self.internal_standardOption, 0, 1)

		# We create the button for the right-most section of the Controls Pane.

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		""" Ratios the project data with a given standard when a button is pressed. """

		mystandard = None
		if self.internal_standardOption.currentText() != "None":
			mystandard = self.internal_standardOption.currentText()

		self.project.eg.ratio(internal_standard=mystandard)

		self.navigationPaneObj.setRightEnabled()

	def updateStageInfo(self):
		for analyte in self.project.eg.analytes:
			self.internal_standardOption.addItem(str(analyte))