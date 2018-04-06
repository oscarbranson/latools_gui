from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

import latools as la

import templates.controlsPane as controlsPane

class ImportStage():
	"""
	Currently, each stage has a class where the details and functionality unique to the
	stage can be defined. They each build a Controls pane object and will later have access
	to update the graph pane.
	"""
	def __init__(self, stageLayout, graphPaneObj, navigationPaneObj, importStageWidget, project):

		self.graphPaneObj = graphPaneObj
		self.navigationPaneObj = navigationPaneObj
		self.importStageWidget = importStageWidget
		self.fileLocation = ""
		self.project = project

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		self.stageControls.setTitle("Import Data")

		self.stageControls.setDescription("""
			This imports all the data files within the data/ folder into an latools.analyse 
			object called eg, along with several parameters describing the dataset and how 
			it should be imported:""")

		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		#self.optionsGrid.addWidget(QLabel("<b>Options</b>"), 0, 0)

		self.findDataButton = QPushButton("Browse")
		self.findDataButton.setMaximumWidth(100)
		self.findDataButton.clicked.connect(self.findDataButtonClicked)
		self.optionsGrid.addWidget(self.findDataButton,0,0)

		self.fileLocationLine = QLineEdit()
		self.optionsGrid.addWidget(self.fileLocationLine, 0, 1)
		self.fileLocationLine.setReadOnly(True)

		self.configOption = QComboBox()
		self.configOption.addItem("DEFAULT")
		self.optionsGrid.addWidget(QLabel("config"), 1,0)
		self.optionsGrid.addWidget(self.configOption, 1,1)

		self.internal_standardOption = QComboBox()
		self.internal_standardOption.addItem("Ca43")
		self.optionsGrid.addWidget(QLabel("internal_standard"), 2, 0)
		self.optionsGrid.addWidget(self.internal_standardOption, 2, 1)

		self.srm_identifierOption = QComboBox()
		self.srm_identifierOption.addItem("STD")
		self.optionsGrid.addWidget(QLabel("srm_identifier"), 3, 0)
		self.optionsGrid.addWidget(self.srm_identifierOption, 3, 1)

		#self.stageControls.addOption(self.configOption)
		#self.stageControls.addOption(QCheckBox("internal_standard"))
		#self.stageControls.addOption(QCheckBox("srm_identifier"))

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		#Add apply button functionality

		self.project.eg = la.analyse(data_folder='./data/',
									 config='DEFAULT',
									 internal_standard='Ca43',
									 srm_identifier='STD')

		self.graphPaneObj.updateGraph('rawdata', True)

		self.navigationPaneObj.setRightEnabled()

	def findDataButtonClicked(self):
		self.fileLocation = QFileDialog.getOpenFileName(self.importStageWidget, 'Open file', '/home')
		self.fileLocationLine.setText(self.fileLocation[0])


