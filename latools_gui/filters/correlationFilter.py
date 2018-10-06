""" A filter for correlated elements """

from PyQt5.QtWidgets import *


class CorrelationFilter:
	"""
	The options and controls for creating a correlation filter within a filterTab
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

		# An option to select the first analyte
		self.y_analyteLabel = QLabel(self.filterTab.filterInfo["y_analyte_label"])
		self.optionsLayout.addWidget(self.y_analyteLabel, 0, 0)
		self.y_analyteCombo = QComboBox()
		self.optionsLayout.addWidget(self.y_analyteCombo, 0, 1)
		self.y_analyteCombo.addItem(" ")

		# As this filter must be created after import, we can access the list of analytes in the latools analyse object
		for i in range(len(self.filterTab.project.eg.analytes)):
			self.y_analyteCombo.addItem(str(self.filterTab.project.eg.analytes[i]))
		self.y_analyteLabel.setToolTip(self.filterTab.filterInfo["y_analyte_description"])
		self.y_analyteCombo.setToolTip(self.filterTab.filterInfo["y_analyte_description"])

		# An option to select the second analyte
		self.x_analyteLabel = QLabel(self.filterTab.filterInfo["x_analyte_label"])
		self.optionsLayout.addWidget(self.x_analyteLabel, 1, 0)
		self.x_analyteCombo = QComboBox()
		self.optionsLayout.addWidget(self.x_analyteCombo, 1, 1)
		self.x_analyteCombo.addItem(" ")
		for i in range(len(self.filterTab.project.eg.analytes)):
			self.x_analyteCombo.addItem(str(self.filterTab.project.eg.analytes[i]))
		self.x_analyteLabel.setToolTip(self.filterTab.filterInfo["x_analyte_description"])
		self.x_analyteCombo.setToolTip(self.filterTab.filterInfo["x_analyte_description"])

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

		# We make sure there is y and x analyte currently selected
		if self.y_analyteCombo.currentText() == " ":
			self.raiseError("You must select a Y analyte to apply the filter to.")
			return
		if self.x_analyteCombo.currentText() == " ":
			self.raiseError("You must select a X analyte to apply the filter to.")
			return

		# If there is text in the window option we make sure we can cast it to an int
		window = None
		if self.windowEdit.text() != "":
			try:
				window = int(self.windowEdit.text())
			except:
				self.raiseError("The " + self.filterTab.filterInfo["window_label"] + " value must be an integer.")
				return

		# We make sure we can cast the r and p threshold values to floats
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

		# We create the filter
		try:
			self.filterTab.project.eg.filter_correlation(x_analyte = self.x_analyteCombo.currentText(),
													 y_analyte = self.y_analyteCombo.currentText(),
													 window = window,
													 r_threshold = r_threshold,
													 p_threshold = p_threshold,
													 filt = self.filtCheckBox.isChecked())
		except:
			self.raiseError("An error occurred while trying to create this filter. <br> There may be a problem with " +
							"the input values.")
			return

		# We update the name of the tab with the filter details
		self.createName(tabIndex, "Correlation", self.x_analyteCombo.currentText(), self.y_analyteCombo.currentText())

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

	def createName(self, index, name, elem1, elem2):
		""" We create a more descriptive name to display on the tab """
		self.filterTab.name = name + " " + elem1 + " " + elem2
		self.filterTab.updateName(index)

	def loadFilter(self, params):
		""" When loading an lalog file, the parameters of this filter are added to the gui, then the
			create button function is called.

			Parameters
			----------
			params : dict
				The key-word arguments of the filter call, saved in the lalog file.
		"""
		# For the args in params, we update each filter option, using the default value if the argument is not in the dict.
		self.y_analyteCombo.setCurrentIndex(self.y_analyteCombo.findText(params.get("y_analyte", "")))
		self.x_analyteCombo.setCurrentIndex(self.x_analyteCombo.findText(params.get("x_analyte", "")))
		self.windowEdit.setText(str(params.get("window", "")))
		self.r_thresholdEdit.setText(str(params.get("r_threshold", "")))
		self.p_thresholdEdit.setText(str(params.get("p_threshold", "")))
		self.filtCheckBox.setChecked(params.get("filt", True))

		# We act as though the user has added these options and clicked the create button.
		self.createClick()

	def freezeOptions(self):
		"""
		We lock the option fields after the filter has been created so that they will give a representation
		of the details of the filter
		"""
		self.y_analyteCombo.setEnabled(False)
		self.x_analyteCombo.setEnabled(False)
		self.windowEdit.setEnabled(False)
		self.r_thresholdEdit.setEnabled(False)
		self.p_thresholdEdit.setEnabled(False)
		self.filtCheckBox.setEnabled(False)
		self.createButton.setEnabled(False)

	def updateOptions(self):
		""" Delivers the current state of each option to the plot pane. """
		return {
			"y_analyte": self.y_analyteCombo.currentText(),
			"x_analyte": self.x_analyteCombo.currentText(),
			"window": self.windowEdit.text(),
			"r_threshold": self.r_thresholdEdit.text(),
			"p_threshold": self.p_thresholdEdit.text(),
			"filt": self.filtCheckBox.isChecked()
		}