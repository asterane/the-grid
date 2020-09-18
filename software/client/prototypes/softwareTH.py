import sys, time, threading
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QColorDialog, QSlider, QLabel, QPushButton, QToolButton, QLineEdit, QInputDialog, QMainWindow, QComboBox, QShortcut
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QColor, QImage, QPixmap, QKeySequence
import re
import mainwindow

gridExists = True

if gridExists:
    import gridClient

rgb = [0, 0, 0]
selectedButtons = []
selectedRows = []
selectedCols = []
cueList = []
editMode = True
cueFileName = "cues.txt"
#cueFileName = "cues.txt"
colorButton = None
doneButton = None
editTrue = True
s = None
colorDialog = None
currentCue = -1
editingCue = None
sideWidgets = []
sendRow = []
sendCol = []
sendR = []
sendG = []
sendB = []

setCubeColor = threading.Event()
threadRunning = False

timeInterval = 0.2
runGrid = []
shortcutLeft = None
shortcutRight = None
shortcutUp = None
shortcutDown = None
runTransition = True

#jump to will show grid or animation IMMEDIATELY, no transition because you could be going there from anywhere
#run will show back, next, pause / start
#changing the cue number checks to make sure they're ordered right and reorders them in the list if not and then re-calls "put cues in thing"

def sendCubeColor():
    #call the grid
    global sendRow
    global sendCol
    global sendR
    global sendG
    global sendB

    while True:
        setCubeColor.wait()
        gridClient.sendColor(s, sendRow, sendCol, sendR, sendG, sendB, len(sendRow))
        print("sent to the grid")
        sendRow = []
        sendCol = []
        sendR = []
        sendG = []
        sendB = []
        setCubeColor.clear()
        
class TransitionWorker(QThread):
    def __init__(self, firstGrid, cue, jump):
        QThread.__init__(self)
        self.firstGrid = firstGrid
        self.cue = cue
        self.jump = jump
    
    def playTransition(self, firstGrid, cue):
        global runGrid
        global setCubeColor
        type = cue.transType
        lastGrid = cue.firstGrid
        length = cue.translen
        if type == "Fade":
            currentTime = timeInterval
            steps = int(length / timeInterval)
            for s in range(steps): #add one to s when using it because it'll start at 0
                for r in range(6):
                    for c in range(10):
                        if not runTransition:
                            break
                        #minFirstRGB = min(firstGrid[r][c][0] / 255.0, firstGrid[r][c][1] / 255.0, firstGrid[r][c][2] / 255.0)
                        #firsth = 0
                        #firsts = 0
                        #firstv = 0
                        
                        diffR = lastGrid[r][c][0] - firstGrid[r][c][0]
                        diffG = lastGrid[r][c][1] - firstGrid[r][c][1]
                        diffB = lastGrid[r][c][2] - firstGrid[r][c][2]
                        stepR = diffR / steps
                        stepG = diffG / steps
                        stepB = diffB / steps
                        newR = int(firstGrid[r][c][0] + stepR * (s + 1))
                        newG = int(firstGrid[r][c][1] + stepG * (s + 1))
                        newB = int(firstGrid[r][c][2] + stepB * (s + 1))
                        #self.changeColorStrange(r, c, newR, newG, newB)
                        sendRow.append(r)
                        sendCol.append(c)
                        sendR.append(newR)
                        sendG.append(newG)
                        sendB.append(newB)
                        #time.sleep(0.2)
                    if not runTransition:
                        break
                if not runTransition:
                    break
                setCubeColor.set()
                time.sleep(timeInterval)
                currentTime = currentTime + timeInterval
        elif type == "Bottom":
            interval = length / 6
            for r in range(5, -1): 
                for c in range(10):
                    newR = lastGrid[r][c][0]
                    newG = lastGrid[r][c][1]
                    newB = lastGrid[r][c][2]
                    #self.changeColorStrange(r, c, newR, newG, newB)
                    sendRow.append(r)
                    sendCol.append(c)
                    sendR.append(newR)
                    sendG.append(newG)
                    sendB.append(newB)
                    #time.sleep(0.2)
                setCubeColor.set()
                time.sleep(timeInterval)
                currentTime = currentTime + timeInterval
        elif type == "Left":
            interval = length / 10
            for c in range(10): 
                for r in range(6):
                    newR = lastGrid[r][c][0]
                    newG = lastGrid[r][c][1]
                    newB = lastGrid[r][c][2]
                    #self.changeColorStrange(r, c, newR, newG, newB)
                    sendRow.append(r)
                    sendCol.append(c)
                    sendR.append(newR)
                    sendG.append(newG)
                    sendB.append(newB)
                    #time.sleep(0.2)
                setCubeColor.set()
                time.sleep(timeInterval)
                currentTime = currentTime + timeInterval
        elif type == "Right":
            interval = length / 10
            for c in range(9, -1): 
                for r in range(6):
                    newR = lastGrid[r][c][0]
                    newG = lastGrid[r][c][1]
                    newB = lastGrid[r][c][2]
                    #self.changeColorStrange(r, c, newR, newG, newB)
                    sendRow.append(r)
                    sendCol.append(c)
                    sendR.append(newR)
                    sendG.append(newG)
                    sendB.append(newB)
                    #time.sleep(0.2)
                setCubeColor.set()
                time.sleep(timeInterval)
                currentTime = currentTime + timeInterval                

    def run(self):
        global threadRunning
        threadRunning = True
        self.playTransition(self.firstGrid, self.cue)
        self.jump(self.cue)
        threadRunning = False
        
    def stop(self):
        global threadRunning
        self.jump(self.cue)
        threadRunning = False
        self.terminate()
        
