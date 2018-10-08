##################
Stage 7. Filtering
##################

Your data is now background corrected, normalised to an internal standard, and calibrated. You can now start thinking about data filtering.

On this page:
=============
* :ref:`What is data filtering, and why use it?`

* :ref:`The filters`

* :ref:`Creating and applying filters`



What is data filtering, and why use it?
=======================================
Laser ablation data are spatially resolved. In heterogeneous samples, this means that the concentrations of different analytes will change within a single analysis. This compositional heterogeneity can either be natural and expected (e.g. Mg/Ca variability in foraminifera), or caused by compositionally distinct contaminant phases included in the sample structure. If the end goal of your analysis is to get integrated compositional estimates for each ablation analysis, how you deal with sample heterogeneity becomes central to data processing, and can have a profound effect on the resulting integrated values. So far, heterogeneous samples tend to be processed manually, by choosing regions to integrate by eye, based on a set of criteria and knowledge of the sample material. While this is a valid approach to data reduction, it is not reproducible: if two ‘expert analysts’ were to process the data, the resulting values would not be quantitatively identical. Reproducibility is fundamental to sound science, and the inability to reproduce integrated values from identical raw data is a fundamental flaw in Laser Ablation studies. In short, this is a serious problem.

To get round this, we have developed ‘Data Filters’. Data Filters are systematic selection criteria, which can be applied to all samples to select specific regions of ablation data for integration. For example, the analyst might apply a filter that removes all regions where a particular analyte exceeds a threshold concentration, or exclude regions where two contaminant elements co-vary through the ablation. Ultimately, the choice of selection criteria remains entirely subjective, but because these criteria are quantitative they can be uniformly applied to all specimens, and most importantly, reported and reproduced by an independent researcher. This removes significant possibilities for ‘human error’ from data analysis, and solves the long-standing problem of reproducibility in LA-MS data processing.

The filters
===========
``latools`` includes several filtering functions, which can be created, combined and applied in any order, repetitively and in any sequence. By their combined application, it should be possible to isolate any specific region within the data that is systematically identified by patterns in the ablation profile. These filter are:

Threshold
---------
The threshold filter identifies regions in the data where a specific analyte is above or below a given threshold. Two sub-filters are created - ‘above’, which selects all regions where the target analyte is above the threshold value, and ‘below’, which selects all regions where the target analyte is below the threshold value. To use this filter, you will need select either the ‘above’ or ‘below’ component for each analyte, either below or in the filter summary table.

There are four different types of threshold filter:
    * Threshold - selects data based on the absolute concentration of a target analyte.
    * Threshold Percentile - similar to ‘threshold’, but instead of specifying the absolute concentration of the analyte, a percentile can be selected to exclude the lowest/highest X% of data points.
    * Gradient Threshold - a running gradient is calculated for the data, and regions can be excluded where the slope is steeper than a specified threshold.
    * Gradient Threshold Percentile - similar to Threshold Percentile, but operates on the running gradient instead of concentration data.


Clustering
----------
The clustering filter uses data clustering algorithms to identify compositionally distinct populations in your data, based on the concentrations of one or more analytes. These filters can be applied at the ‘whole analysis’ or ‘individual ablation’ levels. Two difference clustering algorithms are available:
    * kmeans - separates the data into N clusters, such that the variance within each cluster is minimised. Useful for automatically separating separate materials in data, where the number of separate materials is known.
    * meanshift - automatically determines number of clusters in data based on the bandwidth of expected variation. This one can be useful when the number of materials in the data is not known, although can become difficult to interpret in complex datasets. For most purposes, kmeans will probably be better.


Correlation
-----------
The correlation filter can be used to exclude data where two analytes correlate. The filter calculates the Pearson correlation coefficient (r) and associated significance statistic (p) across the ablation, and can be used to exclude regions where analytes co-vary significantly using r and p thresholds. For example, where an analyte associated with a secondary contaminant phase co-varies with a target analyte in the host material.


Defragment
----------
Remove ‘fragments’ from the calculated filter. For example, if the concentration of an analyte oscillates around a threshold value, the data selected by this filter will be ‘fragmented’. This filter can be used to either remove or include these fragmented regions. Typically, you might you use this towards the end of filtering. It is applied to all currently active filters, so ensure all required filters are active before applying this filter.

Exclude
-------
Removes all selected data regions after the first region excluded by the current filters. This can be useful in spot analyses, where any contaminant present at the start of the ablation will influence the subsequent composition due to down-hole effects.

Trim
----
Remove points from the start and end of currently selected filter regions. This can be used to make your filter selections more conservative.

Signal Optimiser
----------------
Optimise data selection based on specified analytes.

This filter identifies the longest possible contiguous region in the ablation where the concentration and standard deviation of selected analytes is minimised.

WARNING: this one can be slow.

For technical details, see the ``latools`` |location_link2|

	.. |location_link2| raw:: html

		<a href="https://latools.readthedocs.io/en/latest/index.html" target="_blank">User Manual</a>


Creating and applying filters
=============================

1. To create a filter, click on :guilabel:`&+` or :guilabel:`&Create filter`.


2. Select the filter you wish to use from the :guilabel:`&Filter` drop down menu. For example, we wouldn’t expect cultured foraminifera to have a Al/Ca of ~100 µmol/mol, so we therefore want to remove all data from regions with an Al/Ca above this. We’ll do this with a threshold filter:

        1. Choose Threshold from the drop down menu.
        2. Click :guilabel:`&Create filter`.
        3. In the :guilabel:`&Threshold` input box, enter 0.0001.
        4. In the :guilabel:`&Analyte` drop down, select :guilabel:`&Al27`.
        5. Click :guilabel:`&Create filter`.

    You  have now created a filter that goes through all the samples in our analysis, and works out which analyses have an Al/Ca both greater than and less than 100 µmol/mol (remember, all units are in mol/mol at this stage).

        .. image:: gifs/09-createfilter.gif
                :width: 1275px
                :height: 760px
                :scale: 50 %
                :alt: create filter
                :align: center

3. To apply the filters, go to the :guilabel:`&Summary` tab, and select the analytes that you wish to apply the filter to. In this example, we will apply the 'below filter' to all analytes by clicking on :guilabel:`&All`.

        .. image:: gifs/09-applyfilter.gif
                :width: 1275px
                :height: 760px
                :scale: 50 %
                :alt: apply filter
                :align: center

