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
		self.fileName = None
		self.projectName = None
		self.loadProjectBool = False
		self.importListener = None
		self.nameOK = False
		self.locationOK = False

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

		self.newProjectBool = False

		self.nameLabel = QLabel("Project name:")
		self.titleGrid.addWidget(self.nameLabel, 1, 0)
		self.nameLabel.setVisible(False)

		self.nameEdit = QLineEdit()
		self.titleGrid.addWidget(self.nameEdit, 2, 0, 1, 2)
		self.nameEdit.setVisible(False)
		self.nameEdit.setMaxLength(60)

		self.locationLabel = QLabel("Save location:")
		self.titleGrid.addWidget(self.locationLabel, 3, 0)
		self.locationLabel.setVisible(False)

		self.newBrowse = QPushButton("Browse")
		self.titleGrid.addWidget(self.newBrowse, 3, 1)
		self.newBrowse.setVisible(False)
		self.newBrowse.clicked.connect(self.newBrowseClick)

		self.newLocation = QLineEdit()
		self.titleGrid.addWidget(self.newLocation, 4, 0, 1, 2)
		self.newLocation.setVisible(False)
		self.newLocation.setEnabled(False)

		# Currently just a button that begins the demo project
		self.nextButton = QPushButton("Begin")
		# The button click calls the nextButtonClick method, within this class
		self.nextButton.setEnabled(False)
		self.nextButton.clicked.connect(self.nextButtonClick)
		self.titleGrid.addWidget(self.nextButton, 5, 0)

		self.nameEdit.cursorPositionChanged.connect(self.nameEdited)

		self.backButton = QPushButton("Back")
		self.backButton.clicked.connect(self.backButtonClick)
		self.titleGrid.addWidget(self.backButton, 5, 1)
		self.backButton.setVisible(False)

		self.logoSpacer = QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.mainLayout.addItem(self.logoSpacer)

		self.helpButton = QPushButton("Online Manual")
		self.mainLayout.addWidget(self.helpButton)
		self.helpButton.clicked.connect(self.helpButtonClick)

		# A spacer at the bottom.
		self.bottomSpacer = QSpacerItem(0, 125, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.mainLayout.addItem(self.bottomSpacer)

		self.recentProjects = RecentProjects(self.recentDropdown)

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
			# Load project
			self.projectName = self.fileLocation[0]

		elif self.newProjectBool:
			# New project
			self.projectName = self.nameEdit.text()
			self.recentProjects.addNew(self.nameEdit.text(), self.fileLocation)

		else:
			# Dropdown selected
			self.projectName = self.recentDropdown.currentText()
			self.recentProjects.reorderDropdown(self.recentDropdown.currentIndex() - 1)

		self.importListener.setTitle(self.projectName)
		self.parentStack.setCurrentIndex(1)

	def newButtonClick(self):

		self.newProjectBool = True
		self.recentDropdown.setVisible(False)
		self.nameLabel.setVisible(True)
		self.nameEdit.setVisible(True)
		self.backButton.setVisible(True)
		self.locationLabel.setVisible(True)
		self.newBrowse.setVisible(True)
		self.newLocation.setVisible(True)
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
		self.locationLabel.setVisible(False)
		self.newBrowse.setVisible(False)
		self.newLocation.setVisible(False)
		self.nextButton.setEnabled(False)
		self.recentDropdown.setCurrentIndex(0)

	def nameEdited(self):

		forbiddens = {'<','>', ':', '\"', '/', '\\', '|', '?', '*'}

		if self.nameEdit.text() != "":
			self.nameOK = True

			# addedChar = self.nameEdit.text()[self.nameEdit.cursorPosition() - 1]

			for char in self.nameEdit.text():
				if char in forbiddens:
					self.nameOK = False

		else:
			self.nameOK = False

		self.nextButton.setEnabled(self.nameOK and self.locationOK)

	def helpButtonClick(self):

		url = QUrl("https://github.com/oscarbranson/latools")
		QDesktopServices.openUrl(url)

	def newBrowseClick(self):
		self.fileLocation = QFileDialog.getExistingDirectory(self.mainWidget, 'Open file', '/home')

		if self.fileLocation != '':
			self.newLocation.setText(self.fileLocation)
			self.locationOK = True

			self.nextButton.setEnabled(self.nameOK and self.locationOK)




class RecentProjects:

	def __init__(self, recentDropdown):

		recentFile = open("project/recentProjects.txt", "r")
		self.fileContent = recentFile.read().splitlines()
		recentFile.close()

		self.splitContent = []

		for name in self.fileContent:
			self.splitContent.append(name.split('*'))

		i = 0
		for split in self.splitContent:
			recentDropdown.addItem(split[0])
			i += 1
			if i > 9:
				break

		print(self.splitContent)

	def addNew(self, name, location):
		recentFile = open("project/recentProjects.txt", "w")
		recentFile.write(name + "*" + location + "\n")
		for line in self.fileContent:
			recentFile.write(line + "\n")
		recentFile.close()

	def reorderDropdown(self, index):
		recentFile = open("project/recentProjects.txt", "w")
		recentFile.write(self.fileContent[index] + "\n")
		for i in range(len(self.fileContent)):
			if i != index:
				recentFile.write(self.fileContent[i] + "\n")
		recentFile.close()
