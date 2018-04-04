from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

class ControlsPane():
	"""
	Provides the control pane for each stage to customise, and move between.
	A lot of functionality potential will be added to this class, which may require some 
	restructuring.
	"""
	def __init__(self, stageLayout):

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
		self.controlDescriptionBox.setFixedHeight(180)

		# STEP OPTIONS SECTION

		self.optionsWidget = QWidget()
		self.optionsWidget.setMaximumWidth(400)
		self.controlsLayout.addWidget(self.optionsWidget)

		# The actual options will be customised and added via method calls below

		# STEP STANDARDS PANE

		# Similar to the options pane above, the functionality around this
		# will be defined and added soon.
		self.controlStandardsLayout = QVBoxLayout()
		self.controlsLayout.addLayout(self.controlStandardsLayout)
		self.controlStandardsLayout.setAlignment(Qt.AlignTop)
		self.controlStandardsLayout.addWidget(QLabel("Standards"))

		# Dummy options temporarily:
		self.standardsCheck1 = QCheckBox("Standard 1")
		self.controlStandardsLayout.addWidget(self.standardsCheck1)

		self.standardsCheck2 = QCheckBox("Standard 2")
		self.controlStandardsLayout.addWidget(self.standardsCheck2)

		self.standardsCheck3 = QCheckBox("Standard 3")
		self.controlStandardsLayout.addWidget(self.standardsCheck3)

		# We add a stretch to push down the apply button
		self.controlStandardsLayout.addStretch(1)

	def getOptionsWidget(self):
		return self.optionsWidget

	# The description info is passed to the object, starting with the title
	def setTitle(self, title):
		self.controlDescriptionBox.insertHtml("<span style=\"color:#779999; "
			"font-size:24px;\"><b>" + title + "</b></span><br><br>")

	# And then the description text. There is work to be done to make this process
	# cleaner, or automatic.
	def setDescription(self, description):
		self.controlDescriptionBox.setHtml(description)

	# This will be extended with actual funcitonality.
	# The 'style' number here could refer to what kind of function is needed (checkbox/drop-down)
	# But we will probably use something more robust given more specific knowledge of what is 
	# needed here.

	def addApplyButton(self, button):
		self.controlStandardsLayout.addWidget(button)