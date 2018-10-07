""" A filter that Identifies the longest possible contiguous data region in the signal where the relative
standard deviation (std) and concentration of all analytes is minimised.  """

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

import logging

class SignalFilter:
	"""
	The options and controls for creating a signal optimiser filter within a filterTab
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

		# We make a scrollable area to house the list of analyte checkboxes
		self.analytesWidget = QWidget()
		self.scroll = QScrollArea()
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll.setWidgetResizable(True)
		self.scroll.setMinimumWidth(100)
		self.innerWidget = QWidget()
		self.innerWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.analytesLayout = QVBoxLayout(self.innerWidget)
		self.optionsLayout.addWidget(self.scroll, 1, 0, 2, 1)
		self.analytesWidget.scroll = self.scroll
		self.scroll.setWidget(self.innerWidget)

		# We store a list of each checkbox that will be displayed in the scrollable area
		self.analyteList = []

		# We add a label to the top of the scrollable area
		self.analytesLabel = QLabel("<span style=\"color:#779999; font-weight:bold\">" +
									self.filterTab.filterInfo["analyte_label"] + "</span>")
		self.analytesLabel.setToolTip(self.filterTab.filterInfo["analyte_description"])
		self.optionsLayout.addWidget(self.analytesLabel, 0, 0)

		# We create a checkbox for each analyte, add it to out internal list, and to the scrollable area
		for i in range(len(self.filterTab.project.eg.analytes)):
			self.analyteList.append(QCheckBox(str(self.filterTab.project.eg.analytes[i])))
			self.analyteList[-1].setChecked(False)
			self.analytesLayout.addWidget(self.analyteList[-1])
		self.analytesLayout.addStretch(1)

		# We add a tooltip to the whole scrollable area
		self.innerWidget.setToolTip(self.filterTab.filterInfo["analyte_description"])

		# The min_points option
		self.minLabel = QLabel(self.filterTab.filterInfo["min_label"])
		self.minEdit = QLineEdit()
		self.minEdit.setPlaceholderText("int")
		self.minLabel.setToolTip(self.filterTab.filterInfo["min_description"])
		self.minEdit.setToolTip(self.filterTab.filterInfo["min_description"])
		self.optionsLayout.addWidget(self.minLabel, 0, 1)
		self.optionsLayout.addWidget(self.minEdit, 0, 2)

		# The mode of the threshold used
		self.modeLabel = QLabel(self.filterTab.filterInfo["mode_label"])
		self.modeCombo = QComboBox()
		self.modeLabel.setToolTip(self.filterTab.filterInfo["mode_description"])
		self.modeCombo.setToolTip(self.filterTab.filterInfo["mode_description"])

		# We add the different mode options
		self.modes = ["kde_first_max", "mean", "median", "bayes_mvs"]
		for s in self.modes:
			self.modeCombo.addItem(s)
		self.optionsLayout.addWidget(self.modeLabel, 1, 1)
		self.optionsLayout.addWidget(self.modeCombo, 1, 2)

		# The x_bias option
		self.x_biasLabel = QLabel(self.filterTab.filterInfo["x_bias_label"])
		self.x_biasEdit = QLineEdit("1.0")
		self.x_biasEdit.setPlaceholderText("float")
		# self.thresholdEdit.setMaximumWidth(100)
		self.x_biasLabel.setToolTip(self.filterTab.filterInfo["x_bias_description"])
		self.x_biasEdit.setToolTip(self.filterTab.filterInfo["x_bias_description"])
		self.optionsLayout.addWidget(self.x_biasLabel, 2, 1)
		self.optionsLayout.addWidget(self.x_biasEdit, 2, 2)

		# The filt check box
		self.filtCheckBox = QCheckBox(self.filterTab.filterInfo["filt_label"])
		self.filtCheckBox.setToolTip(self.filterTab.filterInfo["filt_description"])
		self.optionsLayout.addWidget(self.filtCheckBox, 0, 3)
		self.filtCheckBox.setMinimumWidth(120)
		self.filtCheckBox.setChecked(True)

		# We add a stretch that will fill any extra space on the right-most column
		self.optionsLayout.setColumnStretch(3, 1)

		# We create the control buttons
		self.createButton = QPushButton("Create filter")
		self.createButton.clicked.connect(self.createClick)
		self.filterTab.addButton(self.createButton)

		self.minEdit.setValidator(QIntValidator())
		self.x_biasEdit.setValidator(QDoubleValidator())
		
		#log
		self.logger = logging.getLogger(__name__)

	def createClick(self):
		""" Adds the new filter to the Summary tab """

		# We record the current tab index so that we know which tab to update the name of
		tabIndex = self.filterTab.tabsArea.currentIndex()

		# We take a reading of the current number of filters so that we can determine how many new
		# ones this will create
		egSubset = self.filterTab.project.eg.subsets['All_Samples'][0]
		oldFilters = len(list(self.filterTab.project.eg.data[egSubset].filt.components.keys()))

		# We create the list of analytes based on the checked boxes
		selectedAnalytes = []
		for i in range(len(self.filterTab.project.eg.analytes)):
			if self.analyteList[i].isChecked():
				selectedAnalytes.append(str(self.filterTab.project.eg.analytes[i]))

		# We make sure the user has selected at least one analyte
		if len(selectedAnalytes) == 0:
			self.raiseError("You must select one or more analytes to apply the signal optimiser filter to.")
			return

		# If there is a min_p value provided we make sure it can be cast to an int
		min_p = 5
		if self.minEdit.text() != "":
			try:
				min_p = int(self.minEdit.text())
			except:
				self.raiseError("The " + self.filterTab.filterInfo["min_label"] + " value must be an integer.")
				return

		# If there is an x_bias value provided we make sure it can be cast to a float
		local_x_bias = 0
		if self.x_biasEdit.text != "":
			try:
				local_x_bias = float(self.x_biasEdit.text())
			except:
				self.raiseError("The " + self.filterTab.filterInfo["x_bias_label"] +
								" value must be a floating point number.")
				return

		# We create the filter
		try:
                        self.filterTab.project.eg.optimise_signal(analytes=selectedAnalytes,
												  min_points=min_p,
												  threshold_mode=self.modeCombo.currentText(),
												  x_bias=local_x_bias,
												  filt=self.filtCheckBox.isChecked())
		except:
			try:    # This has no reference to the latools log currently
					#for l in self.project.eg.log:
					#	self.logger.error(l)
					self.logger.error('Attempting signal filter with variables: [min_points]:{}\n[threshold_mode]:{}\n[x_bias]:'
								'{}\n[filt]:{}\n'.format( min_p,
									self.modeCombo.currentText(),
									local_x_bias,
									self.filtCheckBox.isChecked()))
			except:
				self.logger.exception('Failed to log history:')
			finally:
				self.logger.exception('Exception creating filter:')
			return
		# We update the name of the tab with the filter details
		self.createName(tabIndex, "Signal optimiser", str(selectedAnalytes))

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

	def createName(self, tabIndex, name, analytes):
		""" We create a more descriptive name to display on the tab """
		self.filterTab.name = name + " " + analytes
		self.filterTab.updateName(tabIndex)

	def loadFilter(self, params):
		""" When loading an lalog file, the parameters of this filter are added to the gui, then the
			create button function is called.

			Parameters
			----------
			params : dict
				The key-word arguments of the filter call, saved in the lalog file.
		"""

		# We first take all of the analyte names that were included in the save file's analyte list
		# and put them in a set
		analytes = set()
		for a in params.get("analytes", []):
			analytes.add(str(a))

		# For all of the analytes in our list, if the name is in the set, we check its checkbox
		for i in range(len(self.filterTab.project.eg.analytes)):
			if str(self.filterTab.project.eg.analytes[i]) in analytes:
				self.analyteList[i].setChecked(True)

		# We load the rest of the parameters form the save file
		self.minEdit.setText(str(params.get("min_points", "")))
		self.modeCombo.setCurrentText(params.get("threshold_mode", "kde_first_max"))
		self.x_biasEdit.setText(str(params.get("x_bias", "")))
		self.filtCheckBox.setChecked(params.get("filt", True))

		# We act as though the user has added these options and clicked the create button.
		self.createClick()

	def freezeOptions(self):
		"""
		We lock the option fields after the filter has been created so that they will give a representation
		of the details of the filter
		"""
		for box in self.analyteList:
			box.setEnabled(False)
		self.minEdit.setEnabled(False)
		self.modeCombo.setEnabled(False)
		self.x_biasEdit.setEnabled(False)
		self.filtCheckBox.setEnabled(False)
		self.createButton.setEnabled(False)

	def updateOptions(self):
		""" Delivers the current state of each option to the plot pane. """

		analytes = []
		for box in self.analyteList:
			if box.isChecked():
				analytes.append(box.text())

		return {
			"analytes": analytes,
			"min": self.minEdit.text(),
			"mode": self.modeCombo.currentText(),
			"x_bias": self.x_biasEdit.text(),
			"filt": self.filtCheckBox.isChecked()
		}
