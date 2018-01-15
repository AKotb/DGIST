import cv2
from matplotlib import pyplot as plt
from osgeo import gdal
import xlsxwriter
from random import randint
import numpy as np
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
            self.statusBar().showMessage('Image Viewer cannot load file.')
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
        self.statusBar().showMessage('File loaded in Image Viewer.')

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()


def save(self):
    # this is save method
    filename = QFileDialog.getSaveFileName(self, "Save", "", "All Files (*);;TIF Image (*.tif);;PNG Image (*.png);;JPG Image (*.jpg);;Text Files (*.txt)")[0]
    img = cv2.imread(self.fileName)
    cv2.imwrite(filename, img)
    self.statusBar().showMessage('Image saved into ' + filename)


def metadata(self):
    img = Image.open(self.fileName)
    print(img.getbands)
    self.statusBar().showMessage('Metadata generated.')
    root = Tk()
    root.title("Image Metadata")
    root.geometry("500x600")
    frame = Frame(root, bg="blue", width=500, height=600)
    label = Label(frame, text=img)
    frame.pack()
    label.pack()
    root.mainloop()


def histogram(self):
    self.statusBar().showMessage('Histogram generated.')
    img = cv2.imread(self.fileName)
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.show()

def write_geotiff(fname, data, geo_transform, projection, data_type=gdal.GDT_Byte):
    driver = gdal.GetDriverByName('GTiff')
    rows, cols = data.shape
    dataset = driver.Create(fname, cols, rows, 1, data_type)
    dataset.SetGeoTransform(geo_transform)
    dataset.SetProjection(projection)
    band = dataset.GetRasterBand(1)
    band.WriteArray(data)
    dataset = None
    return

def changeDetection(self):
    image1, _ = QFileDialog.getOpenFileName(self, "Choose The First Image", QDir.currentPath())
    image2, _ = QFileDialog.getOpenFileName(self, "Choose The Second Image", QDir.currentPath())
    outputImageName = QFileDialog.getSaveFileName(self, "Save Change Detection Result", "",
                                                  "TIF Image (*.tif);;PNG Image (*.png);;BMP Image (*.bmp);;JPG Image (*.jpg);;Text Files (*.txt)")[
        0]
    outputMatrixName = QFileDialog.getSaveFileName(self, "Save Change Detection Matrix", "",
                                                   "Excel XLSX (*.xlsx);;Excel XLS (*.xls);;Text Files (*.txt)")[0]

    raster_before = gdal.Open(image1, gdal.GA_ReadOnly)
    raster_after = gdal.Open(image2, gdal.GA_ReadOnly)
    geo_transform = raster_after.GetGeoTransform()
    proj = raster_after.GetProjectionRef()

    band = raster_before.GetRasterBand(1)
    bands_before = band.ReadAsArray()

    band = raster_after.GetRasterBand(1)
    bands_after = band.ReadAsArray()
    rows_after, cols_after = bands_after.shape

    flat_data = bands_after.reshape((rows_after, cols_after))

    change_mat = np.zeros((7, 7), dtype=np.int)

    for i in range(rows_after):
        for j in range(cols_after):
            change_mat[bands_before[i][j]][bands_after[i][j]] += 1
            flat_data[i][j] = 7 * (bands_before[i][j]) + (bands_after[i][j]) + 1
        # print str(int(100.0 * i / rows_after))+"%"
        self.statusBar().showMessage("Difference Image Creation: " + str(int(100.0 * i / rows_after))+"%")

    self.statusBar().showMessage("Difference Image Created @ ")

    write_geotiff(outputImageName, flat_data, geo_transform, proj)

    self.statusBar().showMessage("Difference Image Saved @ " + outputImageName)

    workbook = xlsxwriter.Workbook(outputMatrixName)
    ws_stat = workbook.add_worksheet()

    classes = ["Class 0", "Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6"]

    ws_stat.write(0, 0, "State No.")
    ws_stat.write(0, 1, "BEFORE")
    ws_stat.write(0, 2, "AFTER")
    ws_stat.write(0, 3, "# of pixels")
    ws_stat.write(0, 4, "Percent (%)")
    for i in range(0, 7):
        for j in range(0, 7):
            ws_stat.write(7 * i + j + 1, 0, 7 * i + j + 1)
            ws_stat.write(7 * i + j + 1, 1, classes[i])
            ws_stat.write(7 * i + j + 1, 2, classes[j])
            ws_stat.write(7 * i + j + 1, 3, change_mat[i][j])
            ws_stat.write(7 * i + j + 1, 4, 1.0 * change_mat[i][j] / np.sum(change_mat))

    workbook.close()

    self.statusBar().showMessage("Difference Image Report Saved @ " + outputMatrixName)
    self.statusBar().showMessage("Change Detection Process finished successfully.")
    self.statusBar().showMessage("")
