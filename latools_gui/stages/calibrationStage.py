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
	def __init__(self, stageLayout):
		
		self.stageControls = controlsPane.ControlsPane(stageLayout)

		self.stageControls.setTitle("Calibration")

		self.stageControls.setDescription("""
			Once all your data are normalised to an internal standard, you’re ready to calibrate 
			the data. This is done by creating a calibration curve for each element based on SRMs 
			measured throughout your analysis session, and a table of known SRM values.""")

		self.stageControls.addOption("drift_correct", 0)
		self.stageControls.addOption("srms_used", 0)
