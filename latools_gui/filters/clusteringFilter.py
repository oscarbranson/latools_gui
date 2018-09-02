""" A filter for clustering elements """

from PyQt5.QtWidgets import *


class ClusteringFilter:
	"""
	Clustering Filter info
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

		# The filt check box
		self.filtCheckBox = QCheckBox(self.filterTab.filterInfo["filt_label"])
		self.filtCheckBox.setToolTip(self.filterTab.filterInfo["filt_description"])
		self.optionsLayout.addWidget(self.filtCheckBox, 0, 2)
		self.filtCheckBox.setMinimumWidth(120)

		# The method of clustering algorithm used
		self.methodLabel = QLabel(self.filterTab.filterInfo["method_label"])
		self.methodCombo = QComboBox()
		self.methodLabel.setToolTip(self.filterTab.filterInfo["method_description"])
		self.methodCombo.setToolTip(self.filterTab.filterInfo["method_description"])
		self.methods = ["meanshift", "kmeans"]
		for s in self.methods:
			self.methodCombo.addItem(s)
		self.optionsLayout.addWidget(self.methodLabel, 1, 0)
		self.optionsLayout.addWidget(self.methodCombo, 1, 1)
		self.methodCombo.activated.connect(self.methodUpdate)

		# The normalise check box
		self.normaliseCheckBox = QCheckBox(self.filterTab.filterInfo["normalise_label"])
		self.normaliseCheckBox.setToolTip(self.filterTab.filterInfo["normalise_description"])
		self.optionsLayout.addWidget(self.normaliseCheckBox, 1, 2)
		self.normaliseCheckBox.setChecked(True)

		# The time check box
		self.timeCheckBox = QCheckBox(self.filterTab.filterInfo["time_label"])
		self.timeCheckBox.setToolTip(self.filterTab.filterInfo["time_description"])
		self.optionsLayout.addWidget(self.timeCheckBox, 0, 3)

		# The sort check box
		self.sortCheckBox = QCheckBox(self.filterTab.filterInfo["sort_label"])
		self.sortCheckBox.setToolTip(self.filterTab.filterInfo["sort_description"])
		self.optionsLayout.addWidget(self.sortCheckBox, 1, 3)
		self.sortCheckBox.setChecked(True)

		# The minimum data points option
		self.minLabel = QLabel(self.filterTab.filterInfo["min_label"])
		self.minEdit = QLineEdit()
		self.minEdit.setPlaceholderText("int")
		self.minEdit.setMaximumWidth(100)
		self.minLabel.setToolTip(self.filterTab.filterInfo["min_description"])
		self.minEdit.setToolTip(self.filterTab.filterInfo["min_description"])
		self.optionsLayout.addWidget(self.minLabel, 2, 0)
		self.optionsLayout.addWidget(self.minEdit, 2, 1)

		# The number of clusters option
		self.n_clustersLabel = QLabel(self.filterTab.filterInfo["n_clusters_label"])
		self.n_clustersEdit = QLineEdit()
		self.n_clustersEdit.setPlaceholderText("int")
		self.n_clustersEdit.setMaximumWidth(100)
		self.n_clustersLabel.setToolTip(self.filterTab.filterInfo["n_clusters_description"])
		self.n_clustersEdit.setToolTip(self.filterTab.filterInfo["n_clusters_description"])
		self.optionsLayout.addWidget(self.n_clustersLabel, 2, 2)
		self.optionsLayout.addWidget(self.n_clustersEdit, 2, 3)
		self.n_clustersEdit.setEnabled(False)

		# We add a stretch that will fill any extra space on the right-most column
		self.optionsLayout.setColumnStretch(4, 1)

		# We create the control buttons
		self.createButton = QPushButton("Create filter")
		self.createButton.clicked.connect(self.createClick)
		self.filterTab.addButton(self.createButton)

	def methodUpdate(self):

		if self.methodCombo.currentText() == "meanshift":
			self.n_clustersEdit.setEnabled(False)
		elif self.methodCombo.currentText() == "kmeans":
			self.n_clustersEdit.setEnabled(True)

	def createClick(self):
		""" Adds the new filter to the Summary tab """

		# We take a reading of the current number of filters so that we can determine how many new
		# ones this will create
		egSubset = self.filterTab.project.eg.subsets['All_Samples'][0]
		oldFilters = len(list(self.filterTab.project.eg.data[egSubset].filt.components.keys()))

		if self.analyteCombo.currentText() == " ":
			self.raiseError("You must select an analyte to apply the filter to")
			return

		try:
			min = int(self.minEdit.text())
		except:
			self.raiseError("The " + self.filterTab.filterInfo["min_label"] + " value must be an integer")
			return

		if self.methodCombo.currentText() == "meanshift":
			try:
				self.filterTab.project.eg.filter_clustering(analytes = self.analyteCombo.currentText(),
														filt = self.filtCheckBox.isChecked(),
														normalise = self.normaliseCheckBox.isChecked(),
														method = self.methodCombo.currentText(),
														include_time = self.timeCheckBox.isChecked(),
														sort = self.sortCheckBox.isChecked(),
														min_data = min)
			except:
				self.raiseError("An error occurred while trying to create this filter. <br> There may be a problem with " +
								"the input values.")
				return

		elif self.methodCombo.currentText() == "kmeans":

			try:
				n_clust = int(self.n_clustersEdit.text())
			except:
				self.raiseError("The " + self.filterTab.filterInfo["n_clusters_label"] + " value must be an integer")
				return

			try:
				self.filterTab.project.eg.filter_clustering(analytes = self.analyteCombo.currentText(),
														filt = self.filtCheckBox.isChecked(),
														normalise = self.normaliseCheckBox.isChecked(),
														method = self.methodCombo.currentText(),
														include_time = self.timeCheckBox.isChecked(),
														sort = self.sortCheckBox.isChecked(),
														min_data = min,
														n_clusters = n_clust)
			except:
				self.raiseError("An error occurred while trying to create this filter. <br> There may be a problem with " +
								"the input values.")
				return


		self.createName("Clustering", self.methodCombo.currentText(), self.analyteCombo.currentText())

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

	def createName(self, name, method, analyte):
		""" We create a more descriptive name to display on the tab """
		self.filterTab.name = name + " " + method + " " + analyte
		self.filterTab.updateName()

	def loadFilter(self, params):

		self.analyteCombo.setCurrentIndex(self.analyteCombo.findText(params.get("analytes", "")))
		self.filtCheckBox.setChecked(params.get("filt", True))
		self.methodCombo.setCurrentIndex(self.methodCombo.findText(params.get("method", "meanshift")))
		self.normaliseCheckBox.setChecked(params.get("normalise", True))
		self.timeCheckBox.setChecked(params.get("include_time", True))
		self.sortCheckBox.setChecked(params.get("sort", True))
		self.minEdit.setText(str(params.get("min_data", "")))
		self.n_clustersEdit.setText(str(params.get("n_clusters", "")))
		self.createClick()

	def freezeOptions(self):
		"""
		We lock the option fields after the filter has been created so that they will give a representation
		of the details of the filter
		"""
		self.analyteCombo.setEnabled(False)
		self.filtCheckBox.setEnabled(False)
		self.methodCombo.setEnabled(False)
		self.normaliseCheckBox.setEnabled(False)
		self.timeCheckBox.setEnabled(False)
		self.sortCheckBox.setEnabled(False)
		self.minEdit.setEnabled(False)
		self.n_clustersEdit.setEnabled(False)