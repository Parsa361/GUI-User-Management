from tkinter import *
from tkinter import messagebox
from mysql import connector
from local_settings import *


# check the duplication on id in database
# depends on submit_query()
def check_id():
    my_db = connector.connect(host=DB_HOST, user=DB_USER,
                              password=DB_PASSWORD, database=DB_NAME)
    my_cursor = my_db.cursor()

    my_cursor.execute("select id from person where id = %s", (id.get(),))

    result = my_cursor.fetchone()
    return result


def submit_query():
    my_db = connector.connect(host=DB_HOST, user=DB_USER,
                              password=DB_PASSWORD, database=DB_NAME)
    my_cursor = my_db.cursor()

    try:
        if id.get() == '':
            messagebox.showerror("error msg", "ID field is empty!")
        elif age.get() == '':
            messagebox.showerror("error msg", "Age field is empty!")

        if int(age.get()) <= 18:
            messagebox.showwarning("warning msg", "Age must be greater than 18!!")

        if check_id() == None:
            if f_name.get() != '' and l_name.get() != '':
                sql = "INSERT INTO person (id, first_name, lastname, age) VALUES (%s,%s,%s,%s)"
                value = (id.get(), f_name.get(), l_name.get(), age.get())
                my_cursor.execute(sql, value)
                my_db.commit()

                id.delete(0, END)
                f_name.delete(0, END)
                l_name.delete(0, END)
                age.delete(0, END)

                messagebox.showinfo("Info msg", "Successful!")
            else:
                messagebox.showwarning("warning msg", "Please fill first/last name field first")

        else:
            messagebox.showerror("error msg", "This id is exist")



    except Exception as e:
        print(e)
        my_db.rollback()
        my_db.close()


def show_table_query():
    my_db = connector.connect(host=DB_HOST, user=DB_USER,
                              password=DB_PASSWORD, database=DB_NAME)
    my_cursor = my_db.cursor()

    my_cursor.execute("SELECT * FROM person")
    records = my_cursor.fetchall()

    # Create new window
    new_root = Toplevel()
    new_root.title("Records!")
    new_root.geometry("600x500")

    new_root.config(background="#5cfcff")
    i = 0
    row_list = []
    for rec in records:
        for j in range(len(rec)):
            label = Label(new_root, width=18, text=rec[j], borderwidth=2, relief="ridge", bg="#5cfcff", anchor="w")
            row_list.append(label.grid(row=i, column=j))
        i += 1

    my_db.commit()
    my_db.close()

    new_root.mainloop()


def table_query():
    global my_db
    new_window = Toplevel()
    new_window.geometry("500x500")
    new_window.title("Show tables for university database")
    new_window.config(background="#5cfcff")

    try:
        my_db = connector.connect(host=DB_HOST, user=DB_USER,
                                  password=DB_PASSWORD, database=DB_NAME)
        my_cursor = my_db.cursor()

        my_cursor.execute("SHOW tables")

        tables = my_cursor.fetchall()

        for rec in tables:
            label = Label(new_window, text=str(rec), bg="#5cfcff")
            label.pack()

        my_db.commit()
        my_db.close()

    except Exception as e:
        print(e)
        my_db.rollback()
        my_db.close()

    new_window.mainloop()


# this def will check the duplicate id from database, if it returns none
# means we haven't duplication
# it depends on delete_query()
def check_selected_id():
    my_db = connector.connect(host=DB_HOST, user=DB_USER,
                              password=DB_PASSWORD, database=DB_NAME)
    my_cursor = my_db.cursor()

    my_cursor.execute("select id from person where id = %s", (select_id.get(),))

    result = my_cursor.fetchone()
    return result


def delete_query():
    global my_db
    try:
        my_db = connector.connect(host=DB_HOST, user=DB_USER,
                                  password=DB_PASSWORD, database=DB_NAME)
        my_cursor = my_db.cursor()

        if select_id.get() == '':
            messagebox.showerror("error msg", "You have to select an ID first")
        elif check_selected_id() is None:
            messagebox.showerror("error msg", "Selected ID isn't exist")
        else:
            sql = "DELETE FROM person WHERE id = " + str(select_id.get())
            my_cursor.execute(sql)

            select_id.delete(0, END)

            my_db.commit()
            my_db.close()

            messagebox.showinfo("Info msg", "User is deleted")

    except Exception as e:
        print(e)
        my_db.rollback()
        my_db.close()


