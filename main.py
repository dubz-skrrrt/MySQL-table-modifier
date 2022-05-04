from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import xlrd

window = tk.Tk()
window.title("MySQL Table Modifier")
window.geometry("1080x720")

def getInput():
    inp_db = input_db.get(1.0, "end-1c")
    #lbl.config(text="Database: " + inp_db)
    return inp_db

def Choosing_Database():
    # code
    user = 'root'
    password = 'qwerty1234'
    host = 'localhost'
    port = 3306
    database = getInput()

    try:
        engine = create_engine("mysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))  # after//= user:password@localhost(or ip address)/database name
        lbl.config(text=f"Database: connection to the '{host}' for user '{user}' created successfully")
        print(f"connection to the {host} for user {user} created successfully")
    except SQLAlchemyError as e:
        print("Error in connecting to database due to the following error: ", e)


def Choosing_Table():
    # code
    print()

input_db = tk.Text(window, height=1, width=20)
input_db.pack()

checkDB = tk.Button(window, text="Submit", command=Choosing_Database)
checkDB.pack()

lbl = tk.Label(window, text="")
lbl.pack()
window.mainloop()





