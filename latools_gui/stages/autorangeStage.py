""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import latools as la
import inspect
import templates.controlsPane as controlsPane

class AutorangeStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""

	def __init__(self, stageLayout, graphPaneObj, navigationPaneObj, project):
		"""
		Initialising creates and customises a Controls Pane for this stage.

		Parameters
		----------
		stageLayout : QVBoxLayout
			The layout for the entire stage screen, that the Controls Pane will be added to.
		graphPaneObj : GraphPane
			A reference to the Graph Pane that will sit at the bottom of the stage screen and display
			updates t the graph, produced by the processing defined in the stage.
		navigationPaneObj : NavigationPane
			A reference to the Navigation Pane so that the right button can be enabled by completing the stage.
		project : RunningProject
			A reference to the project object which contains all of the information unique to this project,
			including the latools analyse object that the stages will update.
		"""
		self.graphPaneObj = graphPaneObj
		self.navigationPaneObj = navigationPaneObj
		self.project = project

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We capture the default parameters for this stage's function call
		self.defaultParams = self.stageControls.getDefaultParameters(inspect.signature(la.analyse.autorange))

		# We set the title and description for the stage

		self.stageControls.setDescription("Autorange", """
			The first step in data reduction is the ‘de-spike’ the raw data to 
			remove physically unrealistic outliers from the data (i.e. higher than 
			is physically possible based on your system setup).
			The first step in data reduction is the ‘de-spike’ the raw data to 
			remove physically unrealistic outliers from the data (i.e. higher than 
			is physically possible based on your system setup).
			The first step in data reduction is the ‘de-spike’ the raw data to 
			remove physically unrealistic outliers from the data (i.e. higher than 
			is physically possible based on your system setup).""")

		# The space for the stage options is provided by the Controls Pane.

		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		self.analyteBox = QComboBox()
		self.analyteBox.addItem("total_counts")
		self.optionsGrid.addWidget(QLabel("analyte"), 0, 0)
		self.optionsGrid.addWidget(self.analyteBox, 0, 1)

		self.gwinEdit = QLineEdit(self.defaultParams['gwin'])
		self.optionsGrid.addWidget(QLabel("gwin"), 1, 0)
		self.optionsGrid.addWidget(self.gwinEdit, 1, 1)

		self.swinEdit = QLineEdit(self.defaultParams['swin'])
		self.optionsGrid.addWidget(QLabel("swin"), 2, 0)
		self.optionsGrid.addWidget(self.swinEdit, 2, 1)

		self.winEdit = QLineEdit(self.defaultParams['win'])
		self.optionsGrid.addWidget(QLabel("win"), 3, 0)
		self.optionsGrid.addWidget(self.winEdit, 3, 1)

		self.on_multEdit1 = QLineEdit("1.0")
		self.on_multEdit2 = QLineEdit("1.5")
		self.optionsGrid.addWidget(QLabel("on_mult"), 0, 2)
		self.optionsGrid.addWidget(self.on_multEdit1, 0, 3)
		self.optionsGrid.addWidget(self.on_multEdit2, 0, 4)

		self.off_multEdit1 = QLineEdit("1.5")
		self.off_multEdit2 = QLineEdit("1.0")
		self.optionsGrid.addWidget(QLabel("off_mult"), 1, 2)
		self.optionsGrid.addWidget(self.off_multEdit1, 1, 3)
		self.optionsGrid.addWidget(self.off_multEdit2, 1, 4)

		self.nbinEdit = QLineEdit(self.defaultParams['nbin'])
		self.optionsGrid.addWidget(QLabel("nbin"), 2, 2)
		self.optionsGrid.addWidget(self.nbinEdit, 2, 3, 1, 2)

		self.logTransformCheck = QCheckBox("log transform")
		self.logTransformCheck.setChecked(self.defaultParams['transform'] == 'True')
		self.optionsGrid.addWidget(self.logTransformCheck, 3, 2, 1, 2)

		# We create the button for the right-most section of the Controls Pane.

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		"""
		The functionality for the Apply button.
		It takes the options edited in by the Controls Pane and applies them to the latools analyse object.
		"""
		self.project.eg.autorange(analyte=self.analyteBox.currentText(),
								gwin= int(self.gwinEdit.text()),
								swin= int(self.swinEdit.text()),
								win= int(self.winEdit.text()),
								on_mult=[float(self.on_multEdit1.text()), float(self.on_multEdit2.text())],
								off_mult=[float(self.off_multEdit1.text()), float(self.off_multEdit2.text())],
								nbin=int(self.nbinEdit.text()),
								transform=self.logTransformCheck.isChecked())

		self.graphPaneObj.updateGraph(None)

		# When the stage's processing is complete, the right button is enabled for the next stage.
		self.navigationPaneObj.setRightEnabled()

	def updateStageInfo(self):
		for analyte in self.project.eg.analytes:
			self.analyteBox.addItem(str(analyte))