def update():
    global my_db
    try:
        my_db = connector.connect(host=DB_HOST, user=DB_USER,
                                  password=DB_PASSWORD, database=DB_NAME)
        my_cursor = my_db.cursor()

        record_id = select_id.get()
        sql = "UPDATE person SET first_name = %s,lastname = %s,age = %s WHERE id = %s"
        value = (f_name_editor.get(), l_name_editor.get(), age_editor.get(), select_id.get())
        my_cursor.execute(sql, value)

        my_db.commit()
        my_db.close()

        f_name_editor.delete(0, END)
        l_name_editor.delete(0, END)
        age_editor.delete(0, END)
        select_id.delete(0,END)

    except Exception as e:
        print(e)
        my_db.rollback()
        my_db.close()


def edit():
    if check_selected_id() is None:
        messagebox.showerror("error msg", "This id isn't exist")
        return
    editor = Toplevel()
    editor.geometry("500x500")
    editor.title("Edit record")
    editor.config(background="#5cfcff")

    # create global variables for text box names
    global f_name_editor, my_db
    global l_name_editor
    global age_editor

    # Create text boxes
    f_name_editor = Entry(editor, width=40)
    f_name_editor.grid(row=1, column=1, padx=15)

    l_name_editor = Entry(editor, width=40)
    l_name_editor.grid(row=2, column=1, padx=15)

    age_editor = Entry(editor, width=40)
    age_editor.grid(row=3, column=1, padx=15)

    # Create text box label
    f_name_label_editor = Label(editor, text="First Name", bg="#5cfcff")
    f_name_label_editor.grid(row=1, column=0, padx=20)

    l_name_label_editor = Label(editor, text="Last Name", bg="#5cfcff")
    l_name_label_editor.grid(row=2, column=0)

    age_label_editor = Label(editor, text="Age", bg="#5cfcff")
    age_label_editor.grid(row=3, column=0)

    # create a save button
    editor_button = Button(editor, text="Save Record", command=update)
    editor_button.grid(row=4, column=0, columnspan=2, pady=10,
                       padx=10, ipadx=170)
    try:
        my_db = connector.connect(host="localhost", user="root",
                                  password="password", database="University")
        my_cursor = my_db.cursor()

        record_id = str(select_id.get())
        sql = "SELECT * FROM person WHERE id = " + record_id
        my_cursor.execute(sql)
        records = my_cursor.fetchall()

        for record in records:
            f_name_editor.insert(0, record[1])
            l_name_editor.insert(0, record[2])
            age_editor.insert(0, record[3])


        my_db.commit()
        my_db.close()

    except Exception as e:
        print(e)
        my_db.rollback()
        my_db.close()


# Create main window
root = Tk()
root.title("User Management")
root.geometry("900x500")
root.config(background="#5cfcff")

# background image
IMAGE_PATH = PhotoImage(file="Pics/output-onlinepngtools.png")
Label(root, image=IMAGE_PATH).place(x=460, y=0)

# Create text boxes
id = Entry(root, width=40)
id.grid(row=0, column=1, padx=15)

f_name = Entry(root, width=40)
f_name.grid(row=1, column=1, padx=15)

l_name = Entry(root, width=40)
l_name.grid(row=2, column=1, padx=15)

age = Entry(root, width=40)
age.grid(row=3, column=1, padx=15)

select_id = Entry(root, width=40)
select_id.grid(row=9, column=1, padx=15)

# Create text box label
id_label = Label(root, text="ID", bg="#5cfcff")
id_label.grid(row=0, column=0)

f_name_label = Label(root, text="First Name", bg="#5cfcff")
f_name_label.grid(row=1, column=0, padx=20)

l_name_label = Label(root, text="Last Name", bg="#5cfcff")
l_name_label.grid(row=2, column=0)

age_label = Label(root, text="Age", bg="#5cfcff")
age_label.grid(row=3, column=0)

select_id_label = Label(root, text="Select Id", bg="#5cfcff")
select_id_label.grid(row=9, column=0)

# Make buttons
submit_button = Button(root, text="Add Record", command=submit_query)
submit_button.grid(row=6, column=0, columnspan=2, pady=30,
                   padx=10, ipadx=170)

query_button = Button(root, text="Show Records", command=show_table_query)
query_button.grid(row=7, column=0, columnspan=2, pady=10,
                  padx=10, ipadx=164)

table_button = Button(root, text="Show Tables", command=table_query)
table_button.grid(row=8, column=0, columnspan=2, pady=30,
                  padx=10, ipadx=164)

delete_button = Button(root, text="Delete Record", command=delete_query)
delete_button.grid(row=10, column=0, columnspan=2, pady=20,
                   padx=10, ipadx=160)

edit_button = Button(root, text="Edit Record", command=edit)
edit_button.grid(row=11, column=0, columnspan=2, pady=10,
                 padx=10, ipadx=170)
root.mainloop()
