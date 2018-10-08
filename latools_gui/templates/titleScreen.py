""" Builds and displays the title screen for the program where a new project is started, or an existing project
	is continued with.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import os
import sys
from templates import progressUpdater

class TitleScreen():
	"""
	The screen that shows up at the beginning of the program and allows a user to define a new project,
	or continue an existing one.
	"""
	def __init__(self, stack, project, links):
		"""
		Initialising builds and displays the screen.

		Parameters
		----------
		stack : QStackedWidget
			The stack for the main program, used for switching from the title screen to the stage screen.
		"""
		# We create a widget to hold the entire screen
		self.mainWidget = QWidget()

		self.parentStack = stack
		self.project = project
		self.fileLocation = ""
		self.projectName = None
		self.loadProjectBool = False
		self.importListener = None
		self.nameOK = False
		self.userGuideDomain = links[0]
		self.reportIssue = links[1]

		# The layout is created from the mainWidget
		self.mainLayout = QVBoxLayout(self.mainWidget)
		# and center aligned.
		self.mainLayout.setAlignment(Qt.AlignCenter)

		# We currently use spacers to center the content vertically
		self.topSpacer = QSpacerItem(0, 75, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.mainLayout.addItem(self.topSpacer)

		# We set the file location of the logo graphic depending on whether this is a dev or dist build
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			logoFile = os.path.join(os.path.dirname(sys.executable), 'graphics/latools-logo-small-transparent.png')
			logoFile = logoFile.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			logoFile = "graphics/latools-logo-small-transparent.png"

		# We display the logo using a label
		self.logoImage = QLabel()
		# This is then set with a QPixmap of the image, found in the graphics folder
		self.logoImage.setPixmap(QPixmap(logoFile))
		# The logo is then added to the layout
		self.mainLayout.addWidget(self.logoImage)
		
		# Small spacer after the logo
		self.logoSpacer = QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.mainLayout.addItem(self.logoSpacer)

		# Hard-coded welcome message. We can update this with the appropriate text
		self.welcomeLabel = QLabel("<span style=\"font-size:20px;\">"
			"<b>Welcome to LA tools</b></span>")
		self.welcomeLabel.setAlignment(Qt.AlignCenter)
		#self.mainLayout.addWidget(self.welcomeLabel)

		# Small spacer after the text
		#self.welcomeSpacer = QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		#self.mainLayout.addItem(self.welcomeSpacer)

		# A small grid of buttons and fields for starting or loading a project
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

		self.nameEdit = QLineEdit()
		self.nameEdit.setMaxLength(60)

		self.backButton = QPushButton("Back")
		self.backButton.clicked.connect(self.backButtonClick)

		# The button to load or begin the project
		self.nextButton = QPushButton("Begin")

		# The button click calls the nextButtonClick method, within this class
		self.nextButton.setEnabled(False)
		self.nextButton.clicked.connect(self.nextButtonClick)
		self.titleGrid.addWidget(self.nextButton, 5, 1)

		# Calls nameEdited() when the cursor position changes on NameEdit
		self.nameEdit.cursorPositionChanged.connect(self.nameEdited)

		self.logoSpacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.mainLayout.addItem(self.logoSpacer)

		# A button at the bottom which links to the online user guide
		self.helpWidget = QWidget()
		self.helpLayout = QHBoxLayout(self.helpWidget)
		self.helpButton = QPushButton("Online Manual")
		self.helpButton.setMaximumWidth(130)
		self.helpLayout.addWidget(self.helpButton)
		self.mainLayout.addWidget(self.helpWidget)
		self.helpButton.clicked.connect(self.helpButtonClick)

		# A button for reporting issues
		self.reportButton = QPushButton("Report an issue")
		self.helpLayout.addWidget(self.reportButton)
		self.reportButton.clicked.connect(self.reportButtonClick)
		self.reportButton.setToolTip(links[2])

		# A spacer at the bottom.
		self.bottomSpacer = QSpacerItem(0, 75, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.mainLayout.addItem(self.bottomSpacer)

		# A progress bar for loading a project
		self.progressLabel = QLabel("")
		self.mainLayout.addWidget(self.progressLabel)
		self.progressLabel.setAlignment(Qt.AlignCenter)
		self.progressBar = QProgressBar()
		self.progressBar.setMaximumWidth(300)
		self.progressBar.setAlignment(Qt.AlignCenter)
		self.mainLayout.addWidget(self.progressBar)

		# The progress bar updater runs the progress bar
		self.progressUpdater = progressUpdater.ProgressUpdater(self.progressBar)

		# The recent projects are handled in a separate object
		self.recentProjects = RecentProjects(self.recentDropdown)


	def setImportListener(self, importListener):
		"""
		Provides an object that is called to update the stages at runtime

		Parameters
		----------
		importListener : ImportListener
			An object within the main module that manages communication to the stages at runtime.
		"""
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
		The functionality for the 'begin' button. Either creates of loads a project, based on the options entered.
		"""

		self.progressLabel.setText("Loading project")

		if self.loadProjectBool:
			# Load project
			self.project.loadFile(self.projectName, self.fileLocation, self.progressUpdater)

		elif self.newProjectBool:
			# New project
			self.projectName = self.nameEdit.text()
			self.recentProjects.load(self.projectName, self.fileLocation)
			self.project.newFile(self.projectName, None)

		else:
			# Dropdown selected
			self.projectName = self.recentDropdown.currentText()
			self.fileLocation = self.recentProjects.getLocation(self.recentDropdown.currentIndex() - 1)
			self.recentProjects.reorderDropdown(self.recentDropdown.currentIndex() - 1)
			try:
				self.project.loadFile(self.projectName, self.fileLocation, self.progressUpdater)
			except:
				message = "The .lalog file could not be found."
				errorBox = QMessageBox.critical(self.mainWidget, "Error", message, QMessageBox.Ok)
				return

		# The project title is delivered to the stages screen
		self.importListener.setTitle(self.projectName)

		# We transition to the stages screen
		self.parentStack.setCurrentIndex(1)

	def newButtonClick(self):
		"""
		The functionality for the 'new' button.
		The 'new project' options are displayed, and the recent projects dropdown is hidden.
		"""
		self.newProjectBool = True
		self.recentDropdown.setParent(None)
		self.titleGrid.addWidget(self.nameLabel, 1, 0)
		self.titleGrid.addWidget(self.nameEdit, 2, 0, 1, 2)
		self.titleGrid.addWidget(self.backButton, 5, 0)
		self.nextButton.setEnabled(False)
		self.nameEdit.setFocus()

	def openButtonClick(self):
		"""
		The functionality for the 'browse' button for loading a project
		It opens a file browser and loads the project if given an appropriate file.
		"""

		# A file browser is opened
		loadLocation = QFileDialog.getOpenFileName(self.mainWidget, 'Open file', '/home')

		# If Cancel was not selected...
		if loadLocation[0] != '':
			self.loadProjectBool = True

			# The file name is extracted from the end of the absolute file path
			locationSplit = loadLocation[0].split('/')
			self.projectName = locationSplit[-1]

			# We check that its extension is .sav
			if self.projectName[-6:] != ".lalog":
				message = "file must have extension '.lalog'"
				errorBox = QMessageBox.critical(self.mainWidget, "Error", message, QMessageBox.Ok)
				return

			# The file location is the absolute file path without the file name
			self.fileLocation = loadLocation[0][0:-(len(self.projectName) + 1)]

			# We drop the extension from the file name for the project title
			self.projectName = self.projectName[0:-6]

			# recentProjects handles adding or updating this project in the list of recent projects
			self.recentProjects.load(self.projectName, self.fileLocation)

			# We progress as though the 'begin' button was pressed
			self.nextButtonClick()


	def recentClicked(self):
		"""
		When the recent dropdown is clicked, the begin button should be activated only if a
		project name was selected (rather than the default "Recent projects" message.
		"""
		if self.recentDropdown.currentText() != "Recent projects":
			self.nextButton.setEnabled(True)
		else:
			self.nextButton.setEnabled(False)

	def backButtonClick(self):
		""" The functionality for the back button, when a new project entry is cancelled """
		self.newProjectBool = False
		self.nameLabel.setParent(None)
		self.nameEdit.setParent(None)
		self.backButton.setParent(None)
		self.titleGrid.addWidget(self.recentDropdown, 1, 0, 1, 2)
		self.nextButton.setEnabled(False)
		self.recentDropdown.setCurrentIndex(0)

	def nameEdited(self):
		""" Checks if the new name edit is currently a valid project name, and enabled the begin button accordingly """

		# A list of characters that can't be used in a file name (This could be added to)
		forbiddens = {'<','>', ':', '\"', '/', '\\', '|', '?', '*'}

		if self.nameEdit.text() != "":
			self.nameOK = True
			# If there is a forbidden character in the name, the next button is disabled
			for char in self.nameEdit.text():
				if char in forbiddens:
					self.nameOK = False
		else:
			self.nameOK = False

		# Only when the name and location are okay, is the begin button enabled
		self.nextButton.setEnabled(self.nameOK)

	def helpButtonClick(self):
		""" Link to online user guide """
		url = QUrl(self.userGuideDomain + "LAtoolsGUIUserGuide/index.html")
		QDesktopServices.openUrl(url)

	def reportButtonClick(self):
		""" Links to the online form for reporting an issue """
		QDesktopServices.openUrl(QUrl(self.reportIssue))

	def enterPressed(self):
		if self.nextButton.isEnabled():
			self.nextButtonClick()

