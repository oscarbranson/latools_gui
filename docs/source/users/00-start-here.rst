############
Introduction
############

Welcome to LAtools GUI!

This project represents the efforts of six computer science students participating in the `TechLauncher Initiative <https://cs.anu.edu.au/TechLauncher/>`_ at the Australia National University. The students have worked closely with the `Laser Ablation Tools <https://github.com/oscarbranson/latools>`_ (``latools``) developer, Dr. Oscar Branson, to create a graphical user interface (GUI) for LAtools.

If you are interested, feel free to look at the follow the following links to the LAtools GUI and ``latools`` github repositories, and the ``latools`` manual.

* The LAtools GUI `Github page <https://github.com/oscarbranson/latools_gui>`_
* The ```latools`` `Github page <https://github.com/oscarbranson/latools>`_
* The ```latools`` `readthedocs <https://latools.readthedocs.io/en/latest/index.html>`_


Getting started
=================
If you have never used LAtools GUI before, these are the steps you need to follow to get going.

1. Read and follow the :ref:`installing_latools` guide
2. Go through the :ref:`beginners_guide`, which has an example data analysis
3. Read and follow the :ref:`create_configuration` guide so you can use your own data


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
The LAtools `Graphical User Interface` (GUI) is built on top of ``latools``, and provides the following features:

* An easy to use interface that follows the ``latools`` data processing flow described above
* Live graphing capabilities, so users can see what is happening to their data as it is being processed
* Requires no programming experience!

