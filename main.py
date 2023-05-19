import random

import matplotlib
from PyQt5 import QtWidgets, uic, QtGui
import sys
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QFileDialog, QPushButton, QDialog, QTableWidgetItem
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from FCFS import FCFS
from NonPreemptive import NonPreemptive
from Preemptive import Preemptive
from RoundRobin import RoundRobin


class Ui(QtWidgets.QMainWindow):


    def __init__(self):
        super(Ui, self).__init__()

        self.colorsChart = ['red', 'blue', 'orange', 'green', 'cyan', 'purple', 'brown']

        uic.loadUi('CPUSchedulingWindow.ui', self)
        self.insertProcess.clicked.connect(self.insertNewProcessDialog)
        self.clearTableBtn.clicked.connect(self.clearTableData)
        self.calculateBtn.clicked.connect(self.calculateProcess)
        self.removeProcessBtn.clicked.connect(self.removeProcess)
        self.modifyDataBtn.clicked.connect(self.modifyData)
        self.processTable.setColumnWidth(0, 40)
        self.processTable.verticalHeader().setFixedWidth(30)
        self.processTable.verticalHeader().setDefaultAlignment(Qt.AlignCenter)



        self.figure, self.gnt = plt.subplots()
        self.gnt.set_ylim(0, 50)
        self.gnt.set_xlim(0, 50)
        self.gnt.set_xlabel('Seconds Since Start')
        self.gnt.set_ylabel('Process ID')
        self.gnt.set_yticks([15, 25, 35])
        self.gnt.set_yticklabels(['1', '2', '3'])
        self.gnt.grid(True)
        plt.rcParams["font.size"] = 7


        # fig.show()

        #self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.plotBox.addWidget(self.toolbar)
        self.plotBox.addWidget(self.canvas)

        self.drawChartAverage(0,0)






        self.show()

    def plot(self):
        data = [random.random() for i in range(10)]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*-')
        self.canvas.draw()

    def drawChartAverage(self,AverageTurnaround,AverageWaiting):
        for i in reversed(range(self.plotBox2.count())):
            self.plotBox2.itemAt(i).widget().setParent(None)

        self.fig, ax = plt.subplots()
        chartsLabels = ['Turnaround', 'Waiting']
        counts = [AverageTurnaround, AverageWaiting]
        bar_labels = ['Turnaround', 'Waiting']
        bar_colors = ['tab:orange', 'tab:blue']
        ax.bar(chartsLabels, counts, label=bar_labels, color=bar_colors)
        ax.set_ylabel('Time Chart')
        ax.set_title('Time Chart')
        ax.legend(title='Chart Keys')
        self.canvas2 = FigureCanvas(self.fig)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        # self.plotBox2.addWidget(self.toolbar2)
        self.plotBox2.addWidget(self.canvas2)

    def insertNewProcessDialog(self):
        isModify = False
        self.EditDialog = EditDialog(self,isModify)

    def clearTableData(self):
        self.processTable.setRowCount(0)
    def removeProcess(self):
        self.processTable.removeRow(self.processTable.currentRow())

    def modifyData(self):
        if(self.processTable.currentRow() != -1):
            isModify = True
            self.EditDialog = EditDialog(self,isModify)

    def insertProcessInTable(self,isModify,arrivalTime,burstTime):
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignCenter)

        if(isModify == True):
            rowPosition = self.processTable.currentRow()
        else:
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
    def __init__(self, mainWindow,isModify):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi('editDialog.ui', self)
        self.mainWindow = mainWindow
        self.show()
        self.isModify = isModify

        self.dialogButtonBox.accepted.connect(self.insertIntoTable)
        if (self.isModify == True):
            selectedRow = self.mainWindow.processTable.currentRow()
            self.arrivalTimeText.setValue(int(self.mainWindow.processTable.item(selectedRow, 1).text()))
            self.burstTimeText.setValue(int(self.mainWindow.processTable.item(selectedRow, 2).text()))


    def insertIntoTable(self):
        if (self.isModify == True):
            self.mainWindow.insertProcessInTable(self.isModify,self.arrivalTimeText.value(), self.burstTimeText.value())
        else:
            self.mainWindow.insertProcessInTable(self.isModify,self.arrivalTimeText.value(), self.burstTimeText.value())





app = QtWidgets.QApplication(sys.argv)
window = Ui()

app.exec_()
