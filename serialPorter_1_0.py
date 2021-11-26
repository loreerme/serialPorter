from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import serial
from serial.tools import list_ports_windows , list_ports_common, list_ports
from serial import *
import time,os,struct,sys


class SerialUi (QMainWindow) :
    def __init__(self):
        super(SerialUi, self).__init__()
        
        #Load the ui file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(dir_path + r'\SerialPortGui2.ui',self)
        
        
        # define widgets
        self.serial_port = serial.Serial()
        self.psw_voltage = ""
        self.psw_current =""
        self.brake_speed_trq = ""
        self.portlist = []
        self.temptemP=0
        self.tempList = []
        self.fixed = [0x01, 0x10, 0x11, 0x4c, 0x00 ,0x02, 0x04]
        self.temP=0
        self.crc = 0xFFFF

        # self.setStyleSheet("background: #3C3F41;")
        #Add Menu triggers
        self.actionBlack.triggered.connect(lambda:self.changeColor("black"))
        self.actionWhite.triggered.connect(lambda:self.changeColor("white"))
        self.actionRed.triggered.connect(lambda:self.changeColor("red"))
        self.actionBlue.triggered.connect(lambda:self.changeColor("blue"))
        self.actionGreen.triggered.connect(lambda:self.changeColor("green"))

        #TextBoxes
        self.txtbxInfo = self.findChild(QTextEdit, "txtbxInfo")
        self.lneditPSWVoltage = self.findChild(QTextEdit, "lneditPSWVoltage")
        self.lneditTemp= self.findChild(QTextEdit, "lneditTemp")
        self.txtbxShowPorts = self.findChild(QTextEdit, "txtbxShowPorts")

        #textBrowsers
        self.txtbrwReadSpeed = self.findChild(QTextBrowser, "txtbrwReadSpeed")
        self.txtbrwBrakeInfo = self.findChild(QTextBrowser, "txtbrwBrakeInfo")
        self.txtbrwPSWInfo = self.findChild(QTextBrowser, "txtbrwPSWInfo")
        self.txtbrwClimateInfo = self.findChild(QTextBrowser, "txtbrwClimateInfo")

        #LCD numbers
        self.lcdNumber = self.findChild(QLCDNumber, "lcdNumber")
        self.lcdReadCurrent = self.findChild(QLCDNumber, "lcdReadCurrent")
        self.lcdClimateRead = self.findChild(QLCDNumber, "lcdClimateRead")

        #tabs
        self.tabContainer = self.findChild(QTabWidget, "tabContainer")

        #LineEdits
        self.lneditPSWVoltage = self.findChild(QLineEdit, "lneditPSWVoltage")
        self.lneditOpenLoopTrq = self.findChild(QLineEdit, "lneditOpenLoopTrq")
        self.lneditTemp = self.findChild(QLineEdit, "lneditTemp")
        

        #listWidgets
        self.lswgtSWVoltage = self.findChild(QListWidget, "lswgtSWVoltage")


        #combo boxes
        self.cmbPortList = self.findChild(QComboBox, "cmbPortList")

        #labels
        self.lblPorts = self.findChild(QLabel, "lblPorts")

        #ListViews
        self.lsViewPortInfo = self.findChild(QListView, "lsViewPortInfo")

        #buttons
        self.btnOpenPort = self.findChild(QPushButton, "btnOpenPort")
        self.btnSearchPorts = self.findChild(QPushButton, "btnSearchPorts")
        self.btnClosePort = self.findChild(QPushButton, "btnClose")
        self.btnPortInfo = self.findChild(QPushButton, "btnPortInfo")
        self.btnSetPSWVoltage = self.findChild(QPushButton, "btnSetPSWVoltage")
        self.btnReadPSWVoltage = self.findChild(QPushButton, "btnReadPSWVoltage")
        self.btnReadPSWCurrent = self.findChild(QPushButton, "btnReadPSWCurrent")
        self.btnShowPorts = self.findChild(QPushButton, "btnShowPorts")
        self.btnSetOpenLoopTrq = self.findChild(QPushButton, "btnSetOpenLoopTrq")
        self.btnReadBrakeSpeed = self.findChild(QPushButton, "btnReadBrakeSpeed")
        self.btnResetBrake = self.findChild(QPushButton, "btnResetBrake")
        self.btnBrakeInfo = self.findChild(QPushButton, "btnBrakeInfo")
        self.btnPSWInfo = self.findChild(QPushButton, "btnPSWInfo")
        self.btnReadTemp = self.findChild(QPushButton, "btnReadTemp")
        self.btnSetTemp = self.findChild(QPushButton, "btnSetTemp")
        self.btnClimateInfo = self.findChild(QPushButton, "btnClimateInfo")

        #shadow
        shadow1 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow2 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow3 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow4 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow5 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow6 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow7 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow8 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow9 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow10 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow11 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow12 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow13 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow14 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow15 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow16 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow17 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow18 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow19 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow20 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow21 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow22 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow23 = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)

        #button shadow
        self.btnOpenPort.setGraphicsEffect(shadow1)
        self.btnSearchPorts.setGraphicsEffect(shadow2)
        self.btnClosePort.setGraphicsEffect(shadow4)
        self.btnPortInfo.setGraphicsEffect(shadow5)
        self.btnSetPSWVoltage.setGraphicsEffect(shadow6)
        self.btnReadPSWVoltage.setGraphicsEffect(shadow7)
        self.btnReadPSWCurrent.setGraphicsEffect(shadow8)
        self.btnShowPorts.setGraphicsEffect(shadow9)
        self.btnSetOpenLoopTrq.setGraphicsEffect(shadow10)
        self.btnReadBrakeSpeed.setGraphicsEffect(shadow11)
        self.btnResetBrake.setGraphicsEffect(shadow12)        
        self.btnPSWInfo.setGraphicsEffect(shadow13)
        self.btnBrakeInfo.setGraphicsEffect(shadow14)

        #other shadow

        self.txtbxInfo.setGraphicsEffect(shadow15)
        self.lneditPSWVoltage.setGraphicsEffect(shadow16)
        self.txtbxShowPorts.setGraphicsEffect(shadow17)
        self.txtbrwReadSpeed.setGraphicsEffect(shadow18)
        self.txtbrwBrakeInfo.setGraphicsEffect(shadow19)
        self.txtbrwPSWInfo.setGraphicsEffect(shadow21)
        self.lcdNumber.setGraphicsEffect(shadow22)
        self.lcdReadCurrent.setGraphicsEffect(shadow23)



        # disable buttons if the correct port is not selected
        self.btnReadPSWVoltage.setEnabled(False)
        self.btnSetPSWVoltage.setEnabled(False)
        self.btnReadPSWCurrent.setEnabled(False)
        self.btnSetOpenLoopTrq.setEnabled(False)
        self.btnResetBrake.setEnabled(False)
        self.btnReadBrakeSpeed.setEnabled(False)
        self.btnClosePort.setEnabled(False)
        self.btnOpenPort.setEnabled(False)
        self.btnPSWInfo.setEnabled(False)
        self.btnBrakeInfo.setEnabled(False)

        #change pointer type
        self.btnOpenPort.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSearchPorts.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnClosePort.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnPortInfo.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSetPSWVoltage.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnReadPSWVoltage.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnReadPSWCurrent.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnShowPorts.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSetOpenLoopTrq.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnReadBrakeSpeed.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnResetBrake.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnBrakeInfo.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnPSWInfo.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnReadTemp.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSetTemp.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        


        #define function calls
        self.btnSearchPorts.clicked.connect (self.getThePorts)
        self.btnOpenPort.clicked.connect (self.openPort)
        self.btnClosePort.clicked.connect(self.closePort)
        self.btnPortInfo.clicked.connect(self.showPortInfo)
        self.btnSetPSWVoltage.clicked.connect(self.setPSWVoltage)
        self.btnReadPSWVoltage.clicked.connect(self.readPSWVoltage)
        self.btnReadPSWCurrent.clicked.connect(self.readPSWCurrent)
        self.btnShowPorts.clicked.connect(self.showAllPorts)
        self.btnSetOpenLoopTrq.clicked.connect(self.setOpenLoopTrq)
        self.btnReadBrakeSpeed.clicked.connect(self.readBrakeTrq)
        self.btnResetBrake.clicked.connect(self.resetBrakeSettings)
        self.btnBrakeInfo.clicked.connect(self.readBrakeInfo)
        self.btnPSWInfo.clicked.connect(self.readPSWInfo)
        self.btnReadTemp.clicked.connect(self.readTemp)
        self.btnSetTemp.clicked.connect(self.setTemp)



        # self.show()

    #Functions

    # Style of widgets

    def changeColor (self, color) : 
        backGndColor = "background-color :"+ str(color) +";"
        self.setStyleSheet(backGndColor)


    def setName (self):
       self.lblPorts.setText ("Ports")

    def getThePorts (self) :
        self.cmbPortList.clear()
        self.portlist =  list_ports_windows.comports()
        for port in self.portlist :
            self.cmbPortList.addItem(str(port))

        self.btnClosePort.setEnabled(True)
        self.btnOpenPort.setEnabled(True)
        self.btnPSWInfo.setEnabled(True)
        self.btnBrakeInfo.setEnabled(True)

        self.disableButtons()

    def showAllPorts (self) :
        for port in self.portlist :
            self.txtbxShowPorts.append(str(port))


    def showPortInfo (self):
        port_info =[]
        self.txtbxInfo.clear()
        port_info = str(self.serial_port).split(",")
        for info in port_info :
            self.txtbxInfo.append(info)
    def disableButtons(self) :
        # disable buttons if the correct port is not selected
        self.btnReadPSWVoltage.setEnabled(False)
        self.btnSetPSWVoltage.setEnabled(False)
        self.btnReadPSWCurrent.setEnabled(False)
        self.btnSetOpenLoopTrq.setEnabled(False)
        self.btnResetBrake.setEnabled(False)
        self.btnReadBrakeSpeed.setEnabled(False)

        # self.btnClosePort.setEnabled(False)
        # self.btnOpenPort.setEnabled(False)
        self.btnPSWInfo.setEnabled(False)
        self.btnBrakeInfo.setEnabled(False)
        


        # self.btnClosePort.setEnabled(False)
        # self.btnOpenPort.setEnabled(False)

    def openPort (self) :

        self.serial_port = str (self.cmbPortList.currentText())
        self.serial_port = self.serial_port[0:5]
        try :
            self.serial_port = serial.Serial(self.serial_port, 9600, timeout=None)
            if self.serial_port.isOpen() :
                self.txtbxInfo.setPlainText("The serial port is available")
                self.btnPSWInfo.setEnabled(True)
                self.btnBrakeInfo.setEnabled(True)
        except serial.serialutil.SerialException:
            self.txtbxInfo.setPlainText("The port is used by another application or not open")   

    def closePort (self) :
        self.serial_port.close()
        print ("The serial port is closed")
        if self.serial_port.isOpen() :
            self.txtbxInfo.setPlainText("The serial port cannot be closed")
        else :
            self.txtbxInfo.setPlainText("The serial port is closed")

        self.disableButtons()


    # GW Instek PSW-30-36 control functions
    def setPSWVoltage (self) :
        set_voltage_command = "SOUR:VOLT:LEV:IMM:AMPL "
        textboxValue =""
        set_voltage_command = set_voltage_command
        textboxValue = self.lneditPSWVoltage.text()
        set_voltage_command = set_voltage_command + textboxValue + "\n"
        self.serial_port.write(set_voltage_command.encode('ascii'))

    def readPSWVoltage (self) :
        self.serial_port.write("MEAS:VOLT:DC?\n".encode('ascii'))
        time.sleep(0.5)
        while True:
            data = self.serial_port.read(self.serial_port.inWaiting())
            if (len(data) > 0):
                for i in range(len(data)):
                    # sys.stdout.write(str(data[i])+"\n")
                    # print(chr(data[i]))
                    self.psw_voltage = self.psw_voltage + chr(data[i])
                break

        # self.txtbxReadSpeed.setText(self.brake_speed_trq)
        self.lcdNumber.setSegmentStyle (QLCDNumber.Flat)
        self.lcdNumber.setDigitCount (8)
        self.lcdNumber.display (self.psw_voltage)

    def readPSWCurrent(self) :
        self.serial_port.write("MEAS:CURR:DC?\n".encode('ascii'))
        time.sleep(0.5)
        while True:
            data = self.serial_port.read(self.serial_port.inWaiting())
            if (len(data) > 0):
                for i in range(len(data)):
                    # sys.stdout.write(str(data[i])+"\n")
                    # print(chr(data[i]))
                    self.psw_current = self.psw_current + chr(data[i])
                break

        # self.txtbxReadSpeed.setText(self.brake_speed_trq)
        self.lcdReadCurrent.setSegmentStyle (QLCDNumber.Flat)
        self.lcdReadCurrent.setDigitCount (8)
        self.lcdReadCurrent.display (self.psw_current)

    def readPSWInfo (self):
        psw_info = ""
        self.txtbrwPSWInfo.clear()
        self.serial_port.write("*IDN?\n".encode('ascii'))

        time.sleep(0.5)
        while True:
            data = self.serial_port.read(self.serial_port.inWaiting())
            if (len(data) > 0):
                for i in range(len(data)):
                    sys.stdout.write(str(data[i]))
                    # print(data[i])
                    psw_info= psw_info+chr(data[i])
                break
            else :
                break


        self.txtbrwPSWInfo.setText (psw_info)

        if "GW-INSTEK" in psw_info :
            self.btnReadPSWVoltage.setEnabled(True)
            self.btnSetPSWVoltage.setEnabled(True)
            self.btnReadPSWCurrent.setEnabled(True)


    # Hysteresis Brake Related functions
    def setOpenLoopTrq(self):
        set_open_loop_trq_command = "I1,"
        textboxValue = ""
        set_open_loop_trq_command = set_open_loop_trq_command
        textboxValue = self.lneditOpenLoopTrq.text()
        set_open_loop_trq_command = set_open_loop_trq_command + textboxValue + "\r\n"
        self.serial_port.write(set_open_loop_trq_command.encode('ascii'))
        print ("set the torque")

    def readBrakeTrq (self):
        log_file = open("log.txt", "w")
        self.brake_speed_trq =""
        self.txtbrwReadSpeed.clear()
        self.serial_port.write("OD1\r\n".encode('ascii'))
        time.sleep(0.5)
        while True:
            data = self.serial_port.read(self.serial_port.inWaiting())
            if (len(data) > 0):
                for i in range(len(data)):
                    # sys.stdout.write(str(data[i]))
                    # print(chr(data[i]))
                    # print(data[i])
                    self.brake_speed_trq = self.brake_speed_trq + chr(data[i])
                break
        speed = int (self.brake_speed_trq[2:7])
        self.txtbrwReadSpeed.setText (str(speed))

        log_file.write(str(speed))
        log_file.close()


    def readBrakeInfo (self):
        self.serial_port.flush()
        brake_info = ""
        self.txtbrwBrakeInfo.clear()
        self.serial_port.write("*IDN?\r\n".encode('ascii'))

        time.sleep(0.5)
        while True:
            data = self.serial_port.read(self.serial_port.inWaiting())
            if (len(data) > 0):
                for i in range(len(data)):
                    sys.stdout.write(str(data[i]))
                    # print(chr(data[i]))
                    # print(data[i])
                    # self.brake_speed_trq = self.brake_speed_trq + chr(data[i])
                    brake_info = brake_info+chr(data[i])
                break
            else :
                break


        self.txtbrwBrakeInfo.setText (brake_info)

        if "DSP7" in brake_info :
            self.btnSetOpenLoopTrq.setEnabled(True)
            self.btnResetBrake.setEnabled(True)
            self.btnReadBrakeSpeed.setEnabled(True)

    def resetBrakeSettings (self) :
        self.serial_port.write("OD1\r\n".encode('ascii'))

    def readTemp (self):        
        self.serial_port.write(b"\x01\x04\x10\x04\x00\x02\x34\xCA")        
        time.sleep(1)
        data = self.serial_port.read(self.serial_port.inWaiting())        
        decTemp = data[5]<<24 | data[6]<<16|data[3]<<8|data[4]        
        hexTemp=str(hex(decTemp)[2:])
        finalTemp = str(struct.unpack('!f',bytes.fromhex(hexTemp)))[1:6]
        
        self.lcdClimateRead.setSegmentStyle (QLCDNumber.Flat)
        self.lcdClimateRead.setDigitCount (8)
        self.lcdClimateRead.display (finalTemp)

    def float_to_hex(self):
        tempHex = struct.unpack('<I', struct.pack('<f', self.temP))[0]
        t1 = tempHex>>24
        t2 =(tempHex & 0x00FF0000) >> 16
        t3=(tempHex & 0x0000FF00) >> 8
        t4 = (tempHex & 0x000000FF)

        self.tempList.append(t3)
        self.tempList.append(t4)
        self. tempList.append(t1)
        self.tempList.append(t2)

    def MODBUS_CRC16_v1(self):
        bitt= 0
        for i in self.fixed:
            self.crc = self.crc^i
            for bitt in range(1, 9):
                if self.crc & 0x0001 :
                    self.crc>>= 1;
                    self.crc ^= 0xA001;
                else :
                    self.crc >>=1

    def formTemp(self):
        for i in range(0,4) :
            self.fixed.append(self.tempList[i])
        self.MODBUS_CRC16_v1()
        crc1 = self.crc&0xFF
        crc2 = self.crc>>8
        self.fixed.append(crc1)
        self.fixed.append(crc2)

        
    def setTemp(self):
        if(self.lneditTemp.text().isnumeric()):
            print(1)
            self.temptemP =int(self.lneditTemp.text())
            print(2)
            if (self.temptemP>150 or self.temptemP<-50):
                self.lneditTemp.setText("Invalid")
            else:
                print(3)
                self.temP=self.temptemP
                print(4)
                self.float_to_hex()
                print(5)
                self.formTemp()
                print(6)
                self.serial_port.write(bytearray(self.fixed))
                print(7)
                time.sleep(1)
        else:
            self.lneditTemp.setText("Invalid")
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    UIWindow = SerialUi()
    UIWindow.show()
    app.exec_()
