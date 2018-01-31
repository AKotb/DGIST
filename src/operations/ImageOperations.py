import cv2
import xlsxwriter
import numpy as np
from matplotlib import pyplot as plt
from osgeo import gdal
from Tkinter import *
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QFileDialog)
from PIL import Image


class ImageOperations:
    def __init__(self):
        super(ImageOperations, self).__init__()


def openImage(QMainWindow):
    QMainWindow.fileName = QFileDialog.getOpenFileName(QMainWindow, "Open Image", QDir.currentPath())[0]
    ds = gdal.Open(QMainWindow.fileName)
    lst = []
    for band in range(ds.RasterCount):
        band += 1
        nparray = ds.GetRasterBand(band).ReadAsArray()
        lst.append(nparray)
    if len(lst) > 1:
        data = np.dstack(lst)
        QMainWindow.metadataAct.setEnabled(True)
        QMainWindow.histogramAct.setEnabled(True)
    else:
        data = ds.ReadAsArray()
        QMainWindow.metadataAct.setEnabled(False)
        QMainWindow.histogramAct.setEnabled(False)
    plt.figure(120)
    plt.gcf().canvas.set_window_title(QMainWindow.fileName)
    plt.imshow(data)
    plt.axis('off')
    plt.colorbar()
    plt.show()
    QMainWindow.statusBar().showMessage('File loaded in Image Viewer.')


def metadata(QMainWindow):
    img = Image.open(QMainWindow.fileName)
    root = Tk()
    root.title("Image Metadata")
    root.geometry("500x600")
    frame = Frame(root, bg="blue", width=500, height=600)
    label = Label(frame, text=img)
    frame.pack()
    label.pack()
    root.mainloop()
    QMainWindow.statusBar().showMessage('Metadata generated.')


def histogram(QMainWindow):
    img = cv2.imread(QMainWindow.fileName)
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.figure(121)
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.gcf().canvas.set_window_title('Image Histogram')
    plt.legend(color, loc='best')
    plt.show()
    QMainWindow.statusBar().showMessage('Histogram generated.')


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


def changeDetection(QMainWindow):
    image1, _ = QFileDialog.getOpenFileName(QMainWindow, "Choose The First Image", QDir.currentPath())
    image2, _ = QFileDialog.getOpenFileName(QMainWindow, "Choose The Second Image", QDir.currentPath())
    outputImageName = QFileDialog.getSaveFileName(QMainWindow, "Save Change Detection Result", "",
                                                  "TIF Image (*.tif);;PNG Image (*.png);;BMP Image (*.bmp);;JPG Image (*.jpg);;Text Files (*.txt)")[
        0]
    outputMatrixName = QFileDialog.getSaveFileName(QMainWindow, "Save Change Detection Matrix", "",
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
        QMainWindow.statusBar().showMessage("Difference Image Creation: " + str(int(100.0 * i / rows_after))+"%")

    QMainWindow.statusBar().showMessage("Difference Image Created @ ")

    write_geotiff(outputImageName, flat_data, geo_transform, proj)

    QMainWindow.statusBar().showMessage("Difference Image Saved @ " + outputImageName)

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

    QMainWindow.statusBar().showMessage("Difference Image Report Saved @ " + outputMatrixName)
    QMainWindow.statusBar().showMessage("Change Detection Process finished successfully.")
    QMainWindow.statusBar().showMessage("")