from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QStackedWidget,QLineEdit, QWidget,QGraphicsDropShadowEffect,QComboBox
from PyQt5.QtGui import QIntValidator,QColor
import sys,os




'''
global functions
'''
        

class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage,self).__init__()

        uic.loadUi('HomePage.ui',self)

        self.onlyInt = QIntValidator(0,99999)
        self.findChild(QLineEdit,"NewExpenseInput").setValidator(self.onlyInt)

        self.setShadow()

        self.adjustComboBox()

    def display(self):
        self.show()
        '''
        button press event
        '''
        self.findChild(QPushButton,"FoodButton").clicked.connect(lambda state: self.next("Food"))
        self.findChild(QPushButton,"GroceriesButton").clicked.connect(lambda state: self.next("Groceries"))
        self.findChild(QPushButton,"ShoppingButton").clicked.connect(lambda state: self.next("Shopping"))
        self.findChild(QPushButton,"TravelButton").clicked.connect(lambda state: self.next("Travel"))
        self.findChild(QPushButton,"EntertainmentButton").clicked.connect(lambda state: self.next("Entertainment"))
        self.findChild(QPushButton,"BillsButton").clicked.connect(lambda state: self.next("Bills"))
        self.findChild(QPushButton,"NewExpenseAdd").clicked.connect(lambda state: self.addExpense())
    

    def addExpense(self):
        # get expense amount from input box

        # get expense category from category drop box

        #get current timestamp

        #add it to db

        #update frontend statistics

        pass
    
    def next(self, category):
        # Prepare all the data required in second page here








        # Till here and then increment index to 1
        self.findChild(QStackedWidget,"stackedWidget").setCurrentIndex(1)


########## Styling functions ##########
    def adjustComboBox(self):
        comboBox = self.findChild(QComboBox,"ExpenseCategory")
        

        comboBox.setStyleSheet("""
        QComboBox {
            border:none;
            outline:none;
            background-color:#9EA3F5;
            color:#FFF;
            border-radius:5px;
            text-align:center;
            font-family:Monsterrat;
        }
        QComboBox::drop-down {
            background-color:#9EA3F5;
            border-radius:5px;
            color:#FFF;
        }
        QComboBox::down-arrow {
            image: url(./assets/icons8-expand-arrow-30.png);
            right:6px;
            width:22px;
            height:22px;
        }
        QComboBox QAbstractItemView {
            color:#FFF;
            border:none;
            selection-background-color:#9EA3F5;            
        }
        """)
    
    def setShadow(self):
        shadows = []
        for _ in range(8):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setXOffset(4)
            shadow.setYOffset(4)
            shadow.setColor(QColor(0, 0, 0, 63))
            shadows.append(shadow)

        self.findChild(QPushButton,"NewExpenseAdd").setGraphicsEffect(shadows[0])
        self.findChild(QComboBox,"ExpenseCategory").setGraphicsEffect(shadows[1])
        self.findChild(QWidget,"FoodCard").setGraphicsEffect(shadows[2])
        self.findChild(QWidget,"GroceriesCard").setGraphicsEffect(shadows[3])
        self.findChild(QWidget,"ShoppingCard").setGraphicsEffect(shadows[4])
        self.findChild(QWidget,"TravelCard").setGraphicsEffect(shadows[5])
        self.findChild(QWidget,"EntertainmentCard").setGraphicsEffect(shadows[6])
        self.findChild(QWidget,"BillsCard").setGraphicsEffect(shadows[7])
        

        
        





def display():  
    app=QApplication(sys.argv)
    HomeWindow=HomePage()
    HomeWindow.display()
    app.exec_()


if __name__ == "__main__":
    display()

    
    

