""" Despiking stage module docstring is here.

Lorem ipsum dolor sit amet

"""

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
		self.optionsGrid = QHBoxLayout(self.stageControls.getOptionsWidget())

		self.pane1Frame = QFrame()
		self.pane1Frame.setFrameShape(QFrame.StyledPanel)
		self.pane1Frame.setFrameShadow(QFrame.Raised)

		self.pane1Layout = QGridLayout(self.pane1Frame)
		self.optionsGrid.addWidget(self.pane1Frame)

		self.pane1expdecayOption = QCheckBox("exponential decay despike")
		self.pane1expdecayOption.setChecked(True)
		self.pane1Layout.addWidget(self.pane1expdecayOption, 0, 0, 1, 0)

		self.pane1Exponent = QLineEdit()
		self.pane1Layout.addWidget(QLabel("exponent"), 1, 0)
		self.pane1Layout.addWidget(self.pane1Exponent, 1, 1)

		self.pane1Maxiter = QLineEdit("4")
		self.pane1Layout.addWidget(QLabel("maxiter"), 2, 0)
		self.pane1Layout.addWidget(self.pane1Maxiter, 2, 1)


		# Second pane
		self.pane2Frame = QFrame()
		self.pane2Frame.setFrameShape(QFrame.StyledPanel)
		self.pane2Frame.setFrameShadow(QFrame.Raised)

		self.pane2Layout = QGridLayout(self.pane2Frame)
		self.optionsGrid.addWidget(self.pane2Frame)

		self.pane2NoiseOption = QCheckBox("noise despike")
		self.pane2NoiseOption.setChecked(True)
		self.pane2Layout.addWidget(self.pane2NoiseOption, 0, 0, 1, 0)

		self.pane2win = QLineEdit("3")
		self.pane2Layout.addWidget(QLabel("\'win\'"), 1, 0)
		self.pane2Layout.addWidget(self.pane2win, 1, 1)

		self.pane2nlim = QLineEdit("12")
		self.pane2Layout.addWidget(QLabel("nlim"), 2, 0)
		self.pane2Layout.addWidget(self.pane2nlim, 2, 1)

		self.pane2Maxiter = QLineEdit("4")
		self.pane2Layout.addWidget(QLabel("maxiter"), 3, 0)
		self.pane2Layout.addWidget(self.pane2Maxiter, 3, 1)

		# We define the apply button and its function here, and pass it to stageControls to be displayed
		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):


		localExponent = None
		if (self.pane1Exponent.text() != ""):
			localExponent = float(self.pane1Exponent.text())

		localWin = 3
		if (self.pane2win.text() != ""):
			localWin = float(self.pane2win.text())

		localNlim = 12
		if (self.pane2nlim.text() != ""):
			localNlim = int(self.pane2nlim.text())

		localMaxiter = 4
		if (self.pane1Maxiter.text() != ""):
			localMaxiter = int(self.pane1Maxiter.text())


		self.project.eg.despike(expdecay_despiker=self.pane1expdecayOption.isChecked(),
								exponent=localExponent,
								noise_despiker=self.pane2NoiseOption.isChecked(),
								win=localWin,
								nlim=localNlim,
								exponentplot=False,
								maxiter=localMaxiter)

		self.graphPaneObj.updateGraph('despiked')
		self.navigationPaneObj.setRightEnabled()

