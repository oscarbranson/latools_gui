##############
What you need to know to passably use Sphinx
##############

Browsing our Sphinx Documents
==============

You don’t need to have Sphinx installed to browse the documents. They can be found in “latools_gui/docs/build/html”, where index.html is the main content navigation page. (If you're reading this here though, I assume you already know that)


Installing Sphinx
===============

Installing Sphinx is just a straight forward terminal command depending on your operating system.

`Sphinx Official Installation Guide <http://www.sphinx-doc.org/en/master/usage/installation.html>`_


Installing "Read the Docs" Theme
=================

Our Sphinx documents use the “Read the Docs” theme which needs to be installed separately if you intend to update and build the docs.

Through Anaconda Prompt::

    >pip install sphinx_rtd_theme

`The RTD git repository <https://github.com/rtfd/sphinx_rtd_theme>`_

Running the Build
=================

Any time you update the rst files for the Sphinx documentation and want to see them propagate to the html files, you will need to run the build.

In general, you should build the Sphinx documents by running the following make.bat file from the “latools_gui\docs path” directory in the terminal::

    >make html

This generates all the documents from the source file in the “build\html” directory.
