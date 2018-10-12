""" Builds a custom controls pane for the filtering stage
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
import json
import sys
import os
import latools as la

from filters.thresholdFilter import ThresholdFilter
from filters.clusteringFilter import ClusteringFilter
from filters.correlationFilter import CorrelationFilter
from filters.defragmentFilter import DefragmentFilter
from filters.excludeFilter import ExcludeFilter
from filters.trimFilter import TrimFilter
from filters.signalFilter import SignalFilter

import templates.filterPlot as filterPlot


class FilterControls:
	"""
	The Filtering Stage has its own customised controls pane
	"""
	def __init__(self, stageLayout, project, graphPaneObj, links):
		"""
		Initialising builds the pane and prepares it for options to be added by the stage object.

		Parameters
		----------
		stageLayout : QVBoxLayout
			The layout for the entire stage screen, that the Controls Pane will add itself to.
		project : RunningProject
			A copy of the project info, used for getting the list of analytes
		"""

		# A list of all of the available filter types
		self.filterList = ["Threshold",
						   "Trim",
						   "Correlation",
						   "Defragment",
						   "Exclude Downhole",
						   "Clustering",
						   "Signal Optimiser"]

		# This will hold the contents of the selected filter's json information file
		self.filterInfo = None

		self.project = project
		self.graphPaneObj = graphPaneObj
		self.tabsArea = QTabWidget()
		stageLayout.addWidget(self.tabsArea)

		# A list of all of the filter tabs
		self.tabsList = []

		# The first tab is the Summary tab
		self.summaryTab = SummaryTab(self.project, links, self.graphPaneObj, self.tabsArea)
		self.tabsArea.addTab(self.summaryTab.summary, "Summary")

		# The last tab is the "New Filter tab"
		self.plusTab = QWidget()
		self.tabsArea.addTab(self.plusTab, "+")

		# We build the New Filter tab, starting with a grid layout
		self.plusTab.layout = QGridLayout()
		self.plusTab.setLayout(self.plusTab.layout)

		# The Create new filter label
		self.plusFilterTitle = QLabel("<span style=\"color:#779999; font-size:15px;\"><b>Create new filter</b></span>")
		self.plusTab.layout.addWidget(self.plusFilterTitle, 0, 0, 1, 2)

		# The filter type option for the New Filter
		self.plusFilterLabel = QLabel("Filter")
		self.plusFilterLabel.setMaximumWidth(60)
		self.plusTab.layout.addWidget(self.plusFilterLabel, 1, 0)
		self.plusFilterCombo = QComboBox()
		self.plusFilterCombo.activated.connect(self.plusFilterChange)
		self.plusTab.layout.addWidget(self.plusFilterCombo, 1, 1, 1, 2)

		# We populate the new filter dropdown with all of our filter names
		self.plusFilterCombo.addItem("")
		for filter in self.filterList:
			self.plusFilterCombo.addItem(filter)

		# The description box for the New Filter
		self.plusDescription = QTextEdit()
		self.plusDescription.setReadOnly(True)
		#self.plusDescription.setFixedHeight(180)

		self.plusTab.layout.addWidget(self.plusDescription, 0, 3, 4, 8)

		# The Add button for the New Filter
		self.plusAddButton = QPushButton("Create filter")
		self.plusAddButton.clicked.connect(self.addTab)
		self.plusAddButton.setEnabled(False)
		self.plusTab.layout.addWidget(self.plusAddButton, 3, 2)

	def addTab(self):
		""" Makes a new filter tab when the New Filter Add button is pressed """

		# Creates the filter's control tab
		newTab = FilterTab(self.plusFilterCombo.currentText(),
						   self.plusFilterCombo.currentText(),
						   self.summaryTab,
						   self.filterInfo,
						   self.project,
						   self.graphPaneObj,
						   self.tabsArea,
						   self.tabsList)
		# self.summaryTab.addFilter(self.plusNameField.text())
		self.tabsList.append(newTab)

		# Shuffles the tabs so that the Add Filter tab is at the end
		self.plusTab.setParent(None)
		self.tabsArea.addTab(newTab.filter, self.plusFilterCombo.currentText())
		self.tabsArea.addTab(self.plusTab, "+")

		# Opens the newly created filter tab
		self.tabsArea.setCurrentIndex(self.tabsArea.currentIndex() + 1)

		# Resets the Add Filter tab fields
		self.plusAddButton.setEnabled(False)
		self.plusFilterCombo.setCurrentIndex(0)
		self.plusFilterChange()

	def updateStageInfo(self):
		""" Updates the stage after data is imported at runtime """

		#for analyte in self.project.eg.analytes:
		self.summaryTab.addElements(self.project.eg.analytes)

	def updateDescription(self, title, description):
		""" Populates the info in the Add Filter tab description box """

		self.plusDescription.setHtml("<span style=\"color:#779999; "
										   "font-size:14px;\"><b>" + title + "</b></span><br><br>" + description)

	def plusFilterChange(self):
		""" Activates when an option is selected in the Add Filter tab's combobox """

		currentFilt = ""

		# We check what was selected
		if self.plusFilterCombo.currentText() == "Threshold":
			currentFilt = "information/thresholdFilterInfo.json"

		elif self.plusFilterCombo.currentText() == "Clustering":
			currentFilt = "information/clusteringFilterInfo.json"

		elif self.plusFilterCombo.currentText() == "Correlation":
			currentFilt = "information/correlationFilterInfo.json"

		elif self.plusFilterCombo.currentText() == "Defragment":
			currentFilt = "information/defragmentFilterInfo.json"

		elif self.plusFilterCombo.currentText() == "Exclude Downhole":
			currentFilt = "information/excludeFilterInfo.json"

		elif self.plusFilterCombo.currentText() == "Trim":
			currentFilt = "information/trimFilterInfo.json"

		elif self.plusFilterCombo.currentText() == "Signal Optimiser":
			currentFilt = "information/signalFilterInfo.json"

		else:
			# Otherwise the blank was selected, so we clear the info box
			self.updateDescription("", "")

		if currentFilt != "":
			# We import the filter information from a json file
			if getattr(sys, 'frozen', False):
				# If the program is running as a bundle, then get the relative directory
				infoFile = os.path.join(os.path.dirname(sys.executable), currentFilt)
				infoFile = infoFile.replace('\\', '/')
			else:
				# Otherwise the program is running in a normal python environment
				infoFile = currentFilt

			with open(infoFile, "r") as read_file:
				self.filterInfo = json.load(read_file)
				read_file.close()

			# We update the filter description box with the info for the selected filter
			self.updateDescription(self.filterInfo["filter_name"], self.filterInfo["filter_description"])

		# Only activates the Create button when the name and filter type options are legit
		if self.plusFilterCombo.currentText() != "":
			self.plusAddButton.setEnabled(True)
		else:
			self.plusAddButton.setEnabled(False)

	def loadFilters(self, filters, filterOnOff):

		for f in filters:

			if f[0] == "filter_threshold":
				self.plusFilterCombo.setCurrentIndex(self.plusFilterCombo.findText("Threshold"))
				self.tabsArea.setCurrentIndex(self.tabsArea.count() - 1)
				self.plusFilterChange()
				self.addTab()
				# f[1] is the filter arguments, the int is the threshold type in the combobox
				self.tabsList[-1].filterType.loadFilter(f[1], 0)

			if f[0] == "filter_threshold_percentile":
				self.plusFilterCombo.setCurrentIndex(self.plusFilterCombo.findText("Threshold"))
				self.tabsArea.setCurrentIndex(self.tabsArea.count() - 1)
				self.plusFilterChange()
				self.addTab()
				# f[1] is the filter arguments, the int is the threshold type in the combobox
				self.tabsList[-1].filterType.loadFilter(f[1], 1)

			if f[0] == "filter_gradient_threshold":
				self.plusFilterCombo.setCurrentIndex(self.plusFilterCombo.findText("Threshold"))
				self.tabsArea.setCurrentIndex(self.tabsArea.count() - 1)
				self.plusFilterChange()
				self.addTab()
				# f[1] is the filter arguments, the int is the threshold type in the combobox
				self.tabsList[-1].filterType.loadFilter(f[1], 2)

			if f[0] == "filter_trim":
				self.plusFilterCombo.setCurrentIndex(self.plusFilterCombo.findText("Trim"))
				self.tabsArea.setCurrentIndex(self.tabsArea.count() - 1)
				self.plusFilterChange()
				self.addTab()
				self.tabsList[-1].filterType.loadFilter(f[1])

			if f[0] == "filter_correlation":
				self.plusFilterCombo.setCurrentIndex(self.plusFilterCombo.findText("Correlation"))
				self.tabsArea.setCurrentIndex(self.tabsArea.count() - 1)
				self.plusFilterChange()
				self.addTab()
				self.tabsList[-1].filterType.loadFilter(f[1])

			if f[0] == "filter_defragment":
				self.plusFilterCombo.setCurrentIndex(self.plusFilterCombo.findText("Defragment"))
				self.tabsArea.setCurrentIndex(self.tabsArea.count() - 1)
				self.plusFilterChange()
				self.addTab()
				self.tabsList[-1].filterType.loadFilter(f[1])

			if f[0] == "filter_exclude_downhole":
				self.plusFilterCombo.setCurrentIndex(self.plusFilterCombo.findText("Exclude Downhole"))
				self.tabsArea.setCurrentIndex(self.tabsArea.count() - 1)
				self.plusFilterChange()
				self.addTab()
				self.tabsList[-1].filterType.loadFilter(f[1])

			if f[0] == "filter_clustering":
				self.plusFilterCombo.setCurrentIndex(self.plusFilterCombo.findText("Clustering"))
				self.tabsArea.setCurrentIndex(self.tabsArea.count() - 1)
				self.plusFilterChange()
				self.addTab()
				self.tabsList[-1].filterType.loadFilter(f[1])

			if f[0] == "optimise_signal":
				self.plusFilterCombo.setCurrentIndex(self.plusFilterCombo.findText("Signal Optimiser"))
				self.tabsArea.setCurrentIndex(self.tabsArea.count() - 1)
				self.plusFilterChange()
				self.addTab()
				self.tabsList[-1].filterType.loadFilter(f[1])

		for f in filterOnOff:
			for tab in self.tabsList:
				tab.filtOnOff(f)


