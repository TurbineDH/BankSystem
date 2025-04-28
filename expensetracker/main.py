from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit,QComboBox,QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate, Qt
import sys

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(550, 550)
        self.setWindowTitle("Expense Tracker")

        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.add_button = QPushButton("Add Expense")
        self.delete_button = QPushButton("Delete Expense")
        #add and delete events 
        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)       

        self.table = QTableWidget() 
        self.table.setColumnCount(5) #id,date,category,amount,description
        header_names = ["ID", "Date", "Category", "Amount", "Description"]
        self.table.setHorizontalHeaderLabels(header_names)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.sortByColumn(1,Qt.DescendingOrder)


        self.dropdown.addItems(["Food", "Transportation", "Rent", "Shopping", "Entertainment", "Bills", "Others"])

        self.setStyleSheet("""
                           QWidget {background-color: #b8c9e1;}
                           QLabel{
                                color: #333;
                                font-size: 14px;
                           }
                           QLineEdit, QComboBox, QDateEdit{
                                background-color: #b8c9e1;
                                color: #333;
                                border: 1px solid #444;
                                padding: 5px;
                           }
                           QTableWidget{
                                background-color: #b8c9e1;
                                color: #333;
                                border: 1px solid #444;                               
                                selection-background-color: #ddd;

                           }
                           QPushButton{
                                background-color: #4caf50;
                                color: #fff;
                                border: none;
                                padding: 8px 16px;
                                font-size: 14px;
                           }
                           QPushButton:hover{background-color: #45a049;}
                            """)


        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(QLabel("Date: "))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category: "))
        self.row1.addWidget(self.dropdown)

        self.row2.addWidget(QLabel("Amount: "))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description: "))
        self.row2.addWidget(self.description)

        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)


        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)

        self.master_layout.addWidget(self.table)

        self.setLayout(self.master_layout)
        

        self.load_table()  #load table when init


    def load_table(self):
        self.table.setRowCount(0)           #set the starting point to 0 

        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        while query.next():                 #while there is a next row in database run:
            expense_id = query.value(0)         #values are the columns of the row
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            # add values to the table
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1 

    def add_expense(self):
        date =  self.date_box.date().toString("yyyy-MM-dd")     #prepare variables to take values
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        query = QSqlQuery() 
        query.prepare("""
                    INSERT INTO expenses (date, category, amount, description)
                    VALUES (?,?,?,?)                                
                    """)                                        #bind values are in order marked by "?"
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()

        #reset table
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()

    def delete_expense(self):
        selected_row = self.table.currentRow()    #select the row to be deleted
        if selected_row == -1:                      # if no row selected 
            QMessageBox.warning(self, "No Expense Chosen", "Please choose an expense to delete!")
            return
        
        expense_id = int(self.table.item(selected_row, 0).text())       # get the row id as string and pass it to integer

        confirm = QMessageBox.question(self, "Are you sure?", "Delete Expense?", QMessageBox.Yes | QMessageBox.No)      #window with 2 options

        if confirm == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?") # ? bind value
        query.addBindValue(expense_id)
        query.exec_()

        self.load_table()




#CREATE DATEBASE
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Could not open database")
    sys.exit(1)             #closes the small window

query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                amount REAL,
                description TEXT
            )
            """)



if __name__ in "__main__":      # this if statement helps the program to exec the app only when ran from the main.py file
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec_()
