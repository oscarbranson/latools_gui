""" This the test suite for the converter. It will attempt to convert all csv and txt files in the data_examples
	directory, and then import them each into an instance of latools.
	You can run these tests from the latools_gui directory with the command:
	python -m unittest tests.test_converterWindow
"""

import os
import unittest
import templates.converterWindow as converterWindow
from PyQt5.QtWidgets import *
import latools as la

class TestConverterWindow(unittest.TestCase):

	def test_main(self):
		testDataDir = os.path.join(os.path.dirname(__file__), "data_examples")

		# You must start a QApplication to run a QWidget (used for the converterWindow)
		app = QApplication([])
		window = converterWindow.ConverterWindow()

		file_list = os.listdir(testDataDir)
		convert_list = []
		index_count = "test_file"

		for file in file_list:
			if file[-4:] == ".csv" or file[-4:] == ".txt":
				convert_list.append(file)

		# We load the  export folder into the converterWindow
		window.exportLocationLine.setText(os.path.join(testDataDir, "latools_formatted"))

		# We set the window to say yes to the first question asked
		window.questionResult = "Yes"

		for inFile in convert_list:

			# We load the file and it's new name into the window
			window.fileLocationLine.setText(os.path.join(testDataDir, inFile))
			window.nameEdit.setText(str(index_count))

			window.runConverter()
			window.yesClicked()

			la.analyse(data_folder=os.path.join(testDataDir, "latools_formatted"),
					   config="DEFAULT",
					   extension=".csv",
					   srm_identifier="STD")

		return

if __name__ == '__main__':
	unittest.main()
