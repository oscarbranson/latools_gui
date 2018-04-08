from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys

import latools.helpers as helpers
import pyqtgraph as pg
import numpy as np
import uncertainties.unumpy as un

class GraphPane():
	"""
	The lower section of the stage screens that displays the graphs produced by the stage controls.
	This is currently under development and simply shows how things will be displayed when the 
	functionality is produced.
	"""
	def __init__(self, project):

		# We make a frame for this section
		self.graphFrame = QFrame()
		self.graphFrame.setFrameShape(QFrame.StyledPanel)
		self.graphFrame.setFrameShadow(QFrame.Raised)

		# We use a vertical layout for the pane as a whole
		self.graphMainLayout = QVBoxLayout(self.graphFrame)
		self.graphMainLayout.stretch(1)

		# We add a label
		self.graphName = QLabel("<b>Data subset name:</b> details of the data visualisation type")
		self.graphMainLayout.addWidget(self.graphName)

		# We use a horizontal layout for the content
		self.graphLayout = QHBoxLayout()
		self.graphMainLayout.addLayout(self.graphLayout)

		# GRAPH

		# This GraphTest class is now sent the project object
		self.graph = GraphWindow(project)

		self.graphLayout.addWidget(self.graph)
		self.graph.setMinimumWidth(900)
		self.graph.setMinimumHeight(300)

		# GRAPH OPTIONS

		# We add a vertical layout, and align the content to the top
		self.graphOptionsLayout = QVBoxLayout()
		#self.graphLayout.addLayout(self.graphOptionsLayout)
		self.graphOptionsLayout.setAlignment(Qt.AlignTop)

		self.graphOptionsLabel = QLabel("Options")
		# We add a minimum width to the layout via this label
		self.graphOptionsLayout.addWidget(self.graphOptionsLabel)

		# We temporarily list a bunch of dummy options.
		self.graphCheck1 = QCheckBox("Option 1")
		self.graphOptionsLayout.addWidget(self.graphCheck1)

		self.graphCheck2 = QCheckBox("Option 2")
		self.graphOptionsLayout.addWidget(self.graphCheck2)

		self.graphCheck3 = QCheckBox("Option 3")
		self.graphOptionsLayout.addWidget(self.graphCheck3)

		self.graphCheck4 = QCheckBox("Option 4")
		self.graphOptionsLayout.addWidget(self.graphCheck4)

		self.graphCheck5 = QCheckBox("Option 5")
		self.graphOptionsLayout.addWidget(self.graphCheck5)

		self.graphCheck6 = QCheckBox("Option 6")
		self.graphOptionsLayout.addWidget(self.graphCheck6)

	# This addToLayout method is used so that the graph frame can be defined early,
	# and therefore, passed to the controls objects so that they can access it.
	# Then, after they are added to the layout, this pane is added below the controls.
	def addToLayout(self, stageLayout):
		stageLayout.addWidget(self.graphFrame)

	# Updates the graph
	def updateGraph(self, stage, importing=False):
		# If importing new data
		if importing:
			self.graph.updateProjectDetails()
		self.graph.updateGraphs(None, stage)

