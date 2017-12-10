from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import (QAction, QApplication, QLabel,
                             QMainWindow, QMenu, QScrollArea, QSizePolicy)

from src.gui import DGISTAbout
from src.operations import ImageOperations, ReportOperations


class DGISTMainWindow(QMainWindow):
    def __init__(self):
        super(DGISTMainWindow, self).__init__()

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.statusBar().showMessage('Ready')
        self.setWindowTitle("DGIST")
        self.resize(500, 400)

    def about(self):
        DGISTAbout.about(self)

    def open(self):
        ImageOperations.open(self)

    def save_(self):
        ImageOperations.save(self)

    def zoomIn(self):
        self.statusBar().showMessage('Zooming in.')
        self.scaleImage(1.25)

    def zoomOut(self):
        self.statusBar().showMessage('Zooming out.')
        self.scaleImage(0.8)

    def normalSize(self):
        self.statusBar().showMessage('Reset to normal size.')
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        self.statusBar().showMessage('Fitting to window size.')
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()
        self.updateActions()

    def metadata(self):
        ImageOperations.metadata(self)

    def histogram(self):
        ImageOperations.histogram(self)

    def changeDetection(self):
        ImageOperations.changeDetection(self)

    def reports(self):
        ReportOperations.prepareReport(self)
        ReportOperations.saveReport(self)


    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.saveAct = QAction("&Save...", self, shortcut="Ctrl+S", enabled=False, triggered=self.save_)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)

        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False,
                                      checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

        self.metadataAct = QAction("&Metadata", self, enabled=False, triggered=self.metadata)
        self.histogramAct = QAction("&Histogram", self, enabled=False, triggered=self.histogram)
        self.changeDetectionAct = QAction("&Change Detection", self, enabled=False, triggered=self.changeDetection)
        self.reportsAct = QAction("&Reports", self, enabled=False, triggered=self.reports)

        self.aboutAct = QAction("&About", self, triggered=self.about)


    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.imageMenu = QMenu("&Image", self)
        self.imageMenu.addAction(self.zoomInAct)
        self.imageMenu.addAction(self.zoomOutAct)
        self.imageMenu.addAction(self.normalSizeAct)
        self.imageMenu.addAction(self.fitToWindowAct)
        self.imageMenu.addSeparator()
        self.imageMenu.addAction(self.metadataAct)
        self.imageMenu.addAction(self.histogramAct)
        self.imageMenu.addAction(self.changeDetectionAct)
        self.imageMenu.addSeparator()
        self.imageMenu.addAction(self.reportsAct)

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
