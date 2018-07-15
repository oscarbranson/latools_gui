""" Builds a custom controls pane for the filtering stage
"""
import typing

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize, QObject, QMetaObject
import latools as la
import sys


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
		"""

		self.project = project
		self.tabsArea = QTabWidget()
		stageLayout.addWidget(self.tabsArea)

		#self.tabsArea.setMinimumHeight(200)

		self.tabsList = []

		#self.tab1 = QWidget()

		self.summaryTab = SummaryTab(self.project)
		self.tabsArea.addTab(self.summaryTab.summary, "Summary")

		#self.tabsArea.addTab(self.tab1, "First tab")

		#self.tab1.layout = QVBoxLayout()
		#self.tab1.layout.addWidget(QLabel("First tab content"))
		#self.tab1.setLayout(self.tab1.layout)

		self.plusTab = QWidget()
		self.tabsArea.addTab(self.plusTab, "+")

		self.plusTab.layout = QGridLayout()
		self.plusTab.setLayout(self.plusTab.layout)

		self.plusNameLabel = QLabel("Name")
		self.plusTab.layout.addWidget(self.plusNameLabel, 0, 0)

		self.plusNameField = QLineEdit()
		self.plusTab.layout.addWidget(self.plusNameField, 0, 1, 1, 2)
		self.plusNameField.cursorPositionChanged.connect(self.plusNameEdit)
		#self.plusNameField.setFixedWidth(200)

		self.plusFilterLabel = QLabel("Filter")
		self.plusTab.layout.addWidget(self.plusFilterLabel, 1, 0)

		self.plusFilterCombo = QComboBox()
		self.plusTab.layout.addWidget(self.plusFilterCombo, 1, 1, 1, 2)

		#Temporary
		self.plusFilterCombo.addItem("")
		self.plusFilterCombo.addItem("Example filter")

		self.plusFilterCombo.activated.connect(self.plusFilterChange)

		self.plusDescription = QTextEdit()
		self.plusDescription.setReadOnly(True)
		self.plusDescription.setFixedHeight(180)

		self.plusTab.layout.addWidget(self.plusDescription, 0, 3, 4, 6)

		self.plusAddButton = QPushButton("Add filter")
		self.plusAddButton.clicked.connect(self.addTab)
		self.plusAddButton.setEnabled(False)
		self.plusTab.layout.addWidget(self.plusAddButton, 3, 2)
		#self.plusAddButton.setFixedWidth(100)

	def addTab(self):

		newTab = FilterTab(self.plusNameField.text(), self.plusFilterCombo.currentText(), self.summaryTab)
		self.summaryTab.addFilter(self.plusNameField.text())
		self.tabsList.append(newTab)

		self.plusTab.setParent(None)
		self.tabsArea.addTab(newTab.filter, self.plusNameField.text())
		self.tabsArea.addTab(self.plusTab, "+")

		self.tabsArea.setCurrentIndex(self.tabsArea.currentIndex() + 1)
		self.plusNameField.setText("")
		self.plusAddButton.setEnabled(False)
		self.plusFilterCombo.setCurrentIndex(0)

	def plusNameEdit(self):
		if self.plusNameField.text() != "":
			self.plusAddButton.setEnabled(True)

	def updateStageInfo(self):
		""" Updates the stage after data is imported at runtime """

		#for analyte in self.project.eg.analytes:
		self.summaryTab.addElements(self.project.eg.analytes)

	def updateDescription(self, title, description):

		self.plusDescription.setHtml("<span style=\"color:#779999; "
										   "font-size:14px;\"><b>" + title + "</b></span><br><br>" + description)

	def plusFilterChange(self):

		if self.plusFilterCombo.currentText() == "Example filter":
			self.updateDescription("Example Filter Name", "Example filter description.")
		else:
			self.updateDescription("", "")


class SummaryTab:

	def __init__(self, project):

		self.summary = SummaryWidget()

		self.scroll = QScrollArea(self.summary)
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		#self.scrollWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll.setFixedHeight(220)
		self.scroll.setFixedWidth(self.summary.frameSize().width())
		self.scroll.setWidgetResizable(True)

		#self.scroll.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		self.summary.scrollArea = self.scroll

		self.innerWidget = QWidget()
		#self.innerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		#self.innerWidget.setMinimumWidth(300)
		#self.innerWidget.setMinimumHeight(220)
		#self.innerWidget.setGeometry(0, 0, 300, 300)

		self.innerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		self.table = QGridLayout(self.innerWidget)
		#self.innerWidget.setLayout(self.table)
		#self.table.setSizeConstraint(QLayout.SetMinAndMaxSize)

		self.filterLabel = QLabel("<span style=\"color:#888888\"><strong>Filter</strong></span>")
		self.filterLabel.setMinimumWidth(100)
		self.table.addWidget(self.filterLabel, 0, 0)

		#self.newFilterButton = QPushButton("+")
		#self.newFilterButton.setMaximumWidth(30)
		# Connect button
		#self.table.addWidget(self.newFilterButton, 2, 0)

		self.scroll.setWidget(self.innerWidget)

	def addElements(self, analytes):

		for i in range(len(analytes)):
			self.table.addWidget(QLabel("<span style=\"color:#779999\"><strong>" +
										str(analytes[i]) +
										"< / strong > < / span > "), 0, i + 1)
		#self.addFilter("Example filter")

	def addFilter(self, filterName):
		self.table.addWidget(QLabel(filterName), self.table.rowCount(), 0)

	def createFilter(self, name):
		for i in range(self.table.columnCount() - 1):
			self.table.addWidget(QCheckBox(), self.table.rowCount() - 1, i + 1)




class SummaryWidget(QWidget):
	# def __init__(self, parent=None, flags=None, Qt_WindowFlags=None, Qt_WindowType=None, *args, **kwargs):
	# 	super().__init__(parent, flags)
	#

	def resizeEvent(self, event):
		self.scrollArea.setFixedWidth(self.frameSize().width())
		return super().resizeEvent(event)


class FilterTab:

	def __init__(self, name, filter, summaryTab):

		self.name = name
		self.filter = filter
		self.summaryTab = summaryTab

		self.filter = QWidget()
		self.filter.layout = QHBoxLayout()
		self.filter.setLayout(self.filter.layout)

		self.infoBox = QTextEdit()
		self.filter.layout.addWidget(self.infoBox)

		self.infoBox.setReadOnly(True)
		self.infoBox.setFixedWidth(300)

		self.infoBox.setHtml("<span style=\"color:#779999; font-size:14px;\"><b> Info </b></span><br><br> about the filter options")

		self.filter.layout.addWidget(QLabel("Options"))
		self.filter.layout.addStretch(1)

		self.createButton = QPushButton("Create")
		self.filter.layout.addWidget(self.createButton)
		self.createButton.clicked.connect(self.createClick)

	def createClick(self):
		self.summaryTab.createFilter(self.name)




