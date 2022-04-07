from calendar import calendar
from msilib.schema import Error
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import *
import sqlite3
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6 import QtCore
from PyQt6.QtCore import Qt



class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui',self)
        self.setWindowTitle('Daily Task Planner')
        
        self.calendarWidget = self.findChild(QCalendarWidget,'calendarWidget')
        self.listWidget = self.findChild(QListWidget,'listWidget')
        
        self.addBtn = self.findChild(QPushButton,'addBtn')
        self.newTask = self.findChild(QLineEdit,'newTask')
        self.addBtn.clicked.connect(self.addNew)
        
        self.saveBtn = self.findChild(QPushButton,'saveBtn')
        self.saveBtn.clicked.connect(self.saveChanges)
        
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()

        
        
        
    def calendarDateChanged(self):
        dateSelected = self.calendarWidget.selectedDate()
        date = (str(dateSelected.toPyDate()))
        self.updateTaskList(date)
        
        
    def addNew(self):
        task = self.newTask.text()
        item = QListWidgetItem(task)
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Unchecked)
        self.listWidget.addItem(item)

    def updateTaskList(self,date):

        try : 
                self.listWidget.clear()
                db = sqlite3.connect('data.db')
                cursor = db.cursor()
                query = 'SELECT task,completed FROM tasks where date = ?'
                row = (date,)
                results = cursor.execute(query,row).fetchall()
            
                for result in results:
                    task = str(result[0])
                    item = QListWidgetItem(task)
                
                    item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
                
                    if result[1] == 'YES':
                        item.setCheckState(Qt.CheckState.Checked)
                        
                    elif result[1] == 'NO':
                        item.setCheckState(Qt.CheckState.Unchecked)
                        
                    self.listWidget.addItem(item)
                
        except sqlite3.Error as e:
                print(e)

    def saveChanges(self):
        try:
        
            db = sqlite3.connect('TodoList.db')
            cursor = db.cursor()
            date = self.calendarWidget.selectedDate().toPyDate()
        
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(i)
                task = item.text()
                if item.checkState() == Qt.CheckState.Checked:
                    completed = 'YES'
                    info = [task,completed,date]
                    cursor.execute('INSERT INTO tasks (task,completed,date) VALUES(?,?,?)',info)
                    db.commit()
                    
            
                else:
                    completed = 'NO'
                    info = [task,completed,date]
                    cursor.execute('INSERT INTO tasks (task,completed,date) VALUES(?,?,?)',info)
                    db.commit()
                    
                    
        except sqlite3.Error as e:
            print(e)



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())