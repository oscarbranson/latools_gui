""" A filter for clustering elements """

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

import logging

class ClusteringFilter:
	"""
	The options and controls for creating a clustering filter within a filterTab
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

		# The filt check box
		self.filtCheckBox = QCheckBox(self.filterTab.filterInfo["filt_label"])
		self.filtCheckBox.setToolTip(self.filterTab.filterInfo["filt_description"])
		self.optionsLayout.addWidget(self.filtCheckBox, 0, 3)
		self.filtCheckBox.setMinimumWidth(120)

		# The method of clustering algorithm used
		self.methodLabel = QLabel(self.filterTab.filterInfo["method_label"])
		self.methodCombo = QComboBox()
		self.methodLabel.setToolTip(self.filterTab.filterInfo["method_description"])
		self.methodCombo.setToolTip(self.filterTab.filterInfo["method_description"])
		self.methods = ["meanshift", "kmeans"]
		for s in self.methods:
			self.methodCombo.addItem(s)
		self.optionsLayout.addWidget(self.methodLabel, 0, 1)
		self.optionsLayout.addWidget(self.methodCombo, 0, 2)
		self.methodCombo.activated.connect(self.methodUpdate)

		# The normalise check box
		self.normaliseCheckBox = QCheckBox(self.filterTab.filterInfo["normalise_label"])
		self.normaliseCheckBox.setToolTip(self.filterTab.filterInfo["normalise_description"])
		self.optionsLayout.addWidget(self.normaliseCheckBox, 1, 3)
		self.normaliseCheckBox.setChecked(True)

		# The time check box
		self.timeCheckBox = QCheckBox(self.filterTab.filterInfo["time_label"])
		self.timeCheckBox.setToolTip(self.filterTab.filterInfo["time_description"])
		self.optionsLayout.addWidget(self.timeCheckBox, 2, 3)

		# The sort check box
		self.sortCheckBox = QCheckBox(self.filterTab.filterInfo["sort_label"])
		self.sortCheckBox.setToolTip(self.filterTab.filterInfo["sort_description"])
		self.optionsLayout.addWidget(self.sortCheckBox, 0, 4)
		self.sortCheckBox.setChecked(True)

		# The minimum data points option
		self.minLabel = QLabel(self.filterTab.filterInfo["min_label"])
		self.minEdit = QLineEdit()
		self.minEdit.setPlaceholderText("int")
		self.minEdit.setMaximumWidth(100)
		self.minLabel.setToolTip(self.filterTab.filterInfo["min_description"])
		self.minEdit.setToolTip(self.filterTab.filterInfo["min_description"])
		self.optionsLayout.addWidget(self.minLabel, 1, 1)
		self.optionsLayout.addWidget(self.minEdit, 1, 2)

		# The number of clusters option
		self.n_clustersLabel = QLabel(self.filterTab.filterInfo["n_clusters_label"])
		self.n_clustersEdit = QLineEdit()
		self.n_clustersEdit.setPlaceholderText("int")
		self.n_clustersEdit.setMaximumWidth(100)
		self.n_clustersLabel.setToolTip(self.filterTab.filterInfo["n_clusters_description"])
		self.n_clustersEdit.setToolTip(self.filterTab.filterInfo["n_clusters_description"])
		self.optionsLayout.addWidget(self.n_clustersLabel, 2, 1)
		self.optionsLayout.addWidget(self.n_clustersEdit, 2, 2)
		self.n_clustersEdit.setEnabled(False)

		# We add a stretch that will fill any extra space on the right-most column
		self.optionsLayout.setColumnStretch(5, 1)
		self.optionsLayout.setRowStretch(2, 1)

		# We create the control buttons
		self.createButton = QPushButton("Create filter")
		self.createButton.clicked.connect(self.createClick)
		self.filterTab.addButton(self.createButton)

		self.minEdit.setValidator(QIntValidator())
		self.n_clustersEdit.setValidator(QIntValidator())
		
		#log
		self.logger = logging.getLogger(__name__)

	def methodUpdate(self):
		""" Enables or disables options based on which method option is currently selected """
		if self.methodCombo.currentText() == "meanshift":
			self.n_clustersEdit.setEnabled(False)
		elif self.methodCombo.currentText() == "kmeans":
			self.n_clustersEdit.setEnabled(True)

	def createClick(self):
		""" Adds the new filter to the Summary tab """

		# We record the current tab index so that we know which tab to update the name of
		tabIndex = self.filterTab.tabsArea.currentIndex()

		# We take a reading of the current number of filters so that we can determine how many new
		# ones this will create
		egSubset = self.filterTab.project.eg.subsets['All_Samples'][0]
		oldFilters = len(list(self.filterTab.project.eg.data[egSubset].filt.components.keys()))

		# The selected analyte checkboxes are added to a list of analytes
		selectedAnalytes = []
		for i in range(len(self.filterTab.project.eg.analytes)):
			if self.analyteList[i].isChecked():
				selectedAnalytes.append(str(self.filterTab.project.eg.analytes[i]))

		# If no analytes have been selected we raise an error
		if len(selectedAnalytes) == 0:
			self.raiseError("You must select one or more analytes to apply the signal optimiser filter to.")
			return

		# We cast the contents of the min field to an int. If there are problems we raise an error.
		try:
			min = int(self.minEdit.text())
		except:
			self.raiseError("The " + self.filterTab.filterInfo["min_label"] + " value must be an integer")
			return

		# Different parameters are needed for the different method options.
		if self.methodCombo.currentText() == "meanshift":
			# We create the filter using the meanshift option
			try:
				self.filterTab.project.eg.filter_clustering(analytes = selectedAnalytes,
														filt = self.filtCheckBox.isChecked(),
														normalise = self.normaliseCheckBox.isChecked(),
														method = self.methodCombo.currentText(),
														include_time = self.timeCheckBox.isChecked(),
														sort = self.sortCheckBox.isChecked(),
														min_data = min)
			except:
				try:
					#for l in self.project.eg.log:
					#	self.logger.error(l)
					self.logger.error('Attempting meanshift clustering filter with variables: [filt]:{}\n[normalise]:{}\n[method]:'
								'{}\n[include_time]:{}\n[sort]:{}\n[min_data]:{}\n'.format( self.filtCheckBox.isChecked(),
									self.normaliseCheckBox.isChecked(),
									self.methodCombo.currentText(),
									self.timeCheckBox.isChecked(),
									self.sortCheckBox.isChecked(),
									min))
				except:
					self.logger.exception('Failed to log history:')
				finally:
					self.logger.exception('Exception creating filter:')
					self.raiseError("An error occurred while trying to create this filter. <br> There may be a problem with " +
								"the input values.")
				return

		elif self.methodCombo.currentText() == "kmeans":
			# We create the filter using the kmeans option

			# For the kmeans option we need the contents of the n_clusters field to be an int
			try:
				n_clust = int(self.n_clustersEdit.text())
			except:
				self.raiseError("The " + self.filterTab.filterInfo["n_clusters_label"] + " value must be an integer")
				return

			# We create the filter
			try:
				self.filterTab.project.eg.filter_clustering(analytes = selectedAnalytes,
														filt = self.filtCheckBox.isChecked(),
														normalise = self.normaliseCheckBox.isChecked(),
														method = self.methodCombo.currentText(),
														include_time = self.timeCheckBox.isChecked(),
														sort = self.sortCheckBox.isChecked(),
														min_data = min,
														n_clusters = n_clust)
			except:
				try:
						      
					#for l in self.project.eg.log:
					#	self.logger.error(l)
					self.logger.error('Attempting kmeans clustering filter with variables: [filt]:{}\n[normalise]:{}\n[method]:'
								'{}\n[include_time]:{}\n[sort]:{}\n[min_data]:{}\n[n_clust]:[]\n'.format( self.filtCheckBox.isChecked(),
									self.normaliseCheckBox.isChecked(),
									self.methodCombo.currentText(),
									self.timeCheckBox.isChecked(),
									self.sortCheckBox.isChecked(),
									min,
									n_clust))
				except:
					self.logger.exception('Failed to log history:')
				finally:
						      
					self.logger.exception('Exception creating filter:')
					self.raiseError("An error occurred while trying to create this filter. <br> There may be a problem with " +
								"the input values.")
				return

		# We set the name of the tab based on the filter options
		self.createName(tabIndex, "Clustering", self.methodCombo.currentText(), str(selectedAnalytes))

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

	def createName(self, tabIndex, name, method, analyte):
		""" We create a more descriptive name to display on the tab """
		self.filterTab.name = name + " " + method + " " + analyte
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

		# For the args in params, we update each filter option, using the default value if the argument is not in the dict.
		self.filtCheckBox.setChecked(params.get("filt", True))
		self.methodCombo.setCurrentIndex(self.methodCombo.findText(params.get("method", "meanshift")))
		self.normaliseCheckBox.setChecked(params.get("normalise", True))
		self.timeCheckBox.setChecked(params.get("include_time", True))
		self.sortCheckBox.setChecked(params.get("sort", True))
		self.minEdit.setText(str(params.get("min_data", "")))
		self.n_clustersEdit.setText(str(params.get("n_clusters", "")))

		# We act as though the user has added these options and clicked the create button.
		self.createClick()

	def freezeOptions(self):
		"""
		We lock the option fields after the filter has been created so that they will give a representation
		of the details of the filter
		"""

		for box in self.analyteList:
			box.setEnabled(False)
		self.filtCheckBox.setEnabled(False)
		self.methodCombo.setEnabled(False)
		self.normaliseCheckBox.setEnabled(False)
		self.timeCheckBox.setEnabled(False)
		self.sortCheckBox.setEnabled(False)
		self.minEdit.setEnabled(False)
		self.n_clustersEdit.setEnabled(False)
		self.createButton.setEnabled(False)

	def updateOptions(self):
		""" Delivers the current state of each option to the plot pane. """

		# We put all checked analytes into a list
		analytes = []
		for box in self.analyteList:
			if box.isChecked():
				analytes.append(box.text())

		# A dict is returned of the keyword arguments and their current values
		return {
			"analytes": analytes,
			"filt": self.filtCheckBox.isChecked(),
			"method": self.methodCombo.currentText(),
			"normalise": self.normaliseCheckBox.isChecked(),
			"time": self.timeCheckBox.isChecked(),
			"sort": self.sortCheckBox.isChecked(),
			"min": self.minEdit.text(),
			"n_clusters": self.n_clustersEdit.text()
		}
