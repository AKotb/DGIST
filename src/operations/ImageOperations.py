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

    def write_geotiff(self, fname, data, geo_transform, projection, data_type=gdal.GDT_Byte):
        driver = gdal.GetDriverByName('GTiff')
        rows, cols = data.shape
        dataset = driver.Create(fname, self.cols, self.rows, 1, data_type)
        dataset.SetGeoTransform(geo_transform)
        dataset.SetProjectionw(projection)
        band = dataset.GetRasterBand(1)
        band.WriteArray(data)
        dataset = None
        return

    def select_initial_path(self):
        print "selecting initial path"
        self.image1, _ = QFileDialog.getOpenFileName(self, "Choose The Input Initial Image", QDir.currentPath())
        if self.image1:
            self.entryInitial.delete(0, END)
            self.entryInitial.insert(0, self.image1)

    def select_final_path(self):
        print "selecting final path"
        self.image2, _ = QFileDialog.getOpenFileName(self, "Choose The Input Final Image", QDir.currentPath())
        if self.image2:
            self.entryFinal.delete(0, END)
            self.entryFinal.insert(0, self.image2)

    def select_img_diff_path(self):
        print "selecting image difference path"
        self.image3 = QFileDialog.getSaveFileName(self, "Choose The Output Image Difference", "", "TIF Image (*.tif);;PNG Image (*.png);;BMP Image (*.bmp);;JPG Image (*.jpg);;Text Files (*.txt)")[0]
        if self.image3:
            self.entryImgDiff.delete(0, END)
            self.entryImgDiff.insert(0, self.image3)

    def run_change_detection(self):

        raster_before = gdal.Open(self.image1, gdal.GA_ReadOnly)
        raster_after = gdal.Open(self.image2, gdal.GA_ReadOnly)
        geo_transform = raster_after.GetGeoTransform()
        #proj = raster_after.GetProjectionRef()

        band = raster_before.GetRasterBand(1)
        bands_before = band.ReadAsArray()

        band = raster_after.GetRasterBand(1)
        bands_after = band.ReadAsArray()
        rows_after, cols_after = bands_after.shape

        flat_data = bands_after.reshape((rows_after, cols_after))

        self.change_mat = np.zeros((7, 7), dtype=np.int)

        for i in range(rows_after):
            for j in range(cols_after):
                self.change_mat[bands_before[i][j]][bands_after[i][j]] += 1
                flat_data[i][j] = 7 * (bands_before[i][j]) + (bands_after[i][j]) + 1
            print str(int(100.0 * i / rows_after))+"%"

        ## write difference image into the output path
        driver = gdal.GetDriverByName('GTiff')
        rows, cols = flat_data.shape
        dataset = driver.Create(self.image3, cols, rows, 1, gdal.GDT_Byte)
        dataset.SetGeoTransform(geo_transform)
        # dataset.SetProjectionw(proj)
        band = dataset.GetRasterBand(1)
        band.WriteArray(flat_data)
        dataset = None

        ## view difference image
        plt.figure(120)
        plt.gcf().canvas.set_window_title(self.image3)
        plt.imshow(flat_data)
        plt.axis('off')
        plt.show()

        self.btnViewReport.configure(state=NORMAL)

    def save_statistical_report(self):

        self.report_path = QFileDialog.getSaveFileName(self, "Save Change Detection Report", "", "Excel XLSX (*.xlsx);;Excel XLS (*.xls);;Text Files (*.txt)")[0]
        if self.report_path:
            workbook = xlsxwriter.Workbook(self.report_path)
            ws_stat = workbook.add_worksheet()

            for i in range(0, 7):
                ws_stat.write_string(0, i + 1, self.classes[i])
                ws_stat.write_string(i + 1, 0, self.classes[i])

            for col, data in enumerate(self.change_mat):
                ws_stat.write_column(1, col + 1, data)

    def view_change_detection_report(self):

        self.rootCDR = Tk()
        self.rootCDR.title("Statistical Report")
        self.frameCDR = Frame(self.rootCDR)
        self.frameCDR.pack()

        header_names = ["State No.", "BEFORE", "AFTER", "# of pixels", "Percent (%)"]
        self.classes = ["Class 0", "Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6"]

        btnSaveStatReport = Button(self.frameCDR, text="Save Statistical Report", fg="blue", command=self.save_statistical_report, bg="white", font=("SansSerif", 10, "bold"))
        btnSaveStatReport.grid(row=0, column=0, sticky=E, pady=10, padx=5)

        Label(self.frameCDR, text="          ", font=("SansSerif", 10, "bold")).grid(row=9, column=2, sticky=E, pady=0, padx=0)
        Label(self.frameCDR, text="          ", font=("SansSerif", 10, "bold")).grid(row=2, column=9, sticky=E, pady=0,padx=0)

        for i in range(0, 7):
            Label(self.frameCDR, text=self.classes[i], width=12, font=("SansSerif", 10, "bold")).grid(row=0, column=i+1, sticky=E, pady=0, padx=0)

        for i in range(0, 7):
            Label(self.frameCDR, text=self.classes[i], width=12, font=("SansSerif", 10, "bold")).grid(row=i+1, column=0,sticky=E, pady=0, padx=0)
            for j in range(0, 7):
                Button(self.frameCDR, text=str(self.change_mat[i][j]), bg="white", width=12, font=("SansSerif", 10, "bold")).grid(row=i+1, column=j+1, sticky=E, pady=0, padx=0)

        self.rootCDR.mainloop()

    def changeDetection(self):

        self.rootCD = Tk()
        self.rootCD.title("Change Detection Process")
        self.frameCD = Frame(self.rootCD)
        self.frameCD.pack()

        labelHeader = Label(self.frameCD, text="Change Detection Process", font=("SansSerif", 20, "bold"))
        labelInitial = Label(self.frameCD, text="Input Initial Image", font=("SansSerif", 12))
        labelFinal = Label(self.frameCD, text="Input Final Image", font=("SansSerif", 12))
        labelImgDiff = Label(self.frameCD, text="Output Difference Image", font=("SansSerif", 12))

        self.entryInitial = Entry(self.frameCD, width=70, font=("SansSerif", 12))
        self.entryFinal = Entry(self.frameCD, width=70, font=("SansSerif", 12))
        self.entryImgDiff = Entry(self.frameCD, width=70, font=("SansSerif", 12))

        btnChooseInitial = Button(self.frameCD, text="Choose", font=("SansSerif", 12), command=self.select_initial_path)
        btnChooseFinal = Button(self.frameCD, text="Choose", font=("SansSerif", 12), command=self.select_final_path)
        btnChooseImgDiff = Button(self.frameCD, text="Choose", font=("SansSerif", 12), command=self.select_img_diff_path)
        btnRun = Button(self.frameCD, text="Run", font=("SansSerif", 14), command=self.run_change_detection)
        self.btnViewReport = Button(self.frameCD, text="View Report", font=("SansSerif", 14), command=self.view_change_detection_report)
        self.btnViewReport.configure(state=DISABLED)

        labelHeader.grid(row=0, column=1, sticky=N, pady=25, padx=15)
        labelInitial.grid(row=1, column=0, sticky=W, pady=12, padx=5)
        labelFinal.grid(row=2, column=0, sticky=W, pady=12, padx=5)
        labelImgDiff.grid(row=3, column=0, sticky=W, pady=12, padx=5)

        self.entryInitial.grid(row=1, column=1, sticky=W, pady=12, padx=5)
        self.entryFinal.grid(row=2, column=1, sticky=W, pady=12, padx=5)
        self.entryImgDiff.grid(row=3, column=1, sticky=W, pady=12, padx=5)

        btnChooseInitial.grid(row=1, column=2, sticky=W, pady=12, padx=5)
        btnChooseFinal.grid(row=2, column=2, sticky=W, pady=12, padx=5)
        btnChooseImgDiff.grid(row=3, column=2, sticky=W, pady=12, padx=5)
        btnRun.grid(row=5, column=1, sticky=S, pady=12)
        self.btnViewReport.grid(row=5, column=1, sticky=E, pady=12)

        self.rootCD.mainloop()

sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = my_exception_hook