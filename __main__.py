import sys
from PyQt4 import QtGui
import os
import group_class
import json
import regexify
from PyQt4.QtCore import*


class OpenFileWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OpenFileWindow, self).__init__()

        self.okButton = QtGui.QPushButton("OK")
        self.cancelButton = QtGui.QPushButton("Cancel")

        self.openFileBtn = QtGui.QPushButton("Choose File Path")
        self.openFileBtn.move(20, 20)
        self.openFileBtn.clicked.connect(self.get_file_path)

        self.pathDisplay = QtGui.QLineEdit(self)
        self.pathDisplay.resize(250,25)
        self.pathDisplay.move(130, 22)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.openFileBtn, 1, 1)
        grid.addWidget(self.pathDisplay, 2, 1)

        grid.addWidget(self.okButton, 1, 0)
        grid.addWidget(self.cancelButton,2 , 0)
        self.connect(self.okButton, SIGNAL("clicked()"), self.clicked)
        self.cancelButton.clicked.connect(QCoreApplication.instance().quit)
        self.setLayout(grid)

        self.setGeometry(500, 250, 500, 100)
        self.setWindowTitle("Regexifier")

    def clicked(self):
        of = open("groups.json", "w")
        of.write(json.dumps(group_class.groups_to_file(self.pathDisplay.text(), None, None), indent=2, sort_keys=True))
        of.close()
        regexify.run()
        QtGui.QMessageBox.about(self, "Program is Done", "The Program Has finished running, The results are now located in the file 'PROGRAM_OUTPUT.csv', any URL groups with errors are in the 'REJECTS_REGEX.txt' file, and had their Regex column marked with a msg to check the rejects file")
        QCoreApplication.instance().quit()

    def get_file_path(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                  os.getcwd(), "*.csv")
        if fname:
            self.pathDisplay.setText(fname)


class App(QtGui.QApplication):
    def __init__(self, *args):
        QtGui.QApplication.__init__(self, *args)
        self.main = OpenFileWindow()
        self.connect(self, SIGNAL("lastWindowClosed()"), self.byebye )
        self.main.show()

    def byebye( self ):
        self.exit(0)


def main(args):
    try:
        global app
        app = App(args)
        app.exec_()
    except:
        pass
if __name__ == '__main__':
    main(sys.argv)