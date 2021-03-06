import os, shutil, sys
import latools as la

import latools.helpers as helpers
import pyqtgraph as pg
import numpy as np
import uncertainties.unumpy as un
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

# We create the analyse object
#eg = la.analyse(data_folder='./data/',
#				config='DEFAULT',
#				internal_standard='Ca43',
#				srm_identifier='STD')

class GraphWindow(pg.GraphicsLayoutWidget):

	def __init__(self, project):
		super().__init__()
		self.project = project
		# For testing purposes, the sample and stage is hard coded
		self.sampleName = 'Sample-1'
		self.focusStage = 'rawdata'
		# Add plot window to the layout
		graph = self.addPlot(title=self.sampleName)
		graph.setLogMode(x=False, y=True)
		graph.setLabel('left', 'Counts')
		graph.setLabel('bottom', 'Time', units='s')

		self.graph = graph

		# Add legend window to the layout
		legend = self.addViewBox()
		legend.setMaximumWidth(100)

		self.legend = legend

		l = pg.LegendItem()
		l.setParentItem(self.legend)
		l.anchor((0,0), (0,0))

		self.l = l

	# Updates the graph based off Sample and Focustage name
	def update(self, sample, stage):
		# Clear existing plot
		self.graph.clear()

		# Set stage
		self.focusStage = stage

		# We create the data object
		dat = self.project.eg.data[self.sampleName]
		# Get list of analytes (elements) from the data object
		analytes = dat.analytes

		# For each analyte: get x and y, and plot them
		# Then add it to the legend
		for a in analytes:
			x = dat.Time
			y, yerr = helpers.stat_fns.unpack_uncertainties(dat.data[self.focusStage][a])
			y[y == 0] = np.nan
			plt = self.graph.plot(x, y, pen=pg.mkPen(dat.cmap[a], width=2), label=a)
			self.l.addItem(plt, a)
		

#Unused but useful code

#la.get_example_data('./data')

#pg.setConfigOption('background', 'w')
#pg.setConfigOption('foreground', 'k')

#colourconver = {'Mg24': (27,158,119), 'Mg25': (217,95,2), 'Al27': (117,112,179), 'Ca43': (231,41,138), 'Ca44': (102,166,30), 'Mn55': (230,171,2), 'Sr88': (166,118,29), 'Ba137': (102,102,102), 'Ba138': (102,102,102)}


#class LogScale(pg.AxisItem):
#    def __init__(self, *args, **kwargs):
#        super(LogScale, self).__init__(*args, **kwargs)

#    def logTickStrings(self, values, scale, spacing):
#       return ["%0.1g"%x for x in 10 ** np.array(values).astype(float)]

#axisItems={'left': LogScale(orientation='left')}