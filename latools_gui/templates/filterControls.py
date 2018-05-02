""" Builds a custom controls pane for the filtering stage
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys

class FilterControls():
	"""
	The Filtering Stage has its own customised controls pane
	"""
	def __init__(self, stageLayout):
		"""
		Initialising builds the pane and prepares it for options to be added by the stage object.

		Parameters
		----------
		stageLayout : QVBoxLayout
			The layout for the entire stage screen, that the Controls Pane will add itself to.
		"""

		self.tabsArea = QTabWidget()
		stageLayout.addWidget(self.tabsArea)

		self.tabsArea.setMinimumHeight(250)

		self.tabsList = []

		self.tab1 = QWidget()
		self.tab2 = QWidget()
		self.tab3 = QWidget()

		self.tabsArea.addTab(self.tab1, "First tab")
		self.tabsArea.addTab(self.tab2, "Second tab")
		self.tabsArea.addTab(self.tab3, "third tab")

		self.tab1.layout = QVBoxLayout()
		self.tab1.layout.addWidget(QLabel("First tab content"))
		self.tab1.setLayout(self.tab1.layout)

		self.tab2.layout = QVBoxLayout()
		self.tab2.layout.addWidget(QLabel("Second tab content"))
		self.tab2.setLayout(self.tab2.layout)

		self.tab3.layout = QVBoxLayout()
		self.tab3.layout.addWidget(QLabel("Third tab content"))
		self.tab3.setLayout(self.tab3.layout)

		self.plusTab = QWidget()
		self.tabsArea.addTab(self.plusTab, "+")

		self.plusTab.layout = QVBoxLayout()
		self.plusTab.layout.addWidget(QLabel("New tab name:"))
		self.plusTab.setLayout(self.plusTab.layout)

		self.plusNameField = QLineEdit()
		self.plusTab.layout.addWidget(self.plusNameField)
		self.plusNameField.cursorPositionChanged.connect(self.plusNameEdit)
		self.plusNameField.setFixedWidth(100)

		self.plusNameButton = QPushButton("Add tab")
		self.plusNameButton.clicked.connect(self.addTab)
		self.plusNameButton.setEnabled(False)
		self.plusTab.layout.addWidget(self.plusNameButton)
		self.plusNameButton.setFixedWidth(100)

	def addTab(self):
		newTab = QWidget()
		newTab.layout = QVBoxLayout()
		newTab.layout.addWidget(QLabel(self.plusNameField.text()))
		newTab.setLayout(newTab.layout)

		self.plusTab.setParent(None)
		self.tabsArea.addTab(newTab, self.plusNameField.text())
		self.tabsArea.addTab(self.plusTab, "+")

		self.tabsArea.setCurrentIndex(self.tabsArea.currentIndex() + 1)
		self.plusNameField.setText("")

	def plusNameEdit(self):
		if self.plusNameField.text() != "":
			self.plusNameButton.setEnabled(True)
