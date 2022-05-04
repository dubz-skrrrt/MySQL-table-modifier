from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import xlrd

window = tk.Tk()
window.title("MySQL Table Modifier")
window.geometry("1080x720")
window.columnconfigure(10, weight=3)
def getInput():
    inp_db = input_db.get(1.0, "end-1c")
    return inp_db

def Choosing_Database():
    # code
    user = 'root'
    password = 'qwerty1234'
    host = 'localhost'
    port = 3306
    database = 'ExcelFileImporter'

    try:
        engine = create_engine("mysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))  # after//= user:password@localhost(or ip address)/database name
        #lbl.config(text=f"Database: connection to the '{host}' for user '{user}' created successfully")

        inspector = inspect(engine)
        tables = inspector.get_table_names()
        total_rows = len(tables)
        total_colums = len(tables[0])
        print(tables)
        list_tbl = Label(window, text=f"Tables in {database}", width=20, borderwidth=2, relief="ridge", anchor='w', bg='green')
        list_tbl.grid(row=6, column=0)
        for i in range(total_rows):

                list_tbl = Label(window, text=tables[i], width=20, borderwidth=2, relief="ridge", anchor='w')
                list_tbl.grid(row=i+7, column=0)
                checkDB = Button(window, text="Update", command=Choosing_Table)
                checkDB.grid(row=i+7, column=2)
                #list_tbl.insert(END, tables[i])
        print(f"connection to the {host} for user {user} created successfully")
    except SQLAlchemyError as e:
        print("Error in connecting to database due to the following error: ", e)
    finally:

        print()
        # input_lbl_tbl = Label(window, text="Table: ")
        # input_lbl_tbl.pack()
        # input_tbl = tk.Text(window, height=1, width=20)
        # input_tbl.pack()

def Choosing_Table():
    # code
    print()

input_lbl_db = Label(window, text="Database: ")
input_lbl_db.grid(row=0, column=5)
input_db = Text(window, height=1, width=30)
input_db.grid()

checkDB = Button(window, text="Submit", command=Choosing_Database)
checkDB.grid()

lbl = Label(window, text="")
lbl.grid()

print(window.grid_size())
#Choosing_Database()
window.mainloop()





