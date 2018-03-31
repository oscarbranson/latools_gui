from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

import templates.controlsPane as controlsPane

class BackgroundStage():
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

		self.stageControls.setTitle("Background Correction")

		self.stageControls.setDescription("""
			The de-spiked data must now be background-corrected. This involves three steps:
			Signal and background identification.
			Background calculation underlying the signal regions.
			Background subtraction from the signal.""")

		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())
		# self.optionsGrid.addWidget(QLabel("<b>Options</b>"), 0, 0)

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		#Add apply button functionality
		self.navigationPaneObj.setRightEnabled()
