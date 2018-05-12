""" Creates tabs for the processing stages and controls movement between them """

from PyQt5.QtWidgets import *

class StageTabs:
	""" The set of tabs that contain the stage information and controls """

	def __init__(self, STAGES, stagesScreenLayout):
		"""
		Creates a set of tabs for the stages, and displays them at the top of the stages screen.

		Parameters
		----------
		STAGES : [string]
			The list of stages
		stagesScreenLayout : QVBoxLayout
			The layout for the screen that the tabs section adds itself to
		"""

		# The tabs are created and displayed
		self.tabs = QTabWidget()
		stagesScreenLayout.addWidget(self.tabs)

		# The tabs are stored in a list
		self.tabsList = []
		self.upToStage = 0
		self.progressPane = None

		# tabs are created
		for i in range(len(STAGES)):
			tab = QWidget()
			self.tabs.addTab(tab, STAGES[i])
			self.tabsList.append(tab)

		# sends a signal whenever a tab changes
		self.tabs.currentChanged.connect(self.tabChanged)

	def passStageLayouts(self, stageLayouts):
		"""
		Receives the a list of layouts for each stage and adds them to their tabs

		Parameters
		----------
		stageLayouts : [QVBoxLayout]
			The list of each stage's layout
		"""
		for i in range(len(stageLayouts)):
			self.tabsList[i].layout = stageLayouts[i]
			self.tabsList[i].setLayout(self.tabsList[i].layout)
			self.tabs.setTabEnabled(i, False)

		# The tabs are disabled at the beginning, except the first tab
		self.tabs.setTabEnabled(0, True)

	def completedStage(self, i):
		"""
		Completed stages are used to inform what stage the project is currently up to.

		Parameters
		----------
		i : int
			The index of the completed stage
		"""
		if self.upToStage - 1 <= i:
			self.upToStage = i + 1

		# As despiking (stage index: 1) is optional, we automatically skip to 2.
		if self.upToStage == 1:
			self.upToStage = 2

		# All tabs up to the stage the project is up to, are enabled. The others are disabled.
		for i in range(len(self.tabsList)):
			self.tabs.setTabEnabled(i, i <= self.upToStage)

	def rightPress(self):
		""" When the right button is pressed we move to the next tab """
		self.tabs.setCurrentIndex(self.tabs.currentIndex() + 1)

	def leftPress(self):
		""" When the left button is pressed we move to the previous tab """
		self.tabs.setCurrentIndex(self.tabs.currentIndex() - 1)

	def addProgressPane(self, progressPane):
		""" We receive the Progress Pane, to communicate with the left and right buttons """
		self.progressPane = progressPane

	def tabChanged(self):
		""" Called whenever a tab is changed, either by the user or the program """

		# Don't worry about connecting when the tabs are being initialised
		if self.progressPane is not None:

			# Determines whether the right and left buttons should be enabled, based on what stage we are up to.
			if self.tabs.currentIndex() < self.upToStage:
				self.progressPane.rightButton.setEnabled(True)
			else:
				self.progressPane.rightButton.setEnabled(False)
			if self.tabs.currentIndex() == 0:
				self.progressPane.leftButton.setEnabled(False)
			else:
				self.progressPane.leftButton.setEnabled(True)

			# Informs the Progress Pane of a stage change, in order to update the graph
			self.progressPane.tabChanged(self.tabs.currentIndex())

	def setStage(self, index):
		"""
		Sets which tab is currently displayed, based on an index

		Parameters
		----------
		index : int
			The index of the stage
		"""
		self.tabs.setCurrentIndex(index)
