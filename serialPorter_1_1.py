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
        uic.loadUi(dir_path + r'\serialPorter_1_1.ui',self)        
        
        # define widgets
        self.serial_port = serial.Serial()
        self.psw_voltage = ""
        self.psw_current =""
        self.brake_speed_trq = ""
        self.portlist = []
        self.temptemP=0
        self.tempList = []
        self.fixedSetTempCmd = []
        # self.fixedSetTempCmd = [0x01, 0x10, 0x11, 0x4c, 0x00, 0x02, 0x04]
        self.temP=0
        self.crc = 0xFFFF
        
        #self.fixedTrgTempCmd = b"\x01\x04\x10\xB2\x00\x02\xD5\x2C"
        self.portInfo = ['Serial ID','Open','Port No','Baudrate','ByteSize','Parity']


        # self.setStyleSheet("background: #3C3F41;")
        #Add Menu triggers
        self.actionBlack.triggered.connect(lambda:self.changeColor("black"))
        self.actionWhite.triggered.connect(lambda:self.changeColor("white"))
        self.actionRed.triggered.connect(lambda:self.changeColor("red"))
        self.actionBlue.triggered.connect(lambda:self.changeColor("blue"))
        self.actionGreen.triggered.connect(lambda:self.changeColor("green"))

        #TextBoxes
        self.txtbxInfo                            = self.findChild(QTextEdit, "txtbxInfo")
        self.lneditPSWVoltage            =  self.findChild(QTextEdit, "lneditPSWVoltage")
        self.lneditTemp                      = self.findChild(QTextEdit, "lneditTemp")
        self.txtbxShowPorts           = self.findChild(QTextEdit, "txtbxShowPorts")

        #textBrowsers
        self.txtbrwReadSpeed    = self.findChild(QTextBrowser, "txtbrwReadSpeed")
        self.txtbrwBrakeInfo        = self.findChild(QTextBrowser, "txtbrwBrakeInfo")
        self.txtbrwPSWInfo          = self.findChild(QTextBrowser, "txtbrwPSWInfo")
        self.txtbrwClimateInfo  = self.findChild(QTextBrowser, "txtbrwClimateInfo")

        #LCD numbers
        self.lcdNumber          = self.findChild(QLCDNumber, "lcdNumber")
        self.lcdReadCurrent     = self.findChild(QLCDNumber, "lcdReadCurrent")
        self.lcdClimateRead     = self.findChild(QLCDNumber, "lcdClimateRead")
        self.lcdClimateReadTrg     = self.findChild(QLCDNumber, "lcdClimateReadTrg")

        #tabs
        self.tabContainer       = self.findChild(QTabWidget, "tabContainer")

        #LineEdits
        self.lneditPSWVoltage   = self.findChild(QLineEdit, "lneditPSWVoltage")
        self.lneditOpenLoopTrq  = self.findChild(QLineEdit, "lneditOpenLoopTrq")
        self.lneditTemp         = self.findChild(QLineEdit, "lneditTemp")
        

        #listWidgets
        self.lswgtSWVoltage     = self.findChild(QListWidget, "lswgtSWVoltage")


        #combo boxes
        self.cmbPortList        = self.findChild(QComboBox, "cmbPortList")

        #labels
        self.lblPorts           = self.findChild(QLabel, "lblPorts")

        #ListViews
        self.lsViewPortInfo     = self.findChild(QListView, "lsViewPortInfo")

        #buttons
        self.btnOpenPort        = self.findChild(QPushButton, "btnOpenPort")
        self.btnSearchPorts     = self.findChild(QPushButton, "btnSearchPorts")
        self.btnClosePort       = self.findChild(QPushButton, "btnClose")
        self.btnPortInfo        = self.findChild(QPushButton, "btnPortInfo")
        self.btnSetPSWVoltage   = self.findChild(QPushButton, "btnSetPSWVoltage")
        self.btnReadPSWVoltage  = self.findChild(QPushButton, "btnReadPSWVoltage")
        self.btnReadPSWCurrent  = self.findChild(QPushButton, "btnReadPSWCurrent")
        self.btnShowPorts       = self.findChild(QPushButton, "btnShowPorts")
        self.btnSetOpenLoopTrq  = self.findChild(QPushButton, "btnSetOpenLoopTrq")
        self.btnReadBrakeSpeed  = self.findChild(QPushButton, "btnReadBrakeSpeed")
        self.btnResetBrake      = self.findChild(QPushButton, "btnResetBrake")
        self.btnBrakeInfo       = self.findChild(QPushButton, "btnBrakeInfo")
        self.btnPSWInfo         = self.findChild(QPushButton, "btnPSWInfo")
        self.btnReadTemp        = self.findChild(QPushButton, "btnReadTemp")
        self.btnSetTemp         = self.findChild(QPushButton, "btnSetTemp")
        self.btnClimateInfo     = self.findChild(QPushButton, "btnClimateInfo")
        self.btnReadTrgTmp      = self.findChild(QPushButton, "btnReadTrgTmp")
        


        #shadow
        
        self.btnSearchPorts.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))        
        self.btnPortInfo.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
        self.txtbxInfo.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
        self.txtbxShowPorts.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
        self.txtbrwBrakeInfo.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
        self.txtbrwPSWInfo.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
        



        # disable buttons if the correct port is not selected
        self.btnShowPorts.setEnabled(False)
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
        self.btnReadTemp.setEnabled(False)
        self.btnSetTemp.setEnabled(False)
        self.btnClimateInfo.setEnabled(False)
        self.btnReadTrgTmp.setEnabled(False)


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
        self.btnReadTrgTmp.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        


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
        self.btnReadTrgTmp.clicked.connect(self.readTrgTemp)



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
        self.btnShowPorts.setEnabled(True)
        
        
        self.btnOpenPort.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
        
        self.btnClosePort.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
        self.btnShowPorts.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
        
        

        self.disableButtons()

    def showAllPorts (self) :
        for port in self.portlist :
            self.txtbxShowPorts.append(str(port))
       

    def showPortInfo (self):
        port_info =[]
        self.txtbxInfo.clear()
        port_info = str(self.serial_port).split(",")
        temp_info1=port_info[1].split(">(")[0]
        temp_info2=port_info[1].split(">(")[1]
        port_info.pop(1)
        port_info.insert(1,temp_info1)
        port_info.insert(2,temp_info2)
        for info in range(0,len(port_info)-5) :
            self.txtbxInfo.insertHtml('<p style="text-align: center;"><span style="font-size: 10px;">{}</span><br></p>'.format("--"+self.portInfo[info]+"--"))
            port_info[info]=port_info[info].strip()
            self.txtbxInfo.insertHtml('<p style="text-align: center;"><span style="color: rgb(189, 217, 191); font-size: 9x;">{}</span><br></p>'.format(port_info[info].split('=')[1]))
        
    def disableButtons(self) :
        # disable buttons if the correct port is not selected
        self.btnReadPSWVoltage.setEnabled(False)
        self.btnSetPSWVoltage.setEnabled(False)
        self.btnReadPSWCurrent.setEnabled(False)
        self.btnSetOpenLoopTrq.setEnabled(False)
        self.btnResetBrake.setEnabled(False)
        self.btnReadBrakeSpeed.setEnabled(False)
        self.btnPSWInfo.setEnabled(False)
        self.btnBrakeInfo.setEnabled(False)        
        self.btnReadTemp.setEnabled(False)
        self.btnSetTemp.setEnabled(False)
        self.btnClimateInfo.setEnabled(False)
        self.btnReadTrgTmp.setEnabled(False)

        self.btnSetTemp.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=0, xOffset=0, yOffset=0))
            

    def openPort (self) :

        self.serial_port = str (self.cmbPortList.currentText())
        serial_port_id = self.serial_port[0:5]
        self.serial_port = serial.Serial()
        self.serial_port.port = serial_port_id
        self.serial_port.baudrate=9600
        self.serial_port.timeout=None
        if (self.serial_port.isOpen()==False):
            try :
                self.serial_port.open()
                if (serial_port_id[0:4]=='COM1'):
                    self.btnReadTemp.setEnabled(True)
                    self.btnSetTemp.setEnabled(True)
                    self.btnClimateInfo.setEnabled(True)
                    self.btnReadTrgTmp.setEnabled(True)
                    self.btnReadTemp.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
                    self.btnSetTemp.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
                    self.btnClimateInfo.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
                    self.btnReadTrgTmp.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

                 
                self.btnPSWInfo.setEnabled(True)
                self.btnBrakeInfo.setEnabled(True)  
            except serial.serialutil.SerialException as e:
                print(e)
                self.txtbxInfo.setText("")
                errStr = "The port is not available"
                self.txtbxInfo.insertHtml('<p style="text-align: center;"><span style="font-size: 10px;">{}</span><br></p>'.format(errStr))
                #raise e
        else:
            print("Port is open")

        self.showPortInfo()
                


    def closePort (self) :
        if (self.serial_port.isOpen()==False):
            self.txtbxInfo.setText("")
            errStr = "Port is already closed"
            self.txtbxInfo.insertHtml('<p style="text-align: center;"><span style="font-size: 10px;">{}</span><br></p>'.format(errStr))
        else:
            try:                
                self.serial_port.close()
                self.txtbxInfo.setText("")
                errStr = "Port is closed"
                self.txtbxInfo.insertHtml('<p style="text-align: center;"><span style="font-size: 10px;">{}</span><br></p>'.format(errStr))
            except:
                self.txtbxInfo.setText("")
                errStr = "The serial port cannot be closed"
                self.txtbxInfo.insertHtml('<p style="text-align: center;"><span style="font-size: 10px;">{}</span><br></p>'.format(errStr))
        self.disableButtons()


    # GW Instek PSW-30-36 control functions

    def setPSWVoltage (self) :
        set_voltage_command = "SOUR:VOLT:LEV:IMM:AMPL "
        textboxValue =""
        set_voltage_command = set_voltage_command
        if(self.lneditPSWVoltage.text().isnumeric() and int(self.lneditPSWVoltage.text())<28 and int(self.lneditPSWVoltage.text())>=0):
            textboxValue = self.lneditPSWVoltage.text()
            set_voltage_command = set_voltage_command + textboxValue + "\n"
            self.serial_port.write(set_voltage_command.encode('ascii'))
        else:
            self.txtbrwPSWInfo.setText("Invalid value! Please enter a number between 0-28")
            time.sleep(3)

    def readPSWVoltage (self) :
        self.serial_port.write("MEAS:VOLT:DC?\n".encode('ascii'))
        time.sleep(0.5)
        while True:
            data = self.serial_port.read(self.serial_port.inWaiting())
            if (len(data) > 0):
                for i in range(len(data)):
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
                    self.psw_current = self.psw_current + chr(data[i])
                break


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
                    psw_info= psw_info+chr(data[i])
                break
            else :
                break


        self.txtbrwPSWInfo.setText (psw_info)

        if "GW-INSTEK" in psw_info :
            self.btnReadPSWVoltage.setEnabled(True)
            self.btnSetPSWVoltage.setEnabled(True)
            self.btnReadPSWCurrent.setEnabled(True)                
            self.btnSetPSWVoltage.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
            self.btnReadPSWVoltage.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
            self.btnReadPSWCurrent.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
            self.lneditPSWVoltage.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
            self.lcdNumber.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
            self.lcdReadCurrent.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))


    # Hysteresis Brake Related functions
    def setOpenLoopTrq(self):
        set_open_loop_trq_command = "I1,"
        textboxValue = ""
        set_open_loop_trq_command = set_open_loop_trq_command
        if(self.lneditOpenLoopTrq.text().numeric and int(self.lneditOpenLoopTrq.text())<99 and int(self.lneditOpenLoopTrq.text()>=0)):
            textboxValue = self.lneditOpenLoopTrq.text()
            set_open_loop_trq_command = set_open_loop_trq_command + textboxValue + "\r\n"
            self.serial_port.write(set_open_loop_trq_command.encode('ascii'))
            print ("set the torque")
        else:
            self.txtbrwBrakeInfo.setText("Invalid value! Please enter a number between 0-99")

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
                    brake_info = brake_info+chr(data[i])
                break
            else :
                break


        self.txtbrwBrakeInfo.setText (brake_info)

        if "DSP7" in brake_info :
            self.btnSetOpenLoopTrq.setEnabled(True)
            self.btnResetBrake.setEnabled(True)
            self.btnReadBrakeSpeed.setEnabled(True)
            self.btnSetOpenLoopTrq.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
            self.btnReadBrakeSpeed.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
            self.btnResetBrake.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
            self.txtbrwReadSpeed.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

    def resetBrakeSettings (self) :
        self.serial_port.write("OD1\r\n".encode('ascii'))

    def readTemp (self):
        time.sleep(1)
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()
        self.serial_port.flush()
        self.serial_port.write(b"\x01\x04\x10\x04\x00\x02\x34\xCA")
        time.sleep(1)
        data = self.serial_port.read(self.serial_port.inWaiting())
        decTemp = data[5]<<24 | data[6]<<16|data[3]<<8|data[4]
        hexTemp=str(hex(decTemp))[2:]
        finalTemp = str(struct.unpack('!f',bytes.fromhex(hexTemp)))[1:5]        
        self.lcdClimateRead.setSegmentStyle (QLCDNumber.Flat)
        self.lcdClimateRead.setDigitCount (8)
        self.lcdClimateRead.display (finalTemp)

    def float_to_hex(self,temp,tempList):
        tempHex = struct.unpack('<I', struct.pack('<f', temp))[0]
        t1 = tempHex>>24
        t2 =(tempHex & 0x00FF0000) >> 16
        t3=(tempHex & 0x0000FF00) >> 8
        t4 = (tempHex & 0x000000FF)

        tempList.append(t3)
        tempList.append(t4)
        tempList.append(t1)
        tempList.append(t2)
        return tempList

    def MODBUS_CRC16_v1(self,command,crc):
        bitt= 0
        for i in command:
            crc = crc^i
            for bitt in range(1, 9):
                if crc & 0x0001 :
                    crc>>= 1;
                    crc ^= 0xA001;
                else :
                    crc >>=1
        return crc

    def formTemp(self,tempList,command,crc):
        for i in range(0,4) :
            command.append(tempList[i])
        crc = self.MODBUS_CRC16_v1(command,crc)
        crc1 = crc&0xFF
        crc2 = crc>>8
        command.append(crc1)
        command.append(crc2)
        return command
        
        
    def setTemp(self):
        self.fixedSetTempCmd = [0x01, 0x10, 0x11, 0x4c, 0x00, 0x02, 0x04]
        self.serial_port.flush()
        if(self.lneditTemp.text().isalpha()==False):
            self.temptemP =int(self.lneditTemp.text())
            if (self.temptemP>150 or self.temptemP<-50):
                self.lneditTemp.setText("Invalid")
            else:
                self.tempList = []
                self.temP=self.temptemP
                self.tempList=self.float_to_hex(self.temP,self.tempList)
                self.fixedSetTempCmd= self.formTemp(self.tempList,self.fixedSetTempCmd,self.crc)
                self.serial_port.write(bytearray(self.fixedSetTempCmd))
                self.serial_port.reset_input_buffer()
                self.serial_port.reset_output_buffer()
                self.serial_port.flush()

        else:
            self.lneditTemp.setText("Invalid")

            
    def readTrgTemp(self):
        self.serial_port.flush()
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()
        self.serial_port.write(b"\x01\x04\x10\xB2\x00\x02\xD5\x2C")
        time.sleep(0.1)
        data = self.serial_port.readline(self.serial_port.inWaiting())
        decTemp = data[5]<<24 | data[6]<<16|data[3]<<8|data[4]
        if(decTemp==0):
            finalTemp = '0.0'
            self.lcdClimateReadTrg.setSegmentStyle (QLCDNumber.Flat)
            self.lcdClimateReadTrg.setDigitCount (8)
            self.lcdClimateReadTrg.display (finalTemp)
        else:
            hexTemp=str(hex(decTemp)[2:])
            finalTemp = str(struct.unpack('!f',bytes.fromhex(hexTemp)))[1:6]
            self.lcdClimateReadTrg.setSegmentStyle (QLCDNumber.Flat)
            self.lcdClimateReadTrg.setDigitCount (8)
            self.lcdClimateReadTrg.display (finalTemp)
            self.serial_port.flush()
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    UIWindow = SerialUi()
    UIWindow.show()
    app.exec_()