class RecentProjects:
	"""
	A class used to record, update and display the list of projects that were accessed most recently
	"""
	def __init__(self, recentDropdown):
		"""
		Initialising opens the text file that lists all past projects, and saves the contents to a list of strings.

		Parameters
		----------
		recentDropdown : QComboBox
			The dropdown box that displays the recent projects
		"""

		# Opens and reads the recentProjects text file.
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			filename = os.path.join(os.path.dirname(sys.executable), 'project/recentProjects.txt')
			filename = filename.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			filename = "project/recentProjects.txt"

		# If the recentProjects.txt file isn't there we make a new one and open it
		try:
			recentFile = open(filename, "r")
		except IOError:
			file = open(filename, "w")
			file.close()
			recentFile = open(filename, "r")

		# Lists to contain the file contents
		self.fileContent = []
		self.splitContent = []

		# Splits each line into the project name and location
		for name in recentFile.read().splitlines():
			self.splitContent.append(name.split('*'))
		recentFile.close()

		# Legitimate entries in the file are recorded as recent projects
		i = 0
		for split in self.splitContent:
			if len(split) == 2:
				if split[0] != "" and split[1] != "":
					# Adds the names to the dropdown in order
					recentDropdown.addItem(split[0])
					self.fileContent.append(split[0] + "*" + split[1])
				i += 1
				# The maximum number of items added to the dropdown:
				if i > 10:
					break

	def addNew(self, name, location):
		""" Adding a new project to the recent projects list """

		# Open the file
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			filename = os.path.join(os.path.dirname(sys.executable), 'project/recentProjects.txt')
			filename = filename.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			filename = "project/recentProjects.txt"

		recentFile = open(filename, "w")

		# Write the new file at the top
		recentFile.write(name + "*" + location + "\n")

		# Write the rest of the file below the new entry
		for line in self.fileContent:
			recentFile.write(line + "\n")

		# Close the file
		recentFile.close()

	def reorderDropdown(self, index):
		""" Moves a particular past project to the top of the list """

		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			filename = os.path.join(os.path.dirname(sys.executable), 'project/recentProjects.txt')
			filename = filename.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			filename = "project/recentProjects.txt"

		recentFile = open(filename, "w")

		# The indexed project is written to the top of the list
		recentFile.write(self.fileContent[index] + "\n")

		# The rest of the projects are added
		for i in range(len(self.fileContent)):
			if i != index:
				recentFile.write(self.fileContent[i] + "\n")
		recentFile.close()

	def load(self, name, location):
		"""
		When a project is loaded, if it is in the recent projects list it is moved to the top of the list,
		otherwise it is added to the top of the list.
		"""
		for i in range(len(self.fileContent)):
			if self.fileContent[i] == name + "*" + location:
				self.reorderDropdown(i)
				return
		# If we didn't find it in the list, add it as new.
		self.addNew(name, location)

	def getLocation(self, index):
		""" Given the index of a project in the recent list, returns the file location """
		return self.fileContent[index].split('*')[1]

	def updateLocation(self, name, location):
		""" When a new project is saved it will currently have a name but no location.
			The location is added and saved in the file
		"""
		# The new file is added to the end of the list, the list is then reordered and saved
		self.fileContent.append(name + "*" + location)
		self.reorderDropdown(len(self.fileContent) - 1)
