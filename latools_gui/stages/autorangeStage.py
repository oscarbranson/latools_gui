from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

import templates.controlsPane as controlsPane

class AutorangeStage():
	"""
	Currently, each stage has a class where the details and functionality unique to the
	stage can be defined. They each build a Controls pane object and will later have access
	to update the graph pane.
	"""
	def __init__(self, stageLayout):
		
		self.stageControls = controlsPane.ControlsPane(stageLayout)

		self.stageControls.setTitle("Autorange")

		self.stageControls.setDescription("""
			The first step in data reduction is the ‘de-spike’ the raw data to 
			remove physically unrealistic outliers from the data (i.e. higher than 
			is physically possible based on your system setup).""")

		self.stageControls.addOption("autorange option 1", 0)
		self.stageControls.addOption("autorange option 2", 0)

