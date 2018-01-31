from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMenu)
from src.gui import DGISTAbout
from src.operations import ImageOperations


class DGISTMainWindow(QMainWindow):
    def __init__(self):
        super(DGISTMainWindow, self).__init__()
        self.createActions()
        self.createMenus()
        self.setWindowTitle("DGIST")
        self.setGeometry(50, 100, 500, 50)

    def about(self):
        DGISTAbout.about(self)

    def open(self):
        ImageOperations.openImage(self)

    def metadata(self):
        ImageOperations.metadata(self)

    def histogram(self):
        ImageOperations.histogram(self)

    def changeDetection(self):
        ImageOperations.changeDetection(self)

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.metadataAct = QAction("&Metadata", self, enabled=False, triggered=self.metadata)
        self.histogramAct = QAction("&Histogram", self, enabled=False, triggered=self.histogram)
        self.changeDetectionAct = QAction("&Change Detection", self, enabled=True, triggered=self.changeDetection)
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
        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.imageMenu)
        self.menuBar().addMenu(self.helpMenu)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dGISTMainWindow = DGISTMainWindow()
    dGISTMainWindow.show()
    sys.exit(app.exec_())
