#################################
Program Structure
#################################

The LAtools GUI program is run from latoolsgui.py which contains the main class MainWindow, which is instantiated
and shown when the program begins. This window consists of a principalLayout which is a QVBoxLayout that houses
a QStackedWidget called the mainStack.

The mainStack is a series of panes which all occupy the same location, however only one is visible at a given
time. The first pane on this stack is the title screen (titleScreenObj), and the second is the stages screen
(stageScreenLayout).

The stageScreenLayout, where the primary functionality of the program lies, is comprised of a number of box
sections which this program refers to as templates. Each template is a unique pane and fills an express purpose
within the layout. The navigationPane fills a thin rectangular section at the top and is used to navigate between
stages within the LAtools process.

Below that is the stagesStack, which is a QStackedWidget of stages, which are each their own QWidget with a QVBoxLayout.
At each stage in the LAtools process, a unique set of tools and operations, used to modify the data, is presented
by the stagesStack. The contents of each stage in the stagesStack is defined by a class in the stages folder. An
object of each stage class is instantiated and passed an established layout of that stage within the stagesStack.

Below the stagesStack is the progressBar, which is not a template but rests above the graphPane. Within the
graphPane, the graphical representation of the data is displayed using PyQtGraph.

Every template and stage object created by the MainWindow is passed requisite information about the rest of
the program as required by design upon creation. This primarily includes pointers to other templates, as well as
a runningProject object, which stores information about the program as a whole.

The runningProject is where the actual data that is being graphed and manipulated is stored. The attribute *eg* is
an instantiation of the *analyse* class within the LATools package which imports the data and contains methods
for manipulating it. Stages within the LATools GUI call the methods of *eg* through the runningProject.