from PyQt5.QtCore import QDir
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QFileDialog,
                             QMainWindow, QMessageBox)


class ImageOperations(QMainWindow):

    def __init__(self):
        super(ImageOperations, self).__init__()


def open(QMainWindow):
    fileName, _ = QFileDialog.getOpenFileName(QMainWindow, "Open File",
                                                  QDir.currentPath())
    if fileName:
        image = QImage(fileName)
        if image.isNull():
            QMessageBox.information(QMainWindow, "Image Viewer",
                                        "Cannot load %s." % fileName)
            return

        QMainWindow.imageLabel.setPixmap(QPixmap.fromImage(image))
        QMainWindow.scaleFactor = 1.0

        QMainWindow.saveAct.setEnabled(True)
        QMainWindow.fitToWindowAct.setEnabled(True)
        QMainWindow.metadataAct.setEnabled(True)
        QMainWindow.histogramAct.setEnabled(True)
        QMainWindow.changeDetectionAct.setEnabled(True)
        QMainWindow.reportsAct.setEnabled(True)
        QMainWindow.updateActions()

        if not QMainWindow.fitToWindowAct.isChecked():
            QMainWindow.imageLabel.adjustSize()


def save(QMainWindow):
    print "write save method code here"


def metadata(QMainWindow):
    print "write Metadata method code here"


def histogram(QMainWindow):
    print "write Histogram method code here"


def changeDetection(QMainWindow):
    print "write Change Detection method code here"

