import os
import time
import json

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

        def saveProject(self, path = None):
                """ The call which saves stored data to a file

		Saves the project state,
		path defaults to own folder.
		Chose to use json.

		Parameters
		----------
		path : str
			The path which points to where the file shall save.
			Its declaration's place might yet be changed.
			Non-default value best supplied in call.
		"""

                if path is None:
                        path = 'projects/default.sav'
                if not os.path.isdir(path):
                       os.mkdir(path)

                header = ['# Sample save file for testing purposes created %s\n' % (time.strftime('%Y:%m:%d %H:%M:%S)'))]
                

                with open(path + name + '.sav', 'w') as f:
                        f.write('\n'.join(header))
                        json.dump(self.dataDictionary, f)
                        f.close()

        def loadProject(self, path = None):
                """ The call which loads stored data from a file

		To recall data from an outside file,
		call method hence and supply path to file.
		A choice was made to favour json's use.

		Parameters
		----------
		path : str
			The path which points to where the file is laid.
			Its declaration's place might yet be changed.
                        Has default value only fit for tests.
		"""

                if path is None:
                        path = 'projects/default.sav'

                with open(path + name + '.sav', 'r') as f:
                        print (f.readline())
                        self.dataDictionary = json.load(f)
                        f.close()
                        

