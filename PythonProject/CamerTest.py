import cv2
import numpy as np
from PyQt4 import QtGui, QtCore

def startCapture(cap):
    print("pressed start")
    while(True):
        ret, frame = cap.read()
        cv2.imshow("Capture", frame)
        cv2.waitKey(5)
    cv2.destroyAllWindows() 

def endCapture(cap):
    print("pressed End")
    cv2.destroyAllWindows()

def quitCapture(cap):
    print("pressed Quit")
    cv2.destroyAllWindows()
    cap.release()
    QtCore.QCoreApplication.quit()

class Window(QtGui.QWidget):
    def __init__(self):

        c = cv2.VideoCapture(0)

        QtGui.QWidget.__init__(self)
        self.setWindowTitle('Control Panel')

        self.start_button = QtGui.QPushButton('Start',self)
        self.start_button.clicked.connect(lambda : startCapture(c, True))

        self.end_button = QtGui.QPushButton('End',self)
        self.end_button.clicked.connect(lambda : endCapture(c))

        self.quit_button = QtGui.QPushButton('Quit',self)
        self.quit_button.clicked.connect(lambda : quit(c))

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.end_button)
        vbox.addWidget(self.quit_button)

        self.setLayout(vbox)
        self.setGeometry(100,100,200,200)
        self.show()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
