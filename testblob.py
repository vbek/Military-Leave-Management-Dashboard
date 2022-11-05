import io
import tkinter as tk
from tkinter import messagebox, filedialog

from PIL import Image
import mysql.connector
from PIL import ImageTk


def upload_file():
    filetypes = [("Image Files, *.jpg", 'All Files, *.*')]
    image_path = filedialog.askopenfilename(filetypes=filetypes)
    binary_value_of_image = get_binary_data(image_path)
    return binary_value_of_image


def get_binary_data(image_path):
    global binary_data_image
    img = Image.open(image_path, 'r')
    img = img.resize((130, 130))
    img_binary = io.BytesIO()
    img.save(img_binary, 'PNG')
    binary_data_image = img_binary.getvalue()
    return binary_data_image


def window():

    my_window = tk.Tk()
    my_window.geometry('400x400')
    global str_var_e1, str_var_e2
    str_var_e1 = tk.StringVar()
    str_var_e2 = tk.StringVar()
    e1 = tk.Entry(my_window, width=10, textvariable=str_var_e1)
    e1.grid(row=0, column=0)

    e2 = tk.Entry(my_window, width=10, textvariable=str_var_e2)
    e2.grid(row=0, column=1)

    bt = tk.Button(my_window, width=10, command=upload_file, text="upload file")
    bt.grid(row=0, column=2)

    bt_add = tk.Button(my_window, width=10, command=add_data, text="Add Data")
    bt_add.grid(row=0, column=3)

    bt_display = tk.Button(my_window, width=10, command=display, text="Display")
    bt_display.grid(row=0, column=4)

    global label_image

    label_image = tk.Label(my_window, bd=4, highlightthickness=2, highlightcolor='red')
    label_image.grid(row=1, column=0)

    my_window.mainloop()


def connection1():
    try:
        my_db = mysql.connector.connect(
            host='localhost',
            user='root',
            port='3306',
            password='12Bibek!@',
            database='bibekdb')
    except Exception:
        messagebox.showerror("Error", ' Couldn\'t open file')
    return my_db


def add_data():
    my_conn = connection1()
    text_e1 = str_var_e1.get()
    text_e2 = str_var_e2.get()
    sql_add = "Insert into blobtable (id, name, photo) values (%s,%s,%s)"
    values = (text_e1, text_e2, binary_data_image)
    my_cursor = my_conn.cursor()
    my_cursor.execute(sql_add, values)
    my_conn.commit()
    my_conn.close()


def display():
    my_conn = connection1()
    my_cursor = my_conn.cursor()
    my_cursor.execute('select * from blobtable')
    row = my_cursor.fetchall()

    image = Image.open(io.BytesIO(row[2][2]))
    image = image.resize((100, 100))
    image = ImageTk.PhotoImage(image)
    label_image.image = image
    label_image.config(image=image)


window()
