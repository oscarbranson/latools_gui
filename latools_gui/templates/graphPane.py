""" Builds and updates the graph, and displays it at the bottom of the stages screen.
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import latools.helpers as helpers
import re
import pyqtgraph as pg
import numpy as np
import uncertainties.unumpy as un
from functools import partial

class GraphPane():
	"""
	The lower section of the stage screens that displays the graphs produced by the stage controls.
	All of the stages share the one Graph Pane instance.
	"""
	def __init__(self, project):
		"""
		Initialising builds the graph pane and prepares it to display data when the stages activate it.

		Parameters
		----------
		project : RunningProject
			This object contains all of the information unique to the current project.
			The stages update the project object and the graph displays its current state.
		"""
		self.project = project

		# We make a frame for this section
		self.graphFrame = QFrame()
		self.graphFrame.setFrameShape(QFrame.StyledPanel)
		self.graphFrame.setFrameShadow(QFrame.Raised)

		# We use a vertical layout for the pane as a whole
		self.graphMainLayout = QVBoxLayout(self.graphFrame)
		self.graphMainLayout.stretch(1)

		# We use a horizontal layout for the content
		self.graphLayout = QHBoxLayout()
		self.graphMainLayout.addLayout(self.graphLayout)

		# GRAPH
		# The project object is sent to the GraphWindow object
		self.graph = MainGraph(project)
		self.bkgGraph = BkgGraph(project)
		self.caliGraph = CaliGraph(project)

		#  We add the graph to the pane and set minimum dimensions
		self.graphLayout.addWidget(self.graph)
		self.graph.setMinimumWidth(900)
		self.graph.setMinimumHeight(300)


	def addToLayout(self, stageLayout):
		""" Adds the graph to the stage layout. It is a function so that this can occur after the rest of the
			stage screens are built.

			Parameters
			----------
			stagelayout : QVBoxLayout
				The layout for the stage screen that the graph pane will be added to the bottom of.
		"""
		stageLayout.addWidget(self.graphFrame)

	# Updates the graph
	def updateGraph(self, importing=False, showRanges=False):
		""" Updates all currently active graphs. Call this function whenever the graphs need to be updated
			to reflect new settings

			Parameters
			----------
			stage : String
				The name of the stage you want the graph to display for the current dataset
			importing: Boolean
				This determines whether or not to update graph's settings (available samples, etc).
				By default this is set to False.

		"""

		# Initialise graph when importing new data
		if importing:
			self.graph.initialiseGraph()
			self.bkgGraph.initialiseGraph()
		self.graph.updateFocus(showRanges)
		self.graph.hideInternalStandard()

	def updateBkg(self):
		self.bkgGraph.populateGraph()

	def showAuxGraph(self, bkg=False, cali=False):
		if bkg:
			self.bkgGraph.showGraph()
		elif cali:
			self.caliGraph.populateGraph()
			self.caliGraph.showGraph()

class GraphWindow(QWidget):
	def __init__(self, project):
		"""	Initialises an empty PyQtGraph plot, containers for all graph settings, a new window button
		that is initially hidden till data is set

		Parameters
		----------
		project : RunningProject
			This object contains all of the information unique to the current project.
			The stages update the project object and the graph displays its current state.

		"""
		super().__init__()
		self.project = project
		self.graphs = []
		self.graphLines = {}
		self.highlightedAnalytes = []
		self.currentInternalStandard = None

		# dicts for storing {analyte: checkbox pairs}
		self.legendEntries = {}

		self.layout = QHBoxLayout()

		self.setLayout(self.layout)

	# function to aid connection development
	def dummy(self, *args, **kwargs):
		"""
		Dummy function for identifying connection content.
		"""
		for arg in args:
			print(arg, type(arg))
		for k, v in kwargs.items():
			print(k, v, type(v))

	# convert hex to rgb colour
	def hex_2_rgba(self, value, alpha=255):
		value = value.lstrip('#')
		lv = len(value)
		rgba = [int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)] + [int(alpha)]
		srgba = ['{:.0f}'.format(s) for s in rgba]
		return rgba
		#return 'rgba(' + ','.join(srgba) + ')'

	def initialiseSamples(self):
		# Add list of samples to the layout

		samples = QWidget()
		samplesLayout = QVBoxLayout()
		samplesLayout.setAlignment(Qt.AlignTop)
		samples.setLayout(samplesLayout)

		# Add List widget
		sampleList = QListWidget()
		sampleList.setMaximumWidth(100)
		sampleList.itemSelectionChanged.connect(self.swapSample)
		samplesLayout.addWidget(sampleList)

		self.sampleList = sampleList

		self.layout.addWidget(samples)

		# log-scale check box
		yLogCheckBox = QCheckBox()
		yLogCheckBox.setMaximumWidth(100)
		yLogCheckBox.setText('log(y)')
		yLogCheckBox.setChecked(True)
		yLogCheckBox.stateChanged.connect(self.updateLogScale)
		samplesLayout.addWidget(yLogCheckBox)

		self.yLogCheckBox = yLogCheckBox

	def initialiseLegend(self):
		# Add setting to the layout
		setting = QWidget()
		settingLayout = QVBoxLayout()
		setting.setLayout(settingLayout)

		# Add legend widget to the settings

		scroll = QScrollArea()
		scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		scroll.setWidgetResizable(False)

		self.scroll = scroll

		legend = QWidget()
		legendLayout = QVBoxLayout()
		legendLayout.setAlignment(Qt.AlignTop)
		legend.setLayout(legendLayout)
		legend.setMinimumWidth(150)

		self.legend = legend
		self.legendLayout = legendLayout

		settingLayout.addWidget(scroll)

		toggleButton = QPushButton('Toggle Legend Items')
		toggleButton.clicked.connect(self.toggleLegendItems)
		settingLayout.addWidget(toggleButton)

		self.setting = settingLayout

		self.layout.addWidget(setting)

	# populate sample list
	def populateSamples(self):
		"""
		Updates the list of available samples from the dataset viewable on the graph
		"""

		samples = self.project.eg.samples
		self.sampleName = samples[0]

		self.sampleList.clear()
		for sample in samples:
			self.sampleList.addItem(sample)

	# populate legend check-boxes
	def populateLegend(self):
		"""
		Populate legend with all analytes
		"""
		# clear legend Entries
		for i in reversed(range(self.legendLayout.count())):
			self.legendLayout.itemAt(i).widget().deleteLater()


		for analyte in self.project.eg.analytes:
			# Create legend entry for the element and add it to the legend widget
			legendEntry = QCheckBox()
			legendEntry.setChecked(True)
			legendEntry.setText(analyte)
			legendEntry.setStyleSheet("color: {:s}".format(self.project.eg.cmaps[analyte]))
			legendEntry.stateChanged.connect(partial(self.legendStateChange, legendEntry.text()))
			# record identity of check box in dict
			self.legendEntries[analyte] = legendEntry
			# add to layout
			self.legendLayout.addWidget(legendEntry)

		self.scroll.setWidget(self.legend)

	def hideInternalStandard(self):
		if self.currentInternalStandard != None:
			self.legendEntries[self.currentInternalStandard].setVisible(True)
			self.graphLines[self.currentInternalStandard].setVisible(True)
		analyte = self.project.eg.internal_standard
		self.currentInternalStandard = analyte
		if self.focusStage not in ['rawdata', 'despiked', 'bkgsub']:
			self.legendEntries[analyte].setVisible(False)
			self.graphLines[analyte].setVisible(False)
		else:
			self.legendEntries[analyte].setVisible(True)
			self.graphLines[analyte].setVisible(True)

	def toggleLegendItems(self):
		for item in reversed(range(self.legendLayout.count())):
			if self.legendLayout.itemAt(item).widget().isChecked():
				self.legendLayout.itemAt(item).widget().setChecked(False)
			else:
				self.legendLayout.itemAt(item).widget().setChecked(True)
				if self.legendLayout.itemAt(item).widget().text() == self.currentInternalStandard:
					self.hideInternalStandard()

class MainGraph(GraphWindow):
	"""
	Widget that contains a PyQtGraph plot, all the settings that control it, and a new window button
	that creates a clone graph

	"""
	def __init__(self, project):
		super().__init__(project)
		self.showRanges = False
		self.ranges = []

		# By default the focus stage is 'rawdata'
		self.focusStage = 'rawdata'

		self.initialiseSamples()

		# Add plot window to the layout
		###
		self.backgroundColour = 'w'

		pg.setConfigOption('background', self.backgroundColour)
		pg.setConfigOption('foreground', 'k')
		graph = pg.PlotWidget()

		self.graphs.append(graph)

		self.layout.addWidget(graph, 1)
		###

		self.initialiseLegend()

	# create lines (only happens once)
	def drawLines(self):
		"""
		Draw lines on graph for the first time.
		"""
		dat = self.project.eg.data[self.sampleName]

		for key, line in self.graphLines.items():
			for graph in self.graphs:
				graph.removeItem(line)

		for analyte in dat.analytes:
			x = dat.Time
			y, yerr = helpers.stat_fns.unpack_uncertainties(dat.data[self.focusStage][analyte])
			line = pg.PlotDataItem(x, y, pen=pg.mkPen(dat.cmap[analyte], width=2), label=analyte, name=analyte, connect='finite')
			line.curve.setClickable(True)
			line.curve.sigClicked.connect(partial(self.onClickLine, analyte))
			self.graphLines[analyte] = line

			for graph in self.graphs:
				graph.addItem(line)
	
	# draw labels
	def drawLabels(self):
		"""
		Draw axis labels, depending on self.focusStage
		"""
		ud = {'rawdata': 'counts',
              'despiked': 'counts',
              'bkgsub': 'background corrected counts',
              'ratios': 'counts/{:s} count',
              'calibrated': 'mol/mol {:s}'}
		
		ylabel = ud[self.focusStage].format(self.project.eg.internal_standard)
		if self.focusStage in ['ratios', 'calibrated']:
			ylabel.format(self.project.eg.internal_standard)

		for graph in self.graphs:
			graph.setLabel('left', ylabel)
			graph.setLabel('bottom', 'Time', units='s')
		
		
	# function for setting all graph objects at initialisation
	def initialiseGraph(self):
		"""
		Draw graph for the first time
		"""
		self.focusStage = self.project.eg.focus_stage

		self.populateSamples()
		self.populateLegend()
		self.drawLabels()
		self.drawLines()
		self.updateLogScale()

		# set sample in list - has to happen *after* lines are drawn
		self.sampleList.setCurrentItem(self.sampleList.item(0))

	# action when
	def swapSample(self):
		"""
		Grabs the name of the currently selected sample and passes it to the "updateGraphs" function
		"""
		# sets current sample to selected sample
		selectedSamples = self.sampleList.selectedItems()
		if len(selectedSamples) > 0:
			selectedSample = selectedSamples[0]
			self.sampleName = selectedSample.text()

			self.updateLines()
			# self.updateLogScale()
	
	# change between log/linear y scale
	def updateLogScale(self):
		"""
		When log(y) checkbox is modified, update y-axis scale
		"""
		for graph in self.graphs:
			graph.setLogMode(x=False, y=self.yLogCheckBox.isChecked())
		self.updateLines()

	# action when legend check-boxes are changed
	def legendStateChange(self, analyte):
		"""
		Actions to perform when legend check box changes state
		"""
		# change line visibility
		self.graphLines[analyte].setVisible(self.legendEntries[analyte].isChecked())
	
	def updateLines(self):
		"""
		Update lines for new self.sampleName and/or self.focusStage
		"""
		dat = self.project.eg.data[self.sampleName]
		# update line data for new sample
		for analyte in dat.analytes:
			x = dat.Time
			y, yerr = helpers.stat_fns.unpack_uncertainties(dat.data[self.focusStage][analyte])
			# if in log mode, transform y
			if self.yLogCheckBox.isChecked():
				y = np.log10(y)
			self.graphLines[analyte].curve.setData(x=x, y=y)

		# this plots the ranges after 'autorange' calculation
		for graph in self.graphs:
			for gRange in self.ranges:
				graph.removeItem(gRange)
				
		if self.showRanges:
			for graph in self.graphs:
				for lims in dat.bkgrng:
					self.addRegion(graph, lims, pg.mkBrush((255,0,0,25)))
				for lims in dat.sigrng:
					self.addRegion(graph, lims, pg.mkBrush((0,0,0,25)))
	
	def updateFocus(self, showRanges):
		"""
		Update graph for new focus stage. Focus-specific tasks should be included here.
		"""
		self.showRanges = showRanges

		self.focusStage = self.project.eg.focus_stage
		
		self.updateLines()
		self.drawLabels()
	
	def onClickLine(self, analyte):
		"""	This function is called when a line on the graph is clicked

			Parameters
			----------
			item : pg.plotDataItem
				The plotDataItem that was clicked

		"""
		if analyte in self.highlightedAnalytes:
			self.highlightedAnalytes.remove(analyte)
		else:
			self.highlightedAnalytes.append(analyte)
		if len(self.highlightedAnalytes) > 0:
			for a in self.project.eg.analytes:
				if a not in self.highlightedAnalytes:
					self.graphLines[a].curve.setPen(pg.mkPen(self.project.eg.cmaps[a], width=0.5))
					self.legendEntries[a].setStyleSheet("color: {:s}".format(self.project.eg.cmaps[a]))
				else:
					self.graphLines[a].curve.setPen(pg.mkPen(self.project.eg.cmaps[a], width=3))
					self.legendEntries[a].setStyleSheet("color: white; background-color: {:s}".format(self.project.eg.cmaps[a]))
		else:
			self.resetColours()
	
	def resetColours(self):
		for a in self.project.eg.analytes:
			self.graphLines[a].curve.setPen(pg.mkPen(self.project.eg.cmaps[a], width=2))
			self.legendEntries[a].setStyleSheet("color: {:s}".format(self.project.eg.cmaps[a]))

	def addRegion(self, targetGraph, lims, brush):
		region = pg.LinearRegionItem(values=lims, brush=brush, movable=False)
		region.lines[0].setPen(pg.mkPen((0,0,0,0)))
		region.lines[1].setPen(pg.mkPen((0,0,0,0)))
		self.ranges.append(region)
		targetGraph.addItem(region)

	# Creates new window which contains a copy of the current main graph
	def makeWindow(self):
		"""
		Creates a new graph that is opened as an external window
		"""
		newWin = pg.PlotWidget(title=self.sampleName)
		newWin.setWindowTitle("LAtools Graph")
		self.graphs.append(newWin)
		self.initialiseGraph()

		# self.updateGraphs(ranges=self.ranges)
		newWin.show()
		
class BkgGraph(GraphWindow):

	def __init__(self, project, err='stderr'):
		super().__init__(project)
		self.bkgScatters = {}
		self.bkgLines = {}
		self.bkgFills = {}
		self.bkgSamplelines = {}
		self.highlightRegions = {}
		self.err = err

		self.populated = False
		
		self.setWindowTitle("LAtools bkg Plot")

		self.initialiseSamples()

		graph = pg.PlotWidget()
		graph.setLogMode(x=False, y=self.yLogCheckBox.isChecked())

		self.graphs.append(graph)

		self.layout.addWidget(graph, 1)

		self.initialiseLegend()

	def initialiseGraph(self):
		self.populated = False
		for graph in self.graphs:
			graph.clear()
		self.populateSamples()
		self.populateLegend()

	def populateGraph(self):
		dat = self.project.eg
		for graph in self.graphs:
			for analyte in self.project.eg.analytes:
				sy = dat.bkg['raw'].loc[:, analyte]

				x = dat.bkg['calc']['uTime']
				y = dat.bkg['calc'][analyte]['mean']
				yl = dat.bkg['calc'][analyte]['mean'] - dat.bkg['calc'][analyte][self.err]
				yu = dat.bkg['calc'][analyte]['mean'] + dat.bkg['calc'][analyte][self.err]

				if self.yLogCheckBox.isChecked():
					sy = np.log10(sy)
					#x = np.log10(x)
					#y = np.log10(y)
					yl = np.log10(yl)
					yu = np.log10(yu)

				if not self.populated:

					scatter = pg.ScatterPlotItem(dat.bkg['raw'].uTime, sy, pen=None, brush=pg.mkBrush(self.hex_2_rgba(dat.cmaps[analyte], 127)), size=3)
					self.bkgScatters[analyte] = scatter

					line = pg.PlotDataItem(x, y, pen=pg.mkPen(dat.cmaps[analyte], width=2), label=analyte, name=analyte, connect='finite')
					self.bkgLines[analyte] = line

					fill = pg.FillBetweenItem(pg.PlotDataItem(x, yl, pen=pg.mkPen(0,0,0,0)), pg.PlotDataItem(x, yu, pen=pg.mkPen(0,0,0,0)), brush=pg.mkBrush(self.hex_2_rgba(dat.cmaps[analyte], 204)))
					self.bkgFills[analyte] = fill

					self.graphLines[analyte] = (scatter, line, fill)

					for graph in self.graphs:
						graph.addItem(scatter)
						graph.addItem(line)
						graph.addItem(fill)

				else:
					self.bkgScatters[analyte].setData(dat.bkg['raw'].uTime, sy)
					self.bkgLines[analyte].setData(x, y)
					self.bkgFills[analyte].setCurves(pg.PlotDataItem(x, yl, pen=pg.mkPen(0,0,0,0)), pg.PlotDataItem(x, yu, pen=pg.mkPen(0,0,0,0)))

			for graph in self.graphs:
				for s, d in dat.data.items():
					if not self.populated:
						self.addRegion(s, graph, (d.uTime[0], d.uTime[-1]), pg.mkBrush((0,0,0,25)))
						sampleLine = pg.InfiniteLine(pos=d.uTime[0], pen=pg.mkPen(color=(0,0,0,51), style=Qt.DashLine, width=2), label=s, labelOpts={'position': .999, 'anchors': ((0., 0.), (0., 0.))})
						self.bkgSamplelines[d] = sampleLine
						graph.addItem(sampleLine)
					else:
						self.highlightRegions[s].setRegion((d.uTime[0], d.uTime[-1]))
						self.bkgSamplelines[d].setValue(d.uTime[0])

		self.populated = True
		self.sampleList.setCurrentItem(self.sampleList.item(0))
	
	def showGraph(self):
		self.show()

	# populate sample list
	def populateSamples(self):
		"""
		Updates the list of available samples from the dataset viewable on the graph
		"""

		samples = self.project.eg.samples
		self.sampleName = samples[0]

		self.sampleList.clear()
		self.sampleList.addItem("NONE")
		for sample in samples:
			self.sampleList.addItem(sample)

	def swapSample(self):
		# sets current sample to selected sample
		selectedSamples = self.sampleList.selectedItems()
		if len(selectedSamples) > 0:
			selectedSample = selectedSamples[0]
			self.sampleName = selectedSample.text()

			for s, d in self.project.eg.data.items():
				if self.sampleName == 'NONE' or s != self.sampleName:
					self.highlightRegions[s].setVisible(False)
				else:
					self.highlightRegions[s].setVisible(True)

	# action when legend check-boxes are changed
	def legendStateChange(self, analyte):
		"""
		Actions to perform when legend check box changes state
		"""

		for item in self.graphLines[analyte]:
			item.setVisible(self.legendEntries[analyte].isChecked())

		for graph in self.graphs:
			box = graph.geterrViewbox()
			box.update()

	# change between log/linear y scale
	def updateLogScale(self):
		"""
		When log(y) checkbox is modified, update y-axis scale
		"""
		for graph in self.graphs:
			graph.setLogMode(x=False, y=self.yLogCheckBox.isChecked())
		self.populateGraph()

	def addRegion(self, name, targetGraph, lims, brush):
		region = pg.LinearRegionItem(values=lims, brush=brush, movable=False)
		region.lines[0].setPen(pg.mkPen((0,0,0,0)))
		region.lines[1].setPen(pg.mkPen((0,0,0,0)))
		region.setVisible(False)
		self.highlightRegions[name] = region
		targetGraph.addItem(region)

class CaliGraph(GraphWindow):

	def __init__(self, project, loglog=False):
		super().__init__(project)
		self.loglog = loglog

		scroll = QScrollArea()
		scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		scroll.setWidgetResizable(True)

		self.scroll = scroll

		self.setWindowTitle("LAtools calibration Plot")

		graph = QWidget()
		graphLayout = QGridLayout()
		graph.setLayout(graphLayout)
		minSize = graph.minimumSize()
		minSize.scale(1000, 1000, Qt.KeepAspectRatio)
		graph.setMinimumSize(minSize)

		self.graph = graph
		self.graphLayout = graphLayout

		self.layout.addWidget(scroll, 1)
	
	def clearGraph(self):
		self.errPlots = {}
		self.errorbars = {}
		self.caliScatters = {}
		self.analyteTexts = {}
		self.histPlots = {}
		self.histograms = {}
		self.eqTexts = {}

		for graph in self.graphs:
			graph.deleteLater()

		self.scroll.update()

	def populateGraph(self):
		self.clearGraph()

		dat = self.project.eg
		analytes = [a for a in dat.analytes if dat.internal_standard not in a]

		dat.get_focus()

		row = 0
		for i in range(0, len(analytes)):
			analyte = analytes[i]
			if i % 3 == 0:
				row += 1

			cell = pg.GraphicsLayoutWidget()
			cell.ci.setSpacing(0)
			cell.ci.layout.setColumnStretchFactor(1,2)
			cell.addLabel('mol/mol ' + dat.internal_standard, 0, 0, angle=-90, rowspan=2)
			cell.addLabel('counts/counts ' + dat.internal_standard, 1, 1, colspan=2)

			self.graphs.append(cell)

			errPlot = cell.addPlot(0, 1)
			errPlot.hideButtons()

			self.errPlots[analyte] = errPlot

			# xAxis = plot.getAxis('bottom')
			# print(dat.srmtabs.loc[analyte, 'meas_mean'].values)
			# xs = dat.srmtabs.loc[analyte, 'meas_mean'].values
			# sxs = ['{:.2f}'.format(x) for x in dat.srmtabs.loc[analyte, 'meas_mean'].values]
			# ticks = zip(xs, sxs)
			# xAxis.setTicks([list(ticks)[::2], list(ticks)[1::2]])

			errViewbox = errPlot.getViewBox()
			errViewbox.setMouseEnabled(False, False)
			# plot calibration data
			errorbar = pg.ErrorBarItem(x=dat.srmtabs.loc[analyte, 'meas_mean'].values,
			y=dat.srmtabs.loc[analyte, 'srm_mean'].values,
			width=dat.srmtabs.loc[analyte, 'meas_err'].values,
			height=dat.srmtabs.loc[analyte, 'srm_err'].values,
			pen=pg.mkPen(self.hex_2_rgba(dat.cmaps[analyte], 153), width=2),
			beam=0)
			
			self.errorbars[analyte] = errorbar
			errPlot.addItem(errorbar)

			scatter = pg.ScatterPlotItem(x=dat.srmtabs.loc[analyte, 'meas_mean'].values,
			y=dat.srmtabs.loc[analyte, 'srm_mean'].values,
			pen=None, brush=pg.mkBrush(self.hex_2_rgba(dat.cmaps[analyte], 153)), size=8)
			
			self.caliScatters[analyte] = scatter
			errPlot.addItem(scatter)
			
			# work out axis scaling
			xmax = np.nanmax(helpers.stat_fns.nominal_values(dat.srmtabs.loc[analyte, 'meas_mean'].values) +
			helpers.stat_fns.nominal_values(dat.srmtabs.loc[analyte, 'meas_err'].values))
			ymax = np.nanmax(helpers.stat_fns.nominal_values(dat.srmtabs.loc[analyte, 'srm_mean'].values) +
			helpers.stat_fns.nominal_values(dat.srmtabs.loc[analyte, 'srm_err'].values))
			xlim = [0, 1.05 * xmax]
			ylim = [0, 1.05 * ymax]
			errViewbox.setRange(xRange=xlim, yRange=ylim, disableAutoRange=True)

			# calculate line and R2
			x = np.array(xlim)

			coefs = dat.calib_params[analyte]
			m = coefs.m.values.mean()
			m_nom = helpers.stat_fns.nominal_values(m)
			# calculate case-specific paramers
			if 'c' in coefs:
				c = coefs.c.values.mean()
				c_nom = helpers.stat_fns.nominal_values(c)
				# calculate R2
				ym = dat.srmtabs.loc[analyte, 'meas_mean'] * m_nom + c_nom
				R2 = helpers.stat_fns.R2calc(dat.srmtabs.loc[analyte, 'srm_mean'], ym, force_zero=False)
				# generate line and label
				line = x * m_nom + c_nom
				label = 'y = {:.2e} x'.format(m)
				if c > 0:
					label += '<br />+ {:.2e}'.format(c)
				else:
					label += '<br /> {:.2e}'.format(c)
			else:
				# calculate R2
				ym = dat.srmtabs.loc[analyte, 'meas_mean'] * m_nom
				R2 = helpers.stat_fns.R2calc(dat.srmtabs.loc[analyte, 'srm_mean'], ym, force_zero=True)
				# generate line and label
				line = x * m_nom
				label = 'y = {:.2e} x'.format(m)

			# plot line of best fit
			graphLine = pg.PlotDataItem(x, line, pen=pg.mkPen(color=self.hex_2_rgba(dat.cmaps[analyte], 127), style=Qt.DashLine, width=2))

			self.graphLines[analyte] = graphLine
			errPlot.addItem(graphLine)

			# add R2 to label
			if round(R2, 3) == 1:
				label = 'R<sup>2</sup>: >0.999<br />' + label
			else:
				label = 'R<sup>2</sup>: {:.3f}<br />'.format(R2) + label

			analyteText = pg.TextItem(anchor=(0,0), color='k')
			el = re.match('.*?([A-z]{1,3}).*?', analyte).groups()[0]
			m = re.match('.*?([0-9]{1,3}).*?', analyte).groups()[0]
			analyteText.setHtml('<div style="text-align: center"><span style="font-size:10pt;"><sup>%(m)s</sup>%(el)s</span></div>'%{"el":el, "m":m})

			self.analyteTexts[analyte] = analyteText
			errPlot.addItem(analyteText)

			#errPlot.setLabel('bottom', 'counts/counts ' + dat.internal_standard)
			#errPlot.setLabel('left', 'mol/mol ' + dat.internal_standard)
			# write calibration equation on graph happens after data distribution

			# plot data distribution historgram alongside calibration plot
			# isolate data
			meas = helpers.stat_fns.nominal_values(dat.focus[analyte])
			meas = meas[~np.isnan(meas)]

			# check and set y scale
			if np.nanmin(meas) < ylim[0]:
				if self.loglog:
					mmeas = meas[meas > 0]
					ylim[0] = 10**np.floor(np.log10(np.nanmin(mmeas)))
				else:
					ylim[0] = 0
					errViewbox.setRange(yRange=ylim)

			m95 = np.percentile(meas[~np.isnan(meas)], 95) * 1.05
			if m95 > ylim[1]:
				if self.loglog:
					ylim[1] = 10**np.ceil(np.log10(m95))
				else:
					ylim[1] = m95

			# hist
			if self.loglog:
				bins = np.logspace(*np.log10(ylim), 30)
			else:
				bins = np.linspace(*ylim, 30)
			
			hy,hx = np.histogram(meas, bins=bins)

			histPlot = cell.addPlot(0, 2)
			histPlot.hideButtons()
			histViewbox = histPlot.getViewBox()
			histViewbox.setMouseEnabled(False, False)
			self.histPlots[analyte] = histPlot

			hist = pg.PlotDataItem(hx, hy, stepMode=True, fillLevel=0, brush=pg.mkBrush(self.hex_2_rgba(dat.cmaps[analyte], 127)), pen=pg.mkPen(color=self.hex_2_rgba(dat.cmaps[analyte], 127), width=0.5))
			
			self.histograms[analyte] = hist
			histPlot.addItem(hist)

			hist.rotate(90)

			if self.loglog:
				hist.setLogMode(xMode=False, yMode=True)
			histViewbox.setRange(yRange=ylim) # ylim of histogram axis
			errViewbox.setRange(yRange=ylim) # ylim of calibration axis
			histViewbox.invertX(True)
			#histLeft = histPlot.getAxis('left')
			#histLeft.setTicks([])
			histBottom = histPlot.getAxis('bottom')
			histBottom.setStyle()
			histBottom.setTicks([])
			histPlot.hideAxis('left')
			#histPlot.hideAxis('bottom')
			
			histRange = histViewbox.viewRange()

			# write calibration equation on graph
			cmax = np.nanmean(dat.srmtabs.loc[analyte, 'srm_mean'].values)
			if cmax / ylim[1] > 0.5:
				eqText = pg.TextItem(anchor=(1,1), color='k')
				eqText.setHtml('<div style="text-align: right"><span style="font-size:8pt">%(label)s</span></div>'%{"label":label})
				eqText.setPos(x[-1],line[0])
			else:
				eqText = pg.TextItem(anchor=(0,-1), color='k')
				eqText.setHtml('<div style="text-align: left"><span style="font-size:8pt">%(label)s</span></div>'%{"label":label})
				eqText.setPos(0,histRange[1][1])

			self.eqTexts[analyte] = eqText
			errPlot.addItem(eqText)

			analyteText.setPos(0,histRange[1][1])

			self.graphLayout.addWidget(cell, row, i%3)
		self.scroll.setWidget(self.graph)

	def showGraph(self):
		self.show()