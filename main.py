import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox
from PyQt5.uic import loadUi
import RPi.GPIO as gpio
import time
import threading


#Pinbelegung niedrigstes Bit ist a0

a0_Current = 20
a1_Current = 21
a2_Current = 17
a3_Current = 18
a4_Current = 27
enable_Current = 22  

a0_Phase = 5  #M2_E1
a1_Phase = 6 #M2_E2
a2_Phase = 13
enable_Phase = 19  #einer der beiden X Pins

sensorPin_Error = 23
sensorPin_6mA_DC = 24
sensorPin_30mA_AC = 25

maxDurationTest = 3000 #time in milliseconds

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)


gpio.setup(a0_Current, gpio.OUT)
gpio.setup(a1_Current, gpio.OUT)
gpio.setup(a2_Current, gpio.OUT)
gpio.setup(a3_Current, gpio.OUT)
gpio.setup(a4_Current, gpio.OUT)
gpio.setup(enable_Current, gpio.OUT)
gpio.setup(a0_Phase, gpio.OUT)
gpio.setup(a1_Phase, gpio.OUT)
gpio.setup(a2_Phase, gpio.OUT)
gpio.setup(enable_Phase, gpio.OUT)

gpio.setup(sensorPin_Error, gpio.IN)
gpio.setup(sensorPin_6mA_DC, gpio.IN)
gpio.setup(sensorPin_30mA_AC, gpio.IN)

transition = False

color_Red = "rgb(255, 142, 142)"
color_Green = "rgb(40, 159, 62)"
color_Yellow = "rgb(230,238,27)"

msg_Error = "Common Error on" 

phaseActivated = [color_Red,color_Red,color_Red]

isActivated = [color_Red,color_Red,color_Red,color_Red,color_Red,color_Red,color_Red,color_Red,color_Red,color_Red,color_Red,color_Red
               ,color_Red,color_Red,color_Red,color_Red,color_Red,color_Red]

buttonText = []

#import time
#start_time = time.time()
#print("--- %s seconds ---" % (time.time() - start_time))

def updateColor(self):
    self.S1.setStyleSheet("border:none; background-color: " + isActivated[0])
    self.S2.setStyleSheet("border:none; background-color: " + isActivated[1])
    self.S3.setStyleSheet("border:none; background-color: " + isActivated[2])
    self.S4.setStyleSheet("border:none; background-color: " + isActivated[3])
    self.S5.setStyleSheet("border:none; background-color: " + isActivated[4])
    self.S6.setStyleSheet("border:none; background-color: " + isActivated[5])
    self.S7.setStyleSheet("border:none; background-color: " + isActivated[6])
    self.S8.setStyleSheet("border:none; background-color: " + isActivated[7])
    self.S9.setStyleSheet("border:none; background-color: " + isActivated[8])
    self.S10.setStyleSheet("border:none; background-color: " + isActivated[9])
    self.S11.setStyleSheet("border:none; background-color: " + isActivated[10])
    self.S12.setStyleSheet("border:none; background-color: " + isActivated[11])
    self.S13.setStyleSheet("border:none; background-color: " + isActivated[12])
    self.S14.setStyleSheet("border:none; background-color: " + isActivated[13])
    self.S15.setStyleSheet("border:none; background-color: " + isActivated[14])
    self.S16.setStyleSheet("border:none; background-color: " + isActivated[15])
    self.S17.setStyleSheet("border:none; background-color: " + isActivated[16])
    self.S18.setStyleSheet("border:none; background-color: " + isActivated[17])
    
    self.repaint()
    
    self.P1.setStyleSheet("border:none; background-color: " + phaseActivated[0])
    self.P2.setStyleSheet("border:none; background-color: " + phaseActivated[1])
    self.P3.setStyleSheet("border:none; background-color: " + phaseActivated[2])
    
def turnOnSwitchCurrent(val):
    gpio.output(a0_Current, val & (0x01 << 0))  
    gpio.output(a1_Current, val & (0x01 << 1))  
    gpio.output(a2_Current, val & (0x01 << 2))  
    gpio.output(a3_Current, val & (0x01 << 3))  
    gpio.output(a4_Current, val & (0x01 << 4))  
      
def turnOnSwitchPhase(val):
    gpio.output(a0_Phase, val & (0x01 << 0))  
    gpio.output(a1_Phase, val & (0x01 << 1))  
    gpio.output(a2_Phase, val & (0x01 << 2))
    
    
