""" Builds a custom controls pane for the filtering stage
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QObject, QMetaObject
import json
import latools as la

from filters.thresholdFilter import ThresholdFilter


class FilterControls:
	"""
	The Filtering Stage has its own customised controls pane
	"""
	def __init__(self, stageLayout, project):
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
		self.filterList = ["Threshold"]

		# This will hold the contents of the selected filter's json information file
		self.filterInfo = None

		self.project = project
		self.tabsArea = QTabWidget()
		stageLayout.addWidget(self.tabsArea)

		# A list of all of the filter tabs
		self.tabsList = []

		# The first tab is the Summary tab
		self.summaryTab = SummaryTab(self.project)
		self.tabsArea.addTab(self.summaryTab.summary, "Summary")

		# The last tab is the "New Filter tab"
		self.plusTab = QWidget()
		self.tabsArea.addTab(self.plusTab, "+")

		# We build the New Filter tab, starting with a grid layout
		self.plusTab.layout = QGridLayout()
		self.plusTab.setLayout(self.plusTab.layout)

		# The name option for the New Filter
		self.plusNameLabel = QLabel("Name")
		self.plusTab.layout.addWidget(self.plusNameLabel, 0, 0)
		self.plusNameField = QLineEdit()
		self.plusTab.layout.addWidget(self.plusNameField, 0, 1, 1, 2)
		self.plusNameField.textChanged.connect(self.plusNameEdit)

		# The filter type option for the New Filter
		self.plusFilterLabel = QLabel("Filter")
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
		self.plusDescription.setFixedHeight(180)

		self.plusTab.layout.addWidget(self.plusDescription, 0, 3, 4, 6)

		# The Add button for the New Filter
		self.plusAddButton = QPushButton("Add filter")
		self.plusAddButton.clicked.connect(self.addTab)
		self.plusAddButton.setEnabled(False)
		self.plusTab.layout.addWidget(self.plusAddButton, 3, 2)

	def addTab(self):
		""" Makes a new filter tab when the New Filter Add button is pressed """

		# Creates the filter's control tab
		newTab = FilterTab(self.plusNameField.text(),
						   self.plusFilterCombo.currentText(),
						   self.summaryTab,
						   self.filterInfo,
						   self.project)
		# self.summaryTab.addFilter(self.plusNameField.text())
		self.tabsList.append(newTab)

		# Shuffles the tabs so that the Add Filter tab is at the end
		self.plusTab.setParent(None)
		self.tabsArea.addTab(newTab.filter, self.plusNameField.text())
		self.tabsArea.addTab(self.plusTab, "+")

		# Opens the newly created filter tab
		self.tabsArea.setCurrentIndex(self.tabsArea.currentIndex() + 1)

		# Resets the Add Filter tab fields
		self.plusNameField.setText("")
		self.plusAddButton.setEnabled(False)
		self.plusFilterCombo.setCurrentIndex(0)
		self.plusFilterChange()

	def plusNameEdit(self):
		""" Activates when the New Filter tab's name field is edited """

		# Only activates the Create button when the name and filter type options are legit
		if self.plusNameField.text() != "" and self.plusFilterCombo.currentText() != "":
			self.plusAddButton.setEnabled(True)
		else:
			self.plusAddButton.setEnabled(False)

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

		# We check what was selected
		if self.plusFilterCombo.currentText() == "Threshold":

			# Here we get the filter description from the json file
			read_file = open("information/thresholdFilterInfo.json", "r")
			self.filterInfo = json.load(read_file)
			read_file.close()

			self.updateDescription(self.filterInfo["filter_name"], self.filterInfo["filter_description"])
		else:
			# Otherwise the blank was selected, so we clear the info box
			self.updateDescription("", "")

		# Only activates the Create button when the name and filter type options are legit
		if self.plusNameField.text() != "" and self.plusFilterCombo.currentText() != "":
			self.plusAddButton.setEnabled(True)
		else:
			self.plusAddButton.setEnabled(False)

class SummaryTab:
	""" The tab that lists all of the created filters and can activate the filtering process """

	def __init__(self, project):

		# We use a special widget purely to help with resizing the scrollable area to the window width
		self.summary = SummaryWidget()

		# We create the scroll area that will display the table of analytes and filters
		self.scroll = QScrollArea(self.summary)
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll.setFixedHeight(220)
		self.scroll.setFixedWidth(self.summary.frameSize().width())
		self.scroll.setWidgetResizable(True)

		self.summary.scrollArea = self.scroll

		# We make an area inside the scroll to fill with the table
		self.innerWidget = QWidget()

		self.innerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		self.table = QGridLayout(self.innerWidget)

		# The Filter label is added to the table first
		self.filterLabel = QLabel("<span style=\"color:#888888\"><strong>Filter</strong></span>")
		self.filterLabel.setMinimumWidth(100)
		self.table.addWidget(self.filterLabel, 0, 0)

		self.scroll.setWidget(self.innerWidget)

	def addElements(self, analytes):
		""" When the analytes are available at run time, they are populated in the table """
		for i in range(len(analytes)):
			self.table.addWidget(QLabel("<span style=\"color:#779999\"><strong>" +
										str(analytes[i]) +
										"< / strong > < / span > "), 0, i + 1)

class SummaryWidget(QWidget):
	""" A simple helper class to allow the scrollable area in the summary filter tab to resize with the window """

	def resizeEvent(self, event):
		self.scrollArea.setFixedWidth(self.frameSize().width())
		return super().resizeEvent(event)


class FilterTab:
	""" Creates the controls tab for a filter """

	def __init__(self, name, filterName, summaryTab, filterInfo, project):

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
		self.infoBox.setFixedHeight(100)

		# The area for the filter options. This will be populated by the specific filter type
		self.optionsWidget = QWidget()
		self.optionsWidget.setMinimumWidth(500)

		self.controlsLayout.addWidget(self.optionsWidget)

		# The section for the buttons
		self.controlButtonsLayout = QVBoxLayout()
		self.controlsLayout.addLayout(self.controlButtonsLayout)
		self.controlButtonsLayout.setAlignment(Qt.AlignTop)

		# We add a stretch to push down the buttons
		self.controlButtonsLayout.addStretch(1)

		# The area for the table of analytes.
		# TO DO: make this area properly scrollable
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

		self.filter.layout.addWidget(self.innerWidget)

		# Here the specific filter type is determined and created
		if self.filterName == "Threshold":
			self.filterType = ThresholdFilter(self)

	def addButton(self, buttonWidget):
		""" Adds a given button to the right-most Options section """
		self.controlButtonsLayout.addWidget(buttonWidget)

