""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
import latools as la
import inspect
import templates.controlsPane as controlsPane

class ImportStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	def __init__(self, stageLayout, graphPaneObj, navigationPaneObj, importStageWidget, project):
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
		self.importStageWidget = importStageWidget
		self.fileLocation = ""
		self.project = project
		self.importListener = None

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We capture the default parameters for this stage's function call
		self.defaultParams = self.stageControls.getDefaultParameters(inspect.signature(la.analyse))

		# We set the title and description for the stage

		self.stageControls.setDescription("Import Data", """
			This imports all the data files within the data/ folder into an latools.analyse 
			object called eg, along with several parameters describing the dataset and how 
			it should be imported:""")

		# The space for the stage options is provided by the Controls Pane.
		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		self.findDataButton = QPushButton("Browse")
		self.findDataButton.setMaximumWidth(100)
		self.findDataButton.clicked.connect(self.findDataButtonClicked)
		self.optionsGrid.addWidget(self.findDataButton,0,0)

		self.fileLocationLine = QLineEdit("./data/")
		self.optionsGrid.addWidget(self.fileLocationLine, 0, 1)
		self.fileLocationLine.setReadOnly(True)

		self.configOption = QComboBox()
		self.configOption.addItem("DEFAULT")
		self.configOption.addItem("REPRODUCE")
		self.configOption.addItem("UCD-AGILENT")
		self.configOption.addItem("USC-ELEMENT")
		self.optionsGrid.addWidget(QLabel("config"), 1,0)
		self.optionsGrid.addWidget(self.configOption, 1,1)

		self.srm_identifierOption = QLineEdit(self.defaultParams['srm_identifier'])
		self.optionsGrid.addWidget(QLabel("SRM identifier"), 2, 0)
		self.optionsGrid.addWidget(self.srm_identifierOption, 2, 1)

		self.file_extensionOption = QLineEdit(self.defaultParams['extension'])
		self.optionsGrid.addWidget(QLabel("file extension"), 3, 0)
		self.optionsGrid.addWidget(self.file_extensionOption, 3, 1)

		# We create the button for the right-most section of the Controls Pane.

		self.applyButton = QPushButton("APPLY")
		self.applyButton.clicked.connect(self.pressedApplyButton)
		self.stageControls.addApplyButton(self.applyButton)

	def pressedApplyButton(self):
		""" Imports data into the project when the apply button is pressed. """
		#Add apply button functionality

		try:
			self.project.eg = la.analyse(data_folder=self.fileLocationLine.text(),
										 config=self.configOption.currentText(),
										 extension=self.file_extensionOption.text(),
										 srm_identifier=self.srm_identifierOption.text())

			self.graphPaneObj.updateGraphDetails(importing=True)
			self.graphPaneObj.updateGraph(stage='rawdata')

			self.navigationPaneObj.setRightEnabled()

			if not self.importListener is None:
				self.importListener.dataImported()
		except:
			print("An error occured")

			errorBox = QMessageBox.critical(self.importStageWidget,
											"Error loading data files",
											"An error occurred while attempting to load the data files. \n" +
											"Please check that the specified data folder contains the correct data files",
											QMessageBox.Ok)

	def findDataButtonClicked(self):
		""" Opens a file dialog to find a file directory for data import when a button is pressed. """

		self.fileLocation = QFileDialog.getExistingDirectory(self.importStageWidget, 'Open file', '/home')
		self.fileLocationLine.setText(self.fileLocation)

	def setImportListener(self, importListener):
		self.importListener = importListener
