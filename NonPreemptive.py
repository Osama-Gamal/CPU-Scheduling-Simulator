import random

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class NonPreemptive:

    def processData(self, mainWindow):
        process_data = []
        global originalWindow
        originalWindow = mainWindow
        for i in range(0, mainWindow.processTable.rowCount()):
            temporary = []
            process_id = i

            arrival_time = mainWindow.processTable.item(i, 1).text()

            burst_time = mainWindow.processTable.item(i, 2).text()
            temporary.extend([int(process_id), int(arrival_time), int(burst_time), 0])
            '''
            '0' is the state of the process. 0 means not executed and 1 means execution complete
            '''
            process_data.append(temporary)
        NonPreemptive.schedulingProcess(self, process_data)

    def schedulingProcess(self, process_data):
        start_time = []
        exit_time = []
        s_time = 0
        sequence_of_process = []
        process_data.sort(key=lambda x: x[1])
        '''
        Sort processes according to the Arrival Time
        '''
        for i in range(len(process_data)):
            ready_queue = []
            temp = []
            normal_queue = []

            for j in range(len(process_data)):
                if (process_data[j][1] <= s_time) and (process_data[j][3] == 0):
                    temp.extend([process_data[j][0], process_data[j][1], process_data[j][2]])
                    ready_queue.append(temp)
                    temp = []
                elif process_data[j][3] == 0:
                    temp.extend([process_data[j][0], process_data[j][1], process_data[j][2]])
                    normal_queue.append(temp)
                    temp = []

            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                '''
                Sort the processes according to the Burst Time
                '''
                start_time.append(s_time)
                s_time = s_time + ready_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                sequence_of_process.append(ready_queue[0][0])
                for k in range(len(process_data)):
                    if process_data[k][0] == ready_queue[0][0]:
                        '''print(process_data[k][0]+1, 'Start IN ' , s_time,' End In ', s_time)
                        print(start_time)'''
                        break
                process_data[k][3] = 1
                process_data[k].append(e_time)

            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                start_time.append(s_time)
                s_time = s_time + normal_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                sequence_of_process.append(normal_queue[0][0])

                for k in range(len(process_data)):
                    if process_data[k][0] == normal_queue[0][0]:
                        break
                process_data[k][3] = 1
                process_data[k].append(e_time)

        t_time = NonPreemptive.calculateTurnaroundTime(self, process_data)
        w_time = NonPreemptive.calculateWaitingTime(self, process_data)
        NonPreemptive.printData(self, process_data, t_time, w_time,sequence_of_process,start_time,exit_time)


    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][4] - process_data[i][1]
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
            waiting_time = process_data[i][5] - process_data[i][2]
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

    def printData(self, process_data, average_turnaround_time, average_waiting_time,sequence_of_process,start_time,exit_time):
        process_data.sort(key=lambda x: x[0])
        '''
        Sort processes according to the Process ID
        '''
        #print("Process_ID  Arrival_Time  Burst_Time      Completed  Completion_Time  Turnaround_Time  Waiting_Time")

        processIDs = [0] * originalWindow.processTable.rowCount()
        originalWindow.gnt.cla()
        originalWindow.gnt.grid(True)

        for i in range(len(process_data)):
            for j in range(len(process_data[i])):
                #print(process_data[i][j], end="				")

                if (j == 0):
                    processIDs[i] = process_data[i][j]
                    print(start_time)
                    originalWindow.gnt.broken_barh([(start_time[i], exit_time[i] - start_time[i])],
                                                   (process_data[i][0] * 10, 10),
                                                   facecolors=('tab:' + originalWindow.colorsChart[
                                                       random.randrange(len(originalWindow.colorsChart))]))


                if (j == 4):
                    item2 = QTableWidgetItem()
                    item2.setTextAlignment(Qt.AlignCenter)
                    item2.setData(Qt.EditRole, process_data[i][j])
                    originalWindow.processTable.setItem(i, 3, item2)

                if (j == 5):
                    item2 = QTableWidgetItem()
                    item2.setTextAlignment(Qt.AlignCenter)
                    item2.setData(Qt.EditRole, process_data[i][j])
                    originalWindow.processTable.setItem(i, 4, item2)

                if (j == 6):
                    item2 = QTableWidgetItem()
                    item2.setTextAlignment(Qt.AlignCenter)
                    item2.setData(Qt.EditRole, process_data[i][j])
                    originalWindow.processTable.setItem(i, 5, item2)
            print()

        print(f'Average Turnaround Time: {average_turnaround_time}')

        print(f'Average Waiting Time: {average_waiting_time}')

        #print('Process Sequence',sequence_of_process)

        originalWindow.drawChartAverage(average_turnaround_time, average_waiting_time)

        yTicksArray = [i * 10 for i in processIDs]
        originalWindow.gnt.set_yticks(yTicksArray)
        processIDsIncreased = [i + 1 for i in processIDs]
        originalWindow.gnt.set_yticklabels(processIDsIncreased)

        originalWindow.canvas = FigureCanvas(originalWindow.figure)
        originalWindow.toolbar = NavigationToolbar(originalWindow.canvas, originalWindow)

        for i in reversed(range(originalWindow.plotBox.count())):
            originalWindow.plotBox.itemAt(i).widget().setParent(None)
        originalWindow.plotBox.addWidget(originalWindow.toolbar)
        originalWindow.plotBox.addWidget(originalWindow.canvas)
