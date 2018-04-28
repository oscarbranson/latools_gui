""" Builds a pane between Controls and Graph with progression buttons and a progress bar
"""

from PyQt5.QtWidgets import *

class ProgressPane:
	"""
	The pane that sits below the Controls pane, containing progression buttons and a progress bar
	"""
	def __init__(self, stagesStack, STAGES, navPane, graphPane, project):
		"""
		Initialising builds and displays the pane.

		Parameters
		----------
		stagesStack : QStackedWidget
			The stack for the stage screens, used for switching from one stage to the next.
		STAGES : [str]
			A list of the stages to be displayed and moved between
		navPane : NavigationPane
			The Pane that runs across the top with the stage names, so that the current stage can be highlighted
		"""

		self.stagesStack = stagesStack
		self.STAGES = STAGES
		self.focusStages = ['rawdata', 'despiked', 'despiked', 'bkgsub', 'ratios', 'calibrated', 'calibrated']
		self.navPane = navPane
		self.graphPane = graphPane
		self.project = project
		self.progressWidget = QWidget()
		self.progressLayout = QHBoxLayout(self.progressWidget)

		# We add a 'left' button for moving through the stages
		self.leftButton = QPushButton("⬅")
		self.progressLayout.addWidget(self.leftButton)
		# The click functionality is defined in a method below.
		self.leftButton.clicked.connect(self.leftButtonClick)

		# The progress bar is added here. This will need to be hooked up with some functionality
		self.progressBar = QProgressBar()
		self.progressLayout.addWidget(self.progressBar)

		# We add a right button
		self.rightButton = QPushButton("➡")
		self.rightButton.clicked.connect(self.rightButtonClick)
		self.progressLayout.addWidget(self.rightButton)

		# As we won't be changing stages until the processing is complete, we disable the buttons
		self.leftButton.setEnabled(False)
		self.rightButton.setEnabled(False)

	def addToLayout(self, stageLayout):
		""" Adds the progress pane to the stage layout. It is a function so that this can occur after the Controls
		 	Pane is built.

			Parameters
			----------
			stagelayout : QVBoxLayout
				The layout for the stage screen that the graph pane will be added to the bottom of.
		"""
		stageLayout.addWidget(self.progressWidget)

	def leftButtonClick(self):
		""" Controls what happens when the left button is pressed. """

		# The stage stack is decremented
		self.stagesStack.setCurrentIndex(self.stagesStack.currentIndex() - 1)

		# Update the graph if stage was completed perviously
		if self.focusStages[self.stagesStack.currentIndex()] in self.project.eg.stages_complete:
			self.project.eg.set_focus(self.focusStages[self.stagesStack.currentIndex()])
			self.graphPane.updateGraph()

		# If we're now on the first stage, we disable the left button.
		if (self.stagesStack.currentIndex() == 0):
			self.leftButton.setEnabled(False)

		# The right button should be enabled
		self.rightButton.setEnabled(True)

		# We send the current stage index to the nameTags object to handle the highlighting.
		self.navPane.setStage(self.stagesStack.currentIndex())

	def rightButtonClick(self):
		""" Controls what happens when the right button is pressed. """
		self.stagesStack.setCurrentIndex(self.stagesStack.currentIndex() + 1)
		if self.focusStages[self.stagesStack.currentIndex()] in self.project.eg.stages_complete:
			self.project.eg.set_focus(self.focusStages[self.stagesStack.currentIndex()])
			self.graphPane.updateGraph()
		if self.focusStages[self.stagesStack.currentIndex() + 1] not in self.project.eg.stages_complete:
			self.rightButton.setEnabled(False)
		self.leftButton.setEnabled(True)
		self.navPane.setStage(self.stagesStack.currentIndex())

	def setRightEnabled(self):
		""" To prevent moving through stages without running the data processing, the right button is
			only enabled by the stages once the Apply button has been successfully pressed.
		"""
		# If we're not in the final stage, set the right button to enabled
		if (self.stagesStack.currentIndex() != (len(self.STAGES) - 1)):
			self.rightButton.setEnabled(True)

	def setStageIndex(self, index):
		self.stagesStack.setCurrentIndex(index)
		self.navPane.setStage(self.stagesStack.currentIndex())
		self.leftButton.setEnabled(True)
