import random

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Preemptive:

    def processData(self, mainWindow):
        process_data = []
        global originalWindow
        originalWindow = mainWindow
        for i in range(0, mainWindow.processTable.rowCount()):
            temporary = []
            process_id = i
            arrival_time = mainWindow.processTable.item(i, 1).text()
            burst_time = mainWindow.processTable.item(i, 2).text()
            temporary.extend([int(process_id), int(arrival_time), int(burst_time), 0, int(burst_time)])
            '''
            '0' is the state of the process. 0 means not executed and 1 means execution complete
            '''
            process_data.append(temporary)
        Preemptive.schedulingProcess(self, process_data)

    def schedulingProcess(self, process_data):
        start_time = []
        exit_time = []
        s_time = 0
        sequence_of_process = []
        process_data.sort(key=lambda x: x[1])
        '''
        Sort processes according to the Arrival Time
        '''
        while 1:
            ready_queue = []
            normal_queue = []
            temp = []
            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    ready_queue.append(temp)
                    temp = []
                elif process_data[i][3] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    normal_queue.append(temp)
                    temp = []
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                '''
                Sort processes according to Burst Time
                '''

                start_time.append(s_time)
                s_time = s_time + 1
                e_time = s_time
                exit_time.append(e_time)
                sequence_of_process.append(ready_queue[0][0])
                for k in range(len(process_data)):
                    if process_data[k][0] == ready_queue[0][0]:
                        #print(process_data[k][0]+1,'Start In ', s_time)

                        break
                process_data[k][2] = process_data[k][2] - 1
                if process_data[k][2] == 0:  # If Burst Time of a process is 0, it means the process is completed
                    process_data[k][3] = 1
                    process_data[k].append(e_time)
            if len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                start_time.append(s_time)
                s_time = s_time + 1
                e_time = s_time
                exit_time.append(e_time)
                sequence_of_process.append(normal_queue[0][0])
                for k in range(len(process_data)):
                    if process_data[k][0] == normal_queue[0][0]:
                        break
                process_data[k][2] = process_data[k][2] - 1
                if process_data[k][2] == 0:  # If Burst Time of a process is 0, it means the process is completed
                    process_data[k][3] = 1
                    process_data[k].append(e_time)
        t_time = Preemptive.calculateTurnaroundTime(self, process_data)
        w_time = Preemptive.calculateWaitingTime(self, process_data)
        Preemptive.printData(self, process_data, t_time, w_time, sequence_of_process)

    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][5] - process_data[i][1]
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
            waiting_time = process_data[i][6] - process_data[i][4]
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

    def printData(self, process_data, average_turnaround_time, average_waiting_time, sequence_of_process):
        process_data.sort(key=lambda x: x[0])

        '''
        Sort processes according to the Process ID
        '''
        '''print(
            "Process_ID  Arrival_Time  Rem_Burst_Time      Completed  Orig_Burst_Time Completion_Time  Turnaround_Time  Waiting_Time")
'''

        processIDs = [0] * originalWindow.processTable.rowCount()
        originalWindow.gnt.cla()
        originalWindow.gnt.grid(True)

        for i in range(len(process_data)):
            for j in range(len(process_data[i])):
                #print(process_data[i][j], end="\t\t\t\t")

                if (j == 0):
                    processIDs[i] = process_data[i][j]
                    self.getTimeSequence(sequence_of_process, process_data, i)

                if (j == 5):
                    item2 = QTableWidgetItem()
                    item2.setTextAlignment(Qt.AlignCenter)
                    item2.setData(Qt.EditRole, process_data[i][j])
                    originalWindow.processTable.setItem(i, 3, item2)

                if (j == 6):
                    item2 = QTableWidgetItem()
                    item2.setTextAlignment(Qt.AlignCenter)
                    item2.setData(Qt.EditRole, process_data[i][j])
                    originalWindow.processTable.setItem(i, 4, item2)

                if (j == 7):
                    item2 = QTableWidgetItem()
                    item2.setTextAlignment(Qt.AlignCenter)
                    item2.setData(Qt.EditRole, process_data[i][j])
                    originalWindow.processTable.setItem(i, 5, item2)
            '''print()
            
            print(f'Average Turnaround Time: {average_turnaround_time}')

            print(f'Average Waiting Time: {average_waiting_time}')

            print(f'Sequence of Process: {sequence_of_process}')'''

        print(sequence_of_process,"Start IN: ", )





        yTicksArray = [i * 10 for i in processIDs]
        originalWindow.gnt.set_yticks(yTicksArray)
        originalWindow.gnt.set_yticklabels(processIDs)

        originalWindow.canvas = FigureCanvas(originalWindow.figure)
        originalWindow.toolbar = NavigationToolbar(originalWindow.canvas, originalWindow)

        for i in reversed(range(originalWindow.plotBox.count())):
            originalWindow.plotBox.itemAt(i).widget().setParent(None)
        originalWindow.plotBox.addWidget(originalWindow.toolbar)
        originalWindow.plotBox.addWidget(originalWindow.canvas)



    def getTimeSequence(self,sequence_of_process, process_data,PID):
        doOnce = False

        for i in range(len(sequence_of_process)):
            if (sequence_of_process[i] == PID):
                if (doOnce == False):
                    startIn = process_data[0][1] + i
                    #print("Start In: ", startIn)
                    doOnce = True
                if (doOnce == True and i == len(sequence_of_process) - 1):
                    endIn = process_data[0][1] + i + 1
                    #print(" End In: ", endIn)
                    originalWindow.gnt.broken_barh([(startIn, endIn-startIn)],
                                                   (process_data[PID][0] * 10, 10),
                                                   facecolors=('tab:' + originalWindow.colorsChart[
                                                       random.randrange(len(originalWindow.colorsChart))]))

            else:
                if (doOnce == True):
                    endIn = process_data[0][1] + i
                    #print(" End In: ", endIn)
                    doOnce = False
                    originalWindow.gnt.broken_barh([(startIn, endIn-startIn)],
                                                   (process_data[PID][0] * 10, 10),
                                                   facecolors=('tab:' + originalWindow.colorsChart[
                                                       random.randrange(len(originalWindow.colorsChart))]))



