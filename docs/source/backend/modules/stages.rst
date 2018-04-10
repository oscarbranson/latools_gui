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
remove a stage, its instantiation in the initUI method of MainWindow should be removed, and it should not be
established in the establishStages method. Lastly it should be removed from the list of stages at the top of
the latoolsgui module.


Addition
====================================

If the existing stages are not enough, new ones can be added following the same design. A stage should have a
class defined within a separate module which the MainWindow in latoolsgui instantiates in its initUI method. The stage
should also be established within the establishStages method of MainWindow, using the same format as the others.
Lastly the stage should be added to the list of stages at the top of the latoolsgui module.



Stages
===================================

.. toctree::
   :glob:
   :maxdepth: 1

   ./stage_documents/*