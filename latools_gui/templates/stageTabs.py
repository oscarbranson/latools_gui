
from PyQt5.QtWidgets import *

class StageTabs:
	""" The set of tabs that contain the stage information and controls """

	def __init__(self, STAGES, stagesScreenLayout):

		self.tabs = QTabWidget()
		stagesScreenLayout.addWidget(self.tabs)

		self.tabsList = []
		self.upToStage = 0
		self.progressPane = None

		for i in range(len(STAGES)):

			tab = QWidget()
			self.tabs.addTab(tab, STAGES[i])
			self.tabsList.append(tab)

		self.tabs.currentChanged.connect(self.tabChanged)

	def passStageLayouts(self, stageLayouts):

		for i in range(len(stageLayouts)):
			self.tabsList[i].layout = stageLayouts[i]
			self.tabsList[i].setLayout(self.tabsList[i].layout)
			self.tabs.setTabEnabled(i, False)
		self.tabs.setTabEnabled(0, True)


	def completedStage(self, i):

		if self.upToStage - 1 <= i:
			self.upToStage = i + 1

		for i in range(len(self.tabsList)):
			self.tabs.setTabEnabled(i, i <= self.upToStage)

	def loadUpToStage(self):
		self.tabs.setCurrentIndex(self.upToStage)

	def rightPress(self):
		self.tabs.setCurrentIndex(self.tabs.currentIndex() + 1)

	def leftPress(self):
		self.tabs.setCurrentIndex(self.tabs.currentIndex() - 1)

	def addProgressPane(self, progressPane):
		self.progressPane = progressPane

	def tabChanged(self):

		if self.progressPane is not None:

			if self.tabs.currentIndex() < self.upToStage:
				self.progressPane.rightButton.setEnabled(True)
			else:
				self.progressPane.rightButton.setEnabled(False)
			if self.tabs.currentIndex() == 0:
				self.progressPane.leftButton.setEnabled(False)
			else:
				self.progressPane.leftButton.setEnabled(True)

			self.progressPane.tabChanged(self.tabs.currentIndex())

	def setStage(self, index):
		self.tabs.setCurrentIndex(index)
