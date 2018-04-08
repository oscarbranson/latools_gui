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

	def __init__(self, stageLayout, graphPaneObj, navigationPaneObj, project):
		self.graphPaneObj = graphPaneObj
		self.navigationPaneObj = navigationPaneObj
		self.project = project

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		self.stageControls.setTitle("Autorange")

		self.stageControls.setDescription("""
			The first step in data reduction is the ‘de-spike’ the raw data to 
			remove physically unrealistic outliers from the data (i.e. higher than 
			is physically possible based on your system setup).
			The first step in data reduction is the ‘de-spike’ the raw data to 
			remove physically unrealistic outliers from the data (i.e. higher than 
			is physically possible based on your system setup).
			The first step in data reduction is the ‘de-spike’ the raw data to 
			remove physically unrealistic outliers from the data (i.e. higher than 
			is physically possible based on your system setup).""")

		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		self.analyteBox = QComboBox()
		self.analyteBox.addItem("total_counts")
		self.analyteBox.addItem("Others (to fill)")
		self.optionsGrid.addWidget(QLabel("analyte"), 0, 0)
		self.optionsGrid.addWidget(self.analyteBox, 0, 1)

		self.gwinEdit = QLineEdit("5")
		self.optionsGrid.addWidget(QLabel("gwin"), 1, 0)
		self.optionsGrid.addWidget(self.gwinEdit, 1, 1)

		self.swinEdit = QLineEdit("3")
		self.optionsGrid.addWidget(QLabel("swin"), 2, 0)
		self.optionsGrid.addWidget(self.swinEdit, 2, 1)

		self.winEdit = QLineEdit("20")
		self.optionsGrid.addWidget(QLabel("win"), 3, 0)
		self.optionsGrid.addWidget(self.winEdit, 3, 1)

		self.on_multEdit1 = QLineEdit("1.0")
		self.on_multEdit2 = QLineEdit("1.5")
		self.optionsGrid.addWidget(QLabel("on_mult"), 0, 2)
		self.optionsGrid.addWidget(self.on_multEdit1, 0, 3)
		self.optionsGrid.addWidget(self.on_multEdit2, 0, 4)

		self.off_multEdit1 = QLineEdit("1.5")
		self.off_multEdit2 = QLineEdit("1.0")
		self.optionsGrid.addWidget(QLabel("off_mult"), 1, 2)
		self.optionsGrid.addWidget(self.off_multEdit1, 1, 3)
		self.optionsGrid.addWidget(self.off_multEdit2, 1, 4)

		self.nbinEdit = QLineEdit("10")
		self.optionsGrid.addWidget(QLabel("nbin"), 2, 2)
		self.optionsGrid.addWidget(self.nbinEdit, 2, 3, 1, 2)

		self.logTransformCheck = QCheckBox("log transform")
		self.logTransformCheck.setChecked(True)
		self.optionsGrid.addWidget(self.logTransformCheck, 3, 2, 1, 2)

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):

		self.project.eg.autorange(analyte=self.analyteBox.currentText(),
								gwin= int(self.gwinEdit.text()),
								swin= int(self.swinEdit.text()),
								win= int(self.winEdit.text()),
								on_mult=[float(self.on_multEdit1.text()), float(self.on_multEdit2.text())],
								off_mult=[float(self.off_multEdit1.text()), float(self.off_multEdit2.text())],
								nbin=int(self.nbinEdit.text()),
								transform=self.logTransformCheck.isChecked())

		self.graphPaneObj.updateGraph(None)
		self.navigationPaneObj.setRightEnabled()
