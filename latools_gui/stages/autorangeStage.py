from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys

from ..templates import controlsPane

class AutorangeStage():
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

		self.stageControls.setTitle("Autorange")

		self.stageControls.setDescription("""
			The first step in data reduction is the ‘de-spike’ the raw data to 
			remove physically unrealistic outliers from the data (i.e. higher than 
			is physically possible based on your system setup).""")

		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())
		# self.optionsGrid.addWidget(QLabel("<b>Options</b>"), 0, 0)



		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		#Add apply button functionality
		self.navigationPaneObj.setRightEnabled()

