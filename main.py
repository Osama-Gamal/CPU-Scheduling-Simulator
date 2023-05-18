from PyQt5 import QtWidgets, uic, QtGui
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QFileDialog, QPushButton, QDialog, QTableWidgetItem

from FCFS import FCFS
from NonPreemptive import NonPreemptive
from Preemptive import Preemptive
from RoundRobin import RoundRobin


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        uic.loadUi('CPUSchedulingWindow.ui', self)
        self.insertProcess.clicked.connect(self.insertNewProcessDialog)
        self.clearTableBtn.clicked.connect(self.clearTableData)
        self.calculateBtn.clicked.connect(self.calculateProcess)
        self.processTable.setColumnWidth(0, 40)
        self.processTable.verticalHeader().setFixedWidth(30)
        self.processTable.verticalHeader().setDefaultAlignment(Qt.AlignCenter)


        self.show()
    def insertNewProcessDialog(self):
        self.EditDialog = EditDialog(self)

    def clearTableData(self):
        self.processTable.setRowCount(0)
    def insertProcessInTable(self,arrivalTime,burstTime):
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignCenter)
        rowPosition = self.processTable.rowCount()
        self.processTable.insertRow(rowPosition)
        item.setData(Qt.EditRole, arrivalTime)
        self.processTable.setItem(rowPosition, 1, item)
        item2 = QTableWidgetItem()
        item2.setTextAlignment(Qt.AlignCenter)
        item2.setData(Qt.EditRole, burstTime)
        self.processTable.setItem(rowPosition, 2, item2)


    def calculateProcess(self):
        #print(self.algorithmBox.currentText())
        if(self.processTable.rowCount() > 0):
            if(self.algorithmBox.currentText() == 'First Come First Served'):
                fcfs = FCFS()
                fcfs.processData(self)
            elif self.algorithmBox.currentText() == 'Short Job First Preemptive':
                preemptive = Preemptive()
                preemptive.processData(self)
            elif self.algorithmBox.currentText() == 'Short Job First Non-Preemptive':
                nonPreemptive = NonPreemptive()
                nonPreemptive.processData(self)
            elif self.algorithmBox.currentText() == 'Round Robin':
                rr = RoundRobin()
                rr.processData(self)

        #print(self.processTable.item(0, 1).text())


class EditDialog(QtWidgets.QDialog):
    def __init__(self, mainWindow):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi('editDialog.ui', self)
        self.mainWindow = mainWindow
        self.show()

        self.dialogButtonBox.accepted.connect(self.insertIntoTable)

    def insertIntoTable(self):
        print(self.mainWindow)
        self.mainWindow.insertProcessInTable(self.arrivalTimeText.value(), self.burstTimeText.value())




app = QtWidgets.QApplication(sys.argv)
window = Ui()

app.exec_()
