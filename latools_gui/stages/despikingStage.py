from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

import templates.controlsPane as controlsPane

class DespikingStage():
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

		self.stageControls.setTitle("Data De-spiking")

		self.stageControls.setDescription("""
			The first step in data reduction is the ‘de-spike’ the raw data to 
			remove physically unrealistic outliers from the data (i.e. higher than 
			is physically possible based on your system setup).""")

		# We create a grid layout for options within the widget displayed in the controls layout
		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# A checkbox is added
		self.expdecayOption = QCheckBox("expdecay_despiker")
		self.expdecayOption.setChecked(True)
		self.optionsGrid.addWidget(self.expdecayOption, 0,0)

		self.noiseOption = QCheckBox("noise_despiker")
		self.noiseOption.setChecked(True)
		self.optionsGrid.addWidget(self.noiseOption, 1,0)

		# We define the apply button and its function here, and pass it to stageControls to be displayed
		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):

		# Currently this function just runs this example.
		# TO DO: Have this button cause the graph to actually update with the new analysis (in this case despiking)
		self.project.eg.despike()
		self.graphPaneObj.updateGraph()
		self.navigationPaneObj.setRightEnabled()

