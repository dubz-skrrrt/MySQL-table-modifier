from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import _column_descriptions
import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk
import pandas as pd
import xlrd

window = tk.Tk()
window.title("MySQL Table Modifier")
window.geometry("600x680")

def getInput():
    inp_db = input_db.get()
    return inp_db

def Choosing_Database():
    # code
    global engine, user, password, host, port, database, r_set
    user = 'root'
    password = 'qwerty1234'
    host = 'localhost'
    port = 3306
    database = getInput()

    try:
        input_db.delete(0, END)
        engine = create_engine("mysql://{0}:{1}@{2}:{3}/{4}".format(
            user,
            password,
            host,
            port,
            database))  # after//= user:password@localhost(or ip address)/database name

        lbl.config(text=f"Database: connection to the '{host}' for user '{user}' created successfully")
        r_set = engine.execute("SHOW TABLES")

        create_table_list()
        print(f"connection to the {host} for user {user} created successfully")
    except SQLAlchemyError as e:
        print("Error in connecting to database due to the following error: ", e)

def create_table_list():
    i = 0
    search_tbl = Entry(table_frame, width=25)
    search_tbl.insert(0, 'search for a table...')
    search_tbl.grid(row=3, column=0)
    search_btn = Button(table_frame, text="Search", command=Choosing_Database)
    search_btn.grid(row=3, column=1)
    title = [i for i in r_set.keys()]
    print(title)
    list_tbl = Label(table_frame, text=f"{title}", width=25, borderwidth=2, relief="ridge", anchor='w',
                     bg='green')
    list_tbl.grid(row=4, column=0, pady=10)

    for data in r_set:
        for j in range(len(data)):
            list_tables = Label(table_frame, text=data[j], width=25, borderwidth=2, relief="ridge", anchor='w')
            list_tables.grid(row=i + 5, column=j, pady=2.5)
            checkDB = Button(table_frame, text="Update", command=Choosing_Table)
            checkDB.grid(row=i + 5, column=j+1, pady=2.5)
        i = i + 1

def Choosing_Table():
    # code

    print()

input_lbl_db = Label(window, text="Database: ")
input_lbl_db.pack()
input_db = Entry(window, width=30)
input_db.pack()

checkDB = Button(window, text="Submit", command=Choosing_Database)
checkDB.pack()

lbl = Label(window, text="")
lbl.pack()

table_frame = Frame(window)
table_frame.pack()
print(window.grid_size())
#Choosing_Database()
window.mainloop()





