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
	def __init__(self, stageLayout, graphPaneObj, progressPaneObj, exportStageWidget, project, guideDomain):
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
		"""
		self.logger = logging.getLogger(__name__)
		self.logger.info('Initialised import stage!')

		self.graphPaneObj = graphPaneObj
		self.progressPaneObj = progressPaneObj
		self.exportStageWidget = exportStageWidget
		self.project = project
		self.guideDomain = guideDomain
		self.defaultDataFolder = ""
		self.statsExportCount = 1

		self.stageControls = controlsPane.ControlsPane(stageLayout)

		# We import the stage information from a json file and set the default data folder
		if getattr(sys, 'frozen', False):
			# If the program is running as a bundle, then get the relative directory
			infoFile = os.path.join(os.path.dirname(sys.executable), 'information/importStageInfo.json')
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
		self.optionsGrid.addWidget(self.pane1Frame, 1, 1, 1, 3)

		self.pane1Layout.addWidget(QLabel("<span style=\"color:#779999; font-weight:bold\">Full export</span>"), 0, 0)

		# A pane for the Sample statistics option
		self.pane2Frame = QFrame()
		self.pane2Frame.setFrameShape(QFrame.StyledPanel)
		self.pane2Frame.setFrameShadow(QFrame.Raised)

		self.pane2Layout = QGridLayout(self.pane2Frame)
		#self.optionsGrid.addWidget(self.pane2Frame, 1, 1, 1, 3)


		# Analytes combo
		self.analyteBoxes = []

		self.analytesWidget = QWidget()

		self.scroll = QScrollArea()
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll.setWidgetResizable(True)
		self.scroll.setMinimumWidth(70)

		self.innerWidget = QWidget()
		self.innerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		self.analyteLayout = QVBoxLayout(self.innerWidget)
		self.analyteLayout.addWidget(QLabel("Analytes:"))
		self.optionsGrid.addWidget(self.scroll, 1, 0)
		self.innerWidget.setToolTip(self.stageInfo["analyte_description"])

		self.analytesWidget.scroll = self.scroll

		self.scroll.setWidget(self.innerWidget)

		# Focus stage
		self.focusSet = set()
		self.focusSet.add("rawdata")

		# A combobox for the focus stage
		self.focusLabel = QLabel(self.stageInfo["focus_label"])
		self.focusCombo = QComboBox()
		self.pane1Layout.addWidget(self.focusLabel, 1, 0)
		self.pane1Layout.addWidget(self.focusCombo, 1, 1)

		self.focusCombo.addItem("rawdata")

		# Set the tooltips
		self.focusLabel.setToolTip(self.stageInfo["focus_description"])
		self.focusCombo.setToolTip(self.stageInfo["focus_description"])

		# To Filt label for Full export
		self.filtExport = QCheckBox(self.stageInfo["filt_label"])
		self.filtExport.setToolTip(self.stageInfo["filt_description"])
		self.pane1Layout.addWidget(self.filtExport, 2, 0, 1, 2)

		self.pane1Layout.setColumnStretch(3, 1)
		self.pane1Layout.setRowStretch(4, 1)

		self.optionsGrid.setColumnStretch(3, 1)
		self.optionsGrid.setRowStretch(1, 1)

		# Stats list area
		self.statsTypes = ["mean", "std", "se", "H15_mean", "H15_std", "H15_se"]

		# Analytes combo
		self.statsBoxes = []

		self.statsWidget = QWidget()

		self.statsScroll = QScrollArea()
		self.statsScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.statsScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.statsScroll.setWidgetResizable(True)
		self.statsScroll.setMinimumWidth(70)

		self.statsInnerWidget = QWidget()
		self.statsInnerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		self.statsLayout = QVBoxLayout(self.statsInnerWidget)
		self.statsLayout.addWidget(QLabel("Stat functions:"))
		self.pane2Layout.addWidget(self.statsScroll, 0, 0, 3, 1)
		self.statsInnerWidget.setToolTip(self.stageInfo["analyte_description"])

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

		# We add a label for the stats section
		self.pane2Layout.addWidget(QLabel("<span style=\"color:#779999; font-weight:bold\">Sample statistics</span>"), 0, 1)

		# To Filt label for Sample statistics
		self.filtStats = QCheckBox(self.stageInfo["filt_label"])
		self.filtStats.setToolTip(self.stageInfo["filt_description"])
		self.pane2Layout.addWidget(self.filtStats, 1, 1)

		self.pane2Layout.setColumnStretch(2, 1)
		self.pane2Layout.setRowStretch(3, 1)

		# We create the export button for the right-most section of the Controls Pane.
		self.exportButton = QPushButton("Export")
		self.exportButton.clicked.connect(self.pressedExportButton)
		self.stageControls.addApplyButton(self.exportButton)


	def typeChange(self):

		if self.typeCombo.currentText() == "Full export":
			self.pane2Frame.setParent(None)
			self.optionsGrid.addWidget(self.pane1Frame, 1, 1, 1, 3)
		else:
			self.pane1Frame.setParent(None)
			self.optionsGrid.addWidget(self.pane2Frame, 1, 1, 1, 3)


	def updateFocus(self):
		""" Updates the list of focus stages when an apply button is pressed """

		# We check the current focus stage, and if it's not in our list we add it.
		stage = self.project.eg.focus_stage
		if stage not in self.focusSet:
			self.focusCombo.addItem(stage)
			self.focusSet.add(stage)
			self.focusCombo.setCurrentText(stage)
			if stage == "bkgsub":
				self.typeCombo.addItem("Sample statistics")
		if stage == "rawdata" and self.typeCombo.count() == 2:
			self.typeCombo.removeItem(1)
			self.typeChange()

	def locationButtonClicked(self):
		""" Opens a file dialog to find a file directory for data export when the button is pressed. """

		self.fileLocation = QFileDialog.getExistingDirectory(self.exportStageWidget, 'Open file', '/home')
		self.fileLocationLine.setText(self.fileLocation)

	def enterPressed(self):
		""" When enter is pressed on this stage """
		pass

	def updateStageInfo(self):
		""" When the data is imported, we set the default export location to the imported data folder """

		if self.project.dataLocation[-1] == "/":
			self.defaultDataFolder = self.project.dataLocation[0:-1] + "_export/"
		else:
			self.defaultDataFolder = self.project.dataLocation + "_export/"
		self.fileLocationLine.setText(self.defaultDataFolder)

		# We create the list of analyte checkboxes
		for analyte in self.project.eg.analytes:
			self.analyteBoxes.append(QCheckBox(str(analyte)))
			self.analyteBoxes[-1].setChecked(True)
			self.analyteLayout.addWidget(self.analyteBoxes[-1])


	def pressedExportButton(self):

		analytes = []
		for a in self.analyteBoxes:
			if a.isChecked():
				analytes.append(a.text())

		if len(analytes) == 0:
			self.raiseError("You must select at least one analyte.")
			return

		if self.typeCombo.currentText() == "Full export":

			#print(analytes)

			self.project.eg.export_traces(outdir=self.fileLocationLine.text(),
										  focus_stage=self.focusCombo.currentText(),
										  analytes=analytes,
										  filt=self.filtExport.isChecked())

			infoBox = QMessageBox.information(self.exportStageWidget, "Export",
											  "The reports have been saved.",
											  QMessageBox.Ok)

		else:
			stats = []
			for s in self.statsBoxes:
				if s.isChecked():
					stats.append(s.text())

			if len(analytes) == 0:
				self.raiseError("You must select at least one stat function.")
				return

			self.project.eg.sample_stats(analytes=analytes,
										 filt=self.filtStats.isChecked(),
										 stats=stats)
			print("sample_stats created")
			df = self.project.eg.getstats(save=False)
			df.to_csv(self.fileLocationLine.text() + "/Sample_stats" + str(self.statsExportCount) + ".csv")
			self.statsExportCount += 1

			infoBox = QMessageBox.information(self.exportStageWidget, "Export",
											  "The sample statistics have been exported at " +
											  self.fileLocationLine.text() + "/Sample_stats" +
											  str(self.statsExportCount - 1) + ".csv",
											  QMessageBox.Ok)

	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.exportStageWidget, "Error", message, QMessageBox.Ok)