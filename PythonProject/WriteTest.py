import sys
import os
import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QImage,QPainter, QBrush, QPen, QColor
from PyQt4.QtCore import QRect,Qt
import os.path

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 1000, 700)
        self.setWindowTitle("BayesApp")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.jpg'))
        self.imgLabel = QtGui.QLabel(self)
        self.imgLabel.setGeometry(10,10,1000,500)
        self.statusBar()
        self.name = None
        self.file = 0
        self.direct = 0
        self.classList = [None]
        
        self.home()

    def home(self):
        folderOpen = QtGui.QAction(QtGui.QIcon('SaveIcon.png'),'OpenFolder',self)
        folderOpen.triggered.connect(self.folder_open)
        self.toolBar = self.addToolBar("Open")
        self.toolBar.addAction(folderOpen)

        self.line_edit = QtGui.QLineEdit()
        #self.line_edit.editingFinished.connect(self.addList)

        label = QtGui.QLabel('Press the ENTER key to finish editing.')
        label.setTextFormat(Qt.PlainText)

        self.toolBar.addWidget(self.line_edit)  
        self.toolBar.addWidget(label)

        Analyse = QtGui.QAction(QtGui.QIcon('Analysis.png'),'Analyse',self)
        Analyse.triggered.connect(self.addList)
        self.toolBar = self.addToolBar("Analyse")
        self.toolBar.addAction(Analyse)
        
        self.show()

    def folder_open(self):
        self.name =  QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")

        prevImage = QtGui.QAction(QtGui.QIcon('Arrow2.jpg'),'NextImage',self)
        prevImage.triggered.connect(self.prev_Image)
        self.toolBar = self.addToolBar("Prev")
        self.toolBar.addAction(prevImage)
        
        nextImage = QtGui.QAction(QtGui.QIcon('Arrow1.jpg'),'NextImage',self)
        nextImage.triggered.connect(self.next_Image)
        self.toolBar = self.addToolBar("Next")
        self.toolBar.addAction(nextImage)       

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
            self.file += (1-self.direct)+ -1*(self.direct)
            self.img = QImage(os.path.join(self.name,filelist[self.file]))
            self.paint_image(self.img)
            return
        else:
            self.file += (1-self.direct)+ -1*(self.direct)
            self.file_open()
                
           
    def paint_image(self,image):
        self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        
    def addList(self):
        if(self.line_edit.text()not in self.classList):
            if(self.classList[0] == None):
                self.classList[0] = self.line_edit.text()
            else:
                self.classList.append(self.line_edit.text())
        print(self.classList)
        
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
