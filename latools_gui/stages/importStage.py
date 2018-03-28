from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

import templates.controlsPane as controlsPane

class ImportStage():
	"""
	Currently, each stage has a class where the details and functionality unique to the
	stage can be defined. They each build a Controls pane object and will later have access
	to update the graph pane.
	"""
	def __init__(self, stageLayout):
		
		self.stageControls = controlsPane.ControlsPane(stageLayout)

		self.stageControls.setTitle("Import Data")

		self.stageControls.setDescription("""
			This imports all the data files within the data/ folder into an latools.analyse 
			object called eg, along with several parameters describing the dataset and how 
			it should be imported:""")

		self.stageControls.addOption("config", 0)
		self.stageControls.addOption("internal_standard", 0)
		self.stageControls.addOption("srm_identifier", 0)
