from PyQt5 import QtWidgets,uic
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QStackedWidget,QLineEdit, QWidget,QGraphicsDropShadowEffect,QComboBox,QLabel,QCommandLinkButton,QVBoxLayout,QHBoxLayout,QSpacerItem
from PyQt5.QtGui import QIntValidator,QColor
import sys,os
from datetime import datetime
import db



'''
global functions
'''
        

class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage,self).__init__()

        uic.loadUi('HomePage.ui',self)

        self.onlyInt = QIntValidator(0,99999)
        self.findChild(QLineEdit,"NewExpenseInput").setValidator(self.onlyInt)

        self.vlayout=self.findChild(QVBoxLayout,"thisMonth_layout")
        self.vlayout1=self.findChild(QVBoxLayout,"prevMonth_layout")
        self.vspacer=QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        
        self.setShadow()

        self.adjustComboBox()

        self.prepareFront()
    
    def list_label(self,expense,time):
        date_time=datetime.fromtimestamp(time)
        hbox=QHBoxLayout()
        expense_lable=QLabel()
        expense_lable.setMinimumSize(QtCore.QSize(460,40))
        expense_lable.setMaximumSize(QtCore.QSize(460,40))
        expense_lable.setStyleSheet("border:1px ;\n"
            "border-radius:6px;\n"
            "background:#3A2C5F;\n"
            "color:#ffffff")
        expense_lable.setText(str(expense)+"\t".expandtabs(70)+str(date_time)+"\t")
        expense_lable.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        # time_lable=QLabel()
        # time_lable.setMinimumSize(QtCore.QSize(230,40))
        # time_lable.setMaximumSize(QtCore.QSize(230,40))
        # time_lable.setStyleSheet("border:1px ;\n"
        #     "border-radius:6px;\n"
        #     "background:#3A2C5F;\n"
        #     "color:#ffffff")
        # time_lable.setText(str(date_time))
        # time_lable.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        hbox.addWidget(expense_lable)
        # hbox.addWidget(time_lable)
        return hbox

    def display(self):
        self.show()
        '''
        button press event
        '''
        #self.firstPage=self.findChild(QWidget,"page")
        self.findChild(QPushButton,"FoodButton").clicked.connect(lambda state: self.next("Food"))
        self.findChild(QPushButton,"GroceriesButton").clicked.connect(lambda state: self.next("Groceries"))
        self.findChild(QPushButton,"ShoppingButton").clicked.connect(lambda state: self.next("Shopping"))
        self.findChild(QPushButton,"TravelButton").clicked.connect(lambda state: self.next("Travel"))
        self.findChild(QPushButton,"EntertainmentButton").clicked.connect(lambda state: self.next("Entertainment"))
        self.findChild(QPushButton,"BillsButton").clicked.connect(lambda state: self.next("Bills"))
        self.findChild(QPushButton,"NewExpenseAdd").clicked.connect(lambda state: self.addExpense())
        self.findChild(QCommandLinkButton,"Back").clicked.connect(lambda state:self.backAndDelete(self.vlayout))
        self.findChild(QCommandLinkButton,"Back").clicked.connect(lambda state:self.delete(self.vlayout1))

    def backAndDelete(self,vlayout):
        self.findChild(QStackedWidget,"stackedWidget").setCurrentIndex(0)
        self.findChild(QComboBox,"sortBy_1").setCurrentText("Sort By")
        self.findChild(QComboBox,"sortBy_2").setCurrentText("Sort By")
        if vlayout is not None:
            while vlayout.count():
                item = vlayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.backAndDelete(item.layout())
        
    def delete(self,vlayout):
        # self.findChild(QStackedWidget,"stackedWidget").setCurrentIndex(0)
        if vlayout is not None:
            while vlayout.count():
                item = vlayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.delete(item.layout())

    def addExpense(self):
        # get expense amount from input box
        expense = int(self.findChild(QLineEdit,"NewExpenseInput").text())
        # clear input box
        self.findChild(QLineEdit,"NewExpenseInput").clear()
        # get expense category from category drop box
        category = self.findChild(QComboBox,"ExpenseCategory").currentText()
        #get current timestamp
        timestamp = int(datetime.now().timestamp())
        #add it to db
        db.insertExpense(timestamp, category, expense)
        #update frontend statistics
        self.prepareFront()

    def Fun(self,e):
        return e[0]

    def next(self, category):
        # Prepare all the data required in second page here
        self.sortList(category)
        self.sortList1(category)
        self.findChild(QComboBox,"sortBy_1").activated.connect(lambda:self.sortList(category))
        self.findChild(QComboBox,"sortBy_2").activated.connect(lambda:self.sortList1(category))
        # Till here and then increment index to 1
        self.findChild(QStackedWidget,"stackedWidget").setCurrentIndex(1)
        
    def sortList(self,category):
        #deleting the previous List
        self.delete(self.vlayout)
        #getting this months expenses List and combobox current text
        thisMonthExpenseListByCategory=db.listByCategoryThisMonth(category)
        sort_1=self.findChild(QComboBox,"sortBy_1").currentText()
        #sorting the list according to the combobox text
        if sort_1=="Date":
            # self.delete()
            thisMonthExpenseListByCategory.sort(reverse=True)
            
            for i in range(len(thisMonthExpenseListByCategory)):
                lab=self.list_label(thisMonthExpenseListByCategory[i][0],thisMonthExpenseListByCategory[i][1])
                self.vlayout.addLayout(lab)  
            self.vlayout.addItem(self.vspacer)
            
        elif sort_1 =="Expenses Low To High":
            asceThisMonthList_1=db.listByCategoryThisMonth(category)
            asceThisMonthList_1.sort(key=self.Fun)

            for i in range(len(asceThisMonthList_1)):
                lab=self.list_label(asceThisMonthList_1[i][0],asceThisMonthList_1[i][1])
                self.vlayout.addLayout(lab)
            self.vlayout.addItem(self.vspacer)

        elif sort_1=="Expenses High To Low":
            descThisMonthList_1=db.listByCategoryThisMonth(category)
            descThisMonthList_1.sort(reverse=True,key=self.Fun)
            for i in range(len(descThisMonthList_1)):
                lab=self.list_label(descThisMonthList_1[i][0],descThisMonthList_1[i][1])
                self.vlayout.addLayout(lab)
            self.vlayout.addItem(self.vspacer)
        
        else:
            thisMonthExpenseListByCategory=db.listByCategoryThisMonth(category)

            for i in range(len(thisMonthExpenseListByCategory)):
                lab=self.list_label(thisMonthExpenseListByCategory[i][0],thisMonthExpenseListByCategory[i][1])
                self.vlayout.addLayout(lab)
            self.vlayout.addItem(self.vspacer)

    def sortList1(self,category):
        #deleting the previous List
        self.delete(self.vlayout1)
        #getting previous months expenses List and combobox current text
        previousMonthsExpenseListByCategory=db.listByCategoryPreviousMonth(category)
        sort_2=self.findChild(QComboBox,"sortBy_2").currentText()
        #sorting the list according to the combobox text
        if sort_2=="Date":
            previousMonthsExpenseListByCategory.sort(reverse=True)

            for i in range(len(previousMonthsExpenseListByCategory)):
                lab=self.list_label(previousMonthsExpenseListByCategory[i][0],previousMonthsExpenseListByCategory[i][1])
                self.vlayout1.addLayout(lab)
            self.vlayout1.addItem(self.vspacer)

        elif sort_2 =="Expenses Low To High":
            ascePrevMonthList_2=db.listByCategoryPreviousMonth(category)
            ascePrevMonthList_2.sort(key=self.Fun)

            for i in range(len(ascePrevMonthList_2)):
                lab=self.list_label(ascePrevMonthList_2[i][0],ascePrevMonthList_2[i][1])
                self.vlayout1.addLayout(lab)
            self.vlayout1.addItem(self.vspacer)

        elif sort_2=="Expenses High To Low":
            descPrevMonthList_2=db.listByCategoryPreviousMonth(category)
            descPrevMonthList_2.sort(reverse=True,key=self.Fun)

            for i in range(len(descPrevMonthList_2)):
                lab=self.list_label(descPrevMonthList_2[i][0],descPrevMonthList_2[i][1])
                self.vlayout1.addLayout(lab)
            self.vlayout1.addItem(self.vspacer)

        else:
            previousMonthsExpenseListByCategory=db.listByCategoryPreviousMonth(category)

            for i in range(len(previousMonthsExpenseListByCategory)):
                lab=self.list_label(previousMonthsExpenseListByCategory[i][0],previousMonthsExpenseListByCategory[i][1])
                self.vlayout1.addLayout(lab)
            self.vlayout1.addItem(self.vspacer)

    def prepareFront(self):
        # this month expenses count
        thisMonthExpensesCount = db.expensesCountThisMonth()
        # this month expenses sum
        thisMonthExpensesSum = db.totalExpenseThisMonth()
        # last month expenses sum
        lastMonthExpensesSum = db.totalExpenseLastMonth()
        # % change from last month
        if lastMonthExpensesSum == 0:
            percentage_change = 0
        else:
            percentage_change = round((thisMonthExpensesSum - lastMonthExpensesSum) / lastMonthExpensesSum * 100,1)
        # this month expense by cateogory
        thisMonthExpensesByCategory = db.expenseByCategory()

        # update frontend
        self.findChild(QLabel,"ExpensesCount").setText("Number of expenses this month: "+str(thisMonthExpensesCount))

        self.findChild(QLabel,"MonthExpense").setText("Rs. "+str(thisMonthExpensesSum))

        if percentage_change > 0:
            self.findChild(QLabel,"MonthExpenseSubTitle").setText(str(percentage_change)+"% more than last month’s expense\nLast Month’s total expense: Rs. "+str(lastMonthExpensesSum))
        elif percentage_change < 0:
            self.findChild(QLabel,"MonthExpenseSubTitle").setText(str(percentage_change * -1)+"% less than last month’s expense\nLast Month’s total expense: Rs. "+str(lastMonthExpensesSum))
        else:
            self.findChild(QLabel,"MonthExpenseSubTitle").setText("No expenses in last month\nLast Month’s total expense: Rs. "+str(lastMonthExpensesSum))
        
        for cat in thisMonthExpensesByCategory:
            self.findChild(QLabel,cat[0]+"Expense").setText("Rs. "+str(cat[1]))
        pass


########## Styling functions ##########
    def adjustComboBox(self):
        comboBox = self.findChild(QComboBox,"ExpenseCategory")
        comboBox_1=self.findChild(QComboBox,"sortBy_1")
        comboBox_2=self.findChild(QComboBox,"sortBy_2")
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
        comboBox_1.setStyleSheet("""
        QComboBox {
            border:none;
            outline:none;
            color:#FFF;
            border-radius:5px;
            text-align:center;
            font-family:Monsterrat;
        }
        QComboBox::drop-down {
            
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
        comboBox_2.setStyleSheet("""
        QComboBox {
            border:none;
            outline:none;
            color:#FFF;
            border-radius:5px;
            text-align:center;
            font-family:Monsterrat;
        }
        QComboBox::drop-down {
            
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

    
    

