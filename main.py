from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk, messagebox
import pandas as pd
import xlrd

window = tk.Tk()
window.title("MySQL Table Modifier")
window.state('zoomed')

list_of_Tables =[]
list_of_entry_lbl = []
list_of_entry_widgets = []
list_of_data = []
# list_combo = []

dataframe = pd.DataFrame({"active":["1", "0"]})
def getInput():
    inp_db = input_db.get()
    return inp_db

def Choosing_Database():
    # code
    # Must have mysql workbench and server to be able to connect
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
        showappinfo()
        lbl.destroy()
        lbl1.destroy()
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

            list_tables = Label(table_frame, text=data[j], width=25, borderwidth=2, relief="ridge", anchor='w', fg='white',bg="#676769")
            list_tables.grid(row=i + 5, column=j, pady=2.5)

            checkDB = Button(table_frame, text="Update Table", fg='white', bg="#676769")

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
    global selected_table, search_tbl, table, persistdata
    persistdata = num

    # if len(list_combo) > 0:
    #     del list_combo[:]
    #     combo.destroy()
    #menubar.add_cascade(label="Choose Table", command=create_table_list)
    for tables in list_of_Tables:
        if persistdata == tables:
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
    # showFilterButton()
    delete_Table()
    clear_entry(list_of_entry_widgets)
    clear_entry(list_of_entry_lbl)


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
                    values=data[0:len(data)])       # Pass the data from mySQL table to the treeview table
        data_ind += 1

def file_save():

    try:
        df = pd.read_sql(f'select * from {table}', engine)
        print(df)
        file = tk.filedialog.asksaveasfile(mode="w", defaultextension=".xlsx")
        file.close()
        df.to_excel(file.name, index=False)
        messagebox.showinfo("Saved", f"File has been saved in: {file.name}")
    except AttributeError as e:
        messagebox.showerror("File not saved", f"File has not been saved due to: {e}")

def singleData_Table():
    id_details = search_tbl.get()
    check_Table(persistdata)
    #print(id_details)
    try:
        for records in tree.get_children():
            tree.delete(records)
        single_data = engine.execute(f"""SELECT * FROM {table} WHERE {headers[0]} = {id_details}""")
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
    del list_of_widgets[:]

def clearDataEntry():
    for inputs in list_of_entry_widgets:
        inputs.delete(0, END)
    del list_of_data[:]

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

# def select_active(event=None):
#     tree.delete(*tree.get_children())
#     for index, row in dataframe.loc[dataframe["active"].eq(combo.get())].iterrows():
#         tree.insert("", END, text=index, values=list(row))

def entries():
    global input

    for headings in headers:
        entryLbl = Label(entry_headings_frame, width=15, text=headings)
        entryLbl.pack(side=LEFT)
        list_of_entry_lbl.append(entryLbl)

    for entry in range(len(headers)):
        var = tk.StringVar()
        input = Entry(entry_frame, width=18, textvariable=var, justify="center")
        input.pack(side=LEFT)       # HERE for loop entries must be able to update
        list_of_entry_widgets.append(input)


def pass_entrytotable():
    global tuple_item
    try:
        selected = tree.focus()
        tuple_items = []
        for items in list_of_entry_widgets:     # passes the entries into a list
            data = items.get()
            tuple_items.append(data)

        tuple_item = tuple(tuple_items)
        print(tuple_item)
        tree.item(selected, values=tuple_item)  # updates the treeview on the new values of each column based on the data passed from the entries
        updatedatabase(tuple_item[0])
    except IndexError as e:
        messagebox.showerror("Error", e)

def updatedatabase(id):
    global key, set_string
    items = []
    count=0
    try:

        for keys in headers:   # gets the headers and the data entries then collates all together to be formatted into the sql query
            key = keys + " = " + "'" + tuple_item[count] + "'"
            items.append(key)
            count +=1

        set_string = ", ".join(items)
        print(set_string)
        # Finds the row of the selected table and updates it based on the set variable where primary id is located
        updatequery = f"""UPDATE {table} SET {set_string} WHERE {headers[0]} = {id}"""
        engine.execute(updatequery)
        messagebox.showinfo('UPDATED', f'Your {table} has been Updated in {id}. \n Values: {set_string}')
    except SQLAlchemyError as e:
        messagebox.showerror("Error", e)
def insertdata():
    global entry, entrylist
    try:
        entrylist = []
        for results in list_of_entry_widgets:     # passes the entries into a list
            data = results.get()
            entrylist.append(data)
        entry_string = ", ".join(entrylist)
        print(entrylist)

        insertdatabase(entrylist[0])
    except IndexError as e:
        messagebox.showerror("Error", e)

