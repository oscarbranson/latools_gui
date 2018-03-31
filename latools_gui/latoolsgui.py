""" This is the docstring for the latoolsgui.py module. It is pulled by autodoc
to describe this module in the sphinx documentation.

Every module should have a docstring at the very top of the file.  The
module's docstring may extend over multiple lines.  If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceded by a blank line.

"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

# Import the templates
import templates.titleScreen as titleScreen
import templates.navigationPane as navigationPane
import templates.controlsPane as controlsPane
import templates.graphPane as graphPane

# Import the stage information files
import stages.importStage as importStage
import stages.despikingStage as despikingStage
import stages.autorangeStage as autorangeStage
import stages.backgroundStage as backgroundStage
import stages.ratioStage as ratioStage
import stages.calibrationStage as calibrationStage
import stages.filteringStage as filteringStage

import project.runningProject as runningProject

# List the stages
STAGES = ["import","despiking","autorange","background","ratio","calibration","filtering"]

class MainWindow(QWidget):
	"""
	A description of the class. The main GUI window. All of the GUI functionality is built through this class.

	Parameters
	----------
	param1 : type
		Description of parameter

	Attributes
	----------
	attribute1 : type
		Description of class attribute

	"""

	def __init__(self):
		""" Summary line.

		Extended description of function.

		Parameters
		----------
		arg1 : int
			Description of arg1
		arg2 : str
			Description of arg2

		Returns
		-------
		bool
			Description of return value

		"""

		super().__init__()
		
		# Determines where the offset for where the window appears on the screen.
		# Moves the window 200px to the right, and 50px down
		self.move(200, 50)
		self.setWindowTitle("LAtools")
		
		# We move on to build the UI
		self.initUI()

	def initUI(self):
		""" Summary line.

		Extended description of function.

		Parameters
		----------
		arg1 : int
			Description of arg1
		arg2 : str
			Description of arg2

		Returns
		-------
		bool
			Description of return value

		"""

		# principalLayout is a vertical box that runs down the entire window
		self.principalLayout = QVBoxLayout(self)

		# mainStack moves between views that occupy the entire window
		self.mainStack = QStackedWidget()

		# Add the mainStack to the principalLayout
		self.principalLayout.addWidget(self.mainStack)

		# Here we create a title screen object from the file in templates
		self.titleScreenObj = titleScreen.TitleScreen(self.mainStack)
		# And it is added to the mainstack in position 0.
		self.mainStack.addWidget(self.titleScreenObj.getPane())

		# We create a widget for the stages screen so that it can be added to the main stack.
		# This way we can move from the title screen to the stages screen.
		self.stageWidget = QWidget()
		# By making the stageWidget the "parent" of the stageScreenLayout, the widget will contain the layout:
		self.stageScreenLayout = QVBoxLayout(self.stageWidget)
		self.mainStack.addWidget(self.stageWidget)

		# We create an instance of a Running Project to store in one place all of the analysis that will be
		# performed in this project
		self.project = runningProject.RunningProject()

		# We make a new stack here, that will move between the different stages.
		# Only the Controls pane will actually be changing, but the graph pane could be added here also.
		self.stagesStack = QStackedWidget()

		# We create one navigation pane object (The horizontal bar across the top)
		self.navigationPaneObj = navigationPane.NavigationPane(self.stagesStack, STAGES, self.stageScreenLayout)

		# And we send it the project name to display. Currently this is hardwired for the demonstration project
		self.navigationPaneObj.setProjectTitle("Demonstration Project", "Demonstration subset")
		
		# Now we add the stages stack to the layout, so that it sits below the top navigation bar.
		self.stageScreenLayout.addWidget(self.stagesStack)

		# Here we define the graph pane, so that it could be passed to the controls pane.
		# However, we want it to sit below the controls, so it's not added to the layout yet.
		self.graphPaneObj = graphPane.GraphPane(self.project)

		# A function is used for building the different stage layouts, and adding them to the stage stack,
		# just to keep this section brief.
		self.establishStages()

		# The stage objects are then produced
		self.importStageObj = importStage.ImportStage(
			self.importStageLayout, self.graphPaneObj, self.navigationPaneObj, self.importStageWidget, self.project)
		self.despikingStageObj = despikingStage.DespikingStage(
			self.despikingStageLayout, self.graphPaneObj, self.navigationPaneObj, self.project)
		self.autorangeStageObj = autorangeStage.AutorangeStage(
			self.autorangeStageLayout, self.graphPaneObj, self.navigationPaneObj, self.project)
		self.backgroundStageObj = backgroundStage.BackgroundStage(
			self.backgroundStageLayout, self.graphPaneObj, self.navigationPaneObj, self.project)
		self.ratioStageObj = ratioStage.RatioStage(
			self.ratioStageLayout, self.graphPaneObj, self.navigationPaneObj, self.project)
		self.calibrationStageObj = calibrationStage.CalibrationStage(
			self.calibrationStageLayout, self.graphPaneObj, self.navigationPaneObj, self.project)
		self.filteringStageObj = filteringStage.FilteringStage(
			self.filteringStageLayout, self.graphPaneObj, self.navigationPaneObj, self.project)

		# The progress bar is added here. This will need to be hooked up with some functionality
		self.progressBar = QProgressBar()
		self.stageScreenLayout.addWidget(self.progressBar)

		#Finally, we call a method on the graphPane object to add it to the layout last.
		self.graphPaneObj.addToLayout(self.stageScreenLayout)

	# This function is simply a section of the initialisation where a layout for each
	# stage is created, and added to the stage stack
	def establishStages(self):
		""" Summary line.

		Extended description of function.

		Parameters
		----------
		arg1 : int
			Description of arg1
		arg2 : str
			Description of arg2

		Returns
		-------
		bool
			Description of return value

		"""

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

# This is where the GUI is actually created and run.
# Autodocs executes side effects when it imports modules to be read. Therefore the GUI must be created and
# run in a conditional that only accepts the main routine.
if __name__ == '__main__':
	app = QApplication([])
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())