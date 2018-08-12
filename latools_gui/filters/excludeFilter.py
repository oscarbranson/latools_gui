""" A filter for excluding data points after a specified threshold """

from PyQt5.QtWidgets import *


class ExcludeFilter:
	"""
	Exclude Downhole Filter info
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

		# The threshold option
		self.thresholdLabel = QLabel(self.filterTab.filterInfo["threshold_label"])
		self.thresholdEdit = QLineEdit()
		self.thresholdEdit.setPlaceholderText("int")
		#self.thresholdEdit.setMaximumWidth(100)
		self.thresholdLabel.setToolTip(self.filterTab.filterInfo["threshold_description"])
		self.thresholdEdit.setToolTip(self.filterTab.filterInfo["threshold_description"])
		self.optionsLayout.addWidget(self.thresholdLabel, 0, 0)
		self.optionsLayout.addWidget(self.thresholdEdit, 0, 1)

		# The filt check box
		self.filtCheckBox = QCheckBox(self.filterTab.filterInfo["filt_label"])
		self.filtCheckBox.setToolTip(self.filterTab.filterInfo["filt_description"])
		self.optionsLayout.addWidget(self.filtCheckBox, 1, 0, 1, 2)
		#self.filtCheckBox.setMinimumWidth(120)
		self.filtCheckBox.setChecked(True)

		# We add a stretch that will fill any extra space on the right-most column
		self.optionsLayout.setColumnStretch(2, 1)

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
						self.filterTab.summaryTab.allPartial(self.summaryRow)

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
						self.filterTab.summaryTab.allPartial(self.summaryRow)

			self.updateAnalyteToggles()
			self.updating = False

	def createClick(self):
		""" Adds the new filter to the Summary tab """

		try:
			threshold = int(self.thresholdEdit.text())
		except:
			self.raiseError("The " + self.filterTab.filterInfo["threshold_label"] + " value must be an integer.")
			return

		self.filterTab.project.eg.filter_exclude_downhole(threshold = threshold,
														  filt = self.filtCheckBox.isChecked())

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
		self.summaryRow = self.filterTab.summaryTab.registerRow(self.analyteCheckBoxes["summary"],
																self.analyteCheckBoxes["controls"])

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
				# If the checkbox is not unchecked...
				if self.analyteCheckBoxes["summary"][i].checkState() != 0:
					# We switch the filter on for that analyte
					self.filterTab.project.eg.filter_on(self.filtName, self.filterTab.project.eg.analytes[i])
				else:
					# We switch the filter off for that analyte
					self.filterTab.project.eg.filter_off(self.filtName, self.filterTab.project.eg.analytes[i])

	def crossPlotClick(self):
		""" Activates when the Cross-plot button is pressed """
		pass

	def plotClick(self):
		""" Activates when the Plot button is pressed """
		pass