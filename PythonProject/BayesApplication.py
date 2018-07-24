import sys
import os
import argparse
import cv2
import numpy as np
import os.path
from matplotlib import pyplot as plt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QImage,QPainter, QBrush, QPen, QColor
from PyQt4.QtCore import QRect,Qt

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 1000, 700)
        self.setWindowTitle("BayesApp")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.jpg'))
        self.imgLabel = QtGui.QLabel(self)
        self.imgLabel.setGeometry(10,10,1000,500)
        self.rubberband = QtGui.QRubberBand(
            QtGui.QRubberBand.Rectangle, self)
        self.setMouseTracking(True)
        self.file = 0
        self.direct = 0
        self.statusBar()

        self.ImportData()
        self.home()

    def home(self):
        
        folderOpen = QtGui.QAction(QtGui.QIcon('SaveIcon.png'),'OpenFolder',self)
        folderOpen.triggered.connect(self.folder_open)
        self.toolBar = self.addToolBar("Open")
        self.toolBar.addAction(folderOpen)

        saveProgress = QtGui.QAction(QtGui.QIcon('exit.png'),'SaveProgress',self)
        saveProgress.triggered.connect(self.SaveProgress)
        self.toolBar = self.addToolBar("Save")
        self.toolBar.addAction(saveProgress)
        
        self.show()
        
    def new_window(self):
        if self.rubberband.isVisible():
            self.rubberband.hide()
            rect = self.rubberband.geometry()
        rectx = rect.x() - (510-(self.img.width()/2))
        recty = rect.y() - 85
        cropped = self.img.copy(QRect(rectx,recty,rect.width(),rect.height()))
        New = Secondary(self,cropped)
        New.show()
        
    def ImportData(self):
        if(os.path.isfile("Matrix.txt")):
            self.data = np.loadtxt("Matrix.txt",delimiter = ",")
        else:
            self.data = np.zeros(shape=(57,28))
        self.file = int(self.data[0,1])
    def ExportData(self):
        self.data[0,1] = self.file
        np.savetxt("Matrix.txt",self.data,fmt="%2.3f", delimiter=",")
        
    def folder_open(self):
        self.name = QtGui.QFileDialog.getExistingDirectory(self,'Select Directory')

        prevImage = QtGui.QAction(QtGui.QIcon('Arrow2.jpg'),'NextImage',self)
        prevImage.triggered.connect(self.prev_Image)
        self.toolBar = self.addToolBar("Prev")
        self.toolBar.addAction(prevImage)
        
        nextImage = QtGui.QAction(QtGui.QIcon('Arrow1.jpg'),'NextImage',self)
        nextImage.triggered.connect(self.next_Image)
        self.toolBar = self.addToolBar("Next")
        self.toolBar.addAction(nextImage)

        NewWindow = QtGui.QAction(QtGui.QIcon('Crop.png'),'EnlargeRegion',self)
        NewWindow.triggered.connect(self.new_window)
        self.toolBar = self.addToolBar("Enlarge")
        self.toolBar.addAction(NewWindow)

        self.file_open()
    def next_Image(self):
        self.direct = 0
        self.file_open()
        
    def prev_Image(self):
        self.direct = 1
        self.file_open()
        
    def file_open(self):
        filelist = os.listdir(self.name)
        if((filelist[self.file].endswith(".png") or filelist[self.file].endswith(".jpeg"))):
            self.img = QImage(os.path.join(self.name,filelist[self.file]))
            self.file += (1-self.direct)+ -1*(self.direct)
            self.paint_image(self.img)
            return
        else:
            self.file += (1-self.direct)+ -1*(self.direct)
            self.file_open()
        
        
    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberband.setGeometry(
            QtCore.QRect(self.origin, QtCore.QSize()))
        self.rubberband.show()
        QtGui.QWidget.mousePressEvent(self, event)
        
    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.setGeometry(
                QtCore.QRect(self.origin, event.pos()).normalized())
        QtGui.QWidget.mouseMoveEvent(self, event)
        
    def paint_image(self,image):
        self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
    def SaveProgress(self):
        self.file += (-1+self.direct)+ (self.direct)
        self.ExportData()
        
class Secondary(QtGui.QMainWindow):
    def __init__(self,parent,image):
        super(Secondary, self).__init__(parent)
        self.image=image
        self.setGeometry(50, 50, 500, 350)
        self.setWindowTitle("AnalysisWindow")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.jpg'))
        self.imgLabel = QtGui.QLabel(self)
        self.imgLabel.setGeometry(10,10,500,350)
        self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        self.meanArray = np.zeros(shape = (28,28))
        self.stdArray = np.zeros(shape = (28,28))
        self.count = 0
        
        self.home()
        
    def home(self):
        Analysis = QtGui.QAction(QtGui.QIcon('Analysis.png'),'PerformAnalysis',self)
        Analysis.triggered.connect(self.convertQImageToMat)
        self.toolBar = self.addToolBar("Analyse")
        self.toolBar.addAction(Analysis)
        self.show()
        
    def convertQImageToMat(self):
        incomingImage = self.image.convertToFormat(4)

        width = incomingImage.width()
        height = incomingImage.height()

        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height,width,4)
        gray_image = cv2.cvtColor(arr,cv2.COLOR_BGR2GRAY)

        resized = cv2.resize(gray_image, (28,28))
        self.PerformAnalysis(resized)
        
        cv2.imshow("image",resized)

    def PerformAnalysis(self,image):
        self.ImportData()
        if(self.count == 0):
            self.count = 1
            for i in range(28):
                for j in range(28):
                    self.meanArray[i,j] = image[i,j]
                    self.stdArray[i,j] = 0
        elif(self.count == 1):
            self.count = 2
            for i in range(28):
                for j in range(28):
                    oldMean = self.meanArray[i,j]
                    self.meanArray[i,j] = self.meanArray[i,j]+((image[i,j]-self.meanArray[i,j])/self.count)
                    self.stdArray[i,j] = np.std((oldMean,image[i,j]),ddof = 1)
        else:
            self.count += 1
            for i in range(28):
                for j in range(28):
                    self.stdArray[i,j] = ((((self.count-2)/(self.count-1))*(self.stdArray[i,j]**2))+((1/self.count)*((image[i,j]-self.meanArray[i,j])**2)))**(0.5)
                    self.meanArray[i,j] = self.meanArray[i,j]+((image[i,j]-self.meanArray[i,j])/self.count)
        print("image:")
        print(image[0,0], ',' , image[9,7],',',image[27,27])
        print("mean:")
        print(self.meanArray[0,0], ',' , self.meanArray[9,7],',',self.meanArray[27,27])
        print("std:")
        print(self.stdArray[0,0], ',' , self.stdArray[9,7],',',self.stdArray[27,27])
        


        self.ExportData()            
    def ImportData(self):
        if(os.path.isfile("Matrix.txt")):
            self.data = np.loadtxt("Matrix.txt",delimiter = ",")
        else:
            self.data = np.zeros(shape=(57,28))
        self.count = self.data[0,0]
        for i in range(1,57):
            for j in range(28):
                if(i<29):
                    self.meanArray[i-1,j] = self.data[i,j]
                else:
                    self.stdArray[i-29,j] = self.data[i,j]
    def ExportData(self):
        self.data[0,0] = self.count
        for i in range(1,57):
            for j in range(28):
                if(i<29):
                    self.data[i,j] = self.meanArray[i-1,j]
                else:
                    self.data[i,j] = self.stdArray[i-29,j]
        np.savetxt("Matrix.txt",self.data,fmt="%2.3f", delimiter=",")

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
