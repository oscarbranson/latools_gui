""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import templates.filterControls as filterControls

class FilteringStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, filteringWidget, project):
		"""
		Initialising creates and customises a Controls Pane for this stage.

		Parameters
		----------
		stageLayout : QVBoxLayout
			The layout for the entire stage screen, that the Controls Pane will be added to.
		graphPaneObj : GraphPane
			A reference to the Graph Pane that will sit at the bottom of the stage screen and display
			updates t the graph, produced by the processing defined in the stage.
		progressPaneObj : ProgressPane
			A reference to the Progress Pane so that the right button can be enabled by completing the stage.
		project : RunningProject
			A reference to the project object which contains all of the information unique to this project,
			including the latools analyse object that the stages will update.
		"""

		self.graphPaneObj = graphPaneObj
		self.progressPaneObj = progressPaneObj
		self.filteringWidget = filteringWidget
		self.project = project

		self.stageControls = filterControls.FilterControls(stageLayout)

		# The space for the stage options is provided by the Controls Pane.

		# We define the stage options and add them to the Controls Pane

		# We create the button for the right-most section of the Controls Pane.

		#self.applyButton = QPushButton("APPLY")
		#self.applyButton.clicked.connect(self.pressedApplyButton)
		#self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		#Add apply button functionality
		self.progressPaneObj.setRightEnabled()

	def loadValues(self):
		x = 1