class Button():
    def __init__(self, row, col, layout, layoutWidget, mainUI, grid, changeButton, initRGB):
        #QtWidgets.QPushButton.__init__("", self.ui.gridLayoutWidget_2, self)
        #super().__init__("", self.ui.gridLayoutWidget_2)
        self.row = row
        self.col = col
        self.button = QToolButton(layoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(initRGB[0], initRGB[1], initRGB[2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.button.setPalette(palette)
        layout.addWidget(self.button, self.row, self.col, 1, 1)
        #self.button.clicked.connect(lambda: mainUI.changeColor(self.button, self.row, self.col, grid))
        self.button.clicked.connect(lambda: mainUI.addClickedButton(self, changeButton))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
            
        global runGrid
        for r in range(6):
            runRow = []
            runGrid.append(runRow)
            for c in range(10):
                button = QPushButton(self.ui.gridLayoutWidget_4)
                palette = QtGui.QPalette()
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
                button.setPalette(palette)
                runRow.append(button)
                button.hide()
        
        self.ui.pushButton_6.hide()
        self.ui.pushButton_7.hide()
        self.ui.pushButton_8.hide()
        
        self.ui.horizontalSlider.hide()
        self.ui.pushButton_13.hide()
        self.ui.pushButton_14.hide()
        
        global shortcutRight
        shortcutRight = QShortcut(self.ui.tab)
        shortcutRight.setKey(QKeySequence(Qt.Key_Right))
        shortcutRight.activated.connect(self.nextCue)
        
        global shortcutUp
        shortcutUp = QShortcut(self.ui.tab)
        shortcutUp.setKey(QKeySequence(Qt.Key_Up))
        shortcutUp.activated.connect(lambda: self.jumpToSolid(cueList[currentCue]))
        
        global shortcutLeft
        shortcutLeft = QShortcut(self.ui.tab)
        shortcutLeft.setKey(QKeySequence(Qt.Key_Left))
        shortcutLeft.activated.connect(self.back)
        
        global shortcutDown
        shortcutDown = QShortcut(self.ui.tab)
        shortcutDown.setKey(QKeySequence(Qt.Key_Down))
        shortcutDown.activated.connect(self.interrupt)
        
        self.toEditMode()
        
        global colorDialog
        colorDialog = QColorDialog(self.ui.tab_2)
        '''e a s t e r   e g g'''
        self.readFromFile()
        
        #cueList.append(Cue())
                
        #self.ui.setWindowState(Qt.WindowMinimized)
        #self.ui.showMaximized()
        #self.ui.MainWindow.showMaximized()
        
        #self.ui.pushButton_1.clicked.connect(self.updateSecondRow)
        #self.ui.lineEdit_11.textChanged.connect(self.updateSecondRow)
        
        #push = QtWidgets.QPushButton("Additional Button 1", self.ui.gridLayoutWidget)
        #self.ui.gridLayout.addWidget(push, 4, 0, 2, 3)
        
        #read cues in from file
        #self.readFromFile("cues.txt", grid)
        
        self.ui.pushButton_2.clicked.connect(self.addRow)
        
        scrollArea = QtWidgets.QScrollArea(self.ui.tab) #stupid workaround :(
        scrollArea.setEnabled(True)
        scrollArea.setGeometry(QtCore.QRect(40, 30, 291, 211))
        scrollArea.setGeometry(self.ui.gridLayoutWidget.geometry())
        scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        scrollArea.setWidgetResizable(True)
        scrollArea.setObjectName("scrollArea")
        scrollArea.setWidget(self.ui.gridLayoutWidget)
        
        self.ui.pushButton.setEnabled(False) 
        
        grid = []
        for r in range (6):
            row = []
            grid.append(row)
            for c in range (10):
                button = Button(r, c, self.ui.gridLayout_2, self.ui.gridLayoutWidget_2, self, grid, self.ui.pushButton, [0, 0, 0])
                row.append(button)

                
        self.ui.gridLayout_2.setVerticalSpacing(0)
        #self.ui.gridLayout_2.setRowStretch(0, 5)
        
        self.ui.pushButton.clicked.connect(lambda: self.changeColor(grid, self.ui.pushButton, self.ui.gridLayout_2, self.ui.gridLayout_3, self.ui.gridLayoutWidget_3))

        self.ui.pushButton_3.clicked.connect(self.jumpToNothing)
                        
        #selRows = []
        #selCols = []
        #selButtons = []
        #grid = [] #makes grid of buttons
        #for r in range (6):
            #row = []
            #grid.append(row)
            #for c in range (10):
                #button = QtWidgets.QPushButton("", self.ui.gridLayoutWidget_2)
                #self.ui.gridLayout_2.addWidget(button, r, c, 1, 1)
                #row.append(button)
                #if r == 0 and c == 0:
                    #grid[r][c].clicked.connect(lambda: self.changeColor(0, 0, grid[0][0])) #will all be lists
                    #button.clicked.connect(lambda: self.addClickedButton(selRows, selCols, selButtons, 0, 0, button))
                #elif r == 1 and c == 1:
                    #grid[r][c].clicked.connect(lambda: self.changeColor(1, 1, grid[1][1])) #will all be lists
                #else:
                    #grid[r][c].clicked.connect(lambda: self.changeColor(r, c, grid[r][c])) #will all be lists
    
    def interrupt(self):
        global runTransition
        global threadRunning
        runTransition = False
        if threadRunning:
            self.transThread.stop()
            threadRunning = False
    
    def back(self):
        if currentCue == 0:
            self.jumpToNothing()
        elif currentCue > 0:
            self.jumpToSolid(cueList[currentCue - 1])
    
    def sort(self):
        global cueList
        tempCueList = cueList.copy()
        tempCueList.sort(key = lambda cue: cue.numShown)
        for k in range(len(tempCueList)):
            tempCueList[k].index = k + 1
            #if not tempCueList[k].animtrue:
                #cueList[k] = Cue(self, tempCueList[k].numShown, tempCueList[k].index, tempCueList[k].label, tempCueList[k].animtrue, tempCueList[k].firstGrid, tempCueList[k].transType, tempCueList[k].translen)
        cueList = tempCueList.copy()
        self.removeAllCues()
        self.addAllCues()
        
    def removeAllCues(self):
        for cue in cueList:
            cue.remove()
                
    def addAllCues(self):
        for cue in cueList:
            cue.add()
    
    def jumpToNothing(self):
        global setCubeColor
        if not editMode:
            global currentCue
            currentCue = -1
            self.ui.label_9.setText(str(currentCue + 1))
            for r in range (6):
                for c in range (10):
                    palette = QtGui.QPalette()
                    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
                    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
                    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
                    runGrid[r][c].setPalette(palette)
                    sendRow.append(r)
                    sendCol.append(c)
                    sendR.append(0)
                    sendG.append(0)
                    sendB.append(0)
            setCubeColor.set()
    
    def nextCue(self):
        global runTransition 
        runTransition = True
        global currentCue
        offGrid = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        #print(currentCue)
        if currentCue < len(cueList) - 1:
            currentCue = currentCue + 1
            if cueList[currentCue].transType != "None":
                if currentCue == 0:
                    self.playTransition(offGrid, cueList[currentCue])
                else:
                    self.playTransition(cueList[currentCue - 1].lastGrid, cueList[currentCue])
        if cueList[currentCue].transType == "None":
                self.jumpToSolid(cueList[currentCue])
        
    def playTransition(self, firstGrid, cue):
        self.transThread = TransitionWorker(firstGrid, cue, self.jumpToSolid)
        self.transThread.start()
        
    def changeColorStrange(self, r, c, R, G, B):
        global runGrid
        #print("begin")
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        runGrid[r][c].setPalette(palette)
        #print("end")
    
    def jumpToSolid(self, cue):
        global currentCue
        global runGrid
        global setCubeColor
        if not editMode:
            #show it in the top grid and send it to the grid
            for r in range (6):
                for c in range (10):
                    currentCue = cue.index - 1
                    self.ui.label_9.setText(str(cue.numShown))
                    initRGB = cue.firstGrid[r][c]
                    palette = QtGui.QPalette()
                    brush = QtGui.QBrush(QtGui.QColor(initRGB[0], initRGB[1], initRGB[2]))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
                    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
                    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
                    runGrid[r][c].setPalette(palette)
                    sendRow.append(r)
                    sendCol.append(c)
                    sendR.append(initRGB[0])
                    sendG.append(initRGB[1])
                    sendB.append(initRGB[2])
            setCubeColor.set()
            
    def delete(self):
        input = QInputDialog(self.ui.tab)
        input.setLabelText("Which cue would you like to delete?")
        input.setOkButtonText("Delete")
        input.setComboBoxEditable(False)
        names = []
        for cue in cueList:
            names.append(cue.label)
        input.setComboBoxItems(names)
        index = input.getItem(self.ui.tab, "", "Which cue would you like to delete?", names, 0, False)
        index = names.index(index[0])
        self.removeAllCues()
        del cueList[index]
        for k in range(len(cueList)):
            cueList[k].index = k + 1
        self.addAllCues()
        
    def duplicate(self):
        input = QInputDialog(self.ui.tab)
        input.setLabelText("Which cue would you like to duplicate?")
        input.setOkButtonText("Duplicate")
        input.setComboBoxEditable(False)
        names = []
        for cue in cueList:
            names.append(cue.label)
        input.setComboBoxItems(names)
        index = input.getItem(self.ui.tab, "", "Which cue would you like to duplicate?", names, 0, False)
        index = names.index(index[0])
        tempGrid = []
        for r in range(6):
            row = []
            tempGrid.append(row)
            for c in range(10):
                col = cueList[index].firstGrid[r][c].copy()
                row.append(col)
                
        cue = Cue(self, cueList[len(cueList) - 1].numShown + 1, len(cueList) + 1, cueList[index].label + "*", cueList[index].animtrue, tempGrid, cueList[index].transType, cueList[index].translen)
        if cueList[index].animtrue: #CHANGE TO A BETTER COPY!!!
            cue.anim = cueList[index].anim.copy()
        if cueList[index].transType == "Custom":
            cue.trans = cueList[index].trans.copy()
        cueList.append(cue)
        cue.add()
    
    def toRunMode(self):
        global editMode
        global shortcut
        editMode = False
        self.ui.pushButton_5.setEnabled(True)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_5.clicked.connect(self.toEditMode)
        self.ui.pushButton_4.disconnect()
        self.ui.pushButton_9.show()
        self.ui.pushButton_10.hide()
        self.ui.pushButton_9.clicked.connect(self.nextCue)
        self.ui.pushButton_10.disconnect()
        self.ui.pushButton_11.hide()
        self.ui.pushButton_11.disconnect()
        self.ui.pushButton_12.hide()
        self.ui.pushButton_12.disconnect()
        shortcutLeft.activated.connect(self.back)
        shortcutRight.activated.connect(self.nextCue)
        shortcutUp.activated.connect(lambda: self.jumpToSolid(cueList[currentCue]))
        shortcutDown.activated.connect(self.interrupt)
        #add all the buttons
        for r in range(6):
            for c in range(10):
                self.ui.gridLayout_4.addWidget(runGrid[r][c], r, c, 1, 1)
                runGrid[r][c].show()
        
    def toEditMode(self):
        global editMode
        global shortcut
        editMode = True
        self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_4.setEnabled(True)
        self.ui.pushButton_4.clicked.connect(self.toRunMode)
        self.ui.pushButton_5.disconnect()
        self.ui.pushButton_9.hide()
        self.ui.pushButton_10.show()
        self.ui.pushButton_10.clicked.connect(self.saveToFile)
        self.ui.pushButton_9.disconnect()
        self.ui.pushButton_11.show()
        self.ui.pushButton_11.clicked.connect(self.delete)
        self.ui.pushButton_12.show()
        self.ui.pushButton_12.clicked.connect(self.duplicate)
        shortcutRight.disconnect()
        shortcutUp.disconnect()
        shortcutLeft.disconnect()
        shortcutDown.disconnect()
        #remove all the buttons
        for r in range(6):
            for c in range(10):
                self.ui.gridLayout_4.removeWidget(runGrid[r][c])
                runGrid[r][c].hide()
    
    def saveToFile(self):
        f = open(cueFileName, "w")
        if f.mode == "w":
            for k in range(len(cueList)):
                cue = cueList[k]
                #print cue 
                if cue.animtrue:
                    #print animation
                    f.write("A")
                    f.write(str(cue.numShown))
                    f.write(":")
                    f.write(cue.label)
                    f.write(":")
                    f.write(str(cue.animlen))
                    f.write(":")
                    #finish anim
                else:
                    #print static
                    f.write("S")
                    f.write(str(cue.numShown))
                    f.write(":")
                    f.write(cue.label)
                    f.write(":")
                    for r in range(6):
                        for c in range(10):
                            f.write(("{}.{}.{}").format(cue.firstGrid[r][c][0], cue.firstGrid[r][c][1], cue.firstGrid[r][c][2]))
                            if c != 9:
                                f.write(",")
                        if r != 5:
                            f.write("R")
                f.write(" ")
                #print trans
                if cue.transType == "None":
                    f.write("N")
                elif cue.transType == "Fade":
                    f.write("F")
                    f.write(str(cue.translen))
                elif cue.transType == "Bottom":
                    f.write("B")
                    f.write(str(cue.translen))
                elif cue.transType == "Left":
                    f.write("L")
                    f.write(str(cue.translen))
                elif cue.transType == "Right":
                    f.write("R")
                    f.write(str(cue.translen))
                else:
                    f.write("C")
                    f.write(str(cue.translen))
                    f.write(":")
                    #finish trans
                if k != len(cueList) - 1:
                    f.write(" ")
    
    def hideGridEdit(self, grid):
        self.ui.pushButton_6.hide()
        self.ui.pushButton_7.hide()
        self.ui.pushButton_8.hide()
        for r in range(6):
            for c in range(10):
                grid[r][c].button.hide()
                
        self.ui.gridLayout_6.removeWidget(colorButton)
        self.ui.gridLayout_6.removeWidget(doneButton)
   
    def editGrid(self):
        #testbutton = QPushButton("hi", window)
        #window.addWidget(testbutton)
        #change widgets on the side to add a color picker (when in edit mode, clicking jump to will show it on the top one 
        #when in show mode, clicking grid or trans will show it in the bottom one because the top one will be for the current setWindowState
        #when in edit mode, clicking grid or trans will show it in the top one and you can either just see it or drag the slider
        self.ui.pushButton_6.show()
        self.ui.pushButton_6.setEnabled(False) 
        self.ui.pushButton_7.show()
        self.ui.pushButton_8.show()
        
        grid = []
        for r in range(6):
            row = []
            grid.append(row)
            for c in range(10):
                initRGB = editingCue.firstGrid[r][c]
                button = Button(r, c, self.ui.gridLayout_4, self.ui.gridLayoutWidget_4, self, grid, self.ui.pushButton_6, initRGB)
                row.append(button)
        
        self.ui.pushButton_6.clicked.connect(lambda: self.changeColor(grid, self.ui.pushButton_6, self.ui.gridLayout_4, self.ui.gridLayout_6, self.ui.gridLayoutWidget_6))
        self.ui.pushButton_7.clicked.connect(lambda: self.hideGridEdit(grid))
        self.ui.pushButton_8.clicked.connect(lambda: self.selectAll(grid, self.ui.pushButton_6))
        
    def editAnim(self):
        self.ui.horizontalSlider.show()
        
    def addRow(self):
        item = QInputDialog.getItem(self.ui.tab, "", "Static or Animation?", ["Static", "Animation"], 0, False)
        anim = True
        if item[0] == "Static":
            anim = False
        
        num = 1
        offGrid = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        if len(cueList) != 0:
            num = cueList[len(cueList) - 1].numShown + 1
        cue = Cue(self, num, len(cueList) + 1, "", anim, offGrid.copy(), "None")
        cueList.append(cue)
        cue.add()
    
    def readFromFile(self): #remove grid after test
        global cueList
        f = open(cueFileName, "r")
        if f.mode == "r":
            contents = f.read()
            if len(contents) != 0:
                cues = contents.split(" ")
                trans = False
                for cue in cues:
                    if trans: #edit most recent cue
                        type = cue[0]
                        if type == "N":
                            type = "None"
                        elif type == "F":
                            type = "Fade All" #has to be the long names because changeTransType is what the combobox calls and so it has to be the actual string
                        elif type == "B":
                            type = "Bottom Up"
                        elif type == "L":
                            type = "Left to Right"
                        elif type == "R":
                            type = "Right to Left"
                        if type != "None":
                            length = int(cue[1:len(cue)])
                            cueList[len(cueList) - 1].translen = length
                        cueList[len(cueList) - 1].changeTransType(type)
                    else:
                        if cue[0] == "S":
                            gridList = []
                            tempList = cue[1:len(cue)].split(":") #split off numShown
                            numShown = int(tempList[0])
                            label = tempList[1]
                            rowList = tempList[2].split("R")
                            for row in rowList:
                                r = []
                                gridList.append(r)
                                colList = row.split(",")
                                for col in colList:
                                    rgb = col.split(".")
                                    rgb[0] = int(rgb[0])
                                    rgb[1] = int(rgb[1])
                                    rgb[2] = int(rgb[2])
                                    r.append(rgb)
                            cueList.append(Cue(self, numShown, len(cueList) + 1, label, False, gridList, "None"))
                            
                            #stuff to update cubes in second tab for testing
                            #palette = QtGui.QPalette()
                            #for bRow in range(6):
                                #for bCol in range(10):
                                    #brush = QtGui.QBrush(QtGui.QColor(gridList[bRow][bCol][0], gridList[bRow][bCol][1], gridList[bRow][bCol][2]))
                                    #brush.setStyle(QtCore.Qt.SolidPattern)
                                    #palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
                                    #palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
                                    #palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
                                    #grid[bRow][bCol].button.setPalette(palette)

                            #print(cueList[0].firstGrid)
                        else: #animation
                            pass
                    if trans:
                        trans = False
                    else:
                        trans = True
                self.addAllCues()
    
    #def updateSecondRow(self):
        #self.ui.lineEdit_12.setText(self.ui.lineEdit_11.text())
        
    #def addRow(self, buttonList, lineList): #add it to one further down than would make sense because it hasn't been appended yet and so the length hasn't been changed yet
        #button = QtWidgets.QPushButton(("Additional Button {}").format(len(buttonList) + 1), self.ui.gridLayoutWidget)
        #lineEdit = QtWidgets.QLineEdit(("Additional Space {}").format(len(lineList) + 1), self.ui.gridLayoutWidget)
        #self.ui.gridLayout.addWidget(button, 4 + len(buttonList), 1, 1, 1)
        #self.ui.gridLayout.addWidget(lineEdit, 4 + len(lineList), 0, 1, 1)
        #length = len(lineList)
        #button.clicked.connect(lambda: self.updateLine(lineEdit, length + 1))
        #buttonList.append(button)
        #lineList.append(lineEdit)
        
    #def updateLine(self, lineEdit, row):
        #lineEdit.setText(("Line {}").format(row))
    
    def addClickedButton(self, button, changeButton):
        global selectedButtons
        global selectedRows
        global selectedCols
        
        changeButton.setEnabled(True)
        
        if button not in selectedButtons:
            button.button.setDown(True)
            selectedButtons.append(button)
            selectedRows.append(button.row)
            selectedCols.append(button.col)
        
            #for button in selectedButtons:
                #button.button.setDown(True)
                
        else:
            button.button.setDown(False)
            selectedButtons.remove(button)
            selectedRows.remove(button.row)
            selectedCols.remove(button.col)
            #palette = QtGui.QPalette()
            #brush = QtGui.QBrush(QtGui.QColor()
            #brush.setStyle(QtCore.Qt.SolidPattern)
            #palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
            #palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
            #palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
            #button.button.setPalette(palette)
            
    def selectAll(self, grid, changeButton):
        global selectedButtons
        global selectedRows
        global selectedCols
        for r in range(6):
            for c in range(10):
                self.addClickedButton(grid[r][c], changeButton)
        
    def changeColor(self, grid, changeButton, buttonLayout, sideLayout, sideLayoutWidget):
        #disable all buttons
        for r in range(6):
            for c in range(10):
                grid[r][c].button.setEnabled(False)
                
        global colorButton
        global doneButton
        colorButton = QtWidgets.QPushButton("", sideLayoutWidget)
        colorButton.setEnabled(False)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        colorButton.setPalette(palette)
        sideLayout.addWidget(colorButton, 0, 0, 2, 3)
        
        #redLabel = QLabel("R", self.ui.gridLayoutWidget_3)
        #self.ui.gridLayout_3.addWidget(redLabel, 2, 0, 1, 1)
        
        #slider1 = QSlider(Qt.Horizontal, self.ui.gridLayoutWidget_3)
        #slider1.setMinimum(0)
        #slider1.setMaximum(255)
        #slider1.setTickInterval(1)
        #self.ui.gridLayout_3.addWidget(slider1, 2, 1, 1, 1)
        
        #value1 = QtWidgets.QLineEdit("", self.ui.gridLayoutWidget_3)
        #self.ui.gridLayout_3.addWidget(value1, 2, 2, 1, 1)
        
        #greenLabel = QLabel("G", self.ui.gridLayoutWidget_3)
        #self.ui.gridLayout_3.addWidget(greenLabel, 3, 0, 1, 1)
        
        #slider2 = QSlider(Qt.Horizontal, self.ui.gridLayoutWidget_3)
        #slider2.setMinimum(0)
        #slider2.setMaximum(255)
        #slider2.setTickInterval(1)
        #self.ui.gridLayout_3.addWidget(slider2, 3, 1, 1, 1)
        
        #value2 = QtWidgets.QLineEdit("", self.ui.gridLayoutWidget_3)
        #self.ui.gridLayout_3.addWidget(value2, 3, 2, 1, 1)
        
        #blueLabel = QLabel("B", self.ui.gridLayoutWidget_3)
        #self.ui.gridLayout_3.addWidget(blueLabel, 4, 0, 1, 1)
        
        #slider3 = QSlider(Qt.Horizontal, self.ui.gridLayoutWidget_3)
        #slider3.setMinimum(0)
        #slider3.setMaximum(255)
        #slider3.setTickInterval(1)
        #self.ui.gridLayout_3.addWidget(slider3, 4, 1, 1, 1)
        
        #value3 = QtWidgets.QLineEdit("", self.ui.gridLayoutWidget_3)
        #self.ui.gridLayout_3.addWidget(value3, 4, 2, 1, 1)
        
        #image = QImage("wheel-3-rgb.png")
        #imageLabel = QLabel()
        #imageLabel.setPixmap(QPixmap.fromImage(image));
        #self.ui.gridLayout_3.addWidget(imageLabel, 2, 0, 6, 2)
        
        doneButton = QtWidgets.QPushButton("Done", sideLayoutWidget)
        sideLayout.addWidget(doneButton, 2, 0, 1, 3)
        #print("two widgets added to sidelayout")
        
        #colorDialog.setOption(QColorDialog.NoButtons, True)
        
        #value1.textChanged.connect(lambda: self.updateSlider(value1, slider1))
        #slider1.valueChanged.connect(lambda: self.updateText(value1, slider1))
        
        #value2.textChanged.connect(lambda: self.updateSlider(value2, slider2))
        #slider2.valueChanged.connect(lambda: self.updateText(value2, slider2))
        
        #value3.textChanged.connect(lambda: self.updateSlider(value3, slider3))
        #slider3.valueChanged.connect(lambda: self.updateText(value3, slider3))
        
        #widgets = [colorButton, redLabel, slider1, value1, greenLabel, slider2, value2, blueLabel, slider3, value3, doneButton]
        global sideWidgets
        sideWidgets = [colorButton, doneButton]
        
        #slider1.valueChanged.connect(lambda: self.updateColor(slider1.value(), slider2.value(), slider3.value(), widgets, grid, changeButton))
        #slider2.valueChanged.connect(lambda: self.updateColor(slider1.value(), slider2.value(), slider3.value(), widgets, grid, changeButton))
        #slider3.valueChanged.connect(lambda: self.updateColor(slider1.value(), slider2.value(), slider3.value(), widgets, grid, changeButton))
        global colorDialog
        try:
            colorDialog.open(lambda: self.updateColor(colorDialog, grid, changeButton))
        except:
            pass
        doneButton.clicked.connect(lambda: self.donePickingColor(grid, changeButton, buttonLayout, sideLayout))
        
    def updateSlider(self, value, slider):
        if value.text() == "":
            slider.setValue(0)
        else:
            slider.setValue(int(value.text()))
        
    def updateText(self, value, slider):
        value.setText(str(slider.value()))
        
    def updateColor(self, colorDialog, grid, changeButton):
        color = colorDialog.selectedColor()
        #colorDialog = None
        red = color.red()
        green = color.green()
        blue = color.blue()
        
        global rgb 
        rgb = [red, green, blue]
        
        #print(("RGB {}, {}, {}").format(redValue, greenValue, blueValue))
        #varR = ((redValue / 255) ** 2.19921875) * 100
        #varG = ((greenValue / 255) ** 2.19921875) * 100
        #varB = ((blueValue / 255) ** 2.19921875) * 100
        
        #X = varR * 0.57667 + varG * 0.18555 + varB * 0.18819
        #Y = varR * 0.29738 + varG * 0.62735 + varB * 0.07527
        #Z = varR * 0.02703 + varG * 0.07069 + varB * 0.99110
        
        #print(("XYZ {}, {}, {}").format(X, Y, Z))
        
        #varX = X / 100
        #varY = Y / 100
        #varZ = Z / 100
        
        #varR = varX * 3.2406 + varY * -1.5372 + varZ * -0.4986
        #varG = varX * -0.9689 + varY * 1.8758 + varZ * 0.0415
        #varB = varX * 0.0557 + varY * -0.2040 + varZ * 1.0570

        #if varR > 0.0031308:
            #varR = 1.055 * ( varR ** ( 1 / 2.4 ) ) - 0.055
        #else:
            #varR = 12.92 * varR
            
        #if varG > 0.0031308:
            #varG = 1.055 * ( varG ** ( 1 / 2.4 ) ) - 0.055
        #else:
            #varG = 12.92 * varG
            
        #if varB > 0.0031308:
            #varB = 1.055 * ( varB ** ( 1 / 2.4 ) ) - 0.055
        #else:
            #varB = 12.92 * varB
            
        #sR = varR * 255
        #sG = varG * 255
        #sB = varB * 255
        
        #print(("sRGB {}, {}, {}").format(sR, sG, sB))
        
        #palette = QtGui.QPalette()
        #brush = QtGui.QBrush(QtGui.QColor(sR, sG, sB))
        #brush.setStyle(QtCore.Qt.SolidPattern)
        #palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        #palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        #palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        #colorButton.setPalette(palette)
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(red, green, blue))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        sideWidgets[0].setPalette(palette)
        
        #global rgb
        #rgb = [redValue, greenValue, blueValue]
            
    def donePickingColor(self, grid, changeButton, buttonLayout, sideLayout):
        global setCubeColor
        #print("done picking color called")
        #print(rgb)
        
        #update the color of square in the grid
        #send the thing to the grid
        #remove all the colorpicking widgets
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(rgb[0], rgb[1], rgb[2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        
        #print(editingCue.index)
        #print(editingCue.firstGrid)
        #print(editingCue.lastGrid)
        global sendRow
        global sendCol
        global sendR
        global sendG
        global sendB
        for button in selectedButtons:
            button.button.setPalette(palette)
            sendRow.append(button.row)
            sendCol.append(button.col)
            sendR.append(rgb[0])
            sendG.append(rgb[1])
            sendB.append(rgb[2])
            if sideLayout is self.ui.gridLayout_6:
                row = button.row
                col = button.col
                editingCue.firstGrid[row][col] = [rgb[0], rgb[1], rgb[2]]
                editingCue.lastGrid[row][col] = [rgb[0], rgb[1], rgb[2]]
                
        setCubeColor.set()
        
        #for each r and c in lists, call setCubeColor
        global sideWidgets
        for widget in sideWidgets:
            #print("remove side widget")
            widget.hide()
            sideLayout.removeWidget(widget)
            #widget.destroy(True, True)
        #sideWidgets[1].setEnabled(False)
        sideWidgets = []
        #selectedButtons.clear()
        #selectedRows.clear()
        #selectedCols.clear()
        
        #reenable all buttons
        #for r in range(6):
            #for c in range(10):
                #grid[r][c].button.setEnabled(True)
                
        #changeButton.setEnabled(False)
        #if buttonLayout is self.ui.gridLayout_4:
            #for r in range(6):
                #for c in range(10):
                    #self.ui.gridLayout_4.removeWidget(grid[r][c].button)
        #else:
        self.reset(grid, changeButton)
        
    def reset(self, grid, changeButton):
        #a = selectedButtons.copy()
        #b = selectedRows.copy()
        #c = selectedCols.copy()
        #selectedButtons = a.clear()
        #selectedRows = b.clear()
        #selectedCols = c.clear()
        #selectedButtons.remove(selectedButtons[1])
        #print(selectedButtons)
        global selectedButtons
        global selectedRows
        global selectedCols
        global rgb
        selectedButtons = []
        selectedRows = []
        selectedCols = []
        rgb = [0, 0, 0]
        
        #reenable all buttons
        for r in range(6):
            for c in range(10):
                grid[r][c].button.setEnabled(True)
                
        changeButton.setEnabled(False)
        
        global editingCue 
        editingCue = None
        
        self.ui.pushButton_6.clicked.disconnect()
        
class Cue():
    def __init__(self, mainUI, numShown, index, label, animtrue, grid, transType, translen = 0, anim = {}, animlen = 0, trans = {}): #gridlayout, gridlayoutwidget, self, cue number, cue label (s - or a -), animation or static, grid if it's static, animation, animation length, fade true or false, fade length (won't check unless fade is true), fancy transition, fancy transition length
    #when creating new cue, add one to existing last number, label = s - or a - and anim value from popup, if from an existing cue, put in stuff about animations and transitions, otherwise, all blank
        tempGrid = grid.copy()
        self.numShown = numShown
        self.index = index
        self.label = label
        self.animtrue = animtrue
        self.anim = anim
        self.animlen = animlen
        self.mainUI = mainUI
        self.transType = transType
        
        if not animtrue:
            self.firstGrid = tempGrid.copy()
            self.lastGrid = tempGrid.copy()
        
        self.translen = translen
            
        if animtrue and len(anim) > 0:
            self.firstGrid = self.anim[0]
            self.lastGrid = self.anim[animlen]
        
        self.jumpButton = QPushButton(mainUI.ui.gridLayoutWidget)
        self.jumpButton.clicked.connect(self.jumpTo)
        
        self.numberLine = QLineEdit(str(numShown), mainUI.ui.gridLayoutWidget)
        self.numberLine.returnPressed.connect(lambda: self.updateNumber(self.numberLine.text()))
        #self.numberLine.textEdited.connect(lambda: self.updateNumber(self.numberLine.text()))
        
        if label[0:2] != "A-" and label [0:2] != "S-":
            if self.animtrue:
                label = "A-" + label
            else:
                label = "S-" + label
        self.labelLine = QLineEdit(label, mainUI.ui.gridLayoutWidget)
        self.labelLine.textEdited.connect(lambda: self.updateLabel(self.labelLine))
        
        self.gridEditButton = QPushButton(mainUI.ui.gridLayoutWidget)
        self.gridEditButton.clicked.connect(self.changeGrid)
        
        self.transDrop = QComboBox(mainUI.ui.gridLayoutWidget)
        self.transDrop.addItems(["None", "Fade All", "Bottom Up", "Left to Right", "Right to Left"])
        self.transDrop.currentIndexChanged.connect(lambda: self.changeTransType(self.transDrop.currentText()))
        
        self.transEditButton = QPushButton(mainUI.ui.gridLayoutWidget)
        self.transEditButton.clicked.connect(self.changeTrans)
        
    def jumpTo(self):
        if self.animtrue:
            pass
        else:
            self.mainUI.jumpToSolid(self)
    
    def updateNumber(self, text):
        if text == "":
            self.numShown = 0
        else:
            self.numShown = int(text)
        self.mainUI.sort()
        
    def updateLabel(self, labelLine):
        text = labelLine.text()
        if self.animtrue and text[0:2] != "A-":
            text = "A-" + text
        elif not self.animtrue and text[0:2] != "S-":
            text = "S-" + text
        self.label = text
        labelLine.setText(text)
        
    def changeGrid(self):
        global editingCue
        if editMode:
            if self.anim:
                editingCue = self
                self.mainUI.editAnim()
            else:
                #call to open grid edit
                editingCue = self
                self.mainUI.editGrid()
            
    def changeTransType(self, text):
        if text == "None":
            self.transType = "None"
        elif text == "Fade All":
            self.transDrop.setCurrentIndex(1)
            self.transType = "Fade"
        elif text == "Bottom Up":
            self.transDrop.setCurrentIndex(2)
            self.transType = "Bottom"
        elif text == "Left to Right":
            self.transDrop.setCurrentIndex(3)
            self.transType = "Left"
        elif text == "Right to Left":
            self.transDrop.setCurrentIndex(4)
            self.transType = "Right"
            
    def changeTrans(self):
        #will show the transition with a slider, no matter what kind it is (unless it has no transition), but 
        if self.transType != "None" and self.transType != "Custom":
            input = QInputDialog(self.mainUI.ui.tab)
            input.setLabelText("Transition length?")
            input.setTextValue(str(self.translen))
            input.open(lambda: self.setLength(input.textValue()))
    
    def setLength(self, length):
        self.translen = int(length)
        
    def add(self):
        self.mainUI.ui.gridLayout.addWidget(self.jumpButton, self.index + 1, 0, 1, 1)
        self.mainUI.ui.gridLayout.addWidget(self.numberLine, self.index + 1, 1, 1, 1)
        self.mainUI.ui.gridLayout.addWidget(self.labelLine, self.index + 1, 2, 1, 1)
        self.mainUI.ui.gridLayout.addWidget(self.gridEditButton, self.index + 1, 3, 1, 1)
        self.mainUI.ui.gridLayout.addWidget(self.transDrop, self.index + 1, 4, 1, 1)
        self.mainUI.ui.gridLayout.addWidget(self.transEditButton, self.index + 1, 5, 1, 1)
        self.jumpButton.show()
        self.numberLine.show()
        self.labelLine.show()
        self.gridEditButton.show()
        self.transDrop.show()
        self.transEditButton.show()
        
    def remove(self):
        self.mainUI.ui.gridLayout.removeWidget(self.jumpButton)
        self.mainUI.ui.gridLayout.removeWidget(self.numberLine)
        self.mainUI.ui.gridLayout.removeWidget(self.labelLine)
        self.mainUI.ui.gridLayout.removeWidget(self.gridEditButton)
        self.mainUI.ui.gridLayout.removeWidget(self.transDrop)
        self.mainUI.ui.gridLayout.removeWidget(self.transEditButton)
        self.jumpButton.hide()
        self.numberLine.hide()
        self.labelLine.hide()
        self.gridEditButton.hide()
        self.transDrop.hide()
        self.transEditButton.hide()

app = QtWidgets.QApplication(sys.argv)

if gridExists:
    time.sleep(1)
    s = gridClient.openSocket('10.101.50.102', 2560)
    colorSet = threading.Thread(target=sendCubeColor, daemon=True)
    colorSet.start()

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
