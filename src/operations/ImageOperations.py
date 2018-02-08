import cv2
import xlsxwriter
import numpy as np
import ttk
import os
from matplotlib import pyplot as plt
from osgeo import gdal
from Tkinter import *
from PyQt5.QtCore import QDir
from PIL import Image
from PyQt5.QtWidgets import (QFileDialog)
from src.gui.DGISTMainWindow import DGISTMainWindow


class ImageOperations(DGISTMainWindow):

    def __init__(self):
        super(ImageOperations, self).__init__()
        self.selectedbnd1=1
        self.selectedbnd2=1
        self.selectedbnd3=1

    def openImage(self, DGISTMainWindow, imagepath):
        self.imagepath=imagepath
        ds = gdal.Open(imagepath)
        self.dsr_array = np.array(ds.ReadAsArray(), dtype=np.uint8)
        lst = []
        for band in range(ds.RasterCount):
            band += 1
            nparray = ds.GetRasterBand(band).ReadAsArray()
            lst.append(nparray)

        if len(lst) > 3:
            self.openMultiBandImage(ds)
            DGISTMainWindow.metadataAct.setEnabled(True)
            DGISTMainWindow.histogramAct.setEnabled(True)
        elif len(lst) ==3:
            data = np.dstack(lst)
            plt.figure(120)
            plt.gcf().canvas.set_window_title(imagepath)
            plt.imshow(data)
            plt.axis('off')
            plt.show()
            DGISTMainWindow.metadataAct.setEnabled(True)
            DGISTMainWindow.histogramAct.setEnabled(True)
        else:
            data = ds.ReadAsArray()
            plt.figure(120)
            plt.gcf().canvas.set_window_title(imagepath)
            plt.imshow(data)
            plt.axis('off')
            plt.show()
            DGISTMainWindow.metadataAct.setEnabled(False)
            DGISTMainWindow.histogramAct.setEnabled(False)


    def submit(self):
        self.bandRed=1
        self.bandGreen=1
        self.bandBlue=1
        band1setto=self.v1.get()
        if band1setto == 1:
            self.bandRed = self.selectedbnd1
        if band1setto == 2:
            self.bandGreen = self.selectedbnd1
        if band1setto == 3:
            self.bandBlue = self.selectedbnd1
        band2setto = self.v2.get()
        if band2setto == 4:
            self.bandRed = self.selectedbnd2
        if band2setto == 5:
            self.bandGreen = self.selectedbnd2
        if band2setto == 6:
            self.bandBlue = self.selectedbnd2
        band3setto = self.v3.get()
        if band3setto == 7:
            self.bandRed = self.selectedbnd3
        if band3setto == 8:
            self.bandGreen = self.selectedbnd3
        if band3setto == 9:
            self.bandBlue = self.selectedbnd3
        self.rgbImg = self.dsr_array[[int(self.bandRed), int(self.bandGreen), int(self.bandBlue)], :, :]
        data = np.dstack(self.rgbImg)
        plt.figure(120)
        plt.gcf().canvas.set_window_title(self.imagepath)
        plt.imshow(data)
        plt.axis('off')
        plt.show()
        plt.savefig('rgbbandimage.png')

    def band1Value(self, event):
        self.selectedbnd1=self.band1.get()

    def band2Value(self, event):
        self.selectedbnd2 = self.band2.get()

    def band3Value(self, event):
        self.selectedbnd3 = self.band3.get()

    def openMultiBandImage(self, ds):
        self.root = Tk()
        self.root.title("RGB Band Selection")
        self.root.geometry("500x300")
        frame = Frame(self.root, bg="white", width=500, height=300)
        labelHeader = Label(frame, text="RGB Band Selection", font=("SansSerif", 16))
        labelRed = Label(frame, text="Set Band", font=("SansSerif", 14))
        labelGreen = Label(frame, text="Set Band", font=("SansSerif", 14))
        labelBlue = Label(frame, text="Set Band", font=("SansSerif", 14))
        frame.pack()
        labelHeader.pack()
        labelHeader.place(x=150, y=20)
        labelRed.pack()
        labelRed.place(x=0, y=100)
        labelGreen.pack()
        labelGreen.place(x=0, y=150)
        labelBlue.pack()
        labelBlue.place(x=0, y=200)

        bndlst = []
        for band in range(ds.RasterCount):
            band += 1
            bndlst.append(band)

        band1_value = StringVar()
        self.band1 = ttk.Combobox(frame, textvariable=band1_value)
        self.band1.bind("<<ComboboxSelected>>", self.band1Value)
        self.band1['values'] = bndlst
        self.band1.current(0)
        self.band1.place(x=130, y=100)

        band2_value = StringVar()
        self.band2 = ttk.Combobox(frame, textvariable=band2_value)
        self.band2.bind("<<ComboboxSelected>>", self.band2Value)
        self.band2['values'] = bndlst
        self.band2.current(0)
        self.band2.place(x=130, y=150)

        band3_value = StringVar()
        self.band3 = ttk.Combobox(frame, textvariable=band3_value)
        self.band3.bind("<<ComboboxSelected>>", self.band3Value)
        self.band3['values'] = bndlst
        self.band3.current(0)
        self.band3.place(x=130, y=200)

        self.v1 = IntVar()
        self.v1.set(1)
        Radiobutton(frame, text="Red", variable=self.v1, value=1).place(x=300, y=100)
        Radiobutton(frame, text="Green", variable=self.v1, value=2).place(x=350, y=100)
        Radiobutton(frame, text="Blue", variable=self.v1, value=3).place(x=400, y=100)

        self.v2 = IntVar()
        self.v2.set(5)
        Radiobutton(frame, text="Red", variable=self.v2, value=4).place(x=300, y=150)
        Radiobutton(frame, text="Green", variable=self.v2, value=5).place(x=350, y=150)
        Radiobutton(frame, text="Blue", variable=self.v2, value=6).place(x=400, y=150)

        self.v3 = IntVar()
        self.v3.set(9)
        Radiobutton(frame, text="Red", variable=self.v3, value=7).place(x=300, y=200)
        Radiobutton(frame, text="Green", variable=self.v3, value=8).place(x=350, y=200)
        Radiobutton(frame, text="Blue", variable=self.v3, value=9).place(x=400, y=200)
        b = Button(frame, text="OK", command=self.submit)
        b.pack()
        b.place(x=200, y=250)
        self.root.mainloop()

    def metadata(self, DGISTMainWindow, imagepath):
        ds = gdal.Open(imagepath)
        self.imgbands=ds.RasterCount
        if self.imgbands>3:
            img=Image.open(os.getcwd() + '/rgbbandimage.png')
        else:
            img = Image.open(imagepath)
        root = Tk()
        root.title("Image Metadata")
        root.geometry("500x600")
        frame = Frame(root, bg="blue", width=500, height=600)
        label = Label(frame, text=img)
        frame.pack()
        label.pack()
        root.mainloop()

    def histogram(self, DGISTMainWindow, imagepath):
        ds = gdal.Open(imagepath)
        self.imgbands = ds.RasterCount
        if self.imgbands > 3:
            img = cv2.imread(os.getcwd() + '/rgbbandimage.png')
        else:
            img = cv2.imread(imagepath)
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.figure(121)
            plt.plot(histr, color=col)
            plt.xlim([0, 256])
        plt.gcf().canvas.set_window_title('Image Histogram')
        plt.legend(color, loc='best')
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
            self.statusBar().showMessage("Difference Image Creation: " + str(int(100.0 * i / rows_after)) + "%")

        self.statusBar().showMessage("Difference Image Created @ ")

        self.write_geotiff(outputImageName, flat_data, geo_transform, proj)

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


sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = my_exception_hook