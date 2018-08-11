""" A filter for defining a threshold """

from PyQt5.QtWidgets import *


class ClusteringFilter:
	"""
	Clustering Filter info
	"""
	def __init__(self, filterTab):

		# This filter has access to the general filter structure
		self.filterTab = filterTab

		# The layout that this filter will put its option controls in
		self.optionsLayout = QGridLayout(self.filterTab.optionsWidget)

		# The complete set of checkboxes that can turn on or off analytes
		self.analyteCheckBoxes = {
			"controls": [],
			"summary": [],
		}

		# Determines is this filter will have "above" and "below" rows
		self.twoRows = False

		# Registers which rows this filter occupies in Summary
		self.summaryRow = 0

		self.filtName = ""

		# Determines if the filter has been created yet
		self.created = False

		# Prevents updating based on the program activating check boxes
		self.updating = False

		# We create each checkbox that will appear in the filter controls and summary tabs
		for i in range(len(self.filterTab.project.eg.analytes)):

			self.analyteCheckBoxes["controls"].append(QCheckBox())
			self.analyteCheckBoxes["summary"].append(QCheckBox())

			# We connect the summary and control checkboxes with functions that will activate when their state changes.
			# There are different functions because we need to know which set to override with the new states
			self.analyteCheckBoxes["controls"][i].stateChanged.connect(self.controlChecksRegister)
			self.analyteCheckBoxes["summary"][i].stateChanged.connect(self.summaryChecksRegister)

		# An option for what analyte to base the filter on
		self.analyteLabel = QLabel(self.filterTab.filterInfo["analyte_label"])
		self.optionsLayout.addWidget(self.analyteLabel, 0, 0)
		self.analyteCombo = QComboBox()
		self.optionsLayout.addWidget(self.analyteCombo, 0, 1)
		self.analyteCombo.addItem(" ")
		for i in range(len(self.filterTab.project.eg.analytes)):
			self.analyteCombo.addItem(str(self.filterTab.project.eg.analytes[i]))
		self.analyteLabel.setToolTip(self.filterTab.filterInfo["analyte_description"])
		self.analyteCombo.setToolTip(self.filterTab.filterInfo["analyte_description"])

		# The filt check box
		self.filtCheckBox = QCheckBox(self.filterTab.filterInfo["filt_label"])
		self.filtCheckBox.setToolTip(self.filterTab.filterInfo["filt_description"])
		self.optionsLayout.addWidget(self.filtCheckBox, 0, 2)
		self.filtCheckBox.setMinimumWidth(120)

		# The method of clustering algorithm used
		self.methodLabel = QLabel(self.filterTab.filterInfo["method_label"])
		self.methodCombo = QComboBox()
		self.methodLabel.setToolTip(self.filterTab.filterInfo["method_description"])
		self.methodCombo.setToolTip(self.filterTab.filterInfo["method_description"])
		self.methods = ["meanshift", "kmeans", "DBSCAN"]
		for s in self.methods:
			self.methodCombo.addItem(s)
		self.optionsLayout.addWidget(self.methodLabel, 1, 0)
		self.optionsLayout.addWidget(self.methodCombo, 1, 1)

		# The normalise check box
		self.normaliseCheckBox = QCheckBox(self.filterTab.filterInfo["normalise_label"])
		self.normaliseCheckBox.setToolTip(self.filterTab.filterInfo["normalise_description"])
		self.optionsLayout.addWidget(self.normaliseCheckBox, 1, 2)

		# The time check box
		self.timeCheckBox = QCheckBox(self.filterTab.filterInfo["time_label"])
		self.timeCheckBox.setToolTip(self.filterTab.filterInfo["time_description"])
		self.optionsLayout.addWidget(self.timeCheckBox, 0, 3)

		# The sort check box
		self.sortCheckBox = QCheckBox(self.filterTab.filterInfo["sort_label"])
		self.sortCheckBox.setToolTip(self.filterTab.filterInfo["sort_description"])
		self.optionsLayout.addWidget(self.sortCheckBox, 1, 3)

		# The minimum data points option
		self.minLabel = QLabel(self.filterTab.filterInfo["min_label"])
		self.minEdit = QLineEdit()
		self.minEdit.setPlaceholderText("int")
		self.minEdit.setMaximumWidth(100)
		self.minLabel.setToolTip(self.filterTab.filterInfo["min_description"])
		self.minEdit.setToolTip(self.filterTab.filterInfo["min_description"])
		self.optionsLayout.addWidget(self.minLabel, 2, 0)
		self.optionsLayout.addWidget(self.minEdit, 2, 1)


		# We add a stretch that will fill any extra space on the right-most column
		self.optionsLayout.setColumnStretch(4, 1)

		# We create the control buttons
		self.crossPlotButton = QPushButton("Cross-plot")
		self.crossPlotButton.clicked.connect(self.crossPlotClick)
		self.filterTab.addButton(self.crossPlotButton)

		self.plotButton = QPushButton("Plot")
		self.plotButton.clicked.connect(self.plotClick)
		self.filterTab.addButton(self.plotButton)

		self.createButton = QPushButton("Create filter")
		self.createButton.clicked.connect(self.createClick)
		self.filterTab.addButton(self.createButton)

		# We create a row in the analytes table for the filter
		self.filterTab.table.addWidget(QLabel(self.filterTab.name), self.filterTab.table.rowCount(), 0)

		# We populate the row with checkboxes
		for i in range(self.filterTab.table.columnCount() - 1):
			self.filterTab.table.addWidget(
				self.analyteCheckBoxes["controls"][i], self.filterTab.table.rowCount() - 1, i + 1)


	def controlChecksRegister(self):
		""" Sets the checkboxes in the Summary tab to be the same as those in the Controls tab """
		if not self.updating:
			self.updating = True
			for i in range(len(self.analyteCheckBoxes["controls"])):

				self.analyteCheckBoxes["summary"][i].setCheckState(
					self.analyteCheckBoxes["controls"][i].checkState())

				# We make sure that if the "Select All" checkbox for that row is on,
				# any deselect will set it to partial
				if self.created:
					if self.analyteCheckBoxes["summary"][i].checkState() == 0:
						self.filterTab.summaryTab.allPartial(self.aboveRow)

			self.updateAnalyteToggles()
			self.updating = False

	def summaryChecksRegister(self):
		""" Sets the checkboxes in the Controls tab to be the same as those in the Summary tab """
		if not self.updating:
			self.updating = True
			for i in range(len(self.analyteCheckBoxes["controls"])):
				self.analyteCheckBoxes["controls"][i].setCheckState(
					self.analyteCheckBoxes["summary"][i].checkState())

				# We make sure that if the "Select All" checkbox for that row is on,
				# any deselect will set it to partial
				if self.created:
					if self.analyteCheckBoxes["summary"][i].checkState() == 0:
						self.filterTab.summaryTab.allPartial(self.aboveRow)

			self.updateAnalyteToggles()
			self.updating = False

	def createClick(self):
		""" Adds the new filter to the Summary tab """

		if self.analyteCombo.currentText() == " ":
			self.raiseError("You must select an analyte to apply the filter to")
			return

		try:
			min = int(self.minEdit.text())
		except:
			self.raiseError("The " + self.filterTab.filterInfo["min_label"] + " value must be an integer")
			return

		self.filterTab.project.eg.filter_clustering(analytes = self.analyteCombo.currentText(),
													filt = self.filtCheckBox.isChecked(),
													normalise = self.normaliseCheckBox.isChecked(),
													method = self.methodCombo.currentText(),
													include_time = self.timeCheckBox.isChecked(),
													sort = self.sortCheckBox.isChecked(),
													min_data = min)

		# To determine the name that LAtools has given the filter, we first take a sample:
		egSubset = self.filterTab.project.eg.subsets['All_Samples'][0]
		print(self.filterTab.project.eg.data[egSubset].filt.components.keys())

		# Then check the last filter names that have been added to that sample:
		self.filtName = list(self.filterTab.project.eg.data[egSubset].filt.components.keys())[-1]

		# We toggle the analytes on and off based on the check boxes
		self.updateAnalyteToggles()

		row = self.filterTab.summaryTab.table.rowCount()

		# We create a row in the analytes table in the Summary tab for the filter
		self.filterTab.summaryTab.table.addWidget(
			QLabel(self.filterTab.name), row, 0)

		# We populate the row with checkboxes
		for i in range(self.filterTab.summaryTab.table.columnCount() - 2):
			self.filterTab.summaryTab.table.addWidget(
				self.analyteCheckBoxes["summary"][i], row, i + 1)

		# We add a "select all" checkbox
		self.filterTab.summaryTab.addSelectAll(row)

		# We register our checkbox list for that row
		self.summaryRow = self.filterTab.summaryTab.registerRow(self.analyteCheckBoxes["summaryAbove"],
															  self.analyteCheckBoxes["controlsAbove"])

		# We deactivate the create button
		self.createButton.setEnabled(False)

		# The actual filter creation
		self.created = True

	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.filterTab.filter, "Error", message, QMessageBox.Ok)

	def updateAnalyteToggles(self):
		""" Updates each analyte in the filter to conform to the state of that analyte's checkbox """

		if self.created:

			for i in range(len(self.filterTab.project.eg.analytes)):
				# We update for the "Above" filter
				# If the checkbox is not unchecked...
				if self.analyteCheckBoxes["summary"][i].checkState() != 0:
					self.filterTab.project.eg.filter_on(self.filtName, self.filterTab.project.eg.analytes[i])
				else:
					self.filterTab.project.eg.filter_off(self.filtName, self.filterTab.project.eg.analytes[i])

	def crossPlotClick(self):
		""" Activates when the Cross-plot button is pressed """
		pass

	def plotClick(self):
		""" Activates when the Plot button is pressed """
		pass