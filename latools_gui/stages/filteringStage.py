from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

import templates.controlsPane as controlsPane

class FilteringStage():
	"""
	Currently, each stage has a class where the details and functionality unique to the
	stage can be defined. They each build a Controls pane object and will later have access
	to update the graph pane.
	"""
	def __init__(self, stageLayout):
		
		self.stageControls = controlsPane.ControlsPane(stageLayout)

		self.stageControls.setTitle("Data Selection and Filtering")

		self.stageControls.setDescription("""
			The data are now background corrected, normalised to an internal standard, and 
			calibrated. Now we can get into some of the new features of latools, and start 
			thinking about data filtering.""")

