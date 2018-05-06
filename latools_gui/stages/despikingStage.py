""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import latools as la
import inspect
import templates.controlsPane as controlsPane
import ast

class DespikingStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, despikingWidget, project):
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
		self.despikingWidget = despikingWidget
		self.project = project

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We capture the default parameters for this stage's function call
		self.defaultParams = self.stageControls.getDefaultParameters(inspect.signature(la.analyse.despike))

		# We set the title and description for the stage

		self.stageControls.setDescription("Data De-spiking", """
			Despiking remotes all physically unrealistic outliers from your data. There are two despiking methods 
			available to use, both of which can be applied.			

			<p><b>Exponential decay despiker</b>
			<p>Removes low outliers, and replaces them with the average of the adjacent values. If you know the 
			exponetial decay constant of your laser you may specify it; otherwise, leave it blank and LAtools will fit 
			an exponential decay function to your data for you. 
			
			<p><b>Noise despiker</b>
			<p>Removes high outliers greater than a specified standard deviation from a rolling mean of your data.
			
			<p>To graph your selected despiking method/s, click APPLY.
		
			""")

		# The space for the stage options is provided by the Controls Pane.

		self.optionsGrid = QHBoxLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		self.pane1Frame = QFrame()
		self.pane1Frame.setFrameShape(QFrame.StyledPanel)
		self.pane1Frame.setFrameShadow(QFrame.Raised)

		self.pane1Layout = QGridLayout(self.pane1Frame)
		self.optionsGrid.addWidget(self.pane1Frame)

		self.pane1expdecayOption = QCheckBox("exponential decay despike")
		self.pane1expdecayOption.setChecked(self.defaultParams['expdecay_despiker'] == 'True')
		self.pane1Layout.addWidget(self.pane1expdecayOption, 0, 0, 1, 0)

		self.pane1Exponent = QLineEdit(self.defaultParams['exponent'])
		self.pane1Layout.addWidget(QLabel("exponent"), 1, 0)
		self.pane1Layout.addWidget(self.pane1Exponent, 1, 1)
		self.pane1Exponent.setToolTip("The exponent for the exponential decay filter.")

		#self.pane1Maxiter = QLineEdit(self.defaultParams('maxiter'))
		#self.pane1Layout.addWidget(QLabel("maxiter"), 2, 0)
		#self.pane1Layout.addWidget(self.pane1Maxiter, 2, 1)

		# Second pane
		self.pane2Frame = QFrame()
		self.pane2Frame.setFrameShape(QFrame.StyledPanel)
		self.pane2Frame.setFrameShadow(QFrame.Raised)

		self.pane2Layout = QGridLayout(self.pane2Frame)
		self.optionsGrid.addWidget(self.pane2Frame)

		self.pane2NoiseOption = QCheckBox("noise despike")
		self.pane2NoiseOption.setChecked(self.defaultParams['noise_despiker'] == 'True')
		self.pane2Layout.addWidget(self.pane2NoiseOption, 0, 0, 1, 0)

		self.pane2win = QLineEdit(self.defaultParams['win'])
		self.pane2Layout.addWidget(QLabel("\'win\'"), 1, 0)
		self.pane2Layout.addWidget(self.pane2win, 1, 1)
		self.pane2win.setToolTip("The rolling window over which the spike filter calculates the trace statistics.")


		self.pane2nlim = QLineEdit(self.defaultParams['nlim'])
		self.pane2Layout.addWidget(QLabel("nlim"), 2, 0)
		self.pane2Layout.addWidget(self.pane2nlim, 2, 1)
		self.pane2nlim.setToolTip("The number of standard deviations above the rolling mean that data are excluded.")


		self.pane2Maxiter = QLineEdit(self.defaultParams['maxiter'])
		self.pane2Layout.addWidget(QLabel("maxiter"), 3, 0)
		self.pane2Layout.addWidget(self.pane2Maxiter, 3, 1)
		self.pane2Maxiter.setToolTip("The maximum number of times that the fitler is applied.")


		# We create the button for the right-most section of the Controls Pane.

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		""" Applies a despiking filter to the project data when a button is pressed. """

		# We process each text entry field by converting blank to the value None, and checking for errors
		localExponent = None
		if (self.pane1Exponent.text() != ""):
			try:
				localExponent = float(self.pane1Exponent.text())
			except:
				self.raiseError("The exponent value must be a floating point number")
				return

		localWin = 3
		if (self.pane2win.text() != ""):
			try:
				localWin = float(self.pane2win.text())
			except:
				self.raiseError("The 'win' value must be a floating point number")
				return

		localNlim = 12.0
		if (self.pane2nlim.text() != ""):
			try:
				localNlim = float(self.pane2nlim.text())
			except:
				self.raiseError("The 'nlim' value must be a floating point number")
				return

		localMaxiter = 4
		if (self.pane2Maxiter.text() != ""):
			try:
				localMaxiter = int(self.pane2Maxiter.text())
			except:
				self.raiseError("The 'maxiter' value must be an integer")
				return

		# The actual call to the analyse object for this stage is run, using the stage values as parameters
		try:
			self.project.eg.despike(expdecay_despiker=self.pane1expdecayOption.isChecked(),
								exponent=localExponent,
								noise_despiker=self.pane2NoiseOption.isChecked(),
								win=localWin,
								nlim=localNlim,
								exponentplot=False,
								maxiter=localMaxiter)
		except:
			self.raiseError("A problem occurred. There may be a problem with the input values.")
			return

		# If the exponential decay despiker is applied without specifying the 'exponent' option, the automatically
		# calculated value is provided to the exponent textbox.
		if self.pane1expdecayOption.isChecked():
			self.pane1Exponent.setText(str(self.project.eg.expdecay_coef[0]))

		self.graphPaneObj.updateGraph()
		self.progressPaneObj.setRightEnabled()

		# Automatically saves the project if it already has a save location
		self.project.reSave()

	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.despikingWidget, "Error", message, QMessageBox.Ok)

	def loadValues(self):
		""" Loads the values saved in the project, and fills in the stage parameters with them """

		# The stage parameters are stored in project as dictionaries
		params = self.project.getStageParams("despike")

		# The stage parameters are applied to the input fields
		if params is not None:
			self.pane1expdecayOption.setChecked(params.get("expdecay_despiker", False))
			self.pane1Exponent.setText(params.get("exponent", ""))
			self.pane2NoiseOption.setChecked(params.get("noise_despiker", True))
			self.pane2win.setText(str(params.get("win", "")))
			self.pane2nlim.setText(str(params.get("nlim", "")))
			# exponentplot value?
			self.pane2Maxiter.setText(str(params.get("maxiter", 4)))

		# The loading process then activates the stage's apply command
		self.pressedApplyButton()
