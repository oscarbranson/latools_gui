Data Import
***********

You are now ready to start your analysis session! In this step, you will be loading your sample and standards data, choosing a configuration, stating your standards identifier and specifying the file extension of your  data files.

.. to do: need to add trouble shooting links and advice for each section; need to create a page for configuration when our program can do it;


.. warning:: **Have you configured LAtools?** Different LA-ICPMS system produce different results in a variety of data formats. Before you begin to analyse your data, you will need to configure LAtools to your instrument and SRMs. If this is your first time using LAtools, or you are using data from a LA-ICPMS machine that you have not configured, click here.

.. http://latools.readthedocs.io/en/latest/users/configuration/howto.html, http://latools.readthedocs.io/en/latest/users/configuration/data-formats.html#data-formats
.. need to create a new page for configuring latools


Selecting your data
===================
To start your analysis session, you will need to load your data. Do this by clicking :guilabel:`&Browse`. This will open your computers file explorer. Navigate to the folder containing all the data - your samples and standards - that you will be using in your project and select it.

[image/gif here]

.. Why am I getting errors when I load my data?


Configurating LAtools
=====================
A configuration stores information about the way your data is formatted, and what SRMs table is to be used in your analysis session. .. one srm table or more?



If you have not configured your


.. list what they are

.. How to create a configuration


.. do we need to select an internal standard ?? or is it always ca43 ?


Selecting a SRM identifier
=============================================

The SRM identifier is required to help the program separate your sample files and standard files. It may help to set up all your files as suggested in this link.
    .. need to create a page about how users should set up their files

The value for this parameter is defaulted to "STD". This means that all the standard files in your folder contain the string "STD" in their file name. If you do not have a unique identifier in your standards file names, you will need to change this. Do this by opening your project folder, and rename your standards files so they include the string "STD", or some other identifier. If you have identified your standards files, enter your identifier in the :guilabel:`&SRM Identifier` dialogue box.

.. probs need to tell the user where there files are moved/copy to after import?

.. link to http://latools.readthedocs.io/en/latest/users/configuration/srm-file.html#srm-file







Data extention
==============
Lastly, you will need to specify the extension type of the files you are using. This parameter is defaulted to **.csv**. If you are using files of another kind, e.g. --------, then you will need to type them into the :guilabel:`&n_min` dialogue box.


Start plotting!
===============

Once you have loaded your data, configured LAtools, and chosen your SRMs, you can now start plotting! To plot your data, click :guilabel:`&apply`. Your data plots should be visible in the plotting panel.


Navigating the plotting panel
==============================

.. will talk about what the grpah is actually showing and what the axes mean
.. talk about log graphing option


You can view each sample by selecting it in the samples panel.

[image/gif here]

You can toggle elements on and off by deselecting and reselected them in the elements panel.

[image/gif here]

You can zoom the graph in and out by scrolling your mouse over the graph. You can also drag the graph around by clicking on the graph and dragging around.

[image/gif here]

To reset the graph, simply click :guilabel:`&Reset`