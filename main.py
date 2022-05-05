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
window.geometry("1080x720")

list_of_Tables =[]

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

        #lbl.config(text=f"Database: connection to the '{host}' for user '{user}' created successfully")
        r_set = engine.execute("SHOW TABLES")

        create_table_list()
        print(f"connection to the {host} for user {user} created successfully")
    except SQLAlchemyError and BaseException as e:
        print("Error in connecting to database due to the following error: ", e)

def create_table_list():
    i = 0

    title = [i for i in r_set.keys()]
    print(title)
    list_tbl = Label(table_frame, text=f"{title}", width=25, borderwidth=2, relief="ridge", anchor='w',
                     bg='green')
    list_tbl.grid(row=4, column=0, pady=10)

    for data in r_set:

        for j in range(len(data)):
            ind = 0

            list_tables = Label(table_frame, text=data[j], width=25, borderwidth=2, relief="ridge", anchor='w')
            list_tables.grid(row=i + 5, column=j, pady=2.5)

            checkDB = Button(table_frame, text="Update Table")
            checkDB.configure(command=lambda b=data[ind]: check_Table(b))
            checkDB.grid(row=i + 5, column=j+1, pady=2.5, padx=50)
            list_of_Tables.append(data[ind])

            ind = ind+1
        i = i + 1

def check_Table(num):
    global selected_table
    for tables in list_of_Tables:
        if num == tables:
            table = tables
            print(table)
            selected_table = engine.execute(f"""SELECT * FROM {table}""")   # selects and executes the table
            Data_Table()

def Data_Table():
    # code
    headers = [i for i in selected_table.keys()]
    tree["columns"] = headers
    tree["show"] = 'headings'
    ind = 0
    for heading in headers:                         # Creates the headers for the treeview table
        tree.column(heading, width=5, anchor='c')
        tree.heading(heading, text=heading)
        ind += 1
    data_ind = 0
    for data in selected_table:
        tree.insert(parent="",
                    index='end',
                    iid=data[data_ind],
                    text=data[data_ind],
                    values=data[0:len(data)])       # Pass the data from mySQL table to the treeview table
        data_ind += 1
    search_tbl = Entry(search_frame, width=25)
    search_tbl.insert(0, 'search for id...')
    search_tbl.grid(row=10, column=0)
    search_btn = Button(search_frame, text="Search")
    search_btn.grid(row=10, column=1)

def selectDetails(items):
    curItem = tree.focus()
    print(tree.item(curItem, option='values'))      # returns the values of the clicked row


input_lbl_db = Label(window, text="Database: ")
input_lbl_db.pack()
input_db = Entry(window, width=20)
input_db.pack()

checkDB = Button(window, text="Submit", command=Choosing_Database)
checkDB.pack()

lbl = Label(window, text="")
lbl.pack()

table_frame = Frame(window, borderwidth=2, relief='ridge')
table_frame.pack()

search_frame = Frame(window)
search_frame.pack()
data_table_frame = Frame(window, width=50)
data_table_frame.pack()
tree = ttk.Treeview(data_table_frame, selectmode='browse', height=5)
tree.pack(side="left")
scroll = ttk.Scrollbar(data_table_frame, orient="vertical", command=tree.yview)
scroll.pack(side="right", fill="y")
tree.configure(yscrollcommand=scroll.set)
tree.bind('<Motion>', 'break')
tree.bind('<ButtonRelease-1>', selectDetails)
#Choosing_Database()
window.mainloop()





