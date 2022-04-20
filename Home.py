from PyQt5 import QtWidgets,uic
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit,QMainWindow, QMessageBox,QPushButton, QScrollArea ,QSizePolicy, QWidget, QVBoxLayout
import sys,os




'''
global functions
'''
        

class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage,self).__init__()

        uic.loadUi('HomePage.ui',self)

    def display(self):
        self.show()
        '''
        button press event
        '''
    
    def next(self):
        pass




def display():  
    app=QApplication(sys.argv)
    HomeWindow=HomePage()
    HomeWindow.display()
    app.exec_()


if __name__ == "__main__":
    display()

    
    

