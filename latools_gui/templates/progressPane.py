""" Builds a pane between Controls and Graph with progression buttons and a progress bar
"""

from PyQt5.QtWidgets import *
from templates import progressUpdater

class ProgressPane:
	"""
	The pane that sits below the Controls pane, containing progression buttons and a progress bar
	"""
	def __init__(self, STAGES, graphPane, project, stageTabs):
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

		self.STAGES = STAGES
		self.focusStages = {'rawdata':('rawdata',), 'despiked':('despiked',), 'autorange':('despiked', 'rawdata'),
							'bkgsub':('bkgsub',), 'ratios':('ratios',), 'calibrated':('calibrated',), 'filtering':('calibrated',)}
		self.graphPane = graphPane
		self.project = project
		self.progressWidget = QWidget()
		self.progressLayout = QHBoxLayout(self.progressWidget)
		self.stageTabs = stageTabs

		self.stageTabs.addProgressPane(self)

		# We add a 'left' button for moving through the stages
		self.leftButton = QPushButton("←")
		self.progressLayout.addWidget(self.leftButton)
		# The click functionality is defined in a method below.
		self.leftButton.clicked.connect(self.leftButtonClick)

		# The progress bar is added here
		# TO DO: progress bar functionality
		self.progressBar = QProgressBar()
		self.progressLayout.addWidget(self.progressBar)

		# The object that updates the progress bar
		self.progressUpdater = progressUpdater.ProgressUpdater(self.progressBar)

		# We add a right button
		self.rightButton = QPushButton("→")
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

		self.stageTabs.leftPress()

	def rightButtonClick(self):
		""" Controls what happens when the right button is pressed. """

		self.stageTabs.rightPress()

	def setRightEnabled(self):
		""" To prevent moving through stages without running the data processing, the right button is
			only enabled by the stages once the Apply button has been successfully pressed.
		"""
		# If we're not in the final stage, set the right button to enabled
		self.rightButton.setEnabled(True)

	def completedStage(self, index):
		"""
		Alerts that a stage is completed, so that the tab and button can be enabled

		Parameters
		----------
		index : int
			The index of the completed stage
		"""
		self.setRightEnabled()
		self.stageTabs.completedStage(index)

	def tabChanged(self, index):
		"""
		Alerts that a stage is completed, so that the tab and button can be enabled

		Parameters
		----------
		index : int
			The index of the completed stage
		"""
		currentStage = list(self.focusStages.keys())[index]
		if currentStage in ['autorange', 'bkgsub']:
			ranges = True
		else:
			ranges = False
		#print(currentStage)
		# If the new stage has already been applied, the graph is updated
		if currentStage in self.project.eg.stages_complete or currentStage == 'filtering':
			stageIndex = 0
			if self.focusStages[currentStage][stageIndex] not in self.project.eg.stages_complete:
				stageIndex += 1
			self.project.eg.set_focus(self.focusStages[currentStage][stageIndex])
		self.graphPane.updateGraph(showRanges=ranges)

		# Resets the progress bar
		self.progressUpdater.reset()
