""" A filter for correlated elements """

from PyQt5.QtWidgets import *


class CorrelationFilter:
	"""
	Correlation Filter info
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

		# An option to select the first analyte
		self.y_analyteLabel = QLabel(self.filterTab.filterInfo["y_analyte_label"])
		self.optionsLayout.addWidget(self.y_analyteLabel, 0, 0)
		self.y_analyteCombo = QComboBox()
		self.optionsLayout.addWidget(self.y_analyteCombo, 0, 1)
		self.y_analyteCombo.addItem(" ")
		for i in range(len(self.filterTab.project.eg.analytes)):
			self.y_analyteCombo.addItem(str(self.filterTab.project.eg.analytes[i]))
		self.y_analyteLabel.setToolTip(self.filterTab.filterInfo["analyte_description"])
		self.y_analyteCombo.setToolTip(self.filterTab.filterInfo["analyte_description"])

		# An option to select the second analyte
		self.x_analyteLabel = QLabel(self.filterTab.filterInfo["x_analyte_label"])
		self.optionsLayout.addWidget(self.x_analyteLabel, 1, 0)
		self.x_analyteCombo = QComboBox()
		self.optionsLayout.addWidget(self.x_analyteCombo, 1, 1)
		self.x_analyteCombo.addItem(" ")
		for i in range(len(self.filterTab.project.eg.analytes)):
			self.x_analyteCombo.addItem(str(self.filterTab.project.eg.analytes[i]))
		self.x_analyteLabel.setToolTip(self.filterTab.filterInfo["analyte_description"])
		self.x_analyteCombo.setToolTip(self.filterTab.filterInfo["analyte_description"])

		# The window option
		self.windowLabel = QLabel(self.filterTab.filterInfo["window_label"])
		self.windowEdit = QLineEdit()
		self.windowEdit.setPlaceholderText("None (int)")
		self.windowEdit.setMaximumWidth(100)
		self.windowLabel.setToolTip(self.filterTab.filterInfo["window_description"])
		self.windowEdit.setToolTip(self.filterTab.filterInfo["window_description"])
		self.optionsLayout.addWidget(self.windowLabel, 2, 0)
		self.optionsLayout.addWidget(self.windowEdit, 2, 1)

		# The r_threshold option
		self.r_thresholdLabel = QLabel(self.filterTab.filterInfo["r_threshold_label"])
		self.r_thresholdEdit = QLineEdit("0.9")
		self.r_thresholdEdit.setPlaceholderText("float")
		self.r_thresholdEdit.setMaximumWidth(100)
		self.r_thresholdLabel.setToolTip(self.filterTab.filterInfo["r_threshold_description"])
		self.r_thresholdEdit.setToolTip(self.filterTab.filterInfo["r_threshold_description"])
		self.optionsLayout.addWidget(self.r_thresholdLabel, 0, 2)
		self.optionsLayout.addWidget(self.r_thresholdEdit, 0, 3)

		# The p_threshold option
		self.p_thresholdLabel = QLabel(self.filterTab.filterInfo["p_threshold_label"])
		self.p_thresholdEdit = QLineEdit("0.05")
		self.p_thresholdEdit.setPlaceholderText("float")
		self.p_thresholdEdit.setMaximumWidth(100)
		self.p_thresholdLabel.setToolTip(self.filterTab.filterInfo["p_threshold_description"])
		self.p_thresholdEdit.setToolTip(self.filterTab.filterInfo["p_threshold_description"])
		self.optionsLayout.addWidget(self.p_thresholdLabel, 1, 2)
		self.optionsLayout.addWidget(self.p_thresholdEdit, 1, 3)

		# The filt check box
		self.filtCheckBox = QCheckBox(self.filterTab.filterInfo["filt_label"])
		self.filtCheckBox.setToolTip(self.filterTab.filterInfo["filt_description"])
		self.optionsLayout.addWidget(self.filtCheckBox, 2, 2, 1, 2)
		#self.filtCheckBox.setMinimumWidth(120)
		self.filtCheckBox.setChecked(True)

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

		if self.y_analyteCombo.currentText() == " ":
			self.raiseError("You must select a Y analyte to apply the filter to.")
			return

		if self.x_analyteCombo.currentText() == " ":
			self.raiseError("You must select a X analyte to apply the filter to.")
			return

		window = None
		if self.windowEdit.text() != "":
			try:
				window = int(self.windowEdit.text())
			except:
				self.raiseError("The " + self.filterTab.filterInfo["window_label"] + " value must be an integer.")
				return

		try:
			r_threshold = float(self.r_thresholdEdit.text())
		except:
			self.raiseError("The " + self.filterTab.filterInfo["r_threshold_label"] +
							" value must be a floating point number.")
			return

		try:
			p_threshold = float(self.p_thresholdEdit.text())
		except:
			self.raiseError("The " + self.filterTab.filterInfo["p_threshold_label"] +
							" value must be a floating point number.")
			return

		self.filterTab.project.eg.filter_correlation(x_analyte = self.x_analyteCombo.currentText(),
													 y_analyte = self.y_analyteCombo.currentText(),
													 window = window,
													 r_threshold = r_threshold,
													 p_threshold = p_threshold,
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