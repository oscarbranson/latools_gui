###########
Start Here!
###########

Welcome to the LAtools GUI user manual!

The LAtools GUI is an intuitive, easy-to-use graphical user interface for ``latools``. The GUI has been developed by six computer science students participating in the |location_link4|

.. |location_link4| raw:: html

	<a href="https://cs.anu.edu.au/TechLauncher/" target="_blank">TechLauncher Initiative</a> at the Australia National University.

The students have worked closely with the |location_link6|

.. |location_link6| raw:: html

	<a href="https://github.com/oscarbranson/latools/" target="_blank"> Laser Ablation Tools</a> developer, Dr. Oscar Branson, to ensure that the interface meets the needs of the laser ablation community.

For those who would like to know more about the mechanics of ``latools`` & the LAtools GUI, check out the following links:


	* LAtools GUI |location_link1|

	.. |location_link1| raw:: html

	   <a href="https://github.com/oscarbranson/latools_gui" target="_blank">GitHub page</a>
	* ``latools`` |location_link2|

	.. |location_link2| raw:: html

		<a href="https://github.com/oscarbranson/latools" target="_blank">GitHub page</a>

Getting started
=================
If you have never used the LAtools GUI before, these are the steps you will need to follow to get going.

1. Read and follow the :ref:`installing_latools` guide.
2. Go through the :ref:`beginners_guide`, which takes you through an example analysis session.
3. Know that we have a communications portal in case you have any problems with our software - see |location_link3|

	.. |location_link3| raw:: html

	   <a href="https://docs.google.com/forms/d/e/1FAIpQLSeqtwnylIPdZ4v4TmsuDm24rCSshX-2H_1lwt_O0tvxu7jJIQ/viewform?usp=sf_link" target="_blank">this form!</a>


What is ``latools``?
================
At present, most LA-MS data requires a degree of manual processing. This introduces subjectivity in data analysis, and independent expert analysts can obtain significantly different results from the same raw data. There is no standard way of reporting LA-MS data analysis, which would allow an independent user to obtain the same results from the same raw data. ``latools`` is designed to tackle this problem.

``latools`` automatically handles all the routine aspects of LA-MS data reduction:

		1. Signal De-spiking
		2. Signal / Background Identification
		3. Background Subtraction
		4. Normalisation to internal standard
		5. Calibration to SRMs

These processing steps perform the same basic functions as other LA-MS processing software. If your end goal is calibrated ablation profiles, these can be exported at this stage for external plotting an analysis. The real strength of ``latools`` comes in the systematic identification and removal of contaminant signals, and calculation of integrated values for ablation spots.
This is accomplished using:

		6. Systematic data selection using quantitative data selection `filters`.
		7. Analyses can be fully reproduced by independent users through the export and import of analytical sessions.

These features provide the user with systematic tools to reduce laser ablation profiles to per-ablation integrated averages. At the end of processing, ``latools`` can export a set of parameters describing your analysis, along with a minimal dataset containing the SRM table and all raw data required to reproduce your analysis (i.e. only analytes explicitly used during processing).

Why use the LAtools GUI?
========================
The LAtools GUI (Graphical User Interface) is built on top of ``latools``, and provides the following features:

* An easy to use interface that follows the ``latools`` data processing flow described above.
* Real-time graphing capabilities, so users can see what is happening to their data as it is being processed.
* Requires no programming experience!
