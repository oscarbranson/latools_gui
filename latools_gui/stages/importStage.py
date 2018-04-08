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

		self.findDataButton = QPushButton("Browse")
		self.findDataButton.setMaximumWidth(100)
		self.findDataButton.clicked.connect(self.findDataButtonClicked)
		self.optionsGrid.addWidget(self.findDataButton,0,0)

		self.fileLocationLine = QLineEdit("./data/")
		self.optionsGrid.addWidget(self.fileLocationLine, 0, 1)
		self.fileLocationLine.setReadOnly(True)

		self.configOption = QComboBox()
		self.configOption.addItem("DEFAULT")
		self.configOption.addItem("REPRODUCE")
		self.configOption.addItem("UCD-AGILENT")
		self.configOption.addItem("USC-ELEMENT")
		self.optionsGrid.addWidget(QLabel("config"), 1,0)
		self.optionsGrid.addWidget(self.configOption, 1,1)

		self.srm_identifierOption = QLineEdit()
		self.optionsGrid.addWidget(QLabel("SRM identifier"), 2, 0)
		self.optionsGrid.addWidget(self.srm_identifierOption, 2, 1)

		self.file_extensionOption = QLineEdit()
		self.optionsGrid.addWidget(QLabel("file extension"), 3, 0)
		self.optionsGrid.addWidget(self.file_extensionOption, 3, 1)

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		#Add apply button functionality

		# TO DO: Deal safely with incorrect data_folder

		self.project.eg = la.analyse(data_folder=self.fileLocationLine.text(),
									 config=self.configOption.currentText(),
									 extension=self.file_extensionOption.text(),
									 srm_identifier=self.srm_identifierOption.text())

		self.graphPaneObj.updateGraph('rawdata', True)

		self.navigationPaneObj.setRightEnabled()

	def findDataButtonClicked(self):

		self.fileLocation = QFileDialog.getExistingDirectory(self.importStageWidget, 'Open file', '/home')
		self.fileLocationLine.setText(self.fileLocation)


