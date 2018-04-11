""" Builds a pane below the navigation bar that displays information on the current stage, and houses the
	options that control the functionality of the stage.
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

class ControlsPane():
	"""
	Each stage has its own Controls Pane that houses the information and options unique to that stage.
	"""
	def __init__(self, stageLayout):
		"""
		Initialising builds the pane and prepares it for options to be added by the stage object.

		Parameters
		----------
		stageLayout : QVBoxLayout
			The layout for the entire stage screen, that the Controls Pane will add itself to.
		"""
		# We make a frame for the panel
		self.controlsFrame = QFrame()
		self.controlsFrame.setFrameShape(QFrame.StyledPanel)
		self.controlsFrame.setFrameShadow(QFrame.Raised)

		# We make the panel a horizontal box layout
		self.controlsLayout = QHBoxLayout(self.controlsFrame)
		stageLayout.addWidget(self.controlsFrame)

		# We use a QTextEdit here for displaying the stage description.
		# The content is defined via a method call below.
		self.controlDescriptionBox = QTextEdit()
		self.controlsLayout.addWidget(self.controlDescriptionBox)

		# We set it to read only
		self.controlDescriptionBox.setReadOnly(True)
		
		# We fix the width and height
		self.controlDescriptionBox.setFixedWidth(300)
		self.controlsFrame.setFixedHeight(200)

		# We create a widget to house the stage options. These will be filled in via function calls from
		# the stage object.
		self.optionsWidget = QWidget()
		self.optionsWidget.setMinimumWidth(400)
		self.controlsLayout.addWidget(self.optionsWidget)

		# The layout for the right-most section where the Apply button(s) will be added.
		self.controlStandardsLayout = QVBoxLayout()
		self.controlsLayout.addLayout(self.controlStandardsLayout)
		self.controlStandardsLayout.setAlignment(Qt.AlignTop)

		# We add a stretch to push down the apply button
		self.controlStandardsLayout.addStretch(1)

	def getOptionsWidget(self):
		""" Allows the stage object to receive the widget for the options section, so that they can add
			stage options to this directly, and have them displayed.

			Returns
			-------
			QWidget
				The widget that the stage options can be added to directly.
		"""
		return self.optionsWidget

	def setTitle(self, title):
		""" Populates the description box with the stage title

			Parameters
			----------
			title : str
				The title to be displayed
		"""
		self.controlDescriptionBox.insertHtml("<span style=\"color:#779999; "
			"font-size:24px;\"><b>" + title + "</b></span><br><br>")

	def setDescription(self, description):
		""" Populates the description box with the stage description

			Parameters
			----------
			description : str
				The description to be displayed
		"""
		self.controlDescriptionBox.setHtml(description)

	def addApplyButton(self, button):
		""" Adds a button to the right-most section of the Controls pane

			Parameters
			----------
			button : QPushButton
				A button to be added to the right-most layout
		"""
		self.controlStandardsLayout.addWidget(button)