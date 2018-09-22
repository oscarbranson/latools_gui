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

		try:
			threshold = int(self.thresholdEdit.text())
		except:
			self.raiseError("The " + self.filterTab.filterInfo["threshold_label"] + " value must be an integer.")
			return

		try:
			self.filterTab.project.eg.filter_exclude_downhole(threshold = threshold,
														  filt = self.filtCheckBox.isChecked())
		except:
			self.raiseError("An error occurred while trying to create this filter. <br> There may be a problem with " +
							"the input values.")
			return

		self.createName(tabIndex, "Exclude", str(threshold))

		# We determine how many filters have been created
		egSubset = self.filterTab.project.eg.subsets['All_Samples'][0]
		currentFilters = list(self.filterTab.project.eg.data[egSubset].filt.components.keys())

		# We create filter rows for each new filter
		for i in range(len(currentFilters) - oldFilters):
			self.filterTab.createFilter(currentFilters[i + oldFilters])

		self.freezeOptions()

	def raiseError(self, message):
		""" Creates an error box with the given message """
		errorBox = QMessageBox.critical(self.filterTab.filter, "Error", message, QMessageBox.Ok)

	def createName(self, index, name, thresh):
		""" We create a more descriptive name to display on the tab """
		self.filterTab.name = name + " " + thresh
		self.filterTab.updateName(index)

	def loadFilter(self, params):

		self.thresholdEdit.setText(str(params.get("threshold", "")))
		self.filtCheckBox.setChecked(params.get("filt", True))
		self.createClick()

	def freezeOptions(self):
		"""
		We lock the option fields after the filter has been created so that they will give a representation
		of the details of the filter
		"""
		self.thresholdEdit.setEnabled(False)
		self.filtCheckBox.setEnabled(False)
		self.createButton.setEnabled(False)