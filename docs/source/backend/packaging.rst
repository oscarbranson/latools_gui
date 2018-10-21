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

    pyinstaller --windowed --onedir latoolsgui.SPEC

It is important to note that PyInstaller creates a package for whichever system it is executed from (i.e. packaging
LAtools GUI on a Windows computer will create a Windows only executable). To create distributables for multiple
operating systems you should repeat these steps on separate computers for each system you wish to deploy to.

This will create a new folder at "latools_gui/latools_gui/dist" called "latoolsgui". This folder contains an executable
file "latoolsgui.exe" at the top level, as well as all the necessary files to run the executable without a native
Python installation. This folder can be compressed and distributed to users as is, however there are system specific
instructions below for creating a more professional distribution package.

This command also creates a directory called "build" which stores information about the built executable. This folder
is not necessary for distribution to users. Its purpose is to make rebuilding the executable more efficient.


Mac OS Specific Instructions
============================

When PyInstaller builds the Mac package, it creates a bundled app alongside the package directory.
This app can be used to run the program as a standalone item, but it is incomplete. By default
PyInstaller does not copy all the necessary content into the bundle, but this can be done manually.
Copy and paste the entire directory of the packaged latoolsgui into the bundle "Contents/MacOS/",
overwriting the existing files in the MacOS directory.

Right click on the bundle, and select "Show package contents" to view the app's contents.

App bundles are conventionally distributed with DMG Disk Installer files, which can be created using the standard
Disk Utility on Mac computers.

1. Open Disk Utility from Applications.
2. Click "New Image" and change the name to "LAtools GUI". Set the size to be as large as the LAtools GUI app bundle and click "Create".
3. Open the new Disk Image.
4. Copy the LAtools GUI app bundle into the Disk Image.
5. Create an Alias of the Applications folder and copy it into the Disk Image next to the app bundle.
6. Close and eject the Disk Image.
7. Right click on the Disk Image and click "Open With -> Disk Utility".
8. Click the "Convert" button and select "Compressed" under "Image Format".
9. Click "Save".

This compressed Disk Image can now be distributed to users who can install LAtools GUI on their Mac computers.
The Disk Image allows users to easily drag the LAtools GUI app bundle into their Applications folder where it can
be quickly launched.


Windows Specific Instructions
=============================

Windows applications are conventionally distributed as .msi files which execute installer wizards. There exist
many third-party applications for converting programs into .msi files, but
`Advanced Installer <https://www.advancedinstaller.com/>`_ is free. Basic instructions for using it in the context of
LAtools GUIwill be outlined below. and the Advanced Installer website has
`abundant documentation <https://www.advancedinstaller.com/user-guide/tutorial-simple.html/>`_ for creating a
simple package which can be customised to your needs.

1. Open Advanced Installer
2. Under New -> Installer -> Generic, select a "Simple" Installer Project
3. Press the "Create Project" button
4. Open the "Product Details" window under "Product Information" from the panel on the left.
5. Fill out the Name, Publisher, and any other relevant fields. Most fields can be left as default.
6. Still under "Product Details", add a "Control Panel icon". The icon used for Windows is in the graphics folder of the repository, "latools_gui\latools_gui\graphics\latools-logo-icon.ico".
7. Open the "Files and Folders" window under "Resources" from the panel on the left.
8. Copy and paste the entire dist directory created by PyInstaller into the "Application Folder". This represents the files that will be installed by the wizard.
9. In the "Application Folder", find the LAtools GUI.exe file and select it by clicking on it, then click on the "New Shortcut" toolbar button. This will open a new dialog for customising the shortcut.
10. In the "New Shortcut" dialog, set the name to "LAtools GUI", tick "Run as Administrator", and set the icon as you did for the "Control Panel icon". Click "OK" and the new shortcut will be added to the "Application Shortcut Folder". It will be installed in the Start menu of the target computer.
11. To create a shortcut on the target computer's desktop, select the "Desktop" folder in the "Folders" tree and click the "New Shortcut" button. A file picker dialog will open up for selecting the target of the shortcut.
12. Select the LATools GUI.exe file in the "Application Folder" and click "OK". A "New Shortcut" dialog will open. Fill it out just as you did for the Start menu shortcut and click "OK".
13. Click on the "Build" toolbar button, select a destination for the build files and wait for the project to build.

Building the Advanced Installer project will create multiple files. The parent directory will contain an Advanced
Installer project which can be reopened with Advanced Installer for modifying the project at later dates. There
will also be a folder named "LAtools GUI-SetupFiles" and within will be a single .msi Windows Installer file.
This file can be sent to any other Windows computer and executed to install LAtools GUI with shortcuts.


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