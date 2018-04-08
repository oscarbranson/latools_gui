from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

import templates.controlsPane as controlsPane

class CalibrationStage():
	"""
	Currently, each stage has a class where the details and functionality unique to the
	stage can be defined. They each build a Controls pane object and will later have access
	to update the graph pane.
	"""
	def __init__(self, stageLayout, graphPaneObj, navigationPaneObj, project):
		self.graphPaneObj = graphPaneObj
		self.navigationPaneObj = navigationPaneObj
		self.project = project

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		self.stageControls.setTitle("Calibration")

		self.stageControls.setDescription("""
			Once all your data are normalised to an internal standard, you’re ready to calibrate 
			the data. This is done by creating a calibration curve for each element based on SRMs 
			measured throughout your analysis session, and a table of known SRM values.""")

		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		self.drift_correctOption = QCheckBox("drift_correct")
		self.drift_correctOption.setChecked(True)
		self.optionsGrid.addWidget(self.drift_correctOption, 0, 0, 2, 0)

		self.scrollWindow = QScrollArea()
		self.scrollLayout = QVBoxLayout(self.scrollWindow)
		self.scrollWindowWidget = QWidget()
		self.scrollWindow.setWidget(self.scrollWindowWidget)

		self.scrollLayout.addWidget(QCheckBox("NIST610"))
		self.scrollLayout.addWidget(QCheckBox("NIST612"))
		self.scrollLayout.addWidget(QCheckBox("NIST614"))

		self.optionsGrid.addWidget(self.scrollWindowWidget, 1, 0)

		self.zero_interceptOption = QCheckBox("zero_intercept")
		self.zero_interceptOption.setChecked(True)
		self.optionsGrid.addWidget(self.zero_interceptOption, 2, 0)

		self.n_minOption = QLineEdit("10")
		self.optionsGrid.addWidget(QLabel("n_min"), 3, 0)
		self.optionsGrid.addWidget(self.n_minOption, 3, 1)


		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		#Add apply button functionality
		self.navigationPaneObj.setRightEnabled()
