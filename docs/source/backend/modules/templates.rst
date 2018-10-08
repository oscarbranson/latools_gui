####################################
Templates
####################################

The term, template, describes various graphical objects which are displayed on the interface. Templates are the
primary building blocks of the graphical interface, and they differ from stages in that each template has a unique
structure and purpose, whereas stages are there solely to house the tools at each step of the LAtools process.


Structure
==================================

In the program, each template is uniquely defined by a class module under "latools_gui/templates". Unlike stages,
templates are not exclusively instatiated within the MainWindow of latoolsgui. Each template is only instantiated once,
and where it is instantiated is dependent on the purpose of that template.


Modification
==================================

The structure of the templates in the LAtools GUI is intrinsically tied to the layout and design of the program
itself. Removing any of the existing templates would have a drastic effect on the program and is not advised as each
one fulfills an integral role in the overall functionality.

Templates can be modified from within their class modules under "latools_gui/templates".


Addition
==================================

The existing package should be complete for most uses, however new sections of the GUI may be added with further
templates if necessary. Templates may be instantiated in whatever section of the program they are needed which
makes it difficult to give instructions for general implementation.

Generally, templates that serve as new screens, such as the titleScreen should likewise be instantiated in the initUI
method of the MainWindow, but should be added to the MainStack. Some form of navigation should also be implemented,
otherwise there are no existing methods to navigate the MainStack farther than the stageScreenLayout.

If the template needs to communicate with modules other than the one it is instantiated in, it should be instantiated
from the MainWindow in the initUI method. It should then be added to the ImportListener class which handles
the passing of information between modules during runtime.


Templates List
==================================

.. toctree::
   :glob:
   :maxdepth: 1

   ./template_documents/*