import random

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FCFS:
    def processData(self, mainWindow):
        global originalWindow
        originalWindow = mainWindow
        process_data = []
        for i in range(0, mainWindow.processTable.rowCount()):
            temporary = []
            process_id = i

            arrival_time = mainWindow.processTable.item(i, 1).text()

            burst_time = mainWindow.processTable.item(i, 2).text()

            temporary.extend([int(process_id), int(arrival_time), int(burst_time)])
            process_data.append(temporary)
        FCFS.schedulingProcess(self, process_data)

    def schedulingProcess(self, process_data):
        process_data.sort(key=lambda x: x[1])

        '''
        Sort according to Arrival Time 
        '''
        start_time = []
        exit_time = []
        s_time = 0
        for i in range(len(process_data)):
            if s_time < process_data[i][1]:
                s_time = process_data[i][1]
            start_time.append(s_time)
            s_time = s_time + process_data[i][2]
            e_time = s_time
            exit_time.append(e_time)
            process_data[i].append(e_time)
        t_time = FCFS.calculateTurnaroundTime(self, process_data)
        w_time = FCFS.calculateWaitingTime(self, process_data)
        FCFS.printData(self, process_data, t_time, w_time)

    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][3] - process_data[i][1]
            '''
            turnaround_time = completion_time - arrival_time
            '''
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        average_turnaround_time = total_turnaround_time / len(process_data)
        '''
        average_turnaround_time = total_turnaround_time / no_of_processes
        '''
        return average_turnaround_time

    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i][4] - process_data[i][2]
            '''
            waiting_time = turnaround_time - burst_time
            '''
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        average_waiting_time = total_waiting_time / len(process_data)
        '''
        average_waiting_time = total_waiting_time / no_of_processes
        '''
        return average_waiting_time

    def printData(self, process_data, average_turnaround_time, average_waiting_time):

        print("Process_ID  Arrival_Time  Burst_Time  Completion_Time  Turnaround_Time  Waiting_Time")
        processIDs = [0]*originalWindow.processTable.rowCount()
        originalWindow.gnt.cla()
        originalWindow.gnt.grid(True)

        for i in range(len(process_data)):
            for j in range(len(process_data[i])):
                print(process_data[i][j], end="				")

                if (j == 0):
                    processIDs[i] = process_data[i][j]
                    if(i == 0):
                        originalWindow.gnt.broken_barh([(process_data[i][1], process_data[i][3])], (process_data[i][0]*10, 10),
                                                       facecolors=('tab:'+originalWindow.colorsChart[random.randrange(len(originalWindow.colorsChart))]))
                    else:
                        originalWindow.gnt.broken_barh([(process_data[i-1][3], process_data[i][2])], (process_data[i][0]*10, 10),
                                                       facecolors=('tab:'+originalWindow.colorsChart[random.randrange(len(originalWindow.colorsChart))]))



                if (j==3):
                    item2 = QTableWidgetItem()
                    item2.setTextAlignment(Qt.AlignCenter)
                    item2.setData(Qt.EditRole, process_data[i][j])
                    originalWindow.processTable.setItem(i, 3, item2)

                if (j==4):
                    item2 = QTableWidgetItem()
                    item2.setTextAlignment(Qt.AlignCenter)
                    item2.setData(Qt.EditRole, process_data[i][j])
                    originalWindow.processTable.setItem(i, 4, item2)

                if (j==5):
                    item2 = QTableWidgetItem()
                    item2.setTextAlignment(Qt.AlignCenter)
                    item2.setData(Qt.EditRole, process_data[i][j])
                    originalWindow.processTable.setItem(i, 5, item2)

            print()

        print(f'Average Turnaround Time: {average_turnaround_time}')

        print(f'Average Waiting Time: {average_waiting_time}')

        originalWindow.drawChartAverage(average_turnaround_time, average_waiting_time)

        yTicksArray = [i * 10 for i in processIDs]
        originalWindow.gnt.set_yticks(yTicksArray)
        originalWindow.gnt.set_yticklabels(processIDs)

        originalWindow.canvas = FigureCanvas(originalWindow.figure)
        originalWindow.toolbar = NavigationToolbar(originalWindow.canvas, originalWindow)

        for i in reversed(range(originalWindow.plotBox.count())):
            originalWindow.plotBox.itemAt(i).widget().setParent(None)
        originalWindow.plotBox.addWidget(originalWindow.toolbar)
        originalWindow.plotBox.addWidget(originalWindow.canvas)

