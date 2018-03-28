from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

import templates.controlsPane as controlsPane

class RatioStage():
	"""
	Currently, each stage has a class where the details and functionality unique to the
	stage can be defined. They each build a Controls pane object and will later have access
	to update the graph pane.
	"""
	def __init__(self, stageLayout):
		
		self.stageControls = controlsPane.ControlsPane(stageLayout)

		self.stageControls.setTitle("Ratio Calculation")

		self.stageControls.setDescription("""
			Next, you must normalise your data to an internal standard
			The internal standard is specified during data import, but can also be changed 
			here by specifying internal_standard in ratio(). In this case, the internal 
			standard is Ca43, so all analytes are divided by Ca43.""")
