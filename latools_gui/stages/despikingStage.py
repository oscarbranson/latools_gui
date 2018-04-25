""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import latools as la
import inspect
import templates.controlsPane as controlsPane

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
			The first step in data reduction is the ‘de-spike’ the raw data to 
			remove physically unrealistic outliers from the data (i.e. higher than 
			is physically possible based on your system setup).""")

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

		self.pane2nlim = QLineEdit(self.defaultParams['nlim'])
		self.pane2Layout.addWidget(QLabel("nlim"), 2, 0)
		self.pane2Layout.addWidget(self.pane2nlim, 2, 1)

		self.pane2Maxiter = QLineEdit(self.defaultParams['maxiter'])
		self.pane2Layout.addWidget(QLabel("maxiter"), 3, 0)
		self.pane2Layout.addWidget(self.pane2Maxiter, 3, 1)

		# We create the button for the right-most section of the Controls Pane.

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		""" Applies a despiking filter to the project data when a button is pressed. """

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

		print(list(self.project.eg.data['STD-1'].data.keys()))
		self.graphPaneObj.updateGraph()
		self.progressPaneObj.setRightEnabled()

	def raiseError(self, message):
		errorBox = QMessageBox.critical(self.despikingWidget, "Error", message, QMessageBox.Ok)