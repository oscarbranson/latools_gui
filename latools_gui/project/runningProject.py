
class RunningProject():
	"""
	This class is intended to house everything that is specific to one project.
	When a project is created or loaded, this class is what is created or loaded.
	The instance of this class is passed to each stage.
	Currently it just contains a class variable which is later assigned as the la.analyse object.
	"""
	def __init__(self):

		self.eg = None
