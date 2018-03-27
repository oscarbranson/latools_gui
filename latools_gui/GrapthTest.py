import os, shutil, sys
import latools as la
import pyqtgraph as pg
import numpy as np
import uncertainties.unumpy as un
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget

# uncertainties unpackers
def unpack_uncertainties(uarray):
    """
    Convenience function to unpack nominal values and uncertainties from an
    ``uncertainties.uarray``.

    Returns:
        (nominal_values, std_devs)
    """
    try:
        return un.nominal_values(uarray), un.std_devs(uarray)
    except:
        return uarray, None

#la.get_example_data('./data')

eg = la.analyse(data_folder='./data/',
                config='DEFAULT',
                internal_standard='Ca43',
                srm_identifier='STD')

sampleName = 'Sample-1'
focusStage = 'rawdata'

eg.despike()
dat = eg.data[sampleName]

#pg.setConfigOption('background', 'w')
#pg.setConfigOption('foreground', 'k')


if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    
    ax = pg.PlotWidget(title=sampleName)
    ax.setLogMode(x=False, y=True)

    layout = QtGui.QGridLayout()
    w.setLayout(layout)

    layout.addWidget(ax, 0, 1, 3, 1)

    #colourconver = {'Mg24': (27,158,119), 'Mg25': (217,95,2), 'Al27': (117,112,179), 'Ca43': (231,41,138), 'Ca44': (102,166,30), 'Mn55': (230,171,2), 'Sr88': (166,118,29), 'Ba137': (102,102,102), 'Ba138': (102,102,102)}
    analytes = dat.analytes

    for a in analytes:
        #print(a)
        x = dat.Time
        y, yerr = unpack_uncertainties(dat.data[focusStage][a])
        y[y == 0] = np.nan
        ax.plot(x, y, pen=pg.mkPen(dat.cmap[a], width=2), label=a)

    w.show();

    sys.exit(app.exec_())