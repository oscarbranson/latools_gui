""" A filter that Identifies the longest possible contiguous data region in the signal where the relative
standard deviation (std) and concentration of all analytes is minimised.  """

from PyQt5.QtWidgets import *


class SignalFilter:
	"""
	Signal Optimiser Filter info
	"""
	def __init__(self, filterTab):

		# This filter has access to the general filter structure
		self.filterTab = filterTab

		# The layout that this filter will put its option controls in
		self.optionsLayout = QGridLayout(self.filterTab.optionsWidget)

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

		# The min_points option
		self.minLabel = QLabel(self.filterTab.filterInfo["min_label"])
		self.minEdit = QLineEdit()
		self.minEdit.setPlaceholderText("int")
		#self.thresholdEdit.setMaximumWidth(100)
		self.minLabel.setToolTip(self.filterTab.filterInfo["min_description"])
		self.minEdit.setToolTip(self.filterTab.filterInfo["min_description"])
		self.optionsLayout.addWidget(self.minLabel, 1, 0)
		self.optionsLayout.addWidget(self.minEdit, 1, 1)

		# The mode of the threshold used
		self.modeLabel = QLabel(self.filterTab.filterInfo["mode_label"])
		self.modeCombo = QComboBox()
		self.modeLabel.setToolTip(self.filterTab.filterInfo["mode_description"])
		self.modeCombo.setToolTip(self.filterTab.filterInfo["mode_description"])
		self.modes = ["mean", "median", "kde_max", "bayes_mvs"]
		for s in self.modes:
			self.modeCombo.addItem(s)
		self.optionsLayout.addWidget(self.modeLabel, 2, 0)
		self.optionsLayout.addWidget(self.modeCombo, 2, 1)

		# The filt check box
		# self.filtCheckBox = QCheckBox(self.filterTab.filterInfo["filt_label"])
		# self.filtCheckBox.setToolTip(self.filterTab.filterInfo["filt_description"])
		# self.optionsLayout.addWidget(self.filtCheckBox, 1, 0, 1, 2)
		# self.filtCheckBox.setMinimumWidth(120)
		# self.filtCheckBox.setChecked(True)

		# We add a stretch that will fill any extra space on the right-most column
		self.optionsLayout.setColumnStretch(2, 1)

		# We create the control buttons
		self.createButton = QPushButton("Create filter")
		#self.createButton.clicked.connect(self.createClick)
		self.filterTab.addButton(self.createButton)

	def createClick(self):
		""" Adds the new filter to the Summary tab """

		# We take a reading of the current number of filters so that we can determine how many new
		# ones this will create
		egSubset = self.filterTab.project.eg.subsets['All_Samples'][0]
		oldFilters = len(list(self.filterTab.project.eg.data[egSubset].filt.components.keys()))

		#self.filterTab.project.eg.signal_optimiser(self.filterTab.project.eg, analytes="Ca43")

		self.createName("Signal")

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

	def createName(self, name):
		""" We create a more descriptive name to display on the tab """
		self.filterTab.name = name
		self.filterTab.updateName()

	def loadFilter(self, params):

		#self.thresholdEdit.setText(str(params.get("threshold", "")))
		#self.filtCheckBox.setChecked(params.get("filt", True))
		self.createClick()

	def freezeOptions(self):
		"""
		We lock the option fields after the filter has been created so that they will give a representation
		of the details of the filter
		"""
		#self.thresholdEdit.setEnabled(False)
		#self.filtCheckBox.setEnabled(False)
		pass