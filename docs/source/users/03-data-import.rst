Data Import
***********

You are now ready to start the analysis session! In this stage of the analysis, you will:

    - Load your data and standards,
    - Choose or create a configuration,
    - State your standards identifier, and
    - Specifying the file extension of your data files.

.. to do: need to add trouble shooting links and advice for each section; need to create a page for configuration when our program can do it;

Selecting your data and standards
=================================
To start the analysis session, you will need to load your data. The data in this demo analysis is stored within the LAtools directory under **latools_gui\\data**. This directory contains the following files:

    -   Sample-1.csv
    -   Sample-2.csv
    -   Sample-3.csv
    -   STD-1.csv
    -   STD-2.csv

To load these files, open your computers file explorer by clicking :guilabel:`&Browse`. Navigate to the folder containing the data - your data and standards - that you will be using in your project, then open it.

.. trouble shoot: why am I getting errors when I load my data?


Configuring LAtools
=====================
A configuration stores information about the way your data is formatted, and where on your computer your SRM tables are saved. In this example, we will use the **DEFAULT** configuration. Click on the :guilabel:`&Configuration` drop down menu, then select **DEFAULT**. This configuration states that you files

If you are using your own data, you may need to create a new configuration. For instructions on how to do this, see :ref:`Creating or modifying a configuration`. Note that multiple configurations can be set up and chosen during data import, allowing LAtools to flexibly work with data from different instruments.


Selecting a SRM identifier
==========================
The SRM identifier identifies which of your analyses contain standard reference materials. In this demo, we have loaded two SRMs: STD-1.csv and STD-2.csv. By default, this value is set to **'STD'**. This means that any data file with **'STD'** in its name will be flagged as an SRM measurement.

When using your own data, you need to have a unique identifier in your standard file names, be it "STD" or something else. You can specify your SRM identifiers by modifying the :guilabel:`&SRM Identifier` dialogue box.


Data extension
==============
Lastly, you will need to specify the extension type of the files you are using. All the files used in this demo are .csv files. The default value for this is **.csv**, so no change is required by us.

However, if you are using your own data files of a different kind, then you will need to type them into the :guilabel:`&n_min` dialogue box.


Start plotting!
===============
Once you have finished all these steps, you can now start plotting! To plot your data, click :guilabel:`&APPLY`. Your data plots should be visible in the plotting panel.

Navigating the plotting panel is quite easy - however, if you're having difficulties see :ref:`Navigating the plotting panel`.

How to check that everything has loaded
=======================================
In the graphing pane, the panel on the right hand side tells us that all five of our files were loaded. The legend on the left pane tells us which analytes are present in the data - in this demo, we have Mg24, Mg25, Al27, Ca43, Ca44, Mn55, Sr88, Ba137, and Ba138.


.. can possible add where users can see their output/report folders
