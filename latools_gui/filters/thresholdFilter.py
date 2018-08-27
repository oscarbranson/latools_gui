""" A filter for defining a threshold """

from PyQt5.QtWidgets import *


class ThresholdFilter:
	"""
	Threshold Filter info
	"""
	def __init__(self, filterTab):

		# This filter has access to the general filter structure
		self.filterTab = filterTab

		# The layout that this filter will put its option controls in
		self.optionsLayout = QGridLayout(self.filterTab.optionsWidget)

		# The complete set of checkboxes that can turn on or off analytes
		self.analyteCheckBoxes = {
			"controlsAbove": [],
			"controlsBelow": [],
			"summaryAbove": [],
			"summaryBelow": [],
		}

		# Determines is this filter will have "above" and "below" rows
		self.twoRows = True

		# Registers which rows this filter occupies in Summary
		self.aboveRow = 0
		self.belowRow = 0

		self.filtNameAbove = ""
		self.filtNameBelow = ""

		# Determines if the filter has been created yet
		self.created = False

		# Prevents updating based on the program activating check boxes
		self.updating = False

		# We create each checkbox that will appear in the filter controls and summary tabs
		for i in range(len(self.filterTab.project.eg.analytes)):

			self.analyteCheckBoxes["controlsAbove"].append(QCheckBox())
			self.analyteCheckBoxes["controlsBelow"].append(QCheckBox())
			self.analyteCheckBoxes["summaryAbove"].append(QCheckBox())
			self.analyteCheckBoxes["summaryBelow"].append(QCheckBox())

			# We connect the summary and control checkboxes with functions that will activate when their state changes.
			# There are different functions because we need to know which set to override with the new states
			self.analyteCheckBoxes["controlsAbove"][i].stateChanged.connect(self.controlChecksRegister)
			self.analyteCheckBoxes["controlsBelow"][i].stateChanged.connect(self.controlChecksRegister)
			self.analyteCheckBoxes["summaryAbove"][i].stateChanged.connect(self.summaryChecksRegister)
			self.analyteCheckBoxes["summaryBelow"][i].stateChanged.connect(self.summaryChecksRegister)

		# A label for the type
		self.typeLabel = QLabel(self.filterTab.filterInfo["type_label"])
		self.optionsLayout.addWidget(self.typeLabel, 0, 0)

		# A combobox for the type
		self.typeCombo = QComboBox()
		self.typeCombo.activated.connect(self.typeChanged)

		self.thresholdTypes = ["Threshold",
							   "Threshold Percentile",
							   "Gradient Threshold"]
							   #"Gradient Threshold Percentile"]

		for t in self.thresholdTypes:
			self.typeCombo.addItem(t)

		self.optionsLayout.addWidget(self.typeCombo, 0, 1)

		self.typeLabel.setToolTip(self.filterTab.filterInfo["type_description"])
		self.typeCombo.setToolTip(self.filterTab.filterInfo["type_description"])

		# An option for the threshold value
		self.threshValueLabel = QLabel(self.filterTab.filterInfo["threshold_value_label"])
		self.optionsLayout.addWidget(self.threshValueLabel, 1, 0)

		self.threshValueEdit = QLineEdit()
		self.optionsLayout.addWidget(self.threshValueEdit, 1, 1)
		self.threshValueEdit.setMaximumWidth(100)
		self.threshValueEdit.setPlaceholderText("float")

		self.threshValueLabel.setToolTip(self.filterTab.filterInfo["threshold_value_description"])
		self.threshValueEdit.setToolTip(self.filterTab.filterInfo["threshold_value_description"])

		# An option for what analyte to base the filter on
		self.analyteLabel = QLabel(self.filterTab.filterInfo["analyte_label"])
		self.optionsLayout.addWidget(self.analyteLabel, 0, 2)

		self.analyteCombo = QComboBox()
		self.optionsLayout.addWidget(self.analyteCombo, 0, 3)

		self.analyteCombo.addItem(" ")
		for i in range(len(self.filterTab.project.eg.analytes)):
			self.analyteCombo.addItem(str(self.filterTab.project.eg.analytes[i]))

		self.analyteLabel.setToolTip(self.filterTab.filterInfo["analyte_description"])
		self.analyteCombo.setToolTip(self.filterTab.filterInfo["analyte_description"])

		# An option for the percentile
		self.percentLabel = QLabel(self.filterTab.filterInfo["percentile_label"])
		self.percentEdit = QLineEdit()
		self.optionsLayout.addWidget(self.percentLabel, 2, 0)
		self.optionsLayout.addWidget(self.percentEdit, 2, 1)
		self.percentEdit.setPlaceholderText("float")
		self.percentEdit.setEnabled(False)

		self.percentLabel.setToolTip(self.filterTab.filterInfo["percentile_description"])
		self.percentEdit.setToolTip(self.filterTab.filterInfo["percentile_description"])

		# An option for the window
		self.winLabel = QLabel(self.filterTab.filterInfo["win_label"])
		self.winEdit = QLineEdit("15")
		self.optionsLayout.addWidget(self.winLabel, 1, 2)
		self.optionsLayout.addWidget(self.winEdit, 1, 3)
		self.winEdit.setEnabled(False)

		self.winLabel.setToolTip(self.filterTab.filterInfo["percentile_description"])
		self.winEdit.setToolTip(self.filterTab.filterInfo["percentile_description"])

		# An option for the level
		self.levelLabel = QLabel(self.filterTab.filterInfo["level_label"])
		self.levelCombo = QComboBox()
		self.levelCombo.addItem("population")
		self.levelCombo.addItem("individual")
		self.optionsLayout.addWidget(self.levelLabel, 2, 2)
		self.optionsLayout.addWidget(self.levelCombo, 2, 3)
		self.levelLabel.setToolTip(self.filterTab.filterInfo["level_description"])
		self.levelCombo.setToolTip(self.filterTab.filterInfo["level_description"])
		self.levelCombo.setEnabled(False)

		# We add a stretch that will fill any extra space on the right-most column
		self.optionsLayout.setColumnStretch(4, 1)

		# We make the create filter button
		self.createButton = QPushButton("Create filter")
		self.createButton.clicked.connect(self.createClick)
		self.filterTab.addButton(self.createButton)

		# We create a row in the analytes table for the "above" version
		self.filterTab.table.addWidget(QLabel(self.filterTab.name + " (above)"), self.filterTab.table.rowCount(), 0)

		# We populate the row with checkboxes
		for i in range(self.filterTab.table.columnCount() - 1):
			self.filterTab.table.addWidget(
				self.analyteCheckBoxes["controlsAbove"][i], self.filterTab.table.rowCount() - 1, i + 1)

		# We create a row in the analytes table for the "below" version
		self.filterTab.table.addWidget(QLabel(self.filterTab.name + " (below)"), self.filterTab.table.rowCount(), 0)

		# We populate the row with checkboxes
		for i in range(self.filterTab.table.columnCount() - 1):
			self.filterTab.table.addWidget(
				self.analyteCheckBoxes["controlsBelow"][i], self.filterTab.table.rowCount() - 1, i + 1)

	def controlChecksRegister(self):
		""" Sets the checkboxes in the Summary tab to be the same as those in the Controls tab """
		if not self.updating:
			self.updating = True
			for i in range(len(self.analyteCheckBoxes["controlsAbove"])):

				self.analyteCheckBoxes["summaryAbove"][i].setCheckState(
					self.analyteCheckBoxes["controlsAbove"][i].checkState())

				self.analyteCheckBoxes["summaryBelow"][i].setCheckState(
					self.analyteCheckBoxes["controlsBelow"][i].checkState())

				# We make sure that if the "Select All" checkbox for that row is on,
				# any deselect will set it to partial
				if self.created:
					if self.analyteCheckBoxes["summaryAbove"][i].checkState() == 0:
						self.filterTab.summaryTab.allPartial(self.aboveRow)
					if self.analyteCheckBoxes["summaryBelow"][i].checkState() == 0:
						self.filterTab.summaryTab.allPartial(self.belowRow)

			self.updateAnalyteToggles()
			self.updating = False

	def summaryChecksRegister(self):
		""" Sets the checkboxes in the Controls tab to be the same as those in the Summary tab """
		if not self.updating:
			self.updating = True
			for i in range(len(self.analyteCheckBoxes["controlsAbove"])):
				self.analyteCheckBoxes["controlsAbove"][i].setCheckState(
					self.analyteCheckBoxes["summaryAbove"][i].checkState())

				self.analyteCheckBoxes["controlsBelow"][i].setCheckState(
					self.analyteCheckBoxes["summaryBelow"][i].checkState())

				# We make sure that if the "Select All" checkbox for that row is on,
				# any deselect will set it to partial
				if self.created:
					if self.analyteCheckBoxes["summaryAbove"][i].checkState() == 0:
						self.filterTab.summaryTab.allPartial(self.aboveRow)
					if self.analyteCheckBoxes["summaryBelow"][i].checkState() == 0:
						self.filterTab.summaryTab.allPartial(self.belowRow)

			self.updateAnalyteToggles()
			self.updating = False

	def createClick(self):
		""" Adds the new filter to the Summary tab """

		# All threshold filter types need an analyte selected
		if self.analyteCombo.currentText() == " ":
			self.raiseError("You must select an analyte")
			return

		# We now run a different function based on the selected threshold type

		# Threshold filter selected:
		if self.typeCombo.currentText() == self.thresholdTypes[0]:

			try:
				localThreshold = float(self.threshValueEdit.text())
			except:
				self.raiseError("The 'Threshold' value must be a floating point number")
				return

			# We create the filter
			self.filterTab.project.eg.filter_threshold(analyte = self.analyteCombo.currentText(),
													   threshold = localThreshold)

		# Threshold Percentile filter selected:
		elif self.typeCombo.currentText() == self.thresholdTypes[1]:

			try:
				localPercent = [float(self.percentEdit.text())]
			except:
				self.raiseError("The 'Percentile' value must be a floating point number")
				return

			# We create the filter
			self.filterTab.project.eg.filter_threshold_percentile(analyte=self.analyteCombo.currentText(),
																  percentiles=localPercent,
																  level=self.levelCombo.currentText())

		# Gradient Threshold filter selected:
		elif self.typeCombo.currentText() == self.thresholdTypes[2]:

			try:
				localThreshold = float(self.threshValueEdit.text())
			except:
				self.raiseError("The 'Threshold' value must be a floating point number")
				return

			try:
				localWin = int(self.winEdit.text())
			except:
				self.raiseError("The 'Window' value must be an integer")
				return

			# We create the filter
			self.filterTab.project.eg.filter_gradient_threshold(analyte=self.analyteCombo.currentText(),
																threshold=localThreshold,
																win=localWin)

		# Gradient Threshold Percentile filter selected:
		elif self.typeCombo.currentText() == self.thresholdTypes[2]:

			try:
				localPercent = [float(self.percentEdit.text())]
			except:
				self.raiseError("The 'Percentile' value must be a floating point number")
				return

			try:
				localWin = int(self.winEdit.text())
			except:
				self.raiseError("The 'Window' value must be an integer")
				return

			# We create the filter
			self.filterTab.project.eg.filter_gradient_threshold_percentile(analyte=self.analyteCombo.currentText(),
																		   percentiles=localPercent,
																		   level=self.levelCombo.currentText(),
																		   win=localWin)

		# To determine the name that LAtools has given the filter, we first take a sample:
		egSubset = self.filterTab.project.eg.subsets['All_Samples'][0]
		print(self.filterTab.project.eg.data[egSubset].filt.components.keys())

		# Then check the last filter names that have been added to that sample:
		self.filtNameAbove = list(self.filterTab.project.eg.data[egSubset].filt.components.keys())[-1]
		self.filtNameBelow = list(self.filterTab.project.eg.data[egSubset].filt.components.keys())[-2]

		# We toggle the analytes on and off based on the check boxes
		self.updateAnalyteToggles()

		row = self.filterTab.summaryTab.table.rowCount()

		# We create a row in the analytes table in the Summary tab for the "above" version of this filter
		self.filterTab.summaryTab.table.addWidget(
			QLabel(self.filterTab.name + " (above)"), row, 0)

		# We populate the row with checkboxes
		for i in range(self.filterTab.summaryTab.table.columnCount() - 2):
			self.filterTab.summaryTab.table.addWidget(
				self.analyteCheckBoxes["summaryAbove"][i], row, i + 1)

		# We add a "select all" checkbox
		self.filterTab.summaryTab.addSelectAll(row)

		# We register our checkbox list for that row
		self.aboveRow = self.filterTab.summaryTab.registerRow(self.analyteCheckBoxes["summaryAbove"],
															  self.analyteCheckBoxes["controlsAbove"])

		row += 1

		# We create a row in the analytes table in the Summary tab for the "below" version of this filter
		self.filterTab.summaryTab.table.addWidget(
			QLabel(self.filterTab.name + " (below)"), row, 0)

		# We populate the row with checkboxes
		for i in range(self.filterTab.summaryTab.table.columnCount() - 2):
			self.filterTab.summaryTab.table.addWidget(
				self.analyteCheckBoxes["summaryBelow"][i], row, i + 1)

		# We add a "select all" checkbox
		self.filterTab.summaryTab.addSelectAll(row)

		# We register our checkbox list for that row
		self.belowRow = self.filterTab.summaryTab.registerRow(self.analyteCheckBoxes["summaryBelow"],
															  self.analyteCheckBoxes["controlsBelow"])

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
				if self.analyteCheckBoxes["summaryAbove"][i].checkState() != 0:
					self.filterTab.project.eg.filter_on(self.filtNameAbove,
															 self.filterTab.project.eg.analytes[i])
				else:
					self.filterTab.project.eg.filter_off(self.filtNameAbove,
															 self.filterTab.project.eg.analytes[i])

				# Update for the "Below" filter
				if self.analyteCheckBoxes["summaryBelow"][i].checkState() != 0:
					self.filterTab.project.eg.filter_on(self.filtNameBelow,
															 self.filterTab.project.eg.analytes[i])
				else:
					self.filterTab.project.eg.filter_off(self.filtNameBelow,
															 self.filterTab.project.eg.analytes[i])

	def typeChanged(self):
		""" Sets the enabled options based on what threshold type is currently selected """

		if self.typeCombo.currentText() == self.thresholdTypes[0]:
			# filter = Threshold
			self.threshValueEdit.setEnabled(True)
			self.percentEdit.setEnabled(False)
			self.winEdit.setEnabled(False)
			self.levelCombo.setEnabled(False)

		elif self.typeCombo.currentText() == self.thresholdTypes[1]:
			# filter = Threshold Percentile
			self.threshValueEdit.setEnabled(False)
			self.percentEdit.setEnabled(True)
			self.winEdit.setEnabled(False)
			self.levelCombo.setEnabled(True)

		elif self.typeCombo.currentText() == self.thresholdTypes[2]:
			# filter = Gradient Threshold
			self.threshValueEdit.setEnabled(True)
			self.percentEdit.setEnabled(False)
			self.winEdit.setEnabled(True)
			self.levelCombo.setEnabled(False)

		elif self.typeCombo.currentText() == self.thresholdTypes[3]:
			# filter = Threshold Gradient Percentile
			self.threshValueEdit.setEnabled(False)
			self.percentEdit.setEnabled(True)
			self.winEdit.setEnabled(True)
			self.levelCombo.setEnabled(True)