""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import templates.filterControls as filterControls

import logging

class FilteringStage():
	"""
	The filtering stage is set up differently to the other stages. It is all run in FilterControls
	"""
	#@logged
	def __init__(self, stageLayout, graphPaneObj, project, links):
		"""
		Initialising creates and customises a Controls Pane for this stage.

		Parameters
		----------
		stageLayout : QVBoxLayout
			The layout for the entire stage screen, that the Controls Pane will be added to.
		graphPaneObj : GraphPane
			A reference to the Graph Pane that will sit at the bottom of the stage screen and display
			updates t the graph, produced by the processing defined in the stage.
		project : RunningProject
			A reference to the project object which contains all of the information unique to this project,
			including the latools analyse object that the stages will update.
		links : (str, str, str)
			links[0] = The User guide website domain
			links[1] = The web link for reporting an issue
			links[2] = The tooltip for the report issue button
		"""

		self.stageControls = filterControls.FilterControls(stageLayout, project, graphPaneObj, links)

	def updateStageInfo(self):
		""" Updates the stage after data is imported at runtime """
		self.stageControls.updateStageInfo()

