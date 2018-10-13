""" A window to plot the options for a particular filter currently being selected """

from PyQt5.QtWidgets import *
import pyqtgraph as pg


class FilterPlot(QWidget):
	""" A popup window to display a custom graph activated by the 'plot' button in a filter
	"""

	def __init__(self, filterTab, project, graphPane):
		"""
		Creates the popup window

		Parameters
		----------
		filterTab : FilterTab
			The object that created this window, that houses the filter options. It can pass these along with
			self.filterTab.updateOptions()
		project : RunningProject
			The analyse object for the project is: self.project.eg
		graphPane : GraphPane
			The graph pane object responsible for displaying graphs
		"""

		self.filterTab = filterTab
		self.project = project
		self.graphPane = graphPane

		# filterOptions will hold a dictionary of the filter's current options
		self.filterOptions = {}
		# We grab the filterOptions to start
		self.updatePressed()

		# We provide the name of this particular type of filter.
		# This could be used to identify what type of graph to create.
		self.name = self.filterTab.filterName
		# As threshold needs a different plot per type, we use the "type" value
		if self.name == "Threshold":
			self.name = self.filterOptions["type"]

		# We initialise the window, and give it a title
		QWidget.__init__(self)
		self.setWindowTitle(self.name + " plot")

		# We use a grid layout
		self.mainGrid = QGridLayout(self)

		self.graph = None
		self.createGraph()

		# The graph is added to the window.
		# The four numbers refer to its position and size in the grid layout:
		# (row, column, how many rows it occupies, how many columns it occupies)
		# We set it to two columns so that the update button below won't stretch across the window,
		# As it would if it were in the same single column as the graph.
		self.mainGrid.addWidget(self.graph, 0, 0, 1, 2)

		# We make an update button, give it a tooltip and tell it what to do when pressed.
		self.updateButton = QPushButton("Update")
		self.updateButton.setToolTip("<qt/>Updates the plot with the values from the filter options.")
		self.updateButton.clicked.connect(self.updatePressed)

		# The button is added to the grid layout. As it doesn't need to occupy more than one row or column,
		# We just give it the position numbers (row 1, column 0)
		self.mainGrid.addWidget(self.updateButton, 1, 0)

		# Here we tell the grid layout how to expand. The first parameter is the column or row index which
		# We want to expand. The second parameter (1) means that it will expand over any row or column
		# with the default stretch value of 0.
		self.mainGrid.setColumnStretch(1, 1)
		self.mainGrid.setRowStretch(1, 1)

	def createGraph(self):
		""" Create a graph based on self.name, and self.filterOptions """

		# A blank default for now:
		self.graph = pg.PlotWidget()

	def updatePressed(self):
		""" When the update button is pressed, an updated dictionary of filter options is returned. """
		self.filterOptions = self.filterTab.updateOptions()
		print(self.filterOptions)