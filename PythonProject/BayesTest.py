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
import random
import math
import scipy.stats

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
        self.prob = []
        self.classList = []
        self.total = 0
        self.count = 0
        self.numclass = 0
        self.numtrain = 0
        self.numtest = 0
        self.currclass = 0
        self.testclass = 0
        self.normalize = 0
        self.meanArray = np.zeros(shape = (28,28))
        self.stdArray = np.zeros(shape = (28,28))
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
        self.numclass = 2
        self.numtrain = 10
        self.numtest = 10
        image = np.zeros(shape = (28,28))
        self.testdata = np.zeros(shape = (56*self.numclass,28))

        for i in range(self.numclass*56):
            for j in range(28):
                self.testdata[i,j] = random.randint(1,10)
        print("test data")
        for i in range(self.numclass):
            print("Class",(i+1))
            print(1+(i*56))
            print(self.testdata[1+(i*56),0])
            print(self.testdata[11+(i*56),0])
            print(self.testdata[29+(i*56),0])
            print(self.testdata[39+(i*56),0])
        
        for i in range(self.numtrain):
            if(i%2==0):
                self.currclass = 1
                #random.randint(0,self.numclass-1)
            else:
                self.currclass = 0
            for j in range(28):
                for k in range(28): 
                    image[j,k] = np.random.normal(self.testdata[j+(56*(self.currclass)),k],self.testdata[j+28+(56*(self.currclass)),k])
            self.PerformAnalysis(image)
            print("Class")
            print(self.currclass)
            print("image")
            print(image[1,0])
            print(image[11,0])
            print("learned data")
            for k in range(self.numclass):
                print("Class",(k+1))
                print(2+(k*56))
                print(self.data[2+(k*56),0])
                print(self.data[12+(k*56),0])
                print(self.data[30+(k*56),0])
                print(self.data[40+(k*56),0])
        for i in range(self.numtest):
            self.testclass = random.randint(0,self.numclass-1)
            for j in range(28):
                for k in range(28):
                    image[j,k] = np.random.normal(self.testdata[j+(56*self.testclass),k],self.testdata[j+28+(56*self.testclass),k])
            self.Prediction(image)
            #print(self.testclass)
