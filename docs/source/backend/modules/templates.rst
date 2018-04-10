####################################
Templates
####################################

The term, template, describes various graphical objects which are displayed on the interface. Templates are the
primary building blocks of the graphical interface, and they differ from stages in that each template has a unique
structure and purpose, whereas stages are solely to house the tools at each step of the LAtools process.


Structure
==================================

In the program, each template is uniquely represented and is incorporated in the MainWindow class within
the latoolsgui module. Primarily their behaviour is defined in classes within separate modules, which the
MainWindow creates instances of. Each template defines its structure in its __init__ method. The structure
of each template can be vastly different, as they are used for different purposes.


Modification
==================================

The structure of the templates in the LAtools GUI is intrinsically tied to the layout and design of the program
itself. Removing any of the existing templates would have a drastic effect on the program and is not advised as each
one fulfills an integral role in the overall functionality.

Modification of existing templates is unique to each one and is detailed on their pages.


Addition
==================================

The existing package should be complete for most uses, however new sections of the GUI may be added with further
templates if necessary. Templates apart of the main process should be instantiated in the initUI method of the
MainWindow and added to the stageScreenLayout.

Templates that serve as new screens, such as the titleScreen should likewise be instantiated in the initUI method
of the MainWindow, but should be added to the MainStack. Some form of navigation should also be implemented,
otherwise there are no existing methods to navigate the MainStack farther than the stageScreenLayout.


Templates
==================================

.. toctree::
   :glob:
   :maxdepth: 1

   ./template_documents/*