""" A filter for defining a threshold """

from PyQt5.QtWidgets import *
import ast


class ThresholdFilter:
	"""
	The options and controls for creating a threshold filter within a filterTab
	"""
	def __init__(self, filterTab):
		"""
		Creates the unique aspects of this filter, housed within the filterTab

		Parameters
		----------
		filterTab : FilterTab
			The general tab in which this filter's unique aspects will be created.
		"""
		# This filter has access to the general filter structure
		self.filterTab = filterTab

		# The layout that this filter will put its option controls in
		self.optionsLayout = QGridLayout(self.filterTab.optionsWidget)

		# A label for the type
		self.typeLabel = QLabel(self.filterTab.filterInfo["type_label"])
		self.optionsLayout.addWidget(self.typeLabel, 0, 0)

		# A combobox for the type
		self.typeCombo = QComboBox()
		self.typeCombo.activated.connect(self.typeChanged)

		# We add the threshold types to the combobox.
		# Currently there is a problem with the Gradient Threshold Percentile filter. When that is resolved
		# it can be added to the list.
		self.thresholdTypes = ["Threshold",
							   "Threshold Percentile",
							   "Gradient Threshold"]
							   #"Gradient Threshold Percentile"]

		for t in self.thresholdTypes:
			self.typeCombo.addItem(t)

		# The type combobox is added to the layout, and the tooltips are set for the box and label
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

	def createClick(self):
		""" Adds the new filter to the Summary tab """

		# We record the current tab index so that we know which tab to update the name of
		tabIndex = self.filterTab.tabsArea.currentIndex()

		# We take a reading of the current number of filters so that we can determine how many new
		# ones this will create
		egSubset = self.filterTab.project.eg.subsets['All_Samples'][0]
		oldFilters = len(list(self.filterTab.project.eg.data[egSubset].filt.components.keys()))

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
			try:
				self.filterTab.project.eg.filter_threshold(analyte = self.analyteCombo.currentText(),
													   threshold = localThreshold)
			except:
				self.raiseError(
					"An error occurred while trying to create this filter. <br> There may be a problem with " +
					"the input values.")
				return

			# We update the name of the filter
			self.createName(tabIndex, "threshold", self.analyteCombo.currentText(), localThreshold)

		# Threshold Percentile filter selected:
		elif self.typeCombo.currentText() == self.thresholdTypes[1]:

			try:
				localPercent = [float(self.percentEdit.text())]
			except:
				self.raiseError("The 'Percentile' value must be a floating point number")
				return

			# We create the filter
			try:
				self.filterTab.project.eg.filter_threshold_percentile(analyte=self.analyteCombo.currentText(),
																  percentiles=localPercent,
																  level=self.levelCombo.currentText())
			except:
				self.raiseError(
					"An error occurred while trying to create this filter. <br> There may be a problem with " +
					"the input values.")
				return

			# We update the name of the filter
			self.createName(tabIndex, "threshold_percentile", self.analyteCombo.currentText(), localPercent)

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
			try:
				self.filterTab.project.eg.filter_gradient_threshold(analyte=self.analyteCombo.currentText(),
																threshold=localThreshold,
																win=localWin)
			except:
				self.raiseError(
					"An error occurred while trying to create this filter. <br> There may be a problem with " +
					"the input values.")
				return

			# We update the name of the filter
			self.createName(tabIndex, "gradient_threshold", self.analyteCombo.currentText(), localThreshold)

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
			try:
				self.filterTab.project.eg.filter_gradient_threshold_percentile(analyte=self.analyteCombo.currentText(),
																		   percentiles=localPercent,
																		   level=self.levelCombo.currentText(),
																		   win=localWin)
			except:
				self.raiseError(
					"An error occurred while trying to create this filter. <br> There may be a problem with " +
					"the input values.")
				return

			# We update the name of the filter
			self.createName(tabIndex, "gradient_threshold_percentile", self.analyteCombo.currentText(), localPercent)

		# We determine how many filters have been created
		egSubset = self.filterTab.project.eg.subsets['All_Samples'][0]
		currentFilters = list(self.filterTab.project.eg.data[egSubset].filt.components.keys())

		# We create filter rows for each new filter
		for i in range(len(currentFilters) - oldFilters):
			self.filterTab.createFilter(currentFilters[i + oldFilters])

		# We disable all of the option fields so that they record the parameters used in creating the filter
		self.freezeOptions()

	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.filterTab.filter, "Error", message, QMessageBox.Ok)

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

	def createName(self, index, type, analyte, thresh):
		""" We create a more descriptive name to display on the tab """
		self.filterTab.name = type + " " + analyte + " " + str(thresh)
		self.filterTab.updateName(index)

	def loadFilter(self, params, typeIndex):
		""" When loading an lalog file, the parameters of this filter are added to the gui, then the
			create button function is called.

			Parameters
			----------
			params : dict
				The key-word arguments of the filter call, saved in the lalog file.
		"""
		# For the args in params, we update each filter option, using the default value if the argument is not in the dict.
		self.typeCombo.setCurrentIndex(typeIndex)
		self.analyteCombo.setCurrentIndex(self.analyteCombo.findText(params.get("analyte", "")))
		self.threshValueEdit.setText(str(params.get("threshold", "")))
		self.percentEdit.setText(str(params.get("percentiles", [""])[0]))
		self.winEdit.setText(str(params.get("win", "")))
		self.levelCombo.setCurrentIndex(self.levelCombo.findText(params.get("level", "")))

		# We act as though the user has added these options and clicked the create button.
		self.createClick()

	def freezeOptions(self):
		"""
		We lock the option fields after the filter has been created so that they will give a representation
		of the details of the filter
		"""
		self.typeCombo.setEnabled(False)
		self.threshValueEdit.setEnabled(False)
		self.analyteCombo.setEnabled(False)
		self.percentEdit.setEnabled(False)
		self.winEdit.setEnabled(False)
		self.levelCombo.setEnabled(False)
		self.createButton.setEnabled(False)

	def updateOptions(self):
		""" Delivers the current state of each option to the plot pane. """

		return {
			"type": self.typeCombo.currentText(),
			"threshold": self.threshValueEdit.text(),
			"analyte": self.analyteCombo.currentText(),
			"percent": self.percentEdit.text(),
			"win": self.winEdit.text(),
			"level": self.levelCombo.currentText()
		}