##            for i in range(self.numclass):
##                if(self.prob[i] == max(self.prob)):
##                    #print(i)
            #print(self.prob)
            
        
    def Prediction(self,image):
        self.ImportData()

        for i in range(self.numclass):
            self.total += self.data[0,i+1]
            for j in range(28):
                for k in range(28):
                    mean = self.data[j+1+(i*56),k]
                    std = self.data[j+29+(i*56),k]
                    if(i+1>len(self.prob)):
                        self.prob.append(0)
                        Norm2 = scipy.stats.norm(mean,std).cdf(image[j,k]+0.5)
                        Norm1 = scipy.stats.norm(mean,std).cdf(image[j,k]-0.5)
                        self.prob[i] = math.log10(Norm2-Norm1)
                    else:
                        Norm2 = scipy.stats.norm(mean,std).cdf(image[j,k]+0.5)
                        Norm1 = scipy.stats.norm(mean,std).cdf(image[j,k]-0.5)
                        self.prob[i] = self.prob[i]+math.log10(Norm2-Norm1)
                              
        for i in range(self.numclass):
            self.prob[i] = self.prob[i] + math.log10(self.data[0,i+1]/self.total)
        self.Normalize()
            
    def Normalize(self):
        total = 0
        cutoff = math.log10(10**-16)-math.log10(self.numclass)
        maximum = max(self.prob)
        for i in range(self.numclass):
            self.prob[i] = self.prob[i] - maximum
            if(self.prob[i]<cutoff):
                self.prob[i] = 0
            self.prob[i] = math.exp(self.prob[i])
            total += self.prob[i]
        for i in range(self.numclass):
            self.prob[i] = self.prob[i]/total

            
        
    def ImportData(self):
        
        if(os.path.isfile("Matrix.txt")):
            self.data = np.loadtxt("Matrix.txt",delimiter = ",")
        else:
            self.data = np.zeros(shape=((self.numclass*56)+1,28))
            
        self.count = self.data[0,self.currclass+1]

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
                    self.meanArray[i,j] = (self.meanArray[i,j]+image[i,j])/self.count
                    self.stdArray[i,j] = np.std((oldMean,image[i,j]),ddof = 1)
        else:
            self.count += 1
            for i in range(28):
                for j in range(28):
                    self.stdArray[i,j] = np.sqrt(((self.count-2)/(self.count-1))*(self.stdArray[i,j]**2)+((1/self.count)*((image[i,j]-self.meanArray[i,j])**2)))
                    self.meanArray[i,j] = self.meanArray[i,j]+((image[i,j]-self.meanArray[i,j])/self.count)
        self.ExportData()
        
    def ExportData(self):
        self.data[0,self.currclass+1] = self.count
        for i in range(1,57):
            for j in range(28):
                if(i<29):
                    self.data[i+(56*(self.currclass)),j] = self.meanArray[i-1,j]
                else:
                    self.data[i+(56*(self.currclass)),j] = self.stdArray[i-29,j]
        
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

        Prediction = QtGui.QAction(QtGui.QIcon('Prediction.png'),'Predict',self)
        Prediction.triggered.connect(self.Prediction)
        self.toolBar = self.addToolBar("Prediction")
        self.toolBar.addAction(Prediction)

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
        file = self.file + (-1+self.direct)+ (self.direct)
        self.ImportData()
        self.file = file
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
        self.classList = []
        self.count = 0
        self.label = 0
        
        self.home()
        
    def home(self):

        Analyse = QtGui.QAction(QtGui.QIcon('Analysis.png'),'Analyse',self)
        Analyse.triggered.connect(self.convertQImageToMat)
        self.toolBar = self.addToolBar("Analyse")
        self.toolBar.addAction(Analyse)
        self.line_edit = QtGui.QLineEdit()
        

        label = QtGui.QLabel('Press the ENTER key to finish labeling.')
        label.setTextFormat(Qt.PlainText)

        self.toolBar.addWidget(self.line_edit)  
        self.toolBar.addWidget(label)
        
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

                    if((i==0 and j == 0) or (i==9 and j==7) or (i==27 and j==27)):
                        print(oldMean)
        else:
            self.count += 1
            for i in range(28):
                for j in range(28):
                    self.stdArray[i,j] = ((((self.count-2)/(self.count-1))*(self.stdArray[i,j]**2))+((1/self.count)*((image[i,j]-self.meanArray[i,j])**2)))**(0.5)
                    self.meanArray[i,j] = self.meanArray[i,j]+((image[i,j]-self.meanArray[i,j])/self.count)
        print(self.label)
        print("image:")
        print(image[0,0], ',' , image[9,7],',',image[27,27])
        print("mean:")
        print(self.meanArray[0,0], ',' , self.meanArray[9,7],',',self.meanArray[27,27])
        print("std:")
        print(self.stdArray[0,0], ',' , self.stdArray[9,7],',',self.stdArray[27,27])

        self.ExportData()            
    def ImportData(self):
        with open('listfile.txt','r') as filehandle:
            for line in filehandle:
                currentClass = line[:-1]
                self.classList.append(currentClass)
            for entry in self.classList:
                if(entry == ''):
                    del(self.classList[0])
                
        if(os.path.isfile("Matrix.txt")):
            self.data = np.loadtxt("Matrix.txt",delimiter = ",")
        else:
            self.data = np.zeros(shape=(57,28))

        self.addList()
        
        
        
        if((len(self.data)-1)<len(self.classList*56)):
           extra = np.zeros(shape = (56,28))
           self.data = np.concatenate((self.data,extra),0)
           print(len(self.data)-1)
           print(len(self.classList*56))
              
        self.count = self.data[0,self.label]
        for i in range(1,57):
            for j in range(28):
                if(i<29):
                    self.meanArray[i-1,j] = self.data[i+(56*(self.label-1)),j]
                else:
                    self.stdArray[i-29,j] = self.data[i+(56*(self.label-1)),j]
        
    def ExportData(self):
        with open('listfile.txt','w') as filehandle:
            for listitem in self.classList:
                if(listitem != ''):
                    filehandle.write('%s\n' % listitem)

        self.data[0,self.label] = self.count
        for i in range(1,57):
            for j in range(28):
                if(i<29):
                    self.data[i+(56*(self.label-1)),j] = self.meanArray[i-1,j]
                else:
                    self.data[i+(56*(self.label-1)),j] = self.stdArray[i-29,j]
        np.savetxt("Matrix.txt",self.data,fmt="%2.3f", delimiter=",")

                
    def addList(self):
        if(self.line_edit.text()not in self.classList):
            self.classList.append(self.line_edit.text())
            self.label = len(self.classList)
        else:
            for i in range(len(self.classList)):
                if(self.classList[i] == self.line_edit.text()):
                    self.label = i+1
        print(self.classList)
            

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
