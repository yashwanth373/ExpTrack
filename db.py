import sqlite3
from datetime import date, datetime, time, timedelta,timezone
import dateutil.relativedelta


conn = sqlite3.connect('test.db')

# conn.execute('''CREATE TABLE EXPENSES(timestamp INT PRIMARY KEY NOT NULL, category TEXT NOT NULL, expense INT NOT NULL);''')

def insertExpense(timestamp, category, expense):
    conn.execute("INSERT INTO EXPENSES VALUES(?,?,?)", (timestamp, category, expense))
    conn.commit()
    print("Expense added")


def expensesCountThisMonth():
    # get current month's beginning timestamp
    begTime = int(datetime.today().replace(day=1,hour=0,minute=0,second=0,microsecond=0).timestamp())
    # get all expenses from this month
    expenses = conn.execute("SELECT COUNT(*) FROM EXPENSES WHERE timestamp >= ?", (begTime,))
    # return the count
    return expenses.fetchone()[0]

def totalExpenseThisMonth():
    # get current month's beginning timestamp
    begTime = int(datetime.today().replace(day=1,hour=0,minute=0,second=0,microsecond=0).timestamp())
    # get all expenses from this month
    expenses = conn.execute("SELECT SUM(expense) FROM EXPENSES WHERE timestamp >= ?", (begTime,))
    # return the count
    return expenses.fetchone()[0]

def totalExpenseLastMonth():
    last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
    lastMonthEndTime = int(datetime.combine(last_day_of_prev_month, time(23,59,59)).timestamp())
    lastMonthBegTime = int(datetime.combine(date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day), time(0,0,0)).timestamp())
    
    expenses = conn.execute("SELECT SUM(expense) FROM EXPENSES WHERE timestamp >= ? AND timestamp <= ?", (lastMonthBegTime, lastMonthEndTime))

    return expenses.fetchone()[0]

