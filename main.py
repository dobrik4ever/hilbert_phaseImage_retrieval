from PyQt5 import QtWidgets
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.pyplot import figure
from skimage import io
from Hilbert import HilbertPhase
import os

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

        
class Example(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.cbar = None
        self.sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        toolbar = NavigationToolbar(self.sc, self)

        self.wavelength = 6328
        self.button_open = QtWidgets.QPushButton('Open')
        self.button_hilbert = QtWidgets.QPushButton('Phase it')
        self.button_open.clicked.connect(self.open_file)
        self.button_hilbert.clicked.connect(self.hilbert)
        self.button_hilbert.setEnabled(False)

        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Offline')
        
        hb = QtWidgets.QVBoxLayout()
        hb.addWidget(self.sc)
        hb.addWidget(toolbar)
        bs = QtWidgets.QHBoxLayout()
        bs.addWidget(self.button_hilbert)
        bs.addWidget(self.button_open)

        # Input Parameters
        layout_params = QtWidgets.QHBoxLayout()
        self.wv_input = QtWidgets.QPlainTextEdit(str(self.wavelength))
        self.wv_input.textChanged.connect(self.change_wv)
        layout_params.addWidget(self.wv_input)
        hb.addLayout(bs)
        hp_layout = QtWidgets.QHBoxLayout()
        hp_layout.addWidget(self.wv_input)
        hp_layout.addWidget(QtWidgets.QLabel('Wavelength: nm'))
        hb.addLayout(hp_layout)
        cw = QtWidgets.QWidget()
        cw.setLayout(hb)
        self.setCentralWidget(cw)
        self.show()

    def change_wv(self):
        self.wavelength = float(self.wv_input.toPlainText())*1e-9

    def hilbert(self):
        h = HilbertPhase(self.file)
        self.image = h.retrieve(wv=self.wavelength)
        self.sc.axes.cla()
        im = self.sc.axes.imshow(self.image)
        if self.sc.cbar != None:
            self.sc.cbar.remove()
        self.sc.cbar = self.sc.fig.colorbar(im)
        self.sc.draw()

    def open_file(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file blin', os.getcwd())[0]
        self.button_hilbert.setEnabled(True)
        self.img = io.imread(self.file)
        self.statusBar.showMessage('Found a new file')
        self.sc.axes.cla()
        self.sc.axes.imshow(self.img, cmap='gray')
        self.sc.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())