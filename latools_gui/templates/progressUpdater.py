
class ProgressUpdater:

	def __init__(self, progressBar):

		self.total = None
		self.desc = None
		self.value = 0
		self.progressBar = progressBar

	def set(self, total, desc):
		self.total = total
		self.desc = desc
		# QProgressBar works off the difference between a min and max
		self.progressBar.setMinimum(1)
		self.progressBar.setMaximum(total)

	def update(self):
		self.value += 1
		if self.value <= self.total:
			self.progressBar.setValue(self.value)

	def reset(self):
		self.progressBar.reset()
		self.value = 0