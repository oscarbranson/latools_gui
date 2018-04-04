######################################
Program Dependencies
######################################

For those wanting to further develop upon the existing code structure for the LAtools GUI, the project depends
on a small handful of packages which are required for anything to run. These are detailed below:


PyQt5
======================================

PyQt5 is a set of Python bindings for the Qt application framework. It forms the basis for the graphical interface
structure of the program.

Through pip:
    pip install PyQt5

`PyQt5 Installation Guide <https://www.riverbankcomputing.com/software/pyqt/download5>`_


SIP
-------------------------------------

SIP is a tool used for creating Python bindings for C and C++ libraries, and was originally developed to
create PyQt. PyQt is dependent on SIP and requires it be installed before anything can be built. If you install
PyQt through pip it will automatically include SIP within the installation, 0therwise SIP can be installed manually.

Through pip:
    pip install SIP

`SIP Installation Guide <https://www.riverbankcomputing.com/software/sip/download>`_


PyQt Graph
======================================

PyQt Graph is a graphics and GUI library built on PyQt and numpy, which extends their functionality to allow
fast graph displays, primarily for  mathematics / scientific / engineering applications.

Through pip:
    pip install pyqtgraph

`PyQt Graph Installation Guide <http://www.pyqtgraph.org/>`_


LAtools
==========================================

LAtools is the base set of tools which LAtools GUI packages for easy use by standard users.

Through pip:
    pip install latools

`LAtools Repository <https://github.com/oscarbranson/latools>`_
