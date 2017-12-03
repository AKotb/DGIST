from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
                             QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PIL import Image as pimg


class ImageOperations:

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

    def save_(QMainWindow):
        newImg1 = pimg.new('RGB', (512, 512))
        newImg1.save("C:/Users/ahmed.kotb/PycharmProjects/DGIST/resources/image.png", "PNG")

    def metadata(QMainWindow):
        QMainWindow.scaleImage(1.25)

    def histogram(QMainWindow):
        QMainWindow.scaleImage(1.25)

    def changeDetection(QMainWindow):
        QMainWindow.scaleImage(1.25)

    def reports(QMainWindow):
        QMainWindow.scaleImage(1.25)