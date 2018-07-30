import sys  # provides interaction with the Python interpreter

from PyQt4 import QtGui  # provides the graphic elements
from PyQt4.QtCore import pyqtSlot  # provides the 'pyqtSlot()' decorator
from PyQt4.QtCore import Qt  # provides Qt identifiers


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # line edit
        line_edit = QtGui.QLineEdit()

        # connects the 'editingFinished()' signal with the 'editing_finished()' slot
        line_edit.editingFinished.connect(self.editing_finished)

        # label
        label = QtGui.QLabel('Press the ENTER key to finish editing.')
        label.setTextFormat(Qt.PlainText)

        # creates a vertical box layout for the window
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(line_edit)  # adds the line edit to the layout
        vlayout.addSpacing(10)  # 10 pixels space between the QLineEdit and QLabel widgets
        vlayout.addWidget(label)  # adds the label to the layout
        vlayout.addStretch()
        self.setLayout(vlayout)  # sets the window layout

    # 'editing_finished()' slot
    @pyqtSlot()
    def editing_finished(self):
        print('edition finished')  # prints a message on the console


# creates the application and takes arguments from the command line
application = QtGui.QApplication(sys.argv)

# creates the window and sets its properties
window = Window()
window.setWindowTitle('QLineEdit')  # title
window.resize(240, 60)  # size
window.show()  # shows the window

# runs the application and waits for its return value at the end
sys.exit(application.exec_())
