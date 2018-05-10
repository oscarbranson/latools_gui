from PyQt5.QtWidgets import *

class ProgressUpdater:

	def __init__(self, progressBar):

		self.total = None
		self.desc = None
		self.value = 0
		self.progressBar = progressBar

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		pass

	def __str__(self):
		return "LAtools GUI progress bar"

	def set(self, total, desc):
		self.total = total
		self.desc = desc
		self.reset()
		# QProgressBar works off the difference between a min and max
		self.progressBar.setMinimum(1)
		self.progressBar.setMaximum(total)
		return self

	def update(self):
		self.value += 1
		if self.value < self.total:
			self.progressBar.setValue(self.value)
		elif self.value == self.total:
			self.reset()
		QApplication.processEvents()

	def reset(self):
		self.progressBar.reset()
		self.value = 0
