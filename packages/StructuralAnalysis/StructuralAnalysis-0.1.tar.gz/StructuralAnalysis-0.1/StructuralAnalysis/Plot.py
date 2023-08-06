from StructuralAnalysis import Structure
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np


app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.setGeometry(50, 100, 700, 700)
w.opts['distance'] = 30000
w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
gz = gl.GLGridItem()
gz.translate(0, 0, -10)
gz.setSize(50000, 50000, 50000)
gz.setSpacing(1000, 1000, 1000)
w.addItem(gz)

def plot_structure(structure: Structure):

    for element in structure.elements:
        x = np.array([element.start_node.x, element.end_node.x])
        y = np.array([element.start_node.y, element.end_node.y])
        z = np.array([element.start_node.z, element.end_node.z])

        pts = np.vstack([x, y, z]).T
        plt = gl.GLLinePlotItem(pos=pts, color='w', width=2, antialias=True)
        plt.rotate(angle=90, x=90,y=0,z=0)
        plt.rotate(angle=90, x=0,y=0,z=90)

        w.addItem(plt)


def plot_deformed_shape(structure: Structure):

    for element in structure.elements:
        pts = element.get_stations_global_displaced_position()
        plt = gl.GLLinePlotItem(pos=pts, color='r', width=2, antialias=True)
        plt.rotate(angle=90, x=90, y=0, z=0)
        plt.rotate(angle=90, x=0, y=0, z=90)
        w.addItem(plt)


# if __name__ == '__main__':
def execute_Qt():
    w.show()
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
