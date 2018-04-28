""" This module needs a top level docstring.

"""

import os
import time
import json
import latools as la
import datetime
import re


class RunningProject():
	""" This class is intended to house everything that is specific to one project.

	When a project is created or loaded, this class is what is created or loaded.
	The instance of this class is passed to each stage.
	Currently it just contains a class variable which is later assigned as the la.analyse object.

	Attributes
	----------
		dataDictionary : dict
			A dictionary meant to store var pairs.
			Defined by calls from outside stages' needs.
	"""

	def __init__(self):
		""" Initialise a blank unaltered state.

		Creates tabula rasa project state.
		"""
		self.eg = None
		self.dataDictionary = {}
		self.folder = None
		self.filePath = None
		self.fileName = None
		self.loadStageIndex = 0

		self.fileStrings = None
		self.importListener = None


	def updateSetting(self, key, value):
		""" The call to update variables stored within

		To change or add new data to be saved,
		this method should be called upon in prime.

		Parameters
		----------
		key : str
			The name which points to data writ anon
		value
			What data to be locked under such key                
		"""

		self.dataDictionary[key] = value

	def readSetting(self, key):
		""" Recall the variables stored within the dict

		To read and query data saved before
		this method's call returns a value stored.

		Parameters
		----------
		key : str
			The name which points to data stored anon  
		Returns
		-------
		value : None or dict value
			The value locked with given key,
			gives None when probes an empty memory.
		"""

		if key in self.dataDictionary:

			return self.dataDictionary[key]
		else:
			return None

	def saveProject(self, path = None, name = 'default.sav'):
		""" The call which saves stored data to a file

		Saves the project dict
		Deprecated, using logs
		Ignore this function.

		Parameters
		----------
		path : str
			The path which points to where the file shall save.
			Its declaration's place might yet be changed.
			Non-default value best supplied in call.
		"""

		if path is None:
			path = 'projects/'
		if not os.path.isdir(path):
			os.mkdir(path)

		header = ['# Sample save file for testing purposes created %s\n' % (time.strftime('%Y:%m:%d %H:%M:%S)'))]

		with open(path + name, 'w') as f:
			f.write('\n'.join(header))
			json.dump(self.dataDictionary, f)
			f.close()

	def loadProject(self, path = None, name = 'analysis.log'):
		""" The call which loads stored data from a file

		Loads the log data
		Translates inbuilt logs to dict
		No more fool json.

		Parameters
		----------
		path : str
			Path to where file is
			Leads to its directory.
			Default not advised.
		name : str
			Name of loaded file
			Points to established format
			Should leave as default?
		"""

		if path is None: #these are for testing don't mind them
			path = 'data_export/minimal_export/'
			#path = 'exp/'
		if os.path.isdir(path):
			with open(path + name, 'r') as f:
				rlog = f.readlines()
			hashind = [i for i, n in enumerate(rlog) if '#' in n]
			self.dataDictionary = {}
			#"borrowed" from oscar's code
			logread = re.compile('([a-z_]+) :: args=(\(.*\)) kwargs=(\{.*\})')
			
			for l in rlog[hashind[1] + 2:]:
				fname, args, kwargs = logread.match(l).groups()
				temp = {} #could be optimised.
				temp.update(**eval(kwargs))
				for key, value in temp.items():
					self.dataDictionary[fname+'.'+key] = value
					

			print ('loading done')
		else:
			print ('file not found')  

	def saveButton(self):

		file = open(self.filePath, "w")
		for line in self.fileStrings:
			file.write(line + "\n")
		file.close()
		#print(self.fileName + " saved")
		#self.eg.minimal_export()

	def newFile(self, name, location):
		self.fileName = name
		self.folder = location
		self.filePath = location + "/" + name + ".sav"

		writeFile = open(self.filePath, "w")
		now = datetime.datetime.now()
		nowString = "LAtools save file. Created " + now.strftime("%Y-%m-%d %H:%M")
		writeFile.write(nowString + "\n\n\n\n\n\n\n\n\n\n")
		writeFile.close()

		self.fileStrings = [nowString, "", "", "", "", "", "", "", "", "", ""]


	def loadFile(self, name, location):

		self.fileName = name
		self.folder = location
		self.filePath = location + "/" + name + ".sav"

		file = open(self.filePath, "r")
		self.fileStrings = file.read().splitlines()

		for i in range(2,9):
			if self.fileStrings[i] != "":
				self.importListener.loadStage(i - 2)
			else:
				self.importListener.setStageIndex(i - 2)
				return

		# self.eg = la.reproduce(location + name + ".log")

	def getLoadStageIndex(self):
		return self.loadStageIndex

	def runStage(self, index, parameters):
		self.fileStrings[index + 2] = parameters

	def setImportListener(self, importListener):
		self.importListener = importListener

	def getStageString(self, index):
		return self.fileStrings[index + 2]