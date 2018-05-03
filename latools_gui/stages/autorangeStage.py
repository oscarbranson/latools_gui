""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import latools as la
import inspect
import templates.controlsPane as controlsPane
import ast

class AutorangeStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""

	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, autorangeWidget, project):
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
		self.autorangeWidget = autorangeWidget
		self.project = project

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We capture the default parameters for this stage's function call
		self.defaultParams = self.stageControls.getDefaultParameters(inspect.signature(la.analyse.autorange))

		# We set the title and description for the stage

		self.stageControls.setDescription("Autorange", """
			Autorange uses your internal standard to discriminate between signal ("laser on") and background 
			("laser off") regions. 
			
			<p> To see the regions identified as signal and background, change any parameters required, and then click 
			APPLY.
			""")

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
		self.gwinEdit.setToolTip("The window used for calculating first derivative.")


		self.swinEdit = QLineEdit(self.defaultParams['swin'])
		self.optionsGrid.addWidget(QLabel("swin"), 2, 0)
		self.optionsGrid.addWidget(self.swinEdit, 2, 1)
		self.swinEdit.setToolTip("The window used for signal smoothing.")


		self.winEdit = QLineEdit(self.defaultParams['win'])
		self.optionsGrid.addWidget(QLabel("win"), 3, 0)
		self.optionsGrid.addWidget(self.winEdit, 3, 1)
		self.winEdit.setToolTip("The width (c +/- win) of the transition data subsets.")


		self.on_multEdit1 = QLineEdit("1.0")
		self.on_multEdit2 = QLineEdit("1.5")
		self.optionsGrid.addWidget(QLabel("on_mult"), 0, 2)
		self.optionsGrid.addWidget(self.on_multEdit1, 0, 3)
		self.optionsGrid.addWidget(self.on_multEdit2, 0, 4)
		self.on_multEdit1.setToolTip("need text")
		self.on_multEdit2.setToolTip("need text")


		self.off_multEdit1 = QLineEdit("1.5")
		self.off_multEdit2 = QLineEdit("1.0")
		self.optionsGrid.addWidget(QLabel("off_mult"), 1, 2)
		self.optionsGrid.addWidget(self.off_multEdit1, 1, 3)
		self.optionsGrid.addWidget(self.off_multEdit2, 1, 4)
		self.off_multEdit1.setToolTip("need text")
		self.off_multEdit2.setToolTip("need text")

		self.nbinEdit = QLineEdit(self.defaultParams['nbin'])
		self.optionsGrid.addWidget(QLabel("nbin"), 2, 2)
		self.optionsGrid.addWidget(self.nbinEdit, 2, 3, 1, 2)
		self.nbinEdit.setToolTip("Used to calculate the number of bins in the data histogram.")


		self.logTransformCheck = QCheckBox("log transform")
		self.logTransformCheck.setChecked(self.defaultParams['transform'] == 'True')
		self.optionsGrid.addWidget(self.logTransformCheck, 3, 2, 1, 2)
		self.logTransformCheck.setToolTip("need text")


		# We create the button for the right-most section of the Controls Pane.

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		"""
		The functionality for the Apply button.
		It takes the options edited in by the Controls Pane and applies them to the latools analyse object.
		"""

		# We process each text entry field by converting blank to the value None, and checking for errors
		localGwin = None
		if self.gwinEdit.text() != "":
			try:
				localGwin = int(self.gwinEdit.text())
			except:
				self.raiseError("The gwin value must be an integer")
				return

		localSwin = None
		if self.swinEdit.text() != "":
			try:
				localSwin = int(self.swinEdit.text())
			except:
				self.raiseError("The swin value must be an integer")
				return

		localWin = None
		if self.winEdit.text() != "":
			try:
				localWin = int(self.winEdit.text())
			except:
				self.raiseError("The win value must be an integer")
				return

		localOn_mult = None
		if self.on_multEdit1.text() != "" and self.on_multEdit2.text() != "":
			try:
				localOn_mult = [float(self.on_multEdit1.text()), float(self.on_multEdit2.text())]
			except:
				self.raiseError("The 'on_mult' values must be floating point numbers")
				return

		localOff_mult = None
		if self.off_multEdit1.text() != "" and self.off_multEdit2.text() != "":
			try:
				localOff_mult = [float(self.off_multEdit1.text()), float(self.off_multEdit2.text())]
			except:
				self.raiseError("The 'off_mult' values must be floating point numbers")
				return

		localNbin = None
		if self.nbinEdit.text() != "":
			try:
				localNbin = int(self.nbinEdit.text())
			except:
				self.raiseError("The 'nbin' value must be an integer")
				return

		# The actual call to the analyse object for this stage is run, using the stage values as parameters
		try:
			self.project.eg.autorange(analyte=self.analyteBox.currentText(),
								gwin=localGwin,
								swin=localSwin,
								win=localWin,
								on_mult=localOn_mult,
								off_mult=localOff_mult,
								nbin=localNbin,
								transform=self.logTransformCheck.isChecked())
		except:
			self.raiseError("A problem occurred. There may be a problem with the input values.")
			return

		print(list(self.project.eg.data['STD-1'].data.keys()))
		
		self.graphPaneObj.updateGraph(showRanges=True)

		# When the stage's processing is complete, the right button is enabled for the next stage.
		self.progressPaneObj.setRightEnabled()

		# Builds a string representation of a dictionary of the current stage values and saves this in project
		self.project.runStage(2, "{'analyte' : '" + self.analyteBox.currentText() +
							  "', 'gwin' : '" + str(localGwin) +
							  "', 'swin' : '" + str(localSwin) +
							  "', 'win' : '" + str(localWin) +
							  "', 'on_mult1' : '" + self.on_multEdit1.text() +
							  "', 'on_mult2' : '" + self.on_multEdit2.text() +
							  "', 'off_mult1' : '" + self.off_multEdit1.text() +
							  "', 'off_mult2' : '" + self.off_multEdit2.text() +
							  "', 'nbin' : '" + str(localNbin) +
							  "', 'transform' : '" + str(self.logTransformCheck.isChecked()) +
							  "'}")
		# Automatically saves the project
		self.project.saveButton()

	def updateStageInfo(self):
		""" The analyte dropdown can only be built once data is imported at runtime """
		for analyte in self.project.eg.analytes:
			self.analyteBox.addItem(str(analyte))

	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.autorangeWidget, "Error", message, QMessageBox.Ok)

	def loadValues(self):
		""" Loads the values saved in the project, and fills in the stage parameters with them """

		# The saved stage string is automatically converted to a dictionary
		# The number passed to getStageString is this stage's index
		values = ast.literal_eval(self.project.getStageString(2))

		# Any parameters saved as None should be a blank string for that field
		for key in values:
			if values[key] == "None":
				values[key] = ""

		# Each stage field is updated with the saved values
		self.analyteBox.setCurrentText(values['analyte'])
		self.gwinEdit.setText(values['gwin'])
		self.swinEdit.setText(values['swin'])
		self.winEdit.setText(values['win'])
		self.on_multEdit1.setText(values['on_mult1'])
		self.on_multEdit2.setText(values['on_mult2'])
		self.off_multEdit1.setText(values['off_mult1'])
		self.off_multEdit2.setText(values['off_mult2'])
		self.nbinEdit.setText(values['nbin'])
		self.logTransformCheck.setChecked(values['transform'] == "True")

		# The loading process then activates the stage's apply command
		self.pressedApplyButton()
