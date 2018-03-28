from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys 

class NavigationPane():
	"""
	The pane that runs across the top of the stages screen, containing the project title, 
	the names of the stages, and left and right buttons for movign between stages.
	"""
	def __init__(self, stagesStack, STAGES, stagesScreenLayout):

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
		self.topBarFrame = QFrame()
		stagesScreenLayout.addWidget(self.topBarFrame)
		self.topBarLayout = QHBoxLayout(self.topBarFrame)

		# We add a 'left' button for moving through the stages
		self.leftButton = QPushButton("<-")
		self.topBarLayout.addWidget(self.leftButton)
		# The click functionality is defined in a method below.
		self.leftButton.clicked.connect(self.leftButtonClick)

		# As we're on step 1 to begin with, we deactivate the left button for now
		self.leftButton.setEnabled(False)
		
		# We use a NavNameTags object to handle building, and highlighting the stage labels
		self.nameTags = NavNameTags(self.topBarLayout)

		# After our steps we add a stretch that will push our right button to the side
		self.topBarLayout.addStretch(1)

		# We add a right button
		self.rightButton = QPushButton("->")
		self.rightButton.clicked.connect(self.rightButtonClick)
		self.topBarLayout.addWidget(self.rightButton)
	
	# Defines what happens when the left button is clicked.
	def leftButtonClick(self):
		
		# The stage stack is decremented
		self.stagesStack.setCurrentIndex(self.stagesStack.currentIndex() - 1)
		
		# If we're now on the first stage, we disable the left button.
		if (self.stagesStack.currentIndex() == 0):
			self.leftButton.setEnabled(False)

		# The right button should be enabled
		self.rightButton.setEnabled(True)

		# We send the current stage index to the nameTags object to handle the highlighting.
		self.nameTags.setBold(self.stagesStack.currentIndex())

	# Just like the left button above, but for the right button.
	def rightButtonClick(self):
		self.stagesStack.setCurrentIndex(self.stagesStack.currentIndex() + 1)
		if (self.stagesStack.currentIndex() == (len(self.STAGES) - 1)):
			self.rightButton.setEnabled(False)
		self.leftButton.setEnabled(True)
		self.nameTags.setBold(self.stagesStack.currentIndex())

	# Here we use a method to build the title. The two strings are combined with some css code
	# to provide display style functionality.
	def setProjectTitle(self, title, subset):
		self.nameSubsetLabel.setText("<span style=\"color:#779999; font-size:16px;\">"
			"<b>" + title + ":</b> " + subset + "</span>")


class NavNameTags():
	"""
	A simple class that handles what stage names are displayed across the navigation bar, 
	and which one should be highlighted.
	"""
	def __init__(self, layout):

		# The horizontal layout is passed along so that we can add the labels.
		self.layout = layout
		self.stageNames = ["Import","De-Spiking","Autorange","Background","Ratio","Calibration","Filtering"]

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
		# When a stage is changed we set all the labels to not highlighted...
		for i in range(len(self.stageNames)):
			self.stageLabels[i].setText(self.stageNames[i])
		# And then highlight the current stage
		self.stageLabels[index].setText("<b><u>" + self.stageNames[index] + "</u></b>")






