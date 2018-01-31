
from osgeo import gdal
import numpy as np
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QLabel, QFileDialog,
                             QComboBox, QApplication, QPushButton)
import sys


class DGISTSelectRGB(QMainWindow):
    def __init__(self):
        #init function
        super(DGISTSelectRGB,self).__init__()

        self.initUI()

    def initUI(self):
        image1, _ = QFileDialog.getOpenFileName(self, "Choose Multilayer Image", QDir.currentPath())
        dsr = gdal.Open(image1)
        self.dsr_array = np.array(dsr.ReadAsArray())

        self.rSelected = 0
        self.gSelected = 0
        self.bSelected = 0

        self.index = 0
        #self.lbl = QLabel("", self)
        self.lblRed = QLabel("", self)
        self.lblRed.setStyleSheet('color: red')
        self.lblRed.setFont(QFont('SansSerif', 15))
        self.lblGreen = QLabel("", self)
        self.lblGreen.setStyleSheet('color: green')
        self.lblGreen.setFont(QFont('SansSerif', 15))
        self.lblBlue = QLabel("", self)
        self.lblBlue.setStyleSheet('color: blue')
        self.lblBlue.setFont(QFont('SansSerif', 15))

        # Button
        self.buttonRed = QPushButton("Set Red", self)
        self.buttonRed.setToolTip("Select band from Combo & Press to select Red in viewer")
        self.buttonRed.clicked.connect(self.red_on_click)

        self.buttonGreen = QPushButton('Set Green', self)
        self.buttonGreen.setToolTip('Select band from Combo & Press to select Green in viewer')
        self.buttonGreen.clicked.connect(self.green_on_click)

        self.buttonBlue = QPushButton('Set Blue', self)
        self.buttonBlue.setToolTip('Select band from Combo & Press to select Blue in viewer')
        self.buttonBlue.clicked.connect(self.blue_on_click)

        self.buttonLoad = QPushButton('Load RGB', self)
        self.buttonLoad.setToolTip('Load selected 3 bands as RGB Combination')
        self.buttonLoad.clicked.connect(self.load_on_click)
        self.buttonLoad.setEnabled(False)

        # Combobox
        combo = QComboBox(self)

        print "[ RASTER BAND COUNT ]: ", dsr.RasterCount
        self.arrBands = []
        for band in range(dsr.RasterCount):
            band += 1
            print "[ GETTING BAND ]: ", band
            srcband = dsr.GetRasterBand(band)
            combo.addItem(str(srcband.GetBand()))


        print "arrBands ", self.arrBands.__len__()

        combo.move(25, 50)
        self.buttonRed.move(150, 50)
        self.buttonGreen.move(150, 100)
        self.buttonBlue.move(150, 150)
        self.buttonLoad.move(150, 200)
        self.lblRed.move(280,50)
        self.lblGreen.move(280,100)
        self.lblBlue.move(280,150)


        #combo.activated[str].connect(self.onActivated)
        combo.currentIndexChanged.connect(self.selectionchange)

        self.setGeometry(500, 300, 500, 500)
        self.setWindowTitle('RGB Selection')
        self.show()


    def load_on_click(self):
        #print "Loading RGB Selection"
        self.rgbImg = self.dsr_array[[self.rIndex, self.gIndex, self.bIndex],:,:]
        print self.rgbImg.shape


    def selectionchange(self, i):
        print "Items selected is :" + str(i)
        self.index = i


    def red_on_click(self):
        print('Red clicked')
        self.lblRed.setText(str(self.index+1))
        self.rIndex = self.index
        self.rSelected = 1
        if self.gSelected + self.rSelected + self.rSelected == 3:
            self.buttonLoad.setEnabled(True)


    def green_on_click(self):
        print('Green clicked')
        self.lblGreen.setText(str(self.index+1))
        self.gIndex = self.index
        self.gSelected = 1
        if self.gSelected + self.rSelected + self.rSelected == 3:
            self.buttonLoad.setEnabled(True)


    def blue_on_click(self):
        print('Blue clicked')
        self.lblBlue.setText(str(self.index+1))
        self.bIndex = self.index
        self.bSelected = 1
        if self.gSelected + self.rSelected + self.rSelected == 3:
            self.buttonLoad.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dgistRGB = DGISTSelectRGB()
    sys.exit(app.exec_())