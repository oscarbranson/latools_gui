""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import latools as la
import inspect
import templates.controlsPane as controlsPane
import json
import ast


from project.ErrLogger import logged

class AutorangeStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	@logged
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

		# We import the stage information from a json file
		read_file = open("information/autorangeStageInfo.json", "r")
		self.stageInfo = json.load(read_file)
		read_file.close()

		# We set the title and description for the stage

		self.stageControls.setDescription("Autorange", self.stageInfo["stage_description"])

		# The space for the stage options is provided by the Controls Pane.

		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		self.analyteBox = QComboBox()
		self.analyteLabel = QLabel(self.stageInfo["analyte_label"])
		self.analyteBox.addItem("total_counts")
		self.optionsGrid.addWidget(self.analyteLabel, 0, 0)
		self.optionsGrid.addWidget(self.analyteBox, 0, 1)
		self.analyteBox.setToolTip(self.stageInfo["analyte_description"])
		self.analyteLabel.setToolTip(self.stageInfo["analyte_description"])

		self.gwinLabel = QLabel(self.stageInfo["gwin_label"])
		self.gwinEdit = QLineEdit(self.defaultParams['gwin'])
		self.optionsGrid.addWidget(self.gwinLabel, 1, 0)
		self.optionsGrid.addWidget(self.gwinEdit, 1, 1)
		self.gwinEdit.setToolTip(self.stageInfo["gwin_description"])
		self.gwinLabel.setToolTip(self.stageInfo["gwin_description"])

		self.swinLabel = QLabel(self.stageInfo["swin_label"])
		self.swinEdit = QLineEdit(self.defaultParams['swin'])
		self.optionsGrid.addWidget(self.swinLabel, 2, 0)
		self.optionsGrid.addWidget(self.swinEdit, 2, 1)
		self.swinEdit.setToolTip(self.stageInfo["swin_description"])
		self.swinLabel.setToolTip(self.stageInfo["swin_description"])

		self.winLabel = QLabel(self.stageInfo["win_label"])
		self.winEdit = QLineEdit(self.defaultParams['win'])
		self.optionsGrid.addWidget(self.winLabel, 3, 0)
		self.optionsGrid.addWidget(self.winEdit, 3, 1)
		self.winEdit.setToolTip(self.stageInfo["win_description"])
		self.winLabel.setToolTip(self.stageInfo["win_description"])

		self.on_multLabel = QLabel(self.stageInfo["on_mult_label"])
		self.on_multEdit1 = QLineEdit("1.0")
		self.on_multEdit2 = QLineEdit("1.5")
		self.optionsGrid.addWidget(self.on_multLabel, 0, 2)
		self.optionsGrid.addWidget(self.on_multEdit1, 0, 3)
		self.optionsGrid.addWidget(self.on_multEdit2, 0, 4)
		self.on_multEdit1.setToolTip(self.stageInfo["on_mult_description"])
		self.on_multEdit2.setToolTip(self.stageInfo["on_mult_description"])
		self.on_multLabel.setToolTip(self.stageInfo["on_mult_description"])

		self.off_multLabel = QLabel(self.stageInfo["off_mult_label"])
		self.off_multEdit1 = QLineEdit("1.5")
		self.off_multEdit2 = QLineEdit("1.0")
		self.optionsGrid.addWidget(self.off_multLabel, 1, 2)
		self.optionsGrid.addWidget(self.off_multEdit1, 1, 3)
		self.optionsGrid.addWidget(self.off_multEdit2, 1, 4)
		self.off_multEdit1.setToolTip(self.stageInfo["off_mult_description"])
		self.off_multEdit2.setToolTip(self.stageInfo["off_mult_description"])
		self.off_multLabel.setToolTip(self.stageInfo["off_mult_description"])

		# self.nbinLabel = QLabel(self.stageInfo["nbin_label"])
		# self.nbinEdit = QLineEdit(self.defaultParams.get('nbin', "10"))
		# self.optionsGrid.addWidget(self.nbinLabel, 2, 2)
		# self.optionsGrid.addWidget(self.nbinEdit, 2, 3, 1, 2)
		# self.nbinEdit.setToolTip(self.stageInfo["nbin_description"])
		# self.nbinLabel.setToolTip(self.stageInfo["nbin_description"])

		self.logTransformCheck = QCheckBox(self.stageInfo["log_transform_label"])
		self.logTransformCheck.setChecked(self.defaultParams['transform'] == 'True')
		self.optionsGrid.addWidget(self.logTransformCheck, 2, 2, 1, 2)
		self.logTransformCheck.setToolTip(self.stageInfo["log_transform_description"])

		# We create a reset to default button

		self.defaultButton = QPushButton("Defaults")
		self.defaultButton.clicked.connect(self.defaultButtonPress)
		self.stageControls.addDefaultButton(self.defaultButton)

		# We create the button for the right-most section of the Controls Pane.

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	@logged
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

		# localNbin = None
		# if self.nbinEdit.text() != "":
		# 	try:
		# 		localNbin = int(self.nbinEdit.text())
		# 	except:
		# 		self.raiseError("The 'nbin' value must be an integer")
		# 		return

		# The actual call to the analyse object for this stage is run, using the stage values as parameters
		try:
			self.project.eg.autorange(analyte=self.analyteBox.currentText(),
								gwin=localGwin,
								swin=localSwin,
								win=localWin,
								on_mult=localOn_mult,
								off_mult=localOff_mult,
								#nbin=localNbin,
								transform=self.logTransformCheck.isChecked())
		except:
			self.raiseError("A problem occurred. There may be a problem with the input values.")
			return

		self.graphPaneObj.updateGraph(showRanges=True)

		# When the stage's processing is complete, the right button is enabled for the next stage.
		self.progressPaneObj.completedStage(2)

		# Automatically saves the project if it already has a save location
		self.project.reSave()

	@logged
	def updateStageInfo(self):
		""" The analyte dropdown can only be built once data is imported at runtime """
		for analyte in self.project.eg.analytes:
			self.analyteBox.addItem(str(analyte))

	@logged
	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.autorangeWidget, "Error", message, QMessageBox.Ok)

	@logged
	def loadValues(self):
		""" Loads the values saved in the project, and fills in the stage parameters with them """

		# The stage parameters are stored in project as dictionaries
		params = self.project.getStageParams("autorange")

		# The stage parameters are applied to the input fields
		self.fillValues(params)

		# The loading process then activates the stage's apply command
		self.pressedApplyButton()

	def fillValues(self, params):
		""" Fills the stage parameters from a given dictionary """

		if params is not None:
			self.analyteBox.setCurrentText(params.get("analyte", "total_counts"))
			self.gwinEdit.setText(str(params.get("gwin", 5)))
			self.swinEdit.setText(str(params.get("swin", 3)))
			self.winEdit.setText(str(params.get("win", 20)))
			self.on_multEdit1.setText(str(params.get("on_mult", [1.0, 1.5])[0]))
			self.on_multEdit2.setText(str(params.get("on_mult", [1.0, 1.5])[1]))
			self.off_multEdit1.setText(str(params.get("off_mult", [1.5, 1.0])[0]))
			self.off_multEdit2.setText(str(params.get("off_mult", [1.5, 1.0])[1]))
			# self.nbinEdit.setText(str(params.get("nbin", 10)))
			self.logTransformCheck.setChecked(params.get("transform", False))

	@logged
	def enterPressed(self):
		""" When enter is pressed on this stage """
		if self.applyButton.isEnabled():
			self.pressedApplyButton()

	@logged
	def defaultButtonPress(self):

		params = {
			"analyte": self.defaultParams["analyte"],
			"gwin": self.defaultParams["gwin"],
			"swin": self.defaultParams["swin"],
			"win": self.defaultParams["win"],
			# "nbin": self.defaultParams.get("nbin", "10"),
			"transform": self.defaultParams['transform'] == 'True'
		}

		self.fillValues(params)