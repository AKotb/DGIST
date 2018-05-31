import sys
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMenu, QFileDialog)
from PyQt5.QtCore import QDir
from src.gui import DGISTAbout

class DGISTMainWindow(QMainWindow):

    def __init__(self):
        super(DGISTMainWindow, self).__init__()
        self.createActions()
        self.createMenus()
        self.setWindowTitle("DGIST")
        self.setGeometry(50, 100, 500, 50)
        self.imagecounter=120
        self.histocounter = 220

    def about(self):
        DGISTAbout.about(self)

    def open(self):
        from src.operations import ImageOperations
        self.imgpath = QFileDialog.getOpenFileName(self, "Open Image", QDir.currentPath())[0]
        imgopt = ImageOperations.ImageOperations()
        imgopt.openImage(self, self.imgpath)

    def metadata(self):
        from src.operations import ImageOperations
        imgopt = ImageOperations.ImageOperations()
        print self.imgpath
        imgopt.metadata(self, self.imgpath)

    def histogram(self):
        from src.operations import ImageOperations
        imgopt = ImageOperations.ImageOperations()
        imgopt.histogram2(self, self.imgpath)

    def changeDetection(self):
        from src.operations import ImageOperations
        imgopt = ImageOperations.ImageOperations()
        imgopt.changeDetection()

    def trendCalculator(self):
        from src.operations import ImageOperations
        imgopt = ImageOperations.ImageOperations()
        imgopt.trendCalculator()

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.metadataAct = QAction("&Metadata", self, enabled=False, triggered=self.metadata)
        self.histogramAct = QAction("&Histogram", self, enabled=False, triggered=self.histogram)
        self.changeDetectionAct = QAction("&Change Detection", self, enabled=True, triggered=self.changeDetection)
        self.trendCalculatorAct = QAction("&Trend Calculator", self, enabled=True, triggered=self.trendCalculator)
        self.aboutAct = QAction("&About", self, triggered=self.about)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.imageMenu = QMenu("&Image", self)
        self.imageMenu.addAction(self.metadataAct)
        self.imageMenu.addAction(self.histogramAct)
        self.imageMenu.addSeparator()
        self.imageMenu.addAction(self.changeDetectionAct)
        self.imageMenu.addAction(self.trendCalculatorAct)
        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.imageMenu)
        self.menuBar().addMenu(self.helpMenu)


sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = my_exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dGISTMainWindow = DGISTMainWindow()
    dGISTMainWindow.show()
    sys.exit(app.exec_())
