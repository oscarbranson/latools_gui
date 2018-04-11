""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

import templates.controlsPane as controlsPane

class CalibrationStage():
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

		self.stageControls.setTitle("Calibration")

		self.stageControls.setDescription("""
			Once all your data are normalised to an internal standard, you’re ready to calibrate 
			the data. This is done by creating a calibration curve for each element based on SRMs 
			measured throughout your analysis session, and a table of known SRM values.""")

		# The space for the stage options is provided by the Controls Pane.
		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		self.drift_correctOption = QCheckBox("drift_correct")
		self.drift_correctOption.setChecked(True)
		self.optionsGrid.addWidget(self.drift_correctOption, 0, 0, 1, 2)

		self.optionsGrid.addWidget(QLabel("srms_used"), 1, 0)
		self.optionsGrid.addWidget(QCheckBox("NIST610"), 1, 1)
		self.optionsGrid.addWidget(QCheckBox("NIST612"), 1, 2)
		self.optionsGrid.addWidget(QCheckBox("NIST614"), 1, 3)

		self.zero_interceptOption = QCheckBox("zero_intercept")
		self.zero_interceptOption.setChecked(True)
		self.optionsGrid.addWidget(self.zero_interceptOption, 2, 0)

		self.n_minOption = QLineEdit("10")
		self.optionsGrid.addWidget(QLabel("n_min"), 3, 0)
		self.optionsGrid.addWidget(self.n_minOption, 3, 1)

		self.reloadButton = QPushButton("Reload SRM")
		self.reloadButton.clicked.connect(self.pressedReloadButton)
		self.stageControls.addApplyButton(self.reloadButton)

		# We create the button for the right-most section of the Controls Pane.

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):

		#self.project.eg.calibrate(analytes=None,
		#						drift_correct=self.drift_correctOption.isChecked(),
		#						srms_used=['NIST610', 'NIST612', 'NIST614'],
		#						zero_intercept=self.zero_interceptOption.isChecked(),
		#						n_min=int(self.n_minOption.text()))

		self.navigationPaneObj.setRightEnabled()

	def pressedReloadButton(self):
		x = 1
