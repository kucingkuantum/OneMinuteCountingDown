# -*- coding: utf-8 -*-
"""

@author: siregar
"""

import sys
from PyQt5.QtGui import QColor 
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.Qt import QMainWindow,qApp,  QTimer
from gui import Ui_MainWindow
import pyaudio  
import wave 

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow, self).__init__(parent)
        qApp.installEventFilter(self)
        
        self.setupUi(self)
        self.lcdNumber.display('{:02d}:{:02d}'.format(1, 0))
        self.pB_Start.clicked.connect(self.readone)
        self.pB_Stop.clicked.connect(self.Stop)


    def closeEvent(self, event):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Exit')
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Warning")
        msgBox.setInformativeText('Are you sure to close the window ?')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        reply = msgBox.exec_()
        if reply == QMessageBox.Yes:
            event.accept()
            if hasattr(self,'timer'):
                self.timer.stop()
            app.quit()
        else:
            event.ignore()
                 
        
    def Stop(self):
        if hasattr(self,'timer'):
            self.timer.stop()
        if hasattr(self,'counter'):
            mins, secs = divmod(self.counter, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.lcdNumber.display(timeformat)
        else:
            self.lcdNumber.display('{:02d}:{:02d}'.format(1, 0))

            
    def readone(self):

        m = 1
        t = int(m*60)
        self.palette = self.lcdNumber.palette()

        # foreground color
        self.palette.setColor(self.palette.WindowText, QColor(0, 0, 0))
        self.lcdNumber.setPalette(self.palette)
        
        self.counter = t
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.lcdNumber.display(timeformat)
        self.timer = QTimer()
        
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
            
    def recurring_timer(self):
        self.counter -=1
        if self.counter < 11:
            self.palette.setColor(self.palette.WindowText, QColor(255, 0, 0))
            self.lcdNumber.setPalette(self.palette)
            
        mins, secs = divmod(self.counter, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.lcdNumber.display(timeformat)
        if (self.counter == -1):
            self.bell()
            self.lcdNumber.display('{:02d}:{:02d}'.format(0, 0))           
            self.bell()

    def bell(self):
        chunk = 1024
        #open a wav format music  
        f = wave.open("service-bell_daniel_simion.wav","rb")  
        #instantiate PyAudio  
        p = pyaudio.PyAudio()  
        #open stream  
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output = True)  
        #read data  
        data = f.readframes(chunk)  
        
        #play stream  
        while data:  
            stream.write(data)  
            data = f.readframes(chunk)  
        
        #stop stream  
        stream.stop_stream()  
        stream.close()  
        
        #close PyAudio  
        p.terminate()  


        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
