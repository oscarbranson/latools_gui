#############################
Packaging
#############################

LAtools GUI is packaged into an executable file using the third-party program PyInstaller. This allows distribution
of the program to users without a native Python installation.

PyInstaller can be installed through pip and has comprehensive documentation available online.

Building the Package
=============================

The step by step procedure for building an executable file for LAtools GUI is as follows:

  1. Open up a console terminal which you can run Python commands from.
  2. In that terminal, navigate to "latools_gui/latools_gui" in your local copy of the program repository.
  3. With PyInstaller installed, run the following command:
::

    pyinstaller --onedir latoolsgui.SPEC

This will create a new folder at "latools_gui/latools_gui/dist" called "latoolsgui". This folder contains an executable
file "latoolsgui.exe" at the top level, as well as all the necessary files to run the executable without a native
Python installation. When distributing to users, this whole folder should be compressed and then delivered.

This command also creates a directory called "build" which stores information about the built executable. This folder
is not necessary for distribution to users. Its purpose is to make rebuilding the executable more efficient.


The SPEC File
=============================

The SPEC file, latoolsgui.SPEC, located in the directory "latools_gui/latools_gui" is called when running
PyInstaller and describes additional information the build might need. There are two main sections to this file
which a developer may find important when working on LAtools GUI.

**Extra Datas**

Extra datas is defined as a list of tuples "extra_datas=[()]" which is passed through the PyInstaller methods. The first
value of each tuple in the list is a file location, in relation to where PyInstaller is being called from. The second
value of each tuple is a new file location which will be created in the newly built directory for the executable. Any
files described in the directory of the first tuple value will be copied and placed in the directory which is created by
the second tuple value.

This is important because while PyInstaller is able to recognise various Python module dependencies and bundle the
appropriate files, it is unable to detect which non-Python files are necessary. If LAtools GUI is dependent on a
non-Python file, for example graphics or text files, that file should be included in the extra datas list, and any
calls to the file should work whether the program is running from an executable or not.

**Hidden Imports**

PyInstaller is not necessarily able to detect all the module dependencies for a given program so it is sometimes
required to manually import these modules. Hidden imports is a list of strings "hiddenimports=['']" which describe
various modules that need to be manually included in the build.


Mac OS Specific Instructions
============================
The Mac OS build of LAtools GUI stumbles on a Python module called Jedi. As of the writing of this documentation the
PyInstaller hook for Jedi is not installed by default.


LAtools Config and Resource Files
============================
The original LAtools module makes use of config and resource files which are necessary for the program to run, but
which PyInstaller does not immediately recognise and package. The fix for this is that the file "latools/latools.cfg"
and the whole folder "latools/resources" are cloned in the LAtools GUI repository under the directory
"latools_gui/latools", and a pointer in the SPEC file directs PyInstaller to include them.

Should any changes be made to "latools/latools.cfg" or the files in "latools/resources", then their copies in the
LAtools GUI repository should be updated as well.


Common Issues
=============================

Any developer working on LAtools GUI and who wishes to package the program may run into various issues. Some of the
most common issues that were encountered while working on packaging the program have been described below.


**Module Not Found Error**

A module not found error will cause an executable that has already been built and run to prematurely crash before
any of the main processes can be run. It will appear briefly in the console and will have the form::

    ModuleNotFoundError: No module named 'module.name'

This error can be solved by copying the given module name into the list of hidden imports in the SPEC file. If this does
not fix the issue, a more detailed hook may need to be created for the specific module as part of PyInstaller.

After adding new imports to the SPEC file, it may be necessary to delete the previous build files before running
PyInstaller again.


**File Path Errors**

Because PyInstaller packages an existing program into a completely new directory, some file paths may be thrown askew.
Absolute path directories are agnostic of this change and should be used as often as possible to avoid issues.