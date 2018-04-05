####################################
Stages
####################################

Each step of the LAtools process is represented graphically by a stage, which houses the tool interface for manipulating
the sample data at that point. Each stage is displayed between the navigation bar and graph pane at the top of the
program interface.

In the program, a stage is a QWidget, which is stored on a QStackedWidget called stagesStack that displays only one
stage at a time. These stages can be toggled through by incrementing the stack index of stagesStack, and they all
use a QVBoxLayout.



.. toctree::
   :glob:
   :maxdepth: 1
   :caption: Stages

   ./stage_documents/*