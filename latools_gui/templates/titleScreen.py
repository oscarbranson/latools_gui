""" Builds and displays the title screen for the program where a new project is started, or an existing project
	is continued with.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

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
		self.fileLocation = None
		self.projectName = None
		self.loadProjectBool = False
		self.importListener = None

		# The layout is created from the mainWidget
		self.mainLayout = QVBoxLayout(self.mainWidget)
		# and center aligned.
		self.mainLayout.setAlignment(Qt.AlignCenter)

		# We currently use spacers to center the content vertically
		self.topSpacer = QSpacerItem(0, 125, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.mainLayout.addItem(self.topSpacer)

		# We display the logo using a label
		self.logoImage = QLabel()
		# This is then set with a QPixmap of the image, found in the graphics folder
		self.logoImage.setPixmap(QPixmap("graphics/latools-logo-small-transparent.png"))
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

		self.titleGridWidget = QWidget()
		self.titleGrid = QGridLayout(self.titleGridWidget)
		self.mainLayout.addWidget(self.titleGridWidget)

		self.newProjectButton = QPushButton("New project")
		self.newProjectButton.clicked.connect(self.newButtonClick)

		self.openProjectButton = QPushButton("Open project")
		self.openProjectButton.clicked.connect(self.openButtonClick)

		self.titleGrid.addWidget(self.newProjectButton, 0, 0)
		self.titleGrid.addWidget(self.openProjectButton, 0, 1)

		self.recentDropdown = QComboBox()
		self.titleGrid.addWidget(self.recentDropdown, 1, 0, 1, 2)
		self.recentDropdown.activated.connect(self.recentClicked)
		self.recentDropdown.addItem("Recent projects")
		self.recentDropdown.addItem("Test 1")
		self.recentDropdown.addItem("Test 2")

		self.newProjectBool = False

		self.nameLabel = QLabel("Project name:")
		self.titleGrid.addWidget(self.nameLabel, 1, 0)
		self.nameLabel.setVisible(False)

		self.nameEdit = QLineEdit()
		self.titleGrid.addWidget(self.nameEdit, 2, 0, 1, 2)
		self.nameEdit.setVisible(False)
		self.nameEdit.cursorPositionChanged.connect(self.nameEdited)

		# Currently just a button that begins the demo project
		self.nextButton = QPushButton("Begin")
		# The button click calls the nextButtonClick method, within this class
		self.nextButton.setEnabled(False)
		self.nextButton.clicked.connect(self.nextButtonClick)
		self.titleGrid.addWidget(self.nextButton, 3, 0)

		self.backButton = QPushButton("Back")
		self.backButton.clicked.connect(self.backButtonClick)
		self.titleGrid.addWidget(self.backButton, 3, 1)
		self.backButton.setVisible(False)

		self.logoSpacer = QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.mainLayout.addItem(self.logoSpacer)

		self.helpButton = QPushButton("Online Manual")
		self.mainLayout.addWidget(self.helpButton)
		self.helpButton.clicked.connect(self.helpButtonClick)

		# A spacer at the bottom.
		self.bottomSpacer = QSpacerItem(0, 125, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.mainLayout.addItem(self.bottomSpacer)

	def setImportListener(self, importListener):
		self.importListener = importListener

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

		#TO DO: load project or begin new one

		if self.loadProjectBool:
			self.projectName = self.fileLocation[0]
		elif self.newProjectBool:
			self.projectName = self.nameEdit.text()
		else:
			self.projectName = self.recentDropdown.currentText()

		self.importListener.setTitle(self.projectName)
		self.parentStack.setCurrentIndex(1)

	def newButtonClick(self):

		self.newProjectBool = True
		self.recentDropdown.setVisible(False)
		self.nameLabel.setVisible(True)
		self.nameEdit.setVisible(True)
		self.backButton.setVisible(True)
		self.nextButton.setEnabled(False)

	def openButtonClick(self):

		self.fileLocation = QFileDialog.getOpenFileName(self.mainWidget, 'Open file', '/home')
		#print(self.fileLocation)

		# TO DO: Load project
		if self.fileLocation[0] != '':
			self.loadProjectBool = True
			self.nextButtonClick()


	def recentClicked(self):

		if self.recentDropdown.currentText() != "Recent projects":
			self.nextButton.setEnabled(True)
		else:
			self.nextButton.setEnabled(False)

	def backButtonClick(self):

		self.newProjectBool = False
		self.recentDropdown.setVisible(True)
		self.nameLabel.setVisible(False)
		self.nameEdit.setVisible(False)
		self.backButton.setVisible(False)
		self.nextButton.setEnabled(False)
		self.recentDropdown.setCurrentIndex(0)

	def nameEdited(self):

		if self.nameEdit.text() != "":
			self.nextButton.setEnabled(True)
		else:
			self.nextButton.setEnabled(False)

	def addRecentProjects(self, names):
		# TO DO: Get list of recent projects and add the names to self.recentDropdown
		x = 1

	def helpButtonClick(self):

		url = QUrl("https://github.com/oscarbranson/latools")
		QDesktopServices.openUrl(url)
