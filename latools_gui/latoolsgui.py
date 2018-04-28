""" This is the main module that builds all aspects of the latools program and runs the GUI."""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import sys 

# Import the templates
from templates import titleScreen
from templates import navigationPane
from templates import graphPane
from templates import progressPane

# Import the stage information files
from stages import importStage
from stages import despikingStage
from stages import autorangeStage
from stages import backgroundStage
from stages import ratioStage
from stages import calibrationStage
from stages import filteringStage

from project import runningProject

# List the stages
STAGES = ["Import","De-Spiking","Autorange","Background","Ratio","Calibration","Filtering"]

class MainWindow(QMainWindow):
	"""
	The main GUI window. All of the GUI functionality is built through this class.
	"""

	def __init__(self):
		""" The initialisation method creates the window and then runs the UI initialisation. """

		super().__init__()
		
		# Determines where the offset for where the window appears on the screen.
		# Moves the window x pixels to the right, and y pixels down
		self.move(200, 0)
		self.setWindowTitle("LAtools")
		
		# We move on to build the UI
		self.initUI()

	def initUI(self):
		""" Creates instances of all screens and stages of the program, and controls movement between them. """

		self.mainWidget = QWidget()
		self.setCentralWidget(self.mainWidget)

		# principalLayout is a vertical box that runs down the entire window
		self.principalLayout = QVBoxLayout(self.mainWidget)

		# The file menu is produced here
		self.initFileMenu()

		# mainStack moves between views that occupy the entire window
		self.mainStack = QStackedWidget()

		# Add the mainStack to the principalLayout
		self.principalLayout.addWidget(self.mainStack)

		# We create an instance of a Running Project to store in one place all of the analysis that will be
		# performed in this project
		self.project = runningProject.RunningProject()

		# Here we create a title screen object from the file in templates
		self.titleScreenObj = titleScreen.TitleScreen(self.mainStack, self.project)
		# And it is added to the mainstack in position 0.
		self.mainStack.addWidget(self.titleScreenObj.getPane())

		# We create a widget for the stages screen so that it can be added to the main stack.
		# This way we can move from the title screen to the stages screen.
		self.stageWidget = QWidget()
		# By making the stageWidget the "parent" of the stageScreenLayout, the widget will contain the layout:
		self.stageScreenLayout = QVBoxLayout(self.stageWidget)
		self.mainStack.addWidget(self.stageWidget)

		# We make a new stack here, that will move between the different stages.
		# Only the Controls pane will actually be changing, but the graph pane could be added here also.
		self.stagesStack = QStackedWidget()

		# We create one navigation pane object (The horizontal bar across the top)
		self.navigationPaneObj = navigationPane.NavigationPane(self.stagesStack, STAGES, self.stageScreenLayout)
		
		# Now we add the stages stack to the layout, so that it sits below the top navigation bar.
		self.stageScreenLayout.addWidget(self.stagesStack)

		# We create the progress pane object but will add it to the stages layout later
		self.progressPaneObj = progressPane.ProgressPane(self.stagesStack, STAGES, self.navigationPaneObj)

		# Here we define the graph pane, so that it could be passed to the controls pane.
		# However, we want it to sit below the controls, so it's not added to the layout yet.
		self.graphPaneObj = graphPane.GraphPane(self.project)

		# A layout for each stage is created, and added to the stage stack

		# First a widget is made, so that it can be added to the stage stack
		self.importStageWidget = QWidget()
		# Then a layout is made from the widget
		self.importStageLayout = QVBoxLayout(self.importStageWidget)
		# And added to the stage stack
		self.stagesStack.addWidget(self.importStageWidget)

		self.despikingStageWidget = QWidget()
		self.despikingStageLayout = QVBoxLayout(self.despikingStageWidget)
		self.stagesStack.addWidget(self.despikingStageWidget)

		self.autorangeStageWidget = QWidget()
		self.autorangeStageLayout = QVBoxLayout(self.autorangeStageWidget)
		self.stagesStack.addWidget(self.autorangeStageWidget)

		self.backgroundStageWidget = QWidget()
		self.backgroundStageLayout = QVBoxLayout(self.backgroundStageWidget)
		self.stagesStack.addWidget(self.backgroundStageWidget)

		self.ratioStageWidget = QWidget()
		self.ratioStageLayout = QVBoxLayout(self.ratioStageWidget)
		self.stagesStack.addWidget(self.ratioStageWidget)

		self.calibrationStageWidget = QWidget()
		self.calibrationStageLayout = QVBoxLayout(self.calibrationStageWidget)
		self.stagesStack.addWidget(self.calibrationStageWidget)

		self.filteringStageWidget = QWidget()
		self.filteringStageLayout = QVBoxLayout(self.filteringStageWidget)
		self.stagesStack.addWidget(self.filteringStageWidget)

		# The stage objects are then produced
		self.importStageObj = importStage.ImportStage(
			self.importStageLayout, self.graphPaneObj, self.progressPaneObj, self.importStageWidget, self.project)
		self.despikingStageObj = despikingStage.DespikingStage(
			self.despikingStageLayout, self.graphPaneObj, self.progressPaneObj, self.despikingStageWidget, self.project)
		self.autorangeStageObj = autorangeStage.AutorangeStage(
			self.autorangeStageLayout, self.graphPaneObj, self.progressPaneObj, self.autorangeStageWidget, self.project)
		self.backgroundStageObj = backgroundStage.BackgroundStage(
			self.backgroundStageLayout, self.graphPaneObj, self.progressPaneObj, self.backgroundStageWidget, self.project)
		self.ratioStageObj = ratioStage.RatioStage(
			self.ratioStageLayout, self.graphPaneObj, self.progressPaneObj, self.ratioStageWidget, self.project)
		self.calibrationStageObj = calibrationStage.CalibrationStage(
			self.calibrationStageLayout, self.graphPaneObj, self.progressPaneObj, self.calibrationStageWidget, self.project)
		self.filteringStageObj = filteringStage.FilteringStage(
			self.filteringStageLayout, self.graphPaneObj, self.progressPaneObj, self.filteringStageWidget, self.project)

		# Object that allows updates to stages to occur during runtime
		importListener = ImportListener(self.importStageObj,
										self.despikingStageObj,
										self.autorangeStageObj,
										self.backgroundStageObj,
										self.ratioStageObj,
										self.calibrationStageObj,
										self.filteringStageObj,
										self.navigationPaneObj,
										self.progressPaneObj,
										self.graphPaneObj)
		self.importStageObj.setImportListener(importListener)
		self.titleScreenObj.setImportListener(importListener)
		self.project.setImportListener(importListener)



		#Finally, we call methods on the progressPane and graphPane object to add them to the layout.
		self.progressPaneObj.addToLayout(self.stageScreenLayout)
		self.graphPaneObj.addToLayout(self.stageScreenLayout)

	def initFileMenu(self):
		""" Builds and displays the file menu"""

		saveFile = QAction(QIcon('save.png'), 'Save', self)
		saveFile.setShortcut('Ctrl+S')
		saveFile.setStatusTip('Save your project')
		saveFile.triggered.connect(self.saveButton)

		loadFile = QAction(QIcon('open.png'), 'Load', self)
		#loadFile.setShortcut('Ctrl+L')
		loadFile.setStatusTip('Load File')
		# loadFile.triggered.connect()

		exitAct = QAction(QIcon('exit.png'), 'Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(qApp.quit)

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(saveFile)
		fileMenu.addAction(loadFile)
		fileMenu.addAction(exitAct)

		makeConfig = QAction(QIcon('open.png'), 'Make', self)
		makeConfig.setStatusTip('Make a new configuration')
		# makeConfig.triggered.connect()

		configMenu = menubar.addMenu('&Configuration')
		configMenu.addAction(makeConfig)

	def saveButton(self):
		self.project.saveButton()

class ImportListener():
	""" Handles the passing of information between modules during runtime """

	def __init__(self,
				 importStage,
				 despikingStage,
				 autorangeStage,
				 backgroundStage,
				 ratioStage,
				 calibrationStage,
				 filteringStage,
				 navigationPane,
				 progressPane,
				 graphPane):
		self.importStage = importStage
		self.despikingStage = despikingStage
		self.autorangeStage = autorangeStage
		self.backgroundStage = backgroundStage
		self.ratioStage = ratioStage
		self.calibrationStage = calibrationStage
		self.filteringStage = filteringStage
		self.navigationPane = navigationPane
		self.progressPane = progressPane
		self.graphPane = graphPane

	def dataImported(self):
		self.autorangeStage.updateStageInfo()
		self.ratioStage.updateStageInfo()
		self.calibrationStage.updateStageInfo()

	def setTitle(self, title):
		# Sends the project name to the navigation pane to display
		# and sets the loaded stage index
		self.navigationPane.setProjectTitle(title, "")

	def setStageIndex(self, index):
		self.progressPane.setStageIndex(index)

	def loadStage(self, index):

		if index == 0:
			self.importStage.loadValues()
		elif index == 1:
			self.despikingStage.loadValues()
		elif index == 2:
			self.autorangeStage.loadValues()
		elif index == 3:
			self.backgroundStage.loadValues()
		elif index == 4:
			self.ratioStage.loadValues()
		elif index == 5:
			self.calibrationStage.loadValues()
		elif index == 6:
			self.filteringStage.loadValues()



# This is where the GUI is actually created and run.
# Autodocs executes side effects when it imports modules to be read. Therefore the GUI must be created and
# run in a conditional that only accepts the main routine.
if __name__ == '__main__':
	app = QApplication([])
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())