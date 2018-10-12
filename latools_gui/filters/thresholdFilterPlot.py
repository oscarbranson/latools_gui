from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from latools.helpers.helpers import nominal_values
from templates.graphPane import GraphWindow


class thresholdFilterPlot(GraphWindow):
    """
    Plot display threshold filter info in popup.
    """

    def __init__(self, project, filterPlot):
        super().__init__(project)

        self.options = filterPlot.filterOptions
        self.filterPlot = filterPlot
        self.populated = False

        # Set window properties
        self.setWindowTitle('Threshold Filter')

        # initialise graph layout
        self.initialiseSamples()
        self.autorangeButton.setParent(None)  # remove auto-range button
        self.initialiseGraph()
        # self.initialiseLegend()

        # histogram bin slider
        self.binSlider = QSlider(Qt.Horizontal)
        self.binSlider.setMaximum(100)
        self.binSlider.setMinimum(10)
        self.binSlider.setTickInterval(10)
        self.binSlider.setSingleStep(5)
        self.binSlider.setValue(50)
        self.binSlider.setMaximumWidth(150)
        self.binSlider.valueChanged.connect(self.updateHist)

        self.filterPlot.mainGrid.addWidget(self.binSlider, 1, 1)
        
        self.populateSamples()

        if self.options['analyte'] in self.project.eg.analytes:
            # draw graph
            self.drawGraph()

    def populateSamples(self):
        """
            Updates the list of available samples from the dataset viewable on the graph
        """

        samples = np.concatenate([['ALL'], self.project.eg.samples])
        self.sampleName = 'ALL'

        self.sampleList.clear()
        for sample in samples:
            self.sampleList.addItem(sample)
        
        self.sampleList.setCurrentItem(self.sampleList.item(0))

    def initialiseGraph(self):
        self.backgroundColour = 'w'

        pg.setConfigOption('background', self.backgroundColour)
        pg.setConfigOption('foreground', 'k')

        self.graphLayout = pg.GraphicsLayoutWidget()
        self.graphLayout.ci.layout.setColumnStretchFactor(0, 4)
        self.graphLayout.ci.layout.setColumnStretchFactor(1, 1)

        ## GraphLayout width does not expand with window... why?

        self.graph = pg.PlotItem(name='Data')
        self.histPane = pg.PlotItem(name='Hist')
        self.histPane.setYLink('Data')
        self.histPane.getAxis('left').setTicks([])
        self.histPane.hideButtons()

        self.graphLayout.addItem(self.graph)
        self.graphLayout.addItem(self.histPane)
        
        self.layout.addWidget(self.graphLayout)

    def updateData(self):
        analyte = self.options['analyte']
        self.analyte = analyte

        if self.sampleName in self.project.eg.samples:
            dat = self.project.eg.data[self.sampleName]
            self.colour = dat.cmap[analyte]
            self.x = dat.Time
            self.y = nominal_values(dat.focus[analyte])
        elif self.sampleName == 'ALL':
            self.project.eg.get_focus(filt=True)
            self.colour = self.project.eg.cmaps[analyte]
            self.x = self.project.eg.focus['uTime']
            self.y = nominal_values(self.project.eg.focus[analyte])
    
    def swapSample(self):
        """
            sets current sample to selected sample
        """
        selectedSamples = self.sampleList.selectedItems()
        if len(selectedSamples) > 0:
            selectedSample = selectedSamples[0]
            self.sampleName = selectedSample.text()

        if self.populated:
            self.updateData()
            self.updateLines()
        
    def updateLogScale(self):
        for graph in [self.graph, self.histPane]:
            graph.setLogMode(x=False, y=self.yLogCheckBox.isChecked())
        self.updateHist()

    def drawGraph(self):
        # get data
        self.updateData()

        # draw trace
        self.line = pg.PlotDataItem(x=self.x, y=self.y, pen=pg.mkPen(self.colour, width=2), label=self.analyte, name=self.analyte, connect='finite')

        self.graph.addItem(self.line)
        self.graph.setLogMode(x=False, y=self.yLogCheckBox.isChecked())

        # draw histogram
        n, x = self.calcHist()
        self.hist = pg.PlotDataItem(x=n, y=x, pen=pg.mkPen(self.colour, width=2), label=self.analyte, name=self.analyte, connect='finite')

        self.histPane.addItem(self.hist)
        self.histPane.setLogMode(x=False, y=self.yLogCheckBox.isChecked())

        # recalculate histogram on zoom
        self.graph.sigRangeChanged.connect(self.updateHist)
        self.histPane.sigYRangeChanged.connect(self.updateHist)

        self.populated = True

    def calcHist(self):
        yr = self.graph.getAxis('left').range
        xr = self.graph.getAxis('bottom').range
        ind = (self.x >= xr[0]) & (self.x <= xr[1])
        
        if self.yLogCheckBox.isChecked():
            bins = np.logspace(*yr, self.binSlider.value())
        else:
            bins = np.linspace(*yr, self.binSlider.value())

        n, edges = np.histogram(self.y[ind], bins=bins)

        return n, edges[:-1] + np.diff(edges)

    def updateHist(self):
        n, x = self.calcHist()
        self.hist.setData(x=n, y=x)

    def drawThreshold(self):
        pass

    def updateThreshold(self):
        pass

    def updateLines(self):
        self.line.setData(x=self.x, y=self.y)
        self.updateHist()

    def updateGraph(self, options):
        self.options = options
        
        


    