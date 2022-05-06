from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk, messagebox
import pandas as pd
import xlrd

window = tk.Tk()
window.title("MySQL Table Modifier")
window.geometry("1080x720")

list_of_Tables =[]
list_of_entry_lbl = []
list_of_entry_widgets = []
list_of_data = []
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
        dbConnect_Top.destroy()
        print(f"connection to the {host} for user {user} created successfully")
    except (SQLAlchemyError, BaseException) as e:
        messagebox.showerror("Error in connecting to database due to the following error: ", e)

def create_table_list():
    i = 0

    title = [i for i in r_set.keys()]
    print(title)
    list_tbl = Label(table_frame, text=f"{title}", width=25, borderwidth=2, relief="ridge", anchor='w',
                     bg='lightgray')
    list_tbl.grid(row=4, column=0, pady=10)

    for data in r_set:

        for j in range(len(data)):
            ind = 0

            list_tables = Label(table_frame, text=data[j], width=25, borderwidth=2, relief="ridge", anchor='w')
            list_tables.grid(row=i + 5, column=j, pady=2.5)

            checkDB = Button(table_frame, text="Update Table")

            checkDB.grid(row=i + 5, column=j+1, padx=50)
            if data[ind] not in list_of_Tables:
                print(data[ind] not in list_of_Tables)
                list_of_Tables.append(data[ind])
                checkDB.configure(command=lambda b=data[ind]: check_Table(b))
            else:
                print(data[ind] not in list_of_Tables)
                checkDB.configure(command=NONE)
            ind = ind+1
        i = i + 1



def check_Table(num):
    global selected_table, search_tbl, table
    #menubar.add_cascade(label="Choose Table", command=create_table_list)
    for tables in list_of_Tables:
        if num == tables:
            table = tables
            print(table)
            selected_table = engine.execute(f"""SELECT * FROM {table}""")   # selects and executes the table
            Data_Table()

def Data_Table():
    # code
    global headers
    num = 0
    headers = [i for i in selected_table.keys()]

    tree["columns"] = headers
    tree["show"] = 'headings'
    ind = 0

    delete_Table()
    clear_entry(list_of_entry_lbl)
    clear_entry(list_of_entry_widgets)

    entries()
    print(list_of_entry_widgets)
    for heading in headers:                         # Creates the headers for the treeview table
        tree.column(heading, width=15*len(headers), anchor='c')
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
def singleData_Table():
    id_details = search_tbl.get()
    #print(id_details)
    try:
        for records in tree.get_children():
            tree.delete(records)
        single_data = engine.execute(f"""SELECT * FROM {table} WHERE id = {id_details}""")
        results = single_data.fetchone()
        print(results)
        tree.insert(parent="",
                    index=0,
                    text=results,
                    values=results[0:len(results)])
    except (NameError, TypeError) as e:
        print(f"Couldn't search due to the following error: {e}")
        messagebox.showerror('Python Error', f"Couldn't search due to the following error: {e}")


def delete_Table():
    x = tree.selection()
    for records in x:
        tree.delete(records)
    for item in tree.get_children():
        tree.delete(item)

def clear_entry(list_of_widgets):
    for widgets in list_of_widgets:
        widgets.destroy()


def open_Connector():
    global input_db, dbConnect_Top
    dbConnect_Top = Toplevel(window)
    dbConnect_Top.geometry("250x200")
    dbConnect_Top.title("Database Connector")

    input_lbl_db = Label(dbConnect_Top, text="Database: ")
    input_lbl_db.pack(pady=25)
    input_db = Entry(dbConnect_Top, width=40)
    input_db.pack(padx=25)

    checkDB = Button(dbConnect_Top, text="Submit", command=Choosing_Database)
    checkDB.pack(pady=10)
def selectDetails(items):
    global values
    clearDataEntry()
    curItem = tree.focus()
    #print(tree.item(curItem, option='values'))      # returns the values of the clicked row (need to pass the values for each entry)
    values = tree.item(curItem, option='values')
    i = 0
    for data in values:
        list_of_data.append(data)
    for passdata in list_of_entry_widgets:
        passdata.insert(0, list_of_data[i])
        i+=1

def clearDataEntry():
    for inputs in list_of_entry_widgets:
        inputs.delete(0, END)
    del list_of_data[:]


def entries():
    global input

    for headings in headers:
        entryLbl = Label(entry_headings_frame, width=15, text=headings)
        entryLbl.pack(side=LEFT)
        list_of_entry_lbl.append(entryLbl)
    for entry in range(len(headers)):
        var = tk.StringVar()

        input = Entry(entry_frame, width=18, textvariable=var)
        input.pack(side=LEFT)       # HERE for loop entries must be able to update
        list_of_entry_widgets.append(input)


def get_entry():
    for results in list_of_entry_widgets:
       print(results.get())

def pass_entrytotable():
    selected = tree.focus()
    tuple_items = []
    for items in list_of_entry_widgets:
        data = items.get()
        tuple_items.append(data)

    tuple_item = tuple(tuple_items)
    print(tuple_item)
    tree.item(selected, values=tuple_item)


menubar = Menu(window)

lbl = Label(window, text="")
lbl.pack()


table_frame = Frame(window, borderwidth=2, relief='ridge')
table_frame.pack(pady=25)

search_frame = Frame(window, width=window.winfo_width())
print(window.winfo_width())
search_frame.pack(pady=25)

search_tbl = Entry(search_frame, width=50)
search_tbl.insert(0, 'search for id...')
search_tbl.pack(side="left", padx=25)
search_btn = Button(search_frame, text="Search ID", command=singleData_Table)
search_btn.pack(side='right')

data_table_frame = Frame(window, width=50)
data_table_frame.pack()

tree = ttk.Treeview(data_table_frame, selectmode='browse', height=10)
tree.pack(side="left")
style = ttk.Style()
style.theme_use("default")
scroll = ttk.Scrollbar(data_table_frame, orient="vertical", command=tree.yview)
scroll.pack(side="right", fill="y")
tree.configure(yscrollcommand=scroll.set)
tree.bind('<Motion>', 'break')
tree.bind('<ButtonRelease-1>', selectDetails)

entry_headings_frame = Frame(window, borderwidth=2, relief='ridge')
entry_headings_frame.pack(pady=25)
entry_frame = Frame(window, borderwidth=2, relief='ridge')
entry_frame.pack(pady=25)

test = Button(entry_frame, text="click", command=pass_entrytotable)
test.pack()
menubar.add_cascade(label="Connect Database Engine", command=open_Connector)
#Choosing_Database()
window.config(menu=menubar)
window.mainloop()





