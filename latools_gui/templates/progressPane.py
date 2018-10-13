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
		STAGES : [str]
			A list of the stages to be displayed and moved between
		graphPaneObj : GraphPane
			A reference to the Graph Pane that will sit at the bottom of the stage screen and display
			updates t the graph, produced by the processing defined in the stage.
		project : RunningProject
			A reference to the project object which contains all of the information unique to this project,
			including the latools analyse object that the stages will update.
		stageTabs : StageTabs
			The object that displays and controls movement between the tabs that comprise each stage of analysis
		"""

		self.STAGES = STAGES
		self.focusStages = {'rawdata':('rawdata',), 'despiked':('despiked',), 'autorange':('despiked', 'rawdata'),
							'bkgsub':('bkgsub',), 'ratios':('ratios',), 'calibrated':('calibrated',),
							'filtering':('calibrated',), 'export':('export')}
		self.graphPane = graphPane
		self.project = project
		self.progressWidget = QWidget()
		self.progressLayout = QHBoxLayout(self.progressWidget)
		self.stageTabs = stageTabs
		self.filter_stage_available = False

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
		self.project.progressBar = self.progressBar

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
		"""
		Adds the progress pane to the stage layout. It is a function so that this can occur after the Controls
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

		# Importing new data after running analysis causes problems.
		# This prevents the user from re-importing data within this run of the software
		if index == 2:
			self.project.importListener.blockReImport()

		# We need to update the export stage with the completed focus stage
		stage = ""
		if index == 5:
			stage = "filtered"
		self.project.importListener.updateExport(stage)


	def tabChanged(self, index):
		"""
		Alerts that a stage is completed, so that the tab and button can be enabled

		Parameters
		----------
		index : int
			The index of the completed stage
		"""

		# If we're on the export tab
		if index == len(self.STAGES) - 1:
			self.progressUpdater.reset()
			self.rightButton.setEnabled(False)
			self.leftButton.setEnabled(False)
			if self.filter_stage_available:
				self.leftButton.setEnabled(True)
			return

		# If we're on the Background stage, we add a tooltip to the right button to explain what
		# The user needs to do to move forward
		if index == 3:
			self.rightButton.setToolTip(
				"<qt/>To continue on you must first Calculate background, then Subtract background.")
		elif index == 5:
			self.rightButton.setToolTip(
				"<qt/>To continue on you must apply the calibration.")
		else:
			self.rightButton.setToolTip("")

		currentStage = list(self.focusStages.keys())[index]

		if currentStage in ['autorange', 'bkgsub']:
			ranges = True
		else:
			ranges = False

		# If the new stage has already been applied, the graph is updated
		if currentStage in self.project.eg.stages_complete or currentStage == 'filtering':
			stageIndex = 0
			if self.focusStages[currentStage][stageIndex] not in self.project.eg.stages_complete:
				stageIndex += 1
			self.project.eg.set_focus(self.focusStages[currentStage][stageIndex])
		
		self.graphPane.updateGraph(showRanges=ranges)

		if currentStage == "filtering":
			self.rightButton.setEnabled(True)
			self.leftButton.setEnabled(True)
			self.filter_stage_available = True
			self.graphPane.graph.filtering = True
			self.graphPane.graph.applyFilters()
		else:
			self.graphPane.graph.filtering = False

		# Resets the progress bar
		self.progressUpdater.reset()

