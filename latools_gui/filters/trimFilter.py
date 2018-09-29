""" A filter for trimming data points """

from PyQt5.QtWidgets import *


class TrimFilter:
	"""
	Trim Filter info
	"""
	def __init__(self, filterTab):

		# This filter has access to the general filter structure
		self.filterTab = filterTab

		# The layout that this filter will put its option controls in
		self.optionsLayout = QGridLayout(self.filterTab.optionsWidget)

		# The start option
		self.startLabel = QLabel(self.filterTab.filterInfo["start_label"])
		self.startEdit = QLineEdit()
		self.startEdit.setPlaceholderText("int")
		self.startLabel.setToolTip(self.filterTab.filterInfo["start_description"])
		self.startEdit.setToolTip(self.filterTab.filterInfo["start_description"])
		self.optionsLayout.addWidget(self.startLabel, 0, 0)
		self.optionsLayout.addWidget(self.startEdit, 0, 1)

		# The end option
		self.endLabel = QLabel(self.filterTab.filterInfo["end_label"])
		self.endEdit = QLineEdit()
		self.endEdit.setPlaceholderText("int")
		self.endLabel.setToolTip(self.filterTab.filterInfo["end_description"])
		self.endEdit.setToolTip(self.filterTab.filterInfo["end_description"])
		self.optionsLayout.addWidget(self.endLabel, 1, 0)
		self.optionsLayout.addWidget(self.endEdit, 1, 1)

		# The filt check box
		self.filtCheckBox = QCheckBox(self.filterTab.filterInfo["filt_label"])
		self.filtCheckBox.setToolTip(self.filterTab.filterInfo["filt_description"])
		self.optionsLayout.addWidget(self.filtCheckBox, 2, 0, 1, 2)
		self.filtCheckBox.setChecked(True)

		# We add a stretch that will fill any extra space on the right-most column
		self.optionsLayout.setColumnStretch(4, 1)

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
			start = int(self.startEdit.text())
		except:
			self.raiseError("The " + self.filterTab.filterInfo["start_label"] + " value must be an integer")
			return

		try:
			end = int(self.endEdit.text())
		except:
			self.raiseError("The " + self.filterTab.filterInfo["end_label"] + " value must be an integer")
			return

		try:
			self.filterTab.project.eg.filter_trim(start = start,
											  end = end,
											  filt = self.filtCheckBox.isChecked())
		except:
			self.raiseError("An error occurred while trying to create this filter. <br> There may be a problem with " +
							"the input values.")
			return

		self.createName(tabIndex, "Trim", str(start), str(end))

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

	def createName(self, index, name, start, stop):
		""" We create a more descriptive name to display on the tab """
		self.filterTab.name = name + " start: " + start + " stop: " + stop
		self.filterTab.updateName(index)

	def loadFilter(self, params):
		self.startEdit.setText(str(params.get("start", "")))
		self.endEdit.setText(str(params.get("end", "")))
		self.filtCheckBox.setChecked(params.get("filt", True))
		self.createClick()

	def freezeOptions(self):
		"""
		We lock the option fields after the filter has been created so that they will give a representation
		of the details of the filter
		"""
		self.startEdit.setEnabled(False)
		self.endEdit.setEnabled(False)
		self.filtCheckBox.setEnabled(False)
		self.createButton.setEnabled(False)

	def updateOptions(self):

		return {
			"start": self.startEdit.text(),
			"end": self.endEdit.text(),
			"filt": self.filtCheckBox.isChecked()
		}