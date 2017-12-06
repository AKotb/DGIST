import cv2
import numpy as np
from matplotlib import pyplot as plt
from Tkinter import *
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QFileDialog, QMainWindow, QMessageBox)
from PIL import Image


class ImageOperations(QMainWindow):
    def __init__(self):
        super(ImageOperations, self).__init__()


def open(self):
    self.fileName, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
    #self.fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "C:/Users/ahmed.kotb/PycharmProjects/DGIST/resources")
    if self.fileName:
        self.image = QImage(self.fileName)
        if self.image.isNull():
            QMessageBox.information(self, "Image Viewer",
                                    "Cannot load %s." % self.fileName)
            return

        self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        self.scaleFactor = 1.0

        self.saveAct.setEnabled(True)
        self.fitToWindowAct.setEnabled(True)
        self.metadataAct.setEnabled(True)
        self.histogramAct.setEnabled(True)
        self.changeDetectionAct.setEnabled(True)
        self.reportsAct.setEnabled(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()


def save(QMainWindow):
    print "write save method code here"


def metadata(self):
    img = Image.open(self.fileName)
    root = Tk()
    root.title("Image Metadata")
    root.geometry("500x600")
    frame = Frame(root, bg="blue", width=500, height=600)
    label = Label(frame, text=img)
    frame.pack()
    label.pack()
    root.mainloop()


def histogram(self):
    img = cv2.imread(self.fileName)
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.show()


def changeDetection(QMainWindow):
    print "write Change Detection method code here"