class SummaryTab:
	""" The tab that lists all of the created filters and can activate the filtering process """

	def __init__(self, project, links, graphPaneObj, tabsArea):

		# We use a special widget purely to help with resizing the scrollable area to the window width
		self.summary = QWidget()
		self.project = project
		self.guideDomain = links[0]
		self.reportIssue = links[1]
		self.graphPaneObj = graphPaneObj
		self.header_items = []
		self.tabsArea = tabsArea

		self.summaryMainLayout = QHBoxLayout(self.summary)

		# We create the scroll area that will display the table of analytes and filters
		self.scroll = QScrollArea()
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll.setFixedHeight(210)
		self.scroll.setWidgetResizable(True)

		self.summaryMainLayout.addWidget(self.scroll)
		self.summary.scroll = self.scroll

		# We make an area inside the scroll to fill with the table
		self.innerWidget = QWidget()

		self.innerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		self.table = QGridLayout(self.innerWidget)

		# The Filter label is added to the table first
		self.filterLabel = QLabel("<span style=\"color:#888888\"><strong>Filter</strong></span>")
		self.filterLabel.setMinimumWidth(100)
		self.table.addWidget(self.filterLabel, 0, 0)

		self.scroll.setWidget(self.innerWidget)

		# We make a layout to house buttons to the right of the summary
		self.buttonLayoutWidget = QWidget()
		self.buttonLayout = QVBoxLayout(self.buttonLayoutWidget)
		self.buttonLayoutWidget.setMaximumWidth(120)

		# We make a button to link to the form for reporting an issue
		self.reportButton = QPushButton("Report issue")
		self.reportButton.clicked.connect(self.reportPressed)
		self.buttonLayout.addWidget(self.reportButton)
		self.reportButton.setToolTip(links[2])

		# We make a user guide button
		self.guideButton = QPushButton("User guide")
		self.guideButton.clicked.connect(self.userGuide)
		self.buttonLayout.addWidget(self.guideButton)

		# The create filter button
		self.createButton = QPushButton("Create filter")
		self.createButton.clicked.connect(self.createPressed)
		self.buttonLayout.addWidget(self.createButton)

		# We make an apply button
		self.applyButton = QPushButton("Apply")
		self.applyButton.clicked.connect(self.applyButtonPress)
		self.buttonLayout.addStretch(1)
		self.buttonLayout.addWidget(self.applyButton)

		# The buttons layout is added to the main layout
		self.summaryMainLayout.addWidget(self.buttonLayoutWidget)

		self.scroll.setWidget(self.innerWidget)

	def addElements(self, analytes):
		""" When the analytes are available at run time, they are populated in the table """

		# If the data has already been imported we need to remove the existing elements
		for i in range(len(self.header_items)):
			self.header_items[i].setParent(None)

		for i in range(len(analytes)):
			new_label = QLabel("<span style=\"color:#779999\"><strong>" +
										str(analytes[i]) +
										"< / strong > < / span > ")
			self.header_items.append(new_label)
			self.table.addWidget(new_label, 0, i + 1)

		new_label = QLabel("<span style=\"color:#888888\"><strong>ALL</strong></span>")
		self.header_items.append(new_label)
		self.table.addWidget(new_label, 0, len(analytes) + 1)

	def applyButtonPress(self):
		""" Called when the 'Apply' button in the summary tab is pressed """

		self.graphPaneObj.graph.applyFilters()

	def userGuide(self):
		""" Opens the online user guide to the filtering section """
		url = QUrl(self.guideDomain + "LAtoolsGUIUserGuide/users/09-filtering.html")
		QDesktopServices.openUrl(url)

	def createPressed(self):
		self.tabsArea.setCurrentIndex(self.tabsArea.count() - 1)

	def reportPressed(self):
		""" Links to the online form for reporting an issue """
		QDesktopServices.openUrl(QUrl(self.reportIssue))


