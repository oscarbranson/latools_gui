""" Builds a pane at the top of the stages screen that displays the stages and controls movement through them.
"""

from PyQt5.QtWidgets import *

class NavigationPane:
	"""
	The pane that runs across the top of the stages screen, containing the project title, 
	the names of the stages, and navigation buttons for moving between stages.
	"""
	def __init__(self, stagesStack, STAGES, stagesScreenLayout):
		"""
		Initialising builds and displays the pane.

		Parameters
		----------
		stagesStack : QStackedWidget
			The stack for the stage screens, used for switching from one stage to the next.
		STAGES : [str]
			A list of the stages to be displayed and moved between
		stagesScreenLayout : QVBoxLayout
			The layout for the stages screen, which the navigation pane will be added to the top of.
		"""

		# A reference to the stack containing all of the different stages is provided,
		# so that the buttons can control movement between the stages.
		self.stagesStack = stagesStack

		# We keep a list of the stages here
		self.STAGES = STAGES

		# The first thing that goes in the layout is the title. 
		# We create the label, but we rely on a method call for filling it in.
		self.nameSubsetLabel = QLabel()
		stagesScreenLayout.addWidget(self.nameSubsetLabel)

		# Here we set up a horizontal layout for our top bar
		# We use a Qframe for the padding
		self.topBarWidget = QWidget()
		stagesScreenLayout.addWidget(self.topBarWidget)
		self.topBarLayout = QHBoxLayout(self.topBarWidget)
		
		# We use a NavNameTags object to handle building, and highlighting the stage labels
		self.nameTags = NavNameTags(self.topBarLayout, STAGES)

		# After our steps we add a stretch that will push our right button to the side
		self.topBarLayout.addStretch(1)

	def setProjectTitle(self, title, subset):
		""" Populates the project title section with the title

			Parameters
			----------
			title : str
				The title of this project
			subset : str
				The name of the subset being worked on
		"""
		self.nameSubsetLabel.setText("<span style=\"color:#779999; font-size:16px;\">"
			"<b>" + title + "</b> " + subset + "</span>")

	def setStage(self, index):
		self.nameTags.setBold(index)

class NavNameTags():
	"""
	A simple class that handles what stage names are displayed across the navigation bar, 
	and which one should be highlighted currently.
	"""
	def __init__(self, layout, STAGES):
		"""
		Initialising displays the stage names across the navigation bar.

		Parameters
		----------
		layout : QHBoxLayout
			The layout that the stage names will be housed in.
		STAGES : [str]
			A list of the stages to be displayed and moved between
		"""

		self.layout = layout
		self.stageNames = STAGES

		# We start with an empty list of labels, and add them based on the strings above
		self.stageLabels = []
		
		# For each of the strings listed above...
		for i in range(len(self.stageNames)):
			# We add a label to the list with that name...
			self.stageLabels.append(QLabel(self.stageNames[i]))
			# and add the label to the layout.
			self.layout.addWidget(self.stageLabels[i])
			# If it's not the last label, we add a text-based spacer
			if (i != len(self.stageNames) - 1):
				self.layout.addWidget(QLabel("  | "))

		# Here we set the first stage to highlighted.
		self.stageLabels[0].setText("<b><u>" + self.stageNames[0] + "</u></b>")

	def setBold(self, index):
		"""
		When a stage is changed, this function updates the stage labels so that the correct one is highlighted.

		Parameters
		----------
		index : int
			The index of the stage now being shown.
		"""
		# When a stage is changed we set all the labels to not highlighted...
		for i in range(len(self.stageNames)):
			self.stageLabels[i].setText(self.stageNames[i])
		# And then highlight the current stage
		self.stageLabels[index].setText("<b><u>" + self.stageNames[index] + "</u></b>")

