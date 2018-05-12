""" An interface for controlling the GUI progress bar """

from PyQt5.QtWidgets import *

class ProgressUpdater:
	""" Provides an interface that controls the GUI progress bar """

	def __init__(self, progressBar):
		"""
		Lists a progress bar which will be updated when the controlling functions are called.

		Parameters
		----------
		progressBar : QProgressBar
			The qt progress bar which will be updated
		"""
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
		"""
		Defines how many steps will be in this progress bar

		Parameters
		----------
		total : int
			Number of steps
		desc : string
			Description, not used here

		Returns
		----------
		Itself: A progress bar updating interface
		"""
		self.total = total
		self.desc = desc
		self.reset()
		# QProgressBar works off the difference between a min and max
		self.progressBar.setMinimum(1)
		self.progressBar.setMaximum(total)
		return self

	def update(self):
		""" Called for each step of the progress bar. Increments the progress bar by 1 """
		self.value += 1
		if self.value <= self.total:
			self.progressBar.setValue(self.value)
		QApplication.processEvents()

	def reset(self):
		""" Resets the progress bar """
		self.progressBar.reset()
		self.value = 0