def showdialog(self, msg):
    QMessageBox.about(self,"Hinweis",msg)
    
def initButtonText(self):
    buttonText.append(self.S1.text())
    buttonText.append(self.S2.text())
    buttonText.append(self.S3.text())
    buttonText.append(self.S4.text())
    buttonText.append(self.S5.text())
    buttonText.append(self.S6.text())
    buttonText.append(self.S7.text())
    buttonText.append(self.S8.text())
    buttonText.append(self.S9.text())
    buttonText.append(self.S10.text())
    buttonText.append(self.S11.text())
    buttonText.append(self.S12.text())
    buttonText.append(self.S13.text())
    buttonText.append(self.S14.text())
    buttonText.append(self.S15.text())
    buttonText.append(self.S16.text())
    buttonText.append(self.S17.text())
    buttonText.append(self.S18.text())
    

def runTest(self, buttonNum):
    gpio.output(enable_Current, 0)
    start_time = time.time()
    errorFound = False
    while (time.time() - start_time) < 10:#maxDurationTest / 1000:
        if gpio.input(sensorPin_Error) == 1:
            isActivated[buttonNum - 1] = color_Red
            gpio.output(enable_Current, 1)
            updateColor(self)
            showdialog(self,"Beim Messen vonm Strom " + buttonText[buttonNum - 1] + " ist ein allgemeiner Fehler aufgetren. Der Fehler ist nach "
                       + str(round((time.time() - start_time) * 1000))  + "ms aufgetreten!" )
            errorFound = True
            break
        elif gpio.input(sensorPin_6mA_DC) == 1:
            isActivated[buttonNum - 1] = color_Red
            gpio.output(enable_Current, 1)
            updateColor(self)
            showdialog(self,"Beim Messen vonm Strom " + buttonText[buttonNum - 1] + " ist ein 6mA DC Fehler aufgetren. Der Fehler ist nach "
                       + str(round((time.time() - start_time) * 1000))  + "ms aufgetreten!")
            errorFound = True
            break
        elif gpio.input(sensorPin_30mA_AC) == 1:
            isActivated[buttonNum - 1] = color_Red
            gpio.output(enable_Current, 1)
            updateColor(self)
            showdialog(self,"Beim Messen vonm Strom " + buttonText[buttonNum - 1] + " ist ein 30 mA AC Fehler aufgetren. Der Fehler ist nach "
                       + str(round((time.time() - start_time) * 1000))  + "ms aufgetreten!")
            errorFound = True
            break
               
    if not errorFound:
        isActivated[buttonNum - 1] = color_Red
        gpio.output(enable_Current, 1)
        updateColor(self)
        print("no error")
        showdialog(self,"Fehlerstrom " + buttonText[buttonNum - 1] + " wurde erfolgreich getestet. Abgeschaltet nach " + str(maxDurationTest) + "ms!" )
    
