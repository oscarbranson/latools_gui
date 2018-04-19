import os
import time
import json
import latools
import re

class RunningProject():
	"""
	This class is intended to house everything that is specific to one project.
	When a project is created or loaded, this class is what is created or loaded.
	The instance of this class is passed to each stage.
	Currently it just contains a class variable which is later assigned as the la.analyse object.
	"""

	
	def __init__(self):
		""" Initialise a blank unaltered state.

		Creates tabula rasa project state.

		Attributes
		----------
		dataDictionary : dict
			A dictionary meant to store var pairs.
			Defined by calls from outside stages' needs.
		"""
		
		self.eg = None
		self.dataDictionary = {}

	def updateSetting (self, key, value):
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

	#def massUpdate(self, path):
		
		
					   

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

			print ('key found, value: ' + self.dataDictionary[key])
			return self.dataDictionary[key]
		else:
			print ('key not found')
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

		if path is None:
			path = 'data_export/minimal_export/'
			#path = 'exp/'
		if os.path.isdir(path):
			with open(path + name, 'r') as f:
				rlog = f.readlines()
			hashind = [i for i, n in enumerate(rlog) if '#' in n]
			self.dataDictionary = {}
			#print (i)
			logread = re.compile('([a-z_]+) :: args=(\(.*\)) kwargs=(\{.*\})')
			
			#a = eval(logread.match(log[hashind[1] + 1]).groups()[-1])
			for l in rlog[hashind[1] + 2:]:
				fname, args, kwargs = logread.match(l).groups()
				self.dataDictionary.update(**eval(kwargs))
					
			#print (a)
			#self.dataDictionary = a
			#print (self.dataDictionary)
			print ('loading done')
		else:
			print ("git rekt")  #not a formal error message

#a = RunningProject()
#a.loadProject()
#print (a.readSetting('exponent'))