class GraphWindow(QWidget):

	def __init__(self, project):
		super().__init__()
		self.project = project
		self.graphs = []

		# List of elements not to be plotted
		self.exceptionList = []

		layout = QHBoxLayout()

		# By default the focus stage is 'rawdata'
		self.focusStage = 'rawdata'

		# Add list of samples to the layout
		###
		samples = QWidget()
		samplesLayout = QVBoxLayout()
		samplesLayout.setAlignment(Qt.AlignTop)
		samples.setLayout(samplesLayout)

		# Add List widget
		sampleList = QListWidget()
		sampleList.setMaximumWidth(100)
		sampleList.itemClicked.connect(self.swapSample)
		samplesLayout.addWidget(sampleList)

		self.sampleList = sampleList

		layout.addWidget(samples)
		###

		# Add plot window to the layout
		###
		graph = pg.PlotWidget()

		self.graphs.append(graph)

		layout.addWidget(graph, 1)
		###

		# Add legend widget to the layout
		###
		legend = QWidget()
		legendLayout = QVBoxLayout()
		legendLayout.setAlignment(Qt.AlignTop)
		legend.setLayout(legendLayout)
		legend.setMinimumWidth(100)

		self.legend = legendLayout

		layout.addWidget(legend)
		###

		# Add setting buttons to the layout
		###
		settingButtons = QWidget()
		settingButtonsLayout = QVBoxLayout()
		settingButtonsLayout.setAlignment(Qt.AlignTop)
		settingButtons.setLayout(settingButtonsLayout)
		settingButtons.setMinimumWidth(125)

		# Add new window button
		newwindowButton = QPushButton("New Window")
		newwindowButton.hide()
		newwindowButton.clicked.connect(self.makeWindow)
		settingButtonsLayout.addWidget(newwindowButton)

		self.settingButtons = settingButtonsLayout

		layout.addWidget(settingButtons)
		###

		self.setLayout(layout)


	# Updates the project details when importing new data
	def updateProjectDetails(self):
		samples = []
		for sample in self.project.eg.data:
			samples.append(sample)
		self.samples = samples
		self.sampleName = samples[0]

		self.sampleList.clear()
		for sample in samples:
			self.sampleList.addItem(sample)
		self.sampleList.setCurrentItem(self.sampleList.item(0))

	# Swap currently viewed sample
	def swapSample(self):
		# sets current sample to selected sample
		selectedSamples = self.sampleList.selectedItems()
		selectedSample = selectedSamples[0]
		# Updates the graph
		self.updateGraphs(selectedSample.text())

	# updates graph to remove current excepted elements
	def updateExceptions(self):

		# Updates a list of excepted elements based off currently checked elements 
		self.exceptionList = []
		for i in (range(self.legend.count())):
			if not self.legend.itemAt(i).widget().isChecked():
				self.exceptionList.append(self.legend.itemAt(i).widget().text())
		
		# Updates the graph
		self.updateGraphs()
		

	# Updates graphs based off Focustage name and Sample name
	def updateGraphs(self, sample=None, stage=None):
		for graph in self.graphs:
			self.update(graph, sample, stage)

	# Updates target graph using given parameters and current settings
	def update(self, targetGraph, sample=None, stage=None):
		# Clear existing plot
		targetGraph.clear()
		for i in reversed(range(self.legend.count())):
			self.legend.itemAt(i).widget().deleteLater()

		# Show setting buttons
		for i in (range(self.settingButtons.count())):
			self.settingButtons.itemAt(i).widget().show()

		# Set sample
		if sample != None:
			self.sampleName = sample

		# Set stage
		if stage != None:
			self.focusStage = stage

		# We create the data object
		dat = self.project.eg.data[self.sampleName]
		# Get list of analytes (elements) from the data object
		analytes = dat.analytes

		# Set graph settings
		targetGraph.setTitle(self.sampleName)
		targetGraph.setLogMode(x=False, y=True)
		ud = {'rawdata': 'counts',
              'despiked': 'counts',
              'bkgsub': 'background corrected counts',
              'ratios': 'counts/{:s} count',
              'calibrated': 'mol/mol {:s}'}
		targetGraph.setLabel('left', ud[self.focusStage])
		targetGraph.setLabel('bottom', 'Time', units='s')

		# For each analyte: get x and y, and plot them
		# Then add it to the legend
		for a in analytes:
			# Create legend entry for the element and add it to the legend widget
			legendEntry = QCheckBox(a)
			legendEntry.setChecked(False)
			legendEntry.setStyleSheet("""
			.QCheckBox {
				background-color: """+dat.cmap[a]+""";
				}
			""")

			# If element is not excepted, set it as checked in the legend and plot it
			if not a in self.exceptionList:
				legendEntry.setChecked(True)

				# Plot element from data onto the graph
				x = dat.Time
				y, yerr = helpers.stat_fns.unpack_uncertainties(dat.data[self.focusStage][a])
				y[y == 0] = np.nan
				plt = targetGraph.plot(x, y, pen=pg.mkPen(dat.cmap[a], width=2), label=a)

			legendEntry.stateChanged.connect(self.updateExceptions)
			self.legend.addWidget(legendEntry)
	
	# Creates new window which contains a copy of the current main graph
	def makeWindow(self):
		newWin = pg.PlotWidget(title=self.sampleName)
		newWin.setWindowTitle("LAtools Graph")
		self.graphs.append(newWin)
		self.updateGraphs()
		newWin.show()