
from osgeo import gdal
from PyQt5.QtWidgets import (QMainWindow, QLabel,
                             QComboBox, QApplication, QPushButton)
import sys


class DGISTSelectRGB(QMainWindow):
    def __init__(self):
        super(DGISTSelectRGB,self).__init__()

        self.initUI()

    def initUI(self):
        dsr = gdal.Open("D:/2.png")
        self.index = 0
        #self.lbl = QLabel("", self)
        self.lblRed = QLabel("", self)
        self.lblGreen = QLabel("", self)
        self.lblBlue = QLabel("", self)

        # Button
        self.buttonRed = QPushButton('Set Red', self)
        self.buttonRed.setToolTip('Select band from Combo & Press to select Red in viewer')
        self.buttonRed.clicked.connect(self.red_on_click)

        self.buttonGreen = QPushButton('Set Green', self)
        self.buttonGreen.setToolTip('Select band from Combo & Press to select Green in viewer')
        self.buttonGreen.clicked.connect(self.green_on_click)

        self.buttonBlue = QPushButton('Set Blue', self)
        self.buttonBlue.setToolTip('Select band from Combo & Press to select Blue in viewer')
        self.buttonBlue.clicked.connect(self.blue_on_click)

        # Combobox
        combo = QComboBox(self)

        print "[ RASTER BAND COUNT ]: ", dsr.RasterCount

        for band in range(dsr.RasterCount):
            band += 1
            print "[ GETTING BAND ]: ", band
            srcband = dsr.GetRasterBand(band)
            combo.addItem(str(srcband.GetBand()))


        combo.move(25, 50)
        self.buttonRed.move(150, 50)
        self.buttonGreen.move(150, 100)
        self.buttonBlue.move(150, 150)

        self.lblRed.move(280,50)
        self.lblGreen.move(280,100)
        self.lblBlue.move(280,150)

        #combo.activated[str].connect(self.onActivated)
        combo.currentIndexChanged.connect(self.selectionchange)

        self.setGeometry(500, 300, 500, 500)
        self.setWindowTitle('RGB Selection')
        self.show()

    '''def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()'''

    def selectionchange(self, i):
        print "Items in the list are :"
        #print "Current index", i, "selection changed ", self.combo.currentText()
        self.index = i




    def red_on_click(self):
        print('Red clicked')
        self.lblRed.setText(str(self.index+1))

    def green_on_click(self):
        print('Green clicked')
        self.lblGreen.setText(str(self.index+1))

    def blue_on_click(self):
        print('Blue clicked')
        self.lblBlue.setText(str(self.index+1))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dgistRGB = DGISTSelectRGB()
    sys.exit(app.exec_())