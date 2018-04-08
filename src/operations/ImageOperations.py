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
            DGISTMainWindow.metadataAct.setEnabled(True)
            DGISTMainWindow.histogramAct.setEnabled(True)
            self.openMultiBandImage(ds)
        elif len(lst) ==3:
            data = np.dstack(lst)
            plt.figure(DGISTMainWindow.imagecounter)
            plt.gcf().canvas.set_window_title(imagepath)
            plt.imshow(data)
            plt.axis('off')
            plt.show()
            DGISTMainWindow.metadataAct.setEnabled(True)
            DGISTMainWindow.histogramAct.setEnabled(True)
        else:
            data = ds.ReadAsArray()
            plt.figure(DGISTMainWindow.imagecounter)
            plt.gcf().canvas.set_window_title(imagepath)
            plt.imshow(data)
            plt.axis('off')
            plt.show()
            DGISTMainWindow.metadataAct.setEnabled(False)
            DGISTMainWindow.histogramAct.setEnabled(False)
        DGISTMainWindow.imagecounter=DGISTMainWindow.imagecounter+1

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
        frame = Frame(self.root, width=500, height=300)
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
#jhjhk
    def metadata(self, DGISTMainWindow, imagepath):

        self.meta_imgpath = imagepath
        ds = gdal.Open(self.meta_imgpath)

        self.meta_bands = ds.RasterCount
        band = ds.GetRasterBand(1)
        arr = band.ReadAsArray()
        self.meta_rows, self.meta_cols = arr.shape
        self.meta_imagesize = str(os.path.getsize(self.meta_imgpath))+" Bytes"
        self.meta_type = ((os.path.splitext(self.meta_imgpath)[1])[1:]).upper()

        ds = None

        self.meta_header = ["Image Path", "Size", "Type", "Columns", "Rows", "Bands"]

        self.rootMeta = Tk()
        self.rootMeta.title("Metadata Viewer")
        self.frameMeta = Frame(self.rootMeta)
        self.frameMeta.pack()

        labelHeader = Label(self.frameMeta, text="Metadata Viewer", font=("SansSerif", 20, "bold"))

        labelMetaimgpath = Label(self.frameMeta, text=self.meta_header[0], font=("SansSerif", 12))
        labelMetasize = Label(self.frameMeta, text=self.meta_header[1], font=("SansSerif", 12))
        labelMetatype = Label(self.frameMeta, text=self.meta_header[2], font=("SansSerif", 12))
        labelMetacols = Label(self.frameMeta, text=self.meta_header[3], font=("SansSerif", 12))
        labelMetarows = Label(self.frameMeta, text=self.meta_header[4], font=("SansSerif", 12))
        labelMetabnds = Label(self.frameMeta, text=self.meta_header[5], font=("SansSerif", 12))

        self.entryMetaimgpath = Entry(self.frameMeta, width=60, font=("SansSerif",  12, "bold"))
        self.entryMetasize = Entry(self.frameMeta, width=60, font=("SansSerif",  12, "bold"))
        self.entryMetatype = Entry(self.frameMeta, width=60, font=("SansSerif",  12, "bold"))
        self.entryMetacols = Entry(self.frameMeta, width=60, font=("SansSerif",  12, "bold"))
        self.entryMetarows = Entry(self.frameMeta, width=60, font=("SansSerif",  12, "bold"))
        self.entryMetabnds = Entry(self.frameMeta, width=60, font=("SansSerif",  12, "bold"))

        self.entryMetaimgpath.insert(0, self.meta_imgpath)
        self.entryMetasize.insert(0, self.meta_imagesize)
        self.entryMetatype.insert(0, self.meta_type)
        self.entryMetacols.insert(0, self.meta_cols)
        self.entryMetarows.insert(0, self.meta_rows)
        self.entryMetabnds.insert(0, self.meta_bands)

        self.entryMetaimgpath.configure(state="disabled")
        self.entryMetasize.configure(state="disabled")
        self.entryMetatype.configure(state="disabled")
        self.entryMetacols.configure(state="disabled")
        self.entryMetarows.configure(state="disabled")
        self.entryMetabnds.configure(state="disabled")

        btnExportmeta = Button(self.frameMeta, text="Export Metadata", font=("SansSerif", 14), command=self.save_metadata)

        labelHeader.grid(row=0, column=1, sticky=N, pady=25, padx=15)

        labelMetaimgpath.grid(row=1, column=0, sticky=W, pady=4, padx=5)
        labelMetasize.grid(row=2, column=0, sticky=W, pady=4, padx=5)
        labelMetatype.grid(row=3, column=0, sticky=W, pady=4, padx=5)
        labelMetacols.grid(row=4, column=0, sticky=W, pady=4, padx=5)
        labelMetarows.grid(row=5, column=0, sticky=W, pady=4, padx=5)
        labelMetabnds.grid(row=6, column=0, sticky=W, pady=4, padx=5)

        self.entryMetaimgpath.grid(row=1, column=1, sticky=W, pady=4, padx=5)
        self.entryMetasize.grid(row=2, column=1, sticky=W, pady=4, padx=5)
        self.entryMetatype.grid(row=3, column=1, sticky=W, pady=4, padx=5)
        self.entryMetacols.grid(row=4, column=1, sticky=W, pady=4, padx=5)
        self.entryMetarows.grid(row=5, column=1, sticky=W, pady=4, padx=5)
        self.entryMetabnds.grid(row=6, column=1, sticky=W, pady=4, padx=5)

        btnExportmeta.grid(row=8, column=1, sticky=S, pady=4)

        self.rootMeta.mainloop()

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
            plt.figure(DGISTMainWindow.histocounter)
            plt.plot(histr, color=col)
            plt.xlim([0, 256])
        plt.gcf().canvas.set_window_title('Image Histogram')
        plt.legend(color, loc='best')
        plt.show()
        DGISTMainWindow.histocounter=DGISTMainWindow.histocounter+1

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

    def select_image1_path(self):
        print "selecting image 1 path"
        self.image_t1, _ = QFileDialog.getOpenFileName(self, "Choose The Input Image 1", QDir.currentPath())
        if self.image_t1:
            self.entryImage1.delete(0, END)
            self.entryImage1.insert(0, self.image_t1)

    def select_image2_path(self):
        print "selecting image 2 path"
        self.image_t2, _ = QFileDialog.getOpenFileName(self, "Choose The Input Image 2", QDir.currentPath())
        if self.image_t2:
            self.entryImage2.delete(0, END)
            self.entryImage2.insert(0, self.image_t2)

    def select_image3_path(self):
        print "selecting image 3 path"
        self.image_t3, _ = QFileDialog.getOpenFileName(self, "Choose The Input Image 3", QDir.currentPath())
        if self.image_t3:
            self.entryImage3.delete(0, END)
            self.entryImage3.insert(0, self.image_t3)

    def select_image4_path(self):
        print "selecting image 4 path"
        self.image_t4, _ = QFileDialog.getOpenFileName(self, "Choose The Input Image 4", QDir.currentPath())
        if self.image_t4:
            self.entryImage4.delete(0, END)
            self.entryImage4.insert(0, self.image_t4)

    def select_image5_path(self):
        print "selecting image 5 path"
        self.image_t5, _ = QFileDialog.getOpenFileName(self, "Choose The Input Image 5", QDir.currentPath())
        if self.image_t5:
            self.entryImage5.delete(0, END)
            self.entryImage5.insert(0, self.image_t5)

    def select_image6_path(self):
        print "selecting image 6 path"
        self.image_t6, _ = QFileDialog.getOpenFileName(self, "Choose The Input Image 6", QDir.currentPath())
        if self.image_t6:
            self.entryImage6.delete(0, END)
            self.entryImage6.insert(0, self.image_t6)

    def run_change_detection(self):

        raster_before = gdal.Open(self.entryInitial.get(), gdal.GA_ReadOnly)
        raster_after = gdal.Open(self.entryFinal.get(), gdal.GA_ReadOnly)
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
        dataset = driver.Create(self.entryImgDiff.get(), cols, rows, 1, gdal.GDT_Byte)
        dataset.SetGeoTransform(geo_transform)
        # dataset.SetProjectionw(proj)
        band = dataset.GetRasterBand(1)
        band.WriteArray(flat_data)
        dataset = None

        ## view difference image
        plt.figure(120)
        plt.gcf().canvas.set_window_title(self.entryImgDiff.get())
        plt.imshow(flat_data)
        plt.axis('off')
        plt.show()

        self.btnViewReport.configure(state=NORMAL)

    def run_trend_calculator(self):

        print "inside trend calculator method"
        raster1 = gdal.Open(self.entryImage1.get(), gdal.GA_ReadOnly)
        raster2 = gdal.Open(self.entryImage2.get(), gdal.GA_ReadOnly)
        raster3 = gdal.Open(self.entryImage3.get(), gdal.GA_ReadOnly)
        raster4 = gdal.Open(self.entryImage4.get(), gdal.GA_ReadOnly)
        raster5 = gdal.Open(self.entryImage5.get(), gdal.GA_ReadOnly)
        raster6 = gdal.Open(self.entryImage6.get(), gdal.GA_ReadOnly)
        geo_transform = raster1.GetGeoTransform()
        # proj = raster_after.GetProjectionRef()

        band = raster1.GetRasterBand(1)
        band1 = band.ReadAsArray()
        band = raster2.GetRasterBand(1)
        band2 = band.ReadAsArray()
        band = raster3.GetRasterBand(1)
        band3 = band.ReadAsArray()
        band = raster4.GetRasterBand(1)
        band4 = band.ReadAsArray()
        band = raster5.GetRasterBand(1)
        band5 = band.ReadAsArray()
        band = raster6.GetRasterBand(1)
        band6 = band.ReadAsArray()

        rows, cols = band1.shape

        no_of_classes = 7
        no_of_images = 6

        self.trend_mat = np.zeros((no_of_classes, no_of_images), dtype=np.int)

        for i in range(rows):
            for j in range(cols):
                self.trend_mat[band1[i][j]][0] += 1
                self.trend_mat[band2[i][j]][1] += 1
                self.trend_mat[band3[i][j]][2] += 1
                self.trend_mat[band4[i][j]][3] += 1
                self.trend_mat[band5[i][j]][4] += 1
                self.trend_mat[band6[i][j]][5] += 1
            print str(int(100.0 * i / rows)) + "%"

        self.btnViewTrend.configure(state=NORMAL)
        self.btnPlotTrend.configure(state=NORMAL)

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

    def save_trend_report(self):

        self.metadata_report_path = QFileDialog.getSaveFileName(self, "Save Metadata", "", "Excel XLSX (*.xlsx);;Excel XLS (*.xls);;Text Files (*.txt)")[0]
        if self.metadata_report_path:
            workbook = xlsxwriter.Workbook(self.metadata_report_path)
            ws_trend = workbook.add_worksheet()

            ws_trend.write_string(1, 1, "Metadata")
            '''
            for i in range(0, 6):
                ws_trend.write_string(0, i + 1, self.image_names[i])

            for i in range(0, 7):
                ws_trend.write_string(i + 1, 0, self.classes[i])

            for col, data in enumerate(self.trend_mat):
                ws_trend.write_row(col + 1, 1, data)
            '''

    def save_metadata(self):

        print "Save metadata file"

        self.trend_report_path = QFileDialog.getSaveFileName(self, "Save Trend Report", "", "Excel XLSX (*.xlsx);;Excel XLS (*.xls);;Text Files (*.txt)")[0]
        if self.trend_report_path:
            workbook = xlsxwriter.Workbook(self.trend_report_path)
            ws_trend = workbook.add_worksheet()

            for i in range(0, 6):
                ws_trend.write_string(i + 1, 1, self.meta_header[i])

            ws_trend.write(1, 2, self.meta_imgpath)
            ws_trend.write(2, 2, self.meta_imagesize)
            ws_trend.write(3, 2, self.meta_type)
            ws_trend.write(4, 2, self.meta_cols)
            ws_trend.write(5, 2, self.meta_rows)
            ws_trend.write(6, 2, self.meta_bands)


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

    def view_trend(self):

        print "inside view trend method"

        self.rootTR = Tk()
        self.rootTR.title("Trend Report")
        self.frameTR = Frame(self.rootTR)
        self.frameTR.pack()

        self.classes = ["Class 0", "Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6"]
        self.image_names = ["Image 1", "Image 2", "Image 3", "Image 4", "Image 5", "Image 6"]

        btnSaveTrendReport = Button(self.frameTR, text="Save Trend Report", fg="blue",
                                   command=self.save_trend_report, bg="white", font=("SansSerif", 10, "bold"))
        btnSaveTrendReport.grid(row=0, column=0, sticky=E, pady=10, padx=5)

        Label(self.frameTR, text="          ", font=("SansSerif", 10, "bold")).grid(row=9, column=2, sticky=E, pady=0,
                                                                                     padx=0)
        Label(self.frameTR, text="          ", font=("SansSerif", 10, "bold")).grid(row=2, column=9, sticky=E, pady=0,
                                                                                     padx=0)

        for i in range(0, 6):
            Label(self.frameTR, text=self.image_names[i], width=12, font=("SansSerif", 10, "bold")).grid(row=0,
                                                                                                      column=i + 1,
                                                                                                      sticky=E, pady=0,
                                                                                                      padx=0)

        for i in range(0, 7):
            Label(self.frameTR, text=self.classes[i], width=12, font=("SansSerif", 10, "bold")).grid(row=i + 1,
                                                                                                      column=0,
                                                                                                      sticky=E, pady=0,
                                                                                                      padx=0)
            for j in range(0, 6):
                Button(self.frameTR, text=str(self.trend_mat[i][j]), bg="white", width=12,
                       font=("SansSerif", 10, "bold")).grid(row=i + 1, column=j + 1, sticky=E, pady=0, padx=0)

        self.rootTR.mainloop()

    def plot_trend(self):

        print "inside plot trend method"

        fig, ax = plt.subplots()
        plt.axis([0, 7, 0, np.amax(self.trend_mat)])
        ax.plot([1, 2, 3, 4, 5, 6], self.trend_mat[1,:], 'b', label='Class 1')
        ax.plot([1, 2, 3, 4, 5, 6], self.trend_mat[2, :], 'g', label='Class 2')
        ax.plot([1, 2, 3, 4, 5, 6], self.trend_mat[3, :], 'r', label='Class 3')
        ax.plot([1, 2, 3, 4, 5, 6], self.trend_mat[4, :], 'c', label='Class 4')
        ax.plot([1, 2, 3, 4, 5, 6], self.trend_mat[5, :], 'm', label='Class 5')
        ax.plot([1, 2, 3, 4, 5, 6], self.trend_mat[6, :], 'y', label='Class 6')

        ax.legend(loc='upper right', shadow=True)
        plt.xlabel('Image Number')
        plt.ylabel('Pixels per Class')
        plt.title('Trend Curve')
        plt.show()

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

    def trendCalculator(self):

        self.rootTC = Tk()
        self.rootTC.title("Trend Calculator")
        self.frameTC = Frame(self.rootTC)
        self.frameTC.pack()

        labelHeader = Label(self.frameTC, text="Trend Calculator", font=("SansSerif", 20, "bold"))

        labelImage1 = Label(self.frameTC, text="Image for Date 1", font=("SansSerif", 12))
        labelImage2 = Label(self.frameTC, text="Image for Date 2", font=("SansSerif", 12))
        labelImage3 = Label(self.frameTC, text="Image for Date 3", font=("SansSerif", 12))
        labelImage4 = Label(self.frameTC, text="Image for Date 4", font=("SansSerif", 12))
        labelImage5 = Label(self.frameTC, text="Image for Date 5", font=("SansSerif", 12))
        labelImage6 = Label(self.frameTC, text="Image for Date 6", font=("SansSerif", 12))

        self.entryImage1 = Entry(self.frameTC, width=70, font=("SansSerif", 12))
        self.entryImage2 = Entry(self.frameTC, width=70, font=("SansSerif", 12))
        self.entryImage3 = Entry(self.frameTC, width=70, font=("SansSerif", 12))
        self.entryImage4 = Entry(self.frameTC, width=70, font=("SansSerif", 12))
        self.entryImage5 = Entry(self.frameTC, width=70, font=("SansSerif", 12))
        self.entryImage6 = Entry(self.frameTC, width=70, font=("SansSerif", 12))

        btnChooseImage1 = Button(self.frameTC, text="Choose", font=("SansSerif", 12), command=self.select_image1_path)
        btnChooseImage2 = Button(self.frameTC, text="Choose", font=("SansSerif", 12), command=self.select_image2_path)
        btnChooseImage3 = Button(self.frameTC, text="Choose", font=("SansSerif", 12), command=self.select_image3_path)
        btnChooseImage4 = Button(self.frameTC, text="Choose", font=("SansSerif", 12), command=self.select_image4_path)
        btnChooseImage5 = Button(self.frameTC, text="Choose", font=("SansSerif", 12), command=self.select_image5_path)
        btnChooseImage6 = Button(self.frameTC, text="Choose", font=("SansSerif", 12), command=self.select_image6_path)

        btnRun = Button(self.frameTC, text="Run", font=("SansSerif", 14), command=self.run_trend_calculator)

        self.btnViewTrend = Button(self.frameTC, text="View Trend", font=("SansSerif", 14), command=self.view_trend)
        self.btnViewTrend.configure(state=DISABLED)

        self.btnPlotTrend = Button(self.frameTC, text="Plot Trend", font=("SansSerif", 14), command=self.plot_trend)
        self.btnPlotTrend.configure(state=DISABLED)

        labelHeader.grid(row=0, column=1, sticky=N, pady=25, padx=15)

        labelImage1.grid(row=1, column=0, sticky=W, pady=12, padx=5)
        labelImage2.grid(row=2, column=0, sticky=W, pady=12, padx=5)
        labelImage3.grid(row=3, column=0, sticky=W, pady=12, padx=5)
        labelImage4.grid(row=4, column=0, sticky=W, pady=12, padx=5)
        labelImage5.grid(row=5, column=0, sticky=W, pady=12, padx=5)
        labelImage6.grid(row=6, column=0, sticky=W, pady=12, padx=5)


        self.entryImage1.grid(row=1, column=1, sticky=W, pady=12, padx=5)
        self.entryImage2.grid(row=2, column=1, sticky=W, pady=12, padx=5)
        self.entryImage3.grid(row=3, column=1, sticky=W, pady=12, padx=5)
        self.entryImage4.grid(row=4, column=1, sticky=W, pady=12, padx=5)
        self.entryImage5.grid(row=5, column=1, sticky=W, pady=12, padx=5)
        self.entryImage6.grid(row=6, column=1, sticky=W, pady=12, padx=5)

        btnChooseImage1.grid(row=1, column=2, sticky=W, pady=12, padx=5)
        btnChooseImage2.grid(row=2, column=2, sticky=W, pady=12, padx=5)
        btnChooseImage3.grid(row=3, column=2, sticky=W, pady=12, padx=5)
        btnChooseImage4.grid(row=4, column=2, sticky=W, pady=12, padx=5)
        btnChooseImage5.grid(row=5, column=2, sticky=W, pady=12, padx=5)
        btnChooseImage6.grid(row=6, column=2, sticky=W, pady=12, padx=5)

        btnRun.grid(row=8, column=1, sticky=S, pady=12)
        self.btnViewTrend.grid(row=8, column=1, sticky=E, pady=12)
        self.btnPlotTrend.grid(row=8, column=1, sticky=W, pady=12)

        self.rootTC.mainloop()

sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = my_exception_hook