def insertdatabase(ID):
    insert = False
    temp = []
    for t in range(len(entrylist)):
        if (t == 0):
            id = entrylist[t]
            temp.append(id)
        #
        else:
            entry = "'" + entrylist[t] + "'"
            temp.append(entry)
        #print(temp)
    try:
        z = ", ".join(temp)
        insert_query = f"""INSERT IGNORE INTO {table} VALUES ({z})"""
        child = tree.get_children('')
        for ch in child:
            data = tree.item(ch, "values")
            if ID in data:
                insert = True
                print("found")

        if insert is False:
            tree.insert("", 'end', values=(entrylist))
            print("insert")
            engine.execute(insert_query)

            messagebox.showinfo('ADDED', f'A new data has been added to your {table}. \n Values: {z}')
    except (SQLAlchemyError, IndexError) as e:
        messagebox.showerror("Error", e)

def showappinfo():
    global search_frame, search_tbl, data_table_frame, tree,entry_headings_frame,entry_frame,button_frame
    search_frame = Frame(window, width=window.winfo_width() , bg="#676769")
    print(window.winfo_width())
    search_frame.pack(pady=25)

    search_tbl = Entry(search_frame, width=50)
    search_tbl.insert(0, 'search for id...')
    search_tbl.pack(side="left", padx=25)
    search_btn = Button(search_frame, text="Search ID",font=("Arial", 10, "bold"), fg='white', command=singleData_Table, bg="#676769")
    search_btn.pack(side='right')
    refresh_btn = Button(search_frame, text="Refresh Table", font=("Arial", 10, "bold"), fg='white', command=lambda: check_Table(persistdata), bg="#676769")
    refresh_btn.pack(side="left", padx=25)
    data_table_frame = Frame(window, width=50, bg="#676769")
    data_table_frame.pack()

    tree = ttk.Treeview(data_table_frame, selectmode='browse', height=20)
    tree.pack(side="left")
    style = ttk.Style()
    style.theme_use("default")
    scroll = ttk.Scrollbar(data_table_frame, orient="vertical", command=tree.yview)
    scroll.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scroll.set)
    tree.bind('<Motion>', 'break')
    tree.bind('<ButtonRelease-1>', selectDetails)
    lbl3 = Label(window, text=" ", bg="#373738")
    lbl3.pack(pady=10)
    entry_headings_frame = Frame(window, borderwidth=2, bg="#676769")
    entry_headings_frame.pack()
    entry_frame = Frame(window, borderwidth=2, relief='ridge', bg="#676769")
    entry_frame.pack(pady=10)

    button_frame = Frame(window, borderwidth=2, relief='ridge', bg="#676769")
    button_frame.pack(pady=25)
    Update = Button(button_frame, text="Update",font=("Arial", 10, "bold"), fg='white', command=pass_entrytotable, bg="#676769")
    Update.pack(side="left", padx=25)
    Insert_btn = Button(button_frame, text="Insert",font=("Arial", 10, "bold"), fg='white', command=insertdata, bg="#676769")
    Insert_btn.pack(side="left", padx=25)
    Clear_btn = Button(button_frame, text="Clear Entries", font=("Arial", 10, "bold"), fg='white', command=clearDataEntry, bg="#676769")
    Clear_btn.pack(side="left", padx=25)
    export_btn = Button(button_frame, text="Export as excel", font=("Arial", 10, "bold"), fg='white', command=file_save, bg="#676769")
    export_btn.pack(side="left", padx=25)

# def showFilterButton():
#     global combo
#     combo = ttk.Combobox(search_frame, values=dataframe, state='readonly')
#     combo.pack()
#     list_combo.append(combo)
#
#     combo.bind("<<ComboboxSelected>>", select_active)
#     print(list_combo)

lbl = Label(window, text="MUST CONNECT TO DATABASE", font=("Arial", 30, "bold"), fg='white', bg='#373738')
lbl.pack(expand=TRUE, pady=20)
lbl1 = Label(window, text="Click 'CONNECT DATABASE ENGINE' on upper the Left Corner.", font=("Arial", 20),fg='#4c9a41', bg='#373738')
lbl1.pack(pady=10)
table_frame = Frame(window, borderwidth=2, relief='ridge', bg="#676769")
table_frame.pack(pady=25)
menubar = Menu(window)

menubar.add_cascade(label="Connect Database Engine", command=open_Connector)
#---------------------------------------------
#Choosing_Database()
window.config(menu=menubar, bg='#373738')
window.mainloop()





