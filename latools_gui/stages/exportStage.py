""" A stage of the program that defines and executes one step of the data-processing """

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt
import latools as la
import logging
import templates.controlsPane as controlsPane
import os
import sys
import json

class ExportStage():
	"""
	Each stage has its own Controls Pane, where it defines a description and the unique options for that
	step of the data-processing. It updates the graph pane based on the modifications that are made to the
	project.
	"""
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, exportStageWidget, project, links, mainWindow):
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
		exportStageWidget : QWidget
			A reference to this stage's widget in order to manage popup windows
		project : RunningProject
			A reference to the project object which contains all of the information unique to this project,
			including the latools analyse object that the stages will update.
		links : (str, str, str)
			links[0] = The User guide website domain
			links[1] = The web link for reporting an issue
			links[2] = The tooltip for the report issue button
		"""
		self.logger = logging.getLogger(__name__)
		self.logger.info('Initialised import stage!')

		self.graphPaneObj = graphPaneObj
		self.progressPaneObj = progressPaneObj
		self.exportStageWidget = exportStageWidget
		self.project = project
		self.guideDomain = links[0]
		self.reportIssue = links[1]

		# Updated on import with the default location to export data to
		self.defaultDataFolder = ""
		self.statsExportCount = 1

		# Updated with each completed focus stage
		self.focus_stages = []
		self.focusSet = set()

		self.mainWindow = mainWindow

		# We create a controls pane object which covers the general aspects of the stage's controls pane
		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We import the stage information from a json file and set the default data folder
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), 'information/exportStageInfo.json')
			infoFile = infoFile.replace('\\', '/')

			#self.defaultDataFolder = os.path.join(os.path.dirname(sys.executable), "./data/")
			#self.defaultDataFolder = self.defaultDataFolder.replace('\\', '/')
		else:
			# Otherwise the program is running in a normal python environment
			infoFile = "information/exportStageInfo.json"
			#self.defaultDataFolder = "./data/"

		with open(infoFile, "r") as read_file:
			self.stageInfo = json.load(read_file)
			read_file.close()

		self.stageControls.setDescription("Export Reports", self.stageInfo["stage_description"])

		# The space for the stage options is provided by the Controls Pane.
		self.optionsGrid = QGridLayout(self.stageControls.getOptionsWidget())

		# We define the stage options and add them to the Controls Pane

		# A combobox for the type of export
		#self.typeLabel = QLabel(self.stageInfo["type_label"])
		self.typeCombo = QComboBox()
		#self.optionsGrid.addWidget(self.typeLabel, 0, 0)
		self.optionsGrid.addWidget(self.typeCombo, 0, 0, 1, 2)

		# We add the full export type option. The other will be added after the background removal stage.
		self.typeCombo.addItem("Full export")

		# Set the tooltips
		#self.typeLabel.setToolTip(self.stageInfo["type_description"])
		self.typeCombo.setToolTip(self.stageInfo["type_description"])

		# Connect a function for the type combobox
		self.typeCombo.activated.connect(self.typeChange)

		# A button to find the export folder's filepath
		self.locationButton = QPushButton(self.stageInfo["location_label"])
		self.locationButton.setMaximumWidth(100)
		self.locationButton.clicked.connect(self.locationButtonClicked)
		self.optionsGrid.addWidget(self.locationButton, 0, 2)
		self.locationButton.setToolTip(self.stageInfo["location_description"])

		# A line to display the currently selected folder path
		self.fileLocationLine = QLineEdit(self.defaultDataFolder)
		self.optionsGrid.addWidget(self.fileLocationLine, 0, 3)
		self.fileLocationLine.setReadOnly(True)
		self.fileLocationLine.setToolTip(self.stageInfo["location_description"])

		# A pane for the export_traces option
		self.pane1Frame = QFrame()
		self.pane1Frame.setFrameShape(QFrame.StyledPanel)
		self.pane1Frame.setFrameShadow(QFrame.Raised)

		self.pane1Layout = QGridLayout(self.pane1Frame)
		self.optionsGrid.addWidget(self.pane1Frame, 1, 1, 2, 3)

		self.analysisLabel = QLabel("<span style=\"color:#779999; font-weight:bold\">" +
									self.stageInfo["focus_label"] + "</span>")
		self.pane1Layout.addWidget(self.analysisLabel, 0, 0)
		self.analysisLabel.setToolTip(self.stageInfo["focus_description"])

		self.updateFocus("rawdata")

		# A pane for the Sample statistics option
		self.pane2Frame = QFrame()
		self.pane2Frame.setFrameShape(QFrame.StyledPanel)
		self.pane2Frame.setFrameShadow(QFrame.Raised)

		self.pane2Layout = QGridLayout(self.pane2Frame)
		#self.optionsGrid.addWidget(self.pane2Frame, 1, 1, 2, 3)


		# Analytes combo

		self.analyteBoxes = []
		self.analytesWidget = QWidget()

		self.analytesLabel = QLabel("<span style=\"color:#779999; font-weight:bold\">Analytes</span>")
		self.optionsGrid.addWidget(self.analytesLabel, 1, 0)

		self.scroll = QScrollArea()
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll.setWidgetResizable(True)
		self.scroll.setMinimumWidth(70)

		self.innerWidget = QWidget()
		self.innerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		self.analyteLayout = QVBoxLayout(self.innerWidget)
		self.optionsGrid.addWidget(self.scroll, 2, 0)
		self.innerWidget.setToolTip(self.stageInfo["analyte_description"])

		self.analytesWidget.scroll = self.scroll

		self.scroll.setWidget(self.innerWidget)

		# Focus stage

		#self.focusSet.add("rawdata")

		# A combobox for the focus stage
		#self.focusLabel = QLabel(self.stageInfo["focus_label"])
		#self.focusCombo = QComboBox()
		#self.pane1Layout.addWidget(self.focusLabel, 1, 0)
		#self.pane1Layout.addWidget(self.focusCombo, 1, 1)

		#self.focusCombo.addItem("rawdata")

		# Set the tooltips
		#self.focusLabel.setToolTip(self.stageInfo["focus_description"])
		#self.focusCombo.setToolTip(self.stageInfo["focus_description"])

		# To Filt label for Full export
		#self.filtExport = QCheckBox(self.stageInfo["filt_label"])
		#self.filtExport.setToolTip(self.stageInfo["filt_description"])
		#self.pane1Layout.addWidget(self.filtExport, 2, 0, 1, 2)

		self.pane1Layout.setColumnStretch(2, 1)

		self.optionsGrid.setColumnStretch(3, 1)
		self.optionsGrid.setRowStretch(2, 1)

		# Stats list area
		self.statsTypes = ["mean", "std", "se", "H15_mean", "H15_std", "H15_se"]

		# Stats Pane
		self.statsBoxes = []
		self.statsWidget = QWidget()

		self.statsLabel = QLabel("<span style=\"color:#779999; font-weight:bold\">" +
									self.stageInfo["stats_label"] + "</span>")
		self.pane2Layout.addWidget(self.statsLabel, 0, 0)
		self.statsLabel.setToolTip(self.stageInfo["stats_description"])

		self.statsScroll = QScrollArea()
		self.statsScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.statsScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.statsScroll.setWidgetResizable(True)
		self.statsScroll.setMinimumWidth(70)

		self.statsInnerWidget = QWidget()
		self.statsInnerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		self.statsLayout = QVBoxLayout(self.statsInnerWidget)
		self.pane2Layout.addWidget(self.statsScroll, 1, 0, 2, 1)

		self.statsWidget.scroll = self.statsScroll

		self.statsScroll.setWidget(self.statsInnerWidget)

		# Set the tooltips
		self.statsInnerWidget.setToolTip(self.stageInfo["stats_description"])

		# Create the stats checkboxes
		for s in self.statsTypes:
			self.statsBoxes.append(QCheckBox(s))
			self.statsLayout.addWidget(self.statsBoxes[-1])
		# We turn on the stats functions that are used in the default call
		self.statsBoxes[0].setChecked(True)
		self.statsBoxes[1].setChecked(True)

		# To Filt label for Sample statistics
		self.filtStats = QCheckBox(self.stageInfo["filt_label"])
		self.filtStats.setToolTip(self.stageInfo["filt_description"])
		self.pane2Layout.addWidget(self.filtStats, 1, 1)

		self.pane2Layout.setColumnStretch(3, 1)
		self.pane2Layout.setRowStretch(3, 1)

		# We create a button to export the error logs to a zip folder in the LAtools directory
		self.exportLogsButton = QPushButton("Export error logs")
		self.exportLogsButton.clicked.connect(self.mainWindow.zipLogs)
		self.exportLogsButton.setToolTip("<qt/>Saves your error log files to \"Logs.zip\" in the LAtools directory. <br>" +
										 "You can also do this at any time via the File menu.")
		self.stageControls.addDefaultButton(self.exportLogsButton)

		# We create a button to link to the form for reporting an issue
		self.reportButton = QPushButton("Report an issue")
		self.reportButton.clicked.connect(self.reportButtonClick)
		self.stageControls.addDefaultButton(self.reportButton)
		self.reportButton.setToolTip(links[2])

		# We create the export button for the right-most section of the Controls Pane.
		self.exportButton = QPushButton("Export")
		self.exportButton.clicked.connect(self.pressedExportButton)
		self.stageControls.addApplyButton(self.exportButton)

	def typeChange(self):
		""" When the type of export is changed we hide or show the different option panes """

		if self.typeCombo.currentText() == "Full export":
			self.pane2Frame.setParent(None)
			self.optionsGrid.addWidget(self.pane1Frame, 1, 1, 2, 3)
		else:
			self.pane1Frame.setParent(None)
			self.optionsGrid.addWidget(self.pane2Frame, 1, 1, 2, 3)

	def updateFocus(self, stage=""):
		""" Updates the list of focus stages when an apply button is pressed """

		# We check the current focus stage, and if it's not in our list we add it.
		if stage == "":
			stage = self.project.eg.focus_stage

		if stage not in self.focusSet:

			# If we have not encountered the current focus stage yet, we create a new checkbox for it
			new = QCheckBox(stage)

			# There is a different tooltip for the 'filtered' checkbox
			if stage == "filtered":
				new.setToolTip(self.stageInfo["focus_filtered"])
			else:
				new.setToolTip(self.stageInfo["focus_description"])

			# We add our new focus stage checkbox to the list, and to the scrollable display area
			self.focus_stages.append(new)
			self.pane1Layout.addWidget(new, len(self.focus_stages), 0)
			self.focusSet.add(stage)

			# We want to stretch the space below the last focus stage checkbox
			self.pane1Layout.setRowStretch(len(self.focus_stages), 0)
			self.pane1Layout.setRowStretch(len(self.focus_stages) + 1, 1)

			# If we are up tot he background subtraction focus stage, then the default export option becomes
			# Sample statistics
			if stage == "bkgsub":
				self.typeCombo.addItem("Sample statistics")
				self.typeCombo.setCurrentText("Sample statistics")
				self.typeChange()

		# If someone reimports data we need to remove the Sample Statistics option
		if stage == "rawdata" and self.typeCombo.count() == 2:
			self.typeCombo.removeItem(1)
			self.typeChange()

	def locationButtonClicked(self):
		""" Opens a file dialog to find a file directory for data export when the button is pressed. """

		self.fileLocation = QFileDialog.getExistingDirectory(self.exportStageWidget, 'Open file', '/home')
		if self.fileLocation != "":
			self.fileLocationLine.setText(self.fileLocation)

	def enterPressed(self):
		""" When enter is pressed on this stage """
		if self.exportButton.isEnabled():
			self.pressedExportButton()

	def updateStageInfo(self):
		""" When the data is imported, we set the default export location to the imported data folder """

		if self.project.dataLocation[-1] == "/" or self.project.dataLocation[-1] == "\\":
			self.defaultDataFolder = self.project.dataLocation[0:-1] + "_export"
		else:
			self.defaultDataFolder = self.project.dataLocation + "_export"
		self.fileLocationLine.setText(self.defaultDataFolder)

		# If we have already imported we need to remove the existing analytes
		for i in range(len(self.analyteBoxes)):
			self.analyteBoxes[i].setParent(None)
		self.analyteBoxes.clear()

		# We create the list of analyte checkboxes
		for analyte in self.project.eg.analytes:
			self.analyteBoxes.append(QCheckBox(str(analyte)))
			self.analyteBoxes[-1].setChecked(True)
			self.analyteLayout.addWidget(self.analyteBoxes[-1])


	def pressedExportButton(self):
		""" When the export button is pressed we run an export command based on the option values. """

		# We create a list of the checked analytes. There must be at least one checked.
		analytes = []
		for a in self.analyteBoxes:
			if a.isChecked():
				analytes.append(a.text())
		if len(analytes) == 0:
			self.raiseError("You must select at least one analyte.")
			return

		# If the type is full export, we run the corresponding export function
		if self.typeCombo.currentText() == "Full export":

			# The user must select at least one focus stage. They are added to a list.
			stages = []
			filtered = False
			for s in self.focus_stages:
				if s.isChecked():
					if s.text() == "filtered":
						filtered = True
					else:
						stages.append(s.text())

			if len(stages) == 0:
				self.raiseError("You must select at least one analysis stage to include.")
				return

			# We run a separate export call for each focus stage selected.
			for stage in stages:
				self.project.eg.export_traces(outdir=self.fileLocationLine.text(),
											  focus_stage=stage,
											  analytes=analytes,
											  filt=filtered)

			infoBox = QMessageBox.information(self.exportStageWidget, "Export",
											  "The data has been exported.",
											  QMessageBox.Ok)

		else:
			# Otherwise run the Sample Statistics export

			# We create a list of stat functions to include
			stats = []
			for s in self.statsBoxes:
				if s.isChecked():
					stats.append(s.text())
			# At least one stat function must be selected
			if len(analytes) == 0:
				self.raiseError("You must select at least one stat function.")
				return

			# We run the sample statistics export function
			self.project.eg.sample_stats(analytes=analytes,
										 filt=self.filtStats.isChecked(),
										 stats=stats)

			# We create a data frame from of the sample statistics data
			df = self.project.eg.getstats(save=False)
			# We save the data frame to csv in the specified location
			df.to_csv(os.path.join(self.fileLocationLine.text(), "Sample_stats" + str(self.statsExportCount) + ".csv"))
			self.statsExportCount += 1

			infoBox = QMessageBox.information(self.exportStageWidget, "Export",
											  "The sample statistics have been exported.",
											  QMessageBox.Ok)

	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.exportStageWidget, "Error", message, QMessageBox.Ok)

	def reportButtonClick(self):
		""" Links to the online form for reporting an issue """
		self.stageControls.reportIssue(self.reportIssue)
