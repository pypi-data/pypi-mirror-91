# Custom FigureCanvas for displaying Matplotlib output
#
# https://github.com/krischer/instaseis/blob/master/instaseis/gui/qt4mplcanvas.py

from matplotlib import rc as matplotlibrc
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas

mpl.rcParams['font.size'] = 10
matplotlibrc('figure.subplot', left=0.0, right=1.0, bottom=0.0, top=1.0)


class MyQt4MplCanvas(FigureCanvas):
    """
    Class to represent the FigureCanvas widget.
    """
    def __init__(self, parent=None):
        # Standard Matplotlib code to generate the plot
        self.fig = Figure()
        # initialize the canvas where the Figure renders into
        super(MyQt4MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
