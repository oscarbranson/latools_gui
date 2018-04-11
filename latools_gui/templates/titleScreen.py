""" Builds and displays the title screen for the program where a new project is started, or an existing project
	is continued with.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

class TitleScreen():
	"""
	The screen that shows up at the beginning of the program and allows a user to define a new project,
	or continue an existing one.
	"""
	def __init__(self, stack):
		"""
		Initialising builds and displays the screen.

		Parameters
		----------
		stack : QStackedWidget
			The stack for the main program, used for switching from the title screen to the stage screen.
		"""
		# We create a widget to hold the entire screen
		self.mainWidget = QWidget()

		# We save a reference to the main stack, so that our buttons can move us to the next screen
		self.parentStack = stack

		# The layout is created from the mainWidget
		self.mainLayout = QVBoxLayout(self.mainWidget)
		# and center aligned.
		self.mainLayout.setAlignment(Qt.AlignCenter)

		# We currently use spacers to center the content vertically
		self.topSpacer = QSpacerItem(0, 150, QSizePolicy.Minimum, QSizePolicy.Expanding) 
		self.mainLayout.addItem(self.topSpacer)

		# We display the logo using a label
		self.logoImage = QLabel()
		# This is then set with a QPixmap of the image, found in the graphics folder
		self.logoImage.setPixmap(QPixmap("graphics/latools-logo-grey-background.png"))
		# The logo is then added to the layout
		self.mainLayout.addWidget(self.logoImage)
		
		# Small spacer after the logo
		self.logoSpacer = QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Expanding) 
		self.mainLayout.addItem(self.logoSpacer)

		# Hard-coded welcome message. We can update this with the appropriate text
		self.welcomeLabel = QLabel("<span style=\"font-size:20px;\">"
			"<b>Welcome to LA tools</b></span>")
		self.welcomeLabel.setAlignment(Qt.AlignCenter)
		self.mainLayout.addWidget(self.welcomeLabel)

		# Small spacer after the text
		self.welcomeSpacer = QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Expanding) 
		self.mainLayout.addItem(self.welcomeSpacer)

		# Currently just a button that begins the demo project
		self.nextButton = QPushButton("Begin demo project")
		# The button click calls the nextButtonClick method, within this class
		self.nextButton.clicked.connect(self.nextButtonClick)
		self.mainLayout.addWidget(self.nextButton)

		# A spacer at the bottom.
		self.bottomSpacer = QSpacerItem(0, 150, QSizePolicy.Minimum, QSizePolicy.Expanding) 
		self.mainLayout.addItem(self.bottomSpacer)

	def getPane(self):
		"""
		Provides the widget that the screen is contained in, so that it can be added to the
		main stack in latoolsgui

		Returns
		-------
		mainWidget : QWidget
			The widget that the houses the title screen.
		"""
		return(self.mainWidget)

	def nextButtonClick(self):
		"""
		The functionality for the 'next' button. Currently, this sets the main stack to
		index 1: the stages screen
		"""
		self.parentStack.setCurrentIndex(1)