class MainWindow(QDialog):
    
 

    def __init__(self):
        super(MainWindow, self).__init__()
        gpio.output(enable_Current, 1)
        
        loadUi('test.ui', self)
        initButtonText(self)
        
        
        updateColor(self)
        
        self.setWindowTitle('Fehlerströme Ansteuerung')
        self.S1.pressed.connect(lambda:self.on_off(1))
        self.S2.pressed.connect(lambda:self.on_off(2))
        self.S3.pressed.connect(lambda:self.on_off(3))
        self.S4.pressed.connect(lambda:self.on_off(4))
        self.S5.pressed.connect(lambda:self.on_off(5))
        self.S6.pressed.connect(lambda:self.on_off(6))
        self.S7.pressed.connect(lambda:self.on_off(7))
        self.S8.pressed.connect(lambda:self.on_off(8))
        self.S9.pressed.connect(lambda:self.on_off(9))
        self.S10.pressed.connect(lambda:self.on_off(10))
        self.S11.pressed.connect(lambda:self.on_off(11))
        self.S12.pressed.connect(lambda:self.on_off(12))
        self.S13.pressed.connect(lambda:self.on_off(13))
        self.S14.pressed.connect(lambda:self.on_off(14))
        self.S15.pressed.connect(lambda:self.on_off(15))
        self.S16.pressed.connect(lambda:self.on_off(16))
        self.S17.pressed.connect(lambda:self.on_off(17))
        self.S18.pressed.connect(lambda:self.on_off(18))
        
        self.P1.pressed.connect(lambda:self.on_off_Phase(1))
        self.P2.pressed.connect(lambda:self.on_off_Phase(2))
        self.P3.pressed.connect(lambda:self.on_off_Phase(3))
        
        """self.S1.clicked.connect(lambda:self.changeColor())
        self.S2.clicked.connect(lambda:self.changeColor())
        self.S3.clicked.connect(lambda:self.changeColor())
        self.S4.clicked.connect(lambda:self.changeColor())
        self.S5.clicked.connect(lambda:self.changeColor())
        self.S6.clicked.connect(lambda:self.changeColor())
        self.S7.clicked.connect(lambda:self.changeColor())
        self.S8.clicked.connect(lambda:self.changeColor())
        self.S9.clicked.connect(lambda:self.changeColor())
        self.S10.clicked.connect(lambda:self.changeColor())
        self.S11.clicked.connect(lambda:self.changeColor())
        self.S12.clicked.connect(lambda:self.changeColor())
        self.S13.clicked.connect(lambda:self.changeColor())
        self.S14.clicked.connect(lambda:self.changeColor())
        self.S15.clicked.connect(lambda:self.changeColor())
        self.S16.clicked.connect(lambda:self.changeColor())
        self.S17.clicked.connect(lambda:self.changeColor())
        self.S18.clicked.connect(lambda:self.changeColor())"""
        
        self.P1.clicked.connect(lambda:self.changeColorPhase())
        self.P2.clicked.connect(lambda:self.changeColorPhase())
        self.P3.clicked.connect(lambda:self.changeColorPhase())
        
        self.Disable.clicked.connect(lambda:self.disableAll()) 
          
        
    @pyqtSlot()
    def on_off(self, buttonNum):
        
        if isActivated.count(color_Green) == 0 and isActivated[buttonNum - 1] == color_Red:
            isActivated[buttonNum - 1] = color_Green
            
            turnOnSwitchCurrent(buttonNum - 1)
            time.sleep(0.25)
        
        elif isActivated[buttonNum - 1] == color_Green:
            isActivated[buttonNum - 1] = color_Red
            
            gpio.output(enable_Current, 1)
        else:
            showdialog(self,"Hier ist etwas schiefgegangen..")
 
        updateColor(self)
        runTest(self, buttonNum)
        
    def disableAll(self):
        gpio.output(enable_Current, 1)
        gpio.output(enable_Phase, 0)
          
        i = 0  
        while(i < len(isActivated)):
            
            isActivated[i] = color_Red
            
            if(i < len(phaseActivated)):
                phaseActivated[i] = color_Red
            i += 1    
        updateColor(self)
        
        
    @pyqtSlot()
    def on_off_Phase(self, buttonNum):
        
        
        if phaseActivated.count(color_Green) == 0 and phaseActivated[buttonNum - 1] == color_Red:
            phaseActivated[buttonNum - 1] = color_Green
            
            turnOnSwitchPhase(buttonNum - 1)
            time.sleep(0.25)
            gpio.output(enable_Phase, 1)
        
        elif phaseActivated[buttonNum - 1] == color_Green:
            phaseActivated[buttonNum - 1] = color_Red
            
            gpio.output(enable_Phase, 0)
            
        else:
            global isOn
            global shouldBeOn
            
            isOn = phaseActivated.index(color_Green)
            shouldBeOn = buttonNum - 1
            
            phaseActivated[isOn] = color_Yellow
            phaseActivated[buttonNum - 1] = color_Yellow
            global transition
            transition = True
            
            gpio.output(enable_Phase, 0)
            
        updateColor(self)
           
    def changeColor(self):
       global transition
       global isOn
       global shouldBeOn
       
       if transition:
           time.sleep(0.25)
           turnOnSwitchCurrent(shouldBeOn)
           time.sleep(0.25)
           isActivated[isOn] = color_Red
           isActivated[shouldBeOn] = color_Green
           updateColor(self)
           transition = False
           
           gpio.output(enable_Current, 0)
           turnOnSwitchCurrent(shouldBeOn) 
           
           
       
    def changeColorPhase(self):
        global transition
        global isOn
        global shouldBeOn
        
        if transition:
           time.sleep(0.25)
           turnOnSwitchPhase(shouldBeOn)
           time.sleep(0.25) 
           phaseActivated[isOn] = color_Red
           phaseActivated[shouldBeOn] = color_Green
           updateColor(self)
           transition = False
           gpio.output(enable_Phase, 1)
           
           
           
           
         
        
        
app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
          