class FilterTab:
	""" Creates the controls tab for a filter """

	def __init__(self, name, filterName, summaryTab, filterInfo, project, graphPaneObj, tabsArea, tabsList):

		# The name given by the user
		self.name = name

		# The filter type
		self.filterName = filterName

		# A reference to the Summary tab
		self.summaryTab = summaryTab

		# This will be the object for the specific filter type being used in this filter
		self.filterType = None

		# The json information for the specific filter type
		self.filterInfo = filterInfo

		# The RunningProject instance, used for listing the analytes
		self.project = project

		# A reference to the graph pane to create the data visualisations
		self.graphPaneObj = graphPaneObj

		self.tabsArea = tabsArea
		self.tabsList = tabsList

		# A list that will contain an AnalyteCheckBoxes object for each row in the filter
		self.checkBoxes = []

		# Builds the layout for the tab
		self.filter = QWidget()
		self.filter.layout = QVBoxLayout()
		self.filter.setLayout(self.filter.layout)

		# The options section of the tab
		self.controlsLayout = QHBoxLayout()
		self.filter.layout.addLayout(self.controlsLayout)

		# The information box
		self.infoBox = QTextEdit()
		self.controlsLayout.addWidget(self.infoBox)

		self.infoBox.setHtml(
			"<p style=\"color:#779999; font-size:14px; margin-bottom:10px;\"><strong>" +
			self.filterInfo["filter_name"] + "</strong></p>" + self.filterInfo["filter_description"])

		self.infoBox.setReadOnly(True)
		self.infoBox.setFixedWidth(300)
		self.infoBox.setFixedHeight(120)

		# The area for the filter options. This will be populated by the specific filter type
		self.optionsWidget = QWidget()
		self.optionsWidget.setMinimumWidth(500)

		self.controlsLayout.addWidget(self.optionsWidget)

		# The section for the buttons
		self.controlButtonsLayout = QVBoxLayout()
		self.controlsLayout.addLayout(self.controlButtonsLayout)
		self.controlButtonsLayout.setAlignment(Qt.AlignTop)

		# We create the control buttons
		self.crossPlotButton = QPushButton("Cross-plot")
		self.crossPlotButton.clicked.connect(self.crossPlotClick)
		#self.controlButtonsLayout.addWidget(self.crossPlotButton)

		# Button to create a pop-up plot.
		self.plotButton = QPushButton("Plot")
		self.plotButton.clicked.connect(self.plotClick)
		self.controlButtonsLayout.addWidget(self.plotButton)

		# We add a stretch to push down the buttons
		self.controlButtonsLayout.addStretch(1)

		self.deleteButton = QPushButton("Delete filter")
		self.deleteButton.clicked.connect(self.deleteClick)
		self.controlButtonsLayout.addWidget(self.deleteButton)

		# The area for the table of analytes.

		# We use a special widget purely to help with resizing the scrollable area to the window width
		self.checksArea = QWidget()

		# We create the scroll area that will display the table of analytes and filters
		self.scroll = QScrollArea()
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll.setFixedHeight(70)
		#self.scroll.setFixedWidth(self.filter.frameSize().width() - 100)
		self.scroll.setWidgetResizable(True)

		self.filter.layout.addWidget(self.scroll)
		self.checksArea.scroll = self.scroll

		self.innerWidget = QWidget()

		self.innerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		self.table = QGridLayout(self.innerWidget)

		# We add the heading row to the table. The rest of the table will be added by the specific filter
		self.filterLabel = QLabel("<span style=\"color:#888888\"><strong>Filter</strong></span>")
		self.filterLabel.setMinimumWidth(100)
		self.table.addWidget(self.filterLabel, 0, 0)

		for i in range(len(self.project.eg.analytes)):
			self.table.addWidget(QLabel("<span style=\"color:#779999\"><strong>" +
										str(self.project.eg.analytes[i]) +
										"< / strong > < / span > "), 0, i + 1)

		self.scroll.setWidget(self.innerWidget)

		# Here the specific filter type is determined and created
		if self.filterName == "Threshold":
			self.filterType = ThresholdFilter(self)
		if self.filterName == "Clustering":
			self.filterType = ClusteringFilter(self)
		if self.filterName == "Correlation":
			self.filterType = CorrelationFilter(self)
		if self.filterName == "Defragment":
			self.filterType = DefragmentFilter(self)
		if self.filterName == "Exclude Downhole":
			self.filterType = ExcludeFilter(self)
		if self.filterName == "Trim":
			self.filterType = TrimFilter(self)
		if self.filterName == "Signal Optimiser":
			self.filterType = SignalFilter(self)

		# Stops the checkboxes from registering programmatic changes
		self.updatingCheckboxes = False

	def updateName(self, index):

		self.tabsArea.setTabText(index, self.name)

		# We also take the opportunity of changing back to the Summary tab
		self.tabsArea.setCurrentIndex(0)

		# We reset the progress bar
		self.project.progressBar.reset()

	def addButton(self, buttonWidget):
		""" Adds a given button to the right-most Options section """
		self.controlButtonsLayout.addWidget(buttonWidget)

	def filtOnOff(self, f):

		for checks in self.checkBoxes:
			checks.filtOnOff(f)

	def createFilter(self, name):
		self.checkBoxes.append(AnalyteCheckBoxes(name, self, self.summaryTab))

	def deleteClick(self):

		# A popup message is created to ask to save the project
		reply = QMessageBox.question(self.filter, 'Message',
									 "Are you sure you want to delete this filter?", QMessageBox.Yes |
									 QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:
			# If yes
			self.tabsArea.setCurrentIndex(0)

			for row in self.checkBoxes:
				row.deleteRow()

			self.filter.setParent(None)

	def updateOptions(self):
		""" Gets a dictionary of the current filter options and passes them to the plot window """
		return self.filterType.updateOptions()

	def crossPlotClick(self):
		""" Activates when the Cross-plot button is pressed """
		self.graphPaneObj.showAuxGraph(cross=True)

	def plotClick(self):
		""" Activates when the Plot button is pressed. Creates the filter plot window """
		self.plot = filterPlot.FilterPlot(self, self.project)
		self.plot.show()


class AnalyteCheckBoxes:
	""" Contains and controls the checkboxes for one row of a filter """

	def __init__(self, filterName, filterTab, summaryTab):
		"""
		:param filterName: The technical name that LA Tools gives the filter row
		:param filterTab: A reference to the Filter's tab object
		:param summaryTab: A reference to the Summary tab
		"""
		self.name = filterName
		self.filterTab = filterTab
		self.summaryTab = summaryTab

		# Lists that contain the checkbox objects for the filter's tab and the summary tab
		self.controlsBoxes = []
		self.summaryBoxes = []
		self.nameLabel = QLabel(self.name)

		# A variable that we use to determine when we are programmatically updating checkboxes, so that
		# these updates will not trigger the program to think that the user has made that update
		self.updatingCheckboxes = False

		# We create each checkbox that will appear in the filter controls and summary tabs
		for i in range(len(self.filterTab.project.eg.analytes)):
			self.controlsBoxes.append(QCheckBox())
			self.summaryBoxes.append(QCheckBox())

			# We connect the summary and control checkboxes with functions that will activate when their state changes
			self.controlsBoxes[i].stateChanged.connect(
				lambda a, i=i: self.updateCheckBox(i, 0))

			self.summaryBoxes[i].stateChanged.connect(
				lambda a, i=i: self.updateCheckBox(i, 1))

		# We create a row in the analytes table for the filter
		self.filterTab.table.addWidget(QLabel(self.name), self.filterTab.table.rowCount(), 0)

		# We populate the row with checkboxes
		for i in range(self.filterTab.table.columnCount() - 1):
			self.filterTab.table.addWidget(self.controlsBoxes[i], self.filterTab.table.rowCount() - 1, i + 1)

		row = self.summaryTab.table.rowCount()

		# We create a row in the analytes table in the Summary tab for the filter
		self.summaryTab.table.addWidget(self.nameLabel, row, 0)

		# We populate the row with checkboxes
		for i in range(self.filterTab.summaryTab.table.columnCount() - 2):
			self.filterTab.summaryTab.table.addWidget(self.summaryBoxes[i], row, i + 1)

		# We add a "select all" checkbox
		self.selectAllCheckBox = QCheckBox()
		self.selectAllCheckBox.stateChanged.connect(self.selectAllClicked)
		self.summaryTab.table.addWidget(self.selectAllCheckBox, row, self.summaryTab.table.columnCount() - 1)

	def updateCheckBox(self, i, ID):
		""" Activates when a checkbox is clicked
		i: The index of the checkbox in the list (same as the list of analytes)
		ID: 0 = controls tab was clicked. 1 == summary tab was clicked
		"""

		# If the change was the result of user input (rather than us updating the checkbox via the program)
		if not self.updatingCheckboxes:

			self.updatingCheckboxes = True

			if ID == 0:
				selfBox = self.controlsBoxes[i]
				otherBox = self.summaryBoxes[i]
			else:
				otherBox = self.controlsBoxes[i]
				selfBox = self.summaryBoxes[i]

			# We set the paired checkbox to the original's state
			otherBox.setCheckState(selfBox.checkState())

			# We update the filter for each analyte
			if selfBox.checkState() != 0:
				# The checkbox is on
				self.filterTab.project.eg.filter_on(self.name, self.filterTab.project.eg.analytes[i])
			else:
				# The checkbox is off
				self.filterTab.project.eg.filter_off(self.name, self.filterTab.project.eg.analytes[i])
				self.selectAllCheckBox.setChecked(False)

			self.updatingCheckboxes = False

	def selectAllClicked(self):
		""" Activates when the "select all" checkbox is clicked """

		# Using the updatingCheckboxes bool will prevent the toggled checkboxes from activating their clicked functions
		if not self.updatingCheckboxes:
			self.updatingCheckboxes = True

			if self.selectAllCheckBox.checkState() == 2:
				# We use a call to filter_on without an analyte listed to turn them all on
				self.filterTab.project.eg.filter_on(self.name)
				# We switch on all of the actual checkboxes.
				for i in range(len(self.controlsBoxes)):
					self.controlsBoxes[i].setChecked(True)
					self.summaryBoxes[i].setChecked(True)
			else:
				# We use a call to filter_off without an analyte listed to turn them all off
				self.filterTab.project.eg.filter_off(self.name)
				# We switch all of the checkboxes off
				for i in range(len(self.controlsBoxes)):
					self.controlsBoxes[i].setChecked(False)
					self.summaryBoxes[i].setChecked(False)

			self.updatingCheckboxes = False

	def filtOnOff(self, f):
		""" When loading a file any line about filter being turned on or off is sent here.
		f: a tuple containing: ("filter_on" or "filter_off", (The filter's technical name, The analyte name or not)
		"""

		# We check all filter on/off calls with all rows, and just update when the names match
		if f[1][0] == self.name:

			# If there is an analyte listed in the filt_on or filt_off call
			if len(f[1]) == 2:
				analyte = f[1][1]
				column = 0

				# We find the column index based on the analyte name
				for i in range(len(self.filterTab.project.eg.analytes)):
					if self.filterTab.project.eg.analytes[i] == analyte:
						column = i

				#self.updatingCheckboxes = True

				# We run the loaded filter on/off call, and then update the checkboxes
				if f[0] == "filter_on":
					#self.filterTab.project.eg.filter_on(self.name, analyte)
					self.summaryBoxes[column].setChecked(True)
					#self.controlsBoxes[column].setChecked(True)
				else:
					#self.filterTab.project.eg.filter_off(self.name, analyte)
					self.summaryBoxes[column].setChecked(False)
					#self.controlsBoxes[column].setChecked(False)

				self.updatingCheckboxes = False

			# The filt_on or filt_off applies to a select all call
			else:
				self.selectAllCheckBox.setChecked(not self.selectAllCheckBox.isChecked())

	def deleteRow(self):
		""" Deletes this filter and removes it from the summary tab """
		self.filterTab.project.eg.filter_off(self.name)
		for box in self.summaryBoxes:
			box.setParent(None)
		self.selectAllCheckBox.setParent(None)
		self.nameLabel.setParent(None)
