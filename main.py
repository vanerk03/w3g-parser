import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QWidget
from PyQt5.uic import loadUi
from Eapm import eapm

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.__replayname = ""
        self.findreplay.clicked.connect(self.browse)
        self.analyze.clicked.connect(self.display_results)

    def browse(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'Warcraft III replay',  '(*.w3g)')
        self.filename.setText(fname[0])
        self.__replayname = fname[0]
    
    def display_results(self):
        lst_of_players = eapm(self.__replayname)

        

app = QApplication(sys.argv)
app.setApplicationName("EPM Analyzer")

mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()

widget.addWidget(mainwindow)
widget.setFixedWidth(400)
widget.setFixedHeight(300)

widget.show()

sys.exit(app.exec_())
