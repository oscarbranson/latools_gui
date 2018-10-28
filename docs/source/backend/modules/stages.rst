####################################
Stages
####################################

Each step of the LAtools process is represented graphically by a stage, which houses the tool interface for manipulating
the sample data at that point. Each stage is displayed between the navigation bar and graph pane at the top of the
program interface.


Structure
====================================

In the program, a stage is a QWidget, which is stored on a QStackedWidget called stagesStack that displays only one
stage at a time. These stages can be toggled through by incrementing the stack index of stagesStack, and they all
use a QVBoxLayout. The behaviour of each stage is defined within a class which the MainWindow of latoolsgui creates
and instance of in its initUI method.


Modification
====================================

Stages can be modified within their respective modules and have minimal impact on the rest of the program
outside of the data manipulations they perform on the main data. The layout, design, and options available within
each stage can all be modified within their respective __init__ method.

Stages can be removed, though this is done at the cost of losing key functionality within the LAtools process. To
remove a stage, follow the steps below for adding a stage but instead delete the code relevant to the stage being
removed.


Addition
====================================

If the existing stages are not enough, new ones can be added following the same design.

Stages are defined as a class within a separate module which the MainWindow in latoolsgui instantiates. These stage
modules are located in the "latools_gui/stages" folder. The layout and design of the stage should be defined within
this class but otherwise the contents are free to be customised.

Once a stage is defined, it must be instatiated and attached to the program. This is handled first in the MainWindow
class in the file "latools_gui/latoolsgui.py". The steps within the initUI method should be replicated for the new class,
following the design of the existing stages. The title of the new stage should also be added to the list of stage names,
STAGES, at the top of this file. Still within this same file is the class ImportListener which handles the passing of
information between modules during runtime. Steps that are taken for the existing stages within this class should be
replicated for the new stage.

Within progressPane.py, accomodations should be made per the existing code if this new stage is a focus stage and if
it will be using the progress pane. Lastly, within stageTabs.py you may want to make additions or changes to account
for how this new stage affects the linear analysis process (i.e. if it is optional or not).

Stages List
===================================

.. toctree::
   :glob:
   :maxdepth: 1

   ./stage_documents/*