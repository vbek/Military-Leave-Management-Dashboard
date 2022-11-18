import math
from datetime import datetime
from decimal import Decimal
from tkinter import *
from tkinter import ttk, messagebox

from mysql.connector import CMySQLConnection
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import io
import mysql.connector


class Employee:
    unit_name = ('', 'Sher Bn', 'No. 14 Bde', 'Kalibhanjan Bn(E)',
                 'Kalibuksh Bn(E)', 'Kalibhakti Bn(E)', 'Kalidal Bn(E)',
                 'Kaliprasad Bn(E)', 'Kalirakshya Bn(E)', 'Kalisiddhi Bn(E)',
                 'Kalishatki Bn(E)')
    sorted_unit_name = tuple(sorted(unit_name))
    quote_text = " \"Training is the Best Incentive to a soldier\""

    def __init__(self, window, user):
        #  **************************************** Window Title  **************************************** #

        self.parent_window = window
        self.parent_window.withdraw()
        self.window = Toplevel(self.parent_window)
        self.user = user
        self.text_unit = StringVar()
        self.text_comp_no = StringVar()
        self.text_name = StringVar()
        self.text_phone = StringVar()
        self.text_email = StringVar()
        self.text_rank = StringVar()
        self.text_temp_add = StringVar()
        self.text_perm_add = StringVar()
        self.text_dob = StringVar()
        self.text_recent_leave = StringVar()
        self.text_sex = StringVar()
        self.text_mar_status = StringVar()
        self.text_search_by = StringVar()
        self.text_search_text = StringVar()
        self.text_bloodgp = StringVar()
        self.binary_data_profile_pic = b''
        self.entry_search = Entry()
        self.image_label = Label()
        self.phone_details_tree = ttk.Treeview()
        self.entry_dob = DateEntry()
        self.set_window()

    def set_window(self):
        window_width = self.window.winfo_screenwidth()
        window_height = self.window.winfo_screenheight()
        self.window.focus_set()
        self.window.geometry("{}x{}+0+0".format(window_width, window_height))
        self.window.title("UNIT MANAGEMENT PORTAL")
        self.window.resizable(width=False, height=False)
        self.window.attributes('-fullscreen', True)

        #  **************************************** String Variables  **************************************** #
        lbl_title = Label(self.window, text="MANAGEMENT DASHBOARD", font=('times new roman', 37, 'bold'), bg='white',
                          fg='darkblue')
        lbl_title.place(x=0, y=0, width=window_width, height=50)
        lbl_user = Label(self.window, text="USER: " + self.user.upper(), font=('times new roman', 10, 'bold'),
                         fg='teal')
        lbl_user.place(x=window_width - lbl_user.winfo_reqwidth(), y=50)

        #  **************************************** Title  **************************************** #
        logo_image = Image.open('res/logo.png')
        photo_logo = ImageTk.PhotoImage(logo_image)
        title_logo = Label(self.window, image=photo_logo)
        title_logo.place(x=0, y=0, width=50, height=50)
        Label(self.window, text='\u00A9 Bibek Koirala', fg="teal").place(
            x=window_width - 90, y=window_height - 20)
        close_button = Button(self.window, width=12, bg='GREY', text="X", command=self.close_app)
        close_button.place(x=window_width - 15, y=0, width=15, height=15)

        minimize_button = Button(self.window, width=12, bg='GREY', text="-", command=self.minimize_app)
        minimize_button.place(x=window_width - 30, y=0, width=15, height=15)

        #  **************************************** Main Frame  **************************************** #
        main_frame = Frame(self.window, bd=2, relief=RIDGE, bg='WHITE')
        main_frame.place(x=100, y=70, width=window_width - 101, height=window_height - 90)

        # ***************************************** Left Icon Frame *********************************** #
        left_frame = Frame(self.window, bd=2, relief=RIDGE, bg='white')
        left_frame.place(x=5, y=70, width=90, height=244)

        Label(self.window, text="WINDOWS", font=('times', '9', 'bold')).place(x=18, y=50)
        # ***************************************** HOME WINDOW BUTTON ******************************
        home_user_window_button = Button(left_frame, width=11, fg='TEAL', text='HOME',
                                         font=("times", 10, 'bold'))
        home_user_window_button.place(x=0, y=0, height=60)

        button_size = 60

        # ***************************************** EDIT WINDOW BUTTON ******************************
        search_user_window_button = Button(left_frame, width=11, fg='TEAL', text='EDIT',
                                           font=("times", 10, 'bold'))
        search_user_window_button.place(x=0, y=button_size * 1, height=60)

        # ***************************************** DISPLAY WINDOW BUTTON ******************************
        display_user_window_button = Button(left_frame, width=11, fg='TEAL', text='LEAVE\nRECORD',
                                            font=("times", 10, 'bold'))
        display_user_window_button.place(x=0, y=button_size * 2, height=60)

        #  **************************************** Upper Frame  **************************************** #
        upper_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Employee Information",
                                 font=('times new roman', 10, 'bold'), bg='white', fg='red')
        upper_frame.place(x=10, y=10, width=window_width - 125, height=window_height / 2 - 50)

        #  **************************************** Unit  **************************************** #
        lbl_unit = Label(upper_frame, text='Unit:', font=('times new roman', 11, 'bold'),
                         bg='white', fg='black')
        lbl_unit.grid(row=0, column=0, sticky=W)

        combo_unit = ttk.Combobox(upper_frame, textvariable=self.text_unit,
                                  font=('times new roman', 10, 'bold'), width=15,
                                  state='readonly')

        combo_unit['value'] = self.sorted_unit_name
        combo_unit.current(0)
        combo_unit.grid(row=0, column=1, padx=2, pady=17, sticky=W)

        #  **************************************** Comp No.  **************************************** #
        lbl_comp_no = Label(upper_frame, text='Comp. No:', font=('times new roman', 11, 'bold'),
                            bg='white', fg='black')
        lbl_comp_no.grid(row=0, column=2, sticky=W)

        entry_comp_no = Entry(upper_frame, textvariable=self.text_comp_no,
                              font=('times new roman', 9), bg='white', fg='black', width=15)
        entry_comp_no.grid(row=0, column=3, sticky=W, padx=2, pady=17)

        #  **************************************** Rank  **************************************** #
        lbl_rank = Label(upper_frame, text='Rank:', font=('times new roman', 11, 'bold'),
                         bg='white', fg='black')
        lbl_rank.grid(row=0, column=4, sticky=W)

        entry_rank = Entry(upper_frame, textvariable=self.text_rank,
                           font=('times new roman', 9), bg='white',
                           width=15)
        # self.entry_rank['values'] = '', 'Sep', 'L/Cpl', 'Cpl', 'Sgt', 'Jam', 'Sub', 'Sub Maj',\
        #                             '2nd Lt', 'Lt', 'Capt', 'Major', 'Lt Col', 'Col', 'Brid Gen', 'Maj Gen',\
        #                             'Lt Gen', 'COAS Gen'
        entry_rank.grid(row=0, column=5, sticky=W, padx=2, pady=17)

        #  **************************************** Name  **************************************** #
        lbl_name = Label(upper_frame, text='Name:', font=('times new roman', 11, 'bold'),
                         bg='white', fg='black')
        lbl_name.grid(row=0, column=6, sticky=W)

        entry_name = Entry(upper_frame, textvariable=self.text_name,
                           font=('times new roman', 9),
                           bg='white', fg='black', width=20)
        entry_name.grid(row=0, column=7, sticky=W, padx=2, pady=17)

        #  **************************************** Phone No  **************************************** #
        lbl_phone = Label(upper_frame, text='Phone No:', font=('times new roman', 11, 'bold'),
                          bg='white', fg='black')
        lbl_phone.grid(row=1, column=0, sticky=W)

        entry_phone = Entry(upper_frame, textvariable=self.text_phone,
                            font=('times new roman', 9),
                            bg='white', fg='black', width=20)
        entry_phone.grid(row=1, column=1, sticky=W, padx=2, pady=17)

        #  **************************************** Email  **************************************** #
        lbl_email = Label(upper_frame, text='Email:', font=('times new roman', 11, 'bold'),
                          bg='white', fg='black')
        lbl_email.grid(row=1, column=2, sticky=W)

        entry_email = Entry(upper_frame, textvariable=self.text_email,
                            font=('times new roman', 9),
                            bg='white', fg='black', width=20)
        entry_email.grid(row=1, column=3, sticky=W, padx=2, pady=17)

        #  **************************************** Temp Address  **************************************** #
        lbl_temp_add = Label(upper_frame, text='Temp Address:', font=('times new roman', 11, 'bold'),
                             bg='white', fg='black')
        lbl_temp_add.grid(row=1, column=4, sticky=W)

        entry_temp_add = Entry(upper_frame, textvariable=self.text_temp_add,
                               font=('times new roman', 9),
                               bg='white', fg='black', width=20)
        entry_temp_add.grid(row=1, column=5, sticky=W, padx=2, pady=17)

        #  **************************************** Perm Address  **************************************** #
        lbl_perm_add = Label(upper_frame, text='Perm Address:', font=('times new roman', 11, 'bold'),
                             bg='white', fg='black')
        lbl_perm_add.grid(row=1, column=6, sticky=W)

        entry_perm_add = Entry(upper_frame, textvariable=self.text_perm_add,
                               font=('times new roman', 9),
                               bg='white', fg='black', width=20)
        entry_perm_add.grid(row=1, column=7, sticky=W, padx=2, pady=17)

        #  **************************************** Date Of Birth  **************************************** #
        lbl_display_age = Label()

        def dob_entry(e):
            current_date = datetime.today().date()
            total_days = current_date - self.entry_dob.get_date()

            years_in_decimal = Decimal(total_days.days) / Decimal(365.2425)
            years = int(years_in_decimal)

            months_in_decimal = ((Decimal(years_in_decimal) - years) * Decimal(12))
            months = int(months_in_decimal)

            days = math.ceil((months_in_decimal - months) * Decimal(30.436875))
            age = (str(years) + "y " + str(months) + "m " + str(days) + "d")
            lbl_display_age.config(text=age)

        lbl_dob = Label(upper_frame, text='DOB:', font=('times new roman', 11, 'bold'),
                        bg='white', fg='black')
        lbl_dob.grid(row=2, column=0, sticky=W)

        self.entry_dob = DateEntry(upper_frame, textvariable=self.text_dob,
                                   date_pattern='y-mm-dd')
        self.entry_dob.grid(row=2, column=1, sticky=W, padx=2, pady=17)
        self.entry_dob.bind("<<DateEntrySelected>>", dob_entry)

        #  **************************************** Age  **************************************** #
        lbl_age = Label(upper_frame, text='Age:', font=('times new roman', 11, 'bold'),
                        bg='white', fg='black', width=5)
        lbl_age.grid(row=2, column=2, sticky=W)

        lbl_display_age = Label(upper_frame, width=10, font=('times new roman', 11, 'bold'),
                                bg='white', )
        lbl_display_age.grid(row=2, column=3, sticky=W, pady=17)

        #  **************************************** Date Of Joining  **************************************** #
        lbl_recent_leave = Label(upper_frame, text='Rec Leave:', font=('times new roman', 11, 'bold'),
                                 bg='white', fg='black')
        lbl_recent_leave.grid(row=2, column=4, sticky=W)

        entry_recent_leave = DateEntry(upper_frame, textvariable=self.text_recent_leave,
                                       date_pattern='y-mm-dd')
        entry_recent_leave.grid(row=2, column=5, sticky=W, padx=2, pady=17)

        #  **************************************** Sex  **************************************** #
        lbl_sex = Label(upper_frame, text='Sex:', font=('times new roman', 11, 'bold'),
                        bg='white', fg='black')
        lbl_sex.grid(row=2, column=6, sticky=W)

        combo_sex = ttk.Combobox(upper_frame, textvariable=self.text_sex,
                                 font=('times new roman', 10, 'bold'), width=10, state='readonly')
        combo_sex['value'] = ('', 'Male', 'Female')
        combo_sex.current(0)
        combo_sex.grid(row=2, column=7, sticky=W, padx=2, pady=17)

        #  **************************************** Marital Status  **************************************** #
        lbl_ms = Label(upper_frame, text='Marital Status:', font=('times new roman', 11, 'bold'),
                       bg='white', fg='black')
        lbl_ms.grid(row=3, column=0, sticky=W)

        combo_ms = ttk.Combobox(upper_frame, textvariable=self.text_mar_status,
                                font=('times new roman', 10, 'bold'), width=10, state='readonly')
        combo_ms['value'] = ('', 'Unmarried', 'Married')
        combo_ms.current(0)
        combo_ms.grid(row=3, column=1, sticky=W, padx=2, pady=17)

        #  **************************************** Blood Gp  **************************************** #
        lbl_blood_gp = Label(upper_frame, text='Blood GP:', font=('times new roman', 11, 'bold'),
                             bg='white', fg='black')
        lbl_blood_gp.grid(row=3, column=2, sticky=W)

        combo_ms = ttk.Combobox(upper_frame, textvariable=self.text_bloodgp,
                                font=('times new roman', 10, 'bold'), width=10, state='readonly')
        combo_ms['value'] = ('', 'A +ve', 'B +ve', 'AB +ve', 'O +ve', 'A -ve', 'B -ve', 'AB -ve', 'O -ve')
        combo_ms.current(0)
        combo_ms.grid(row=3, column=3, sticky=W, padx=2, pady=17)

        #  **************************************** Photo Frame  **************************************** #
        icon_photo_button = PhotoImage(file=r'res/pc.png')
        photo_sample = icon_photo_button.subsample(10, 10)

        button_photo = Button(upper_frame, bg='white', command=self.upload_pp, image=photo_sample,
                              compound=LEFT)
        #  **************************************** Army Logo Frame  **************************************** #
        army_logo = PhotoImage(file="res/nepal army.png")
        army_logo = army_logo.subsample(3, 3)
        army_logo_label = Label(self.window, image=army_logo, width=96)
        army_logo_label.place(x=0, y=window_height - 102)

        # self.label_title = Label(self.upper_frame, image=self.photo_sample)
        photo_lbl = LabelFrame(upper_frame, labelwidget=button_photo, bg='white',
                               font=('times new roman', 9),
                               fg='red')
        photo_lbl.place(x=window_width - 360, width=150, height=160)
        photo_frame = Frame(upper_frame, bd=5, relief=RIDGE, bg='white')
        photo_frame.place(x=window_width - 350, y=25, width=130, height=130)
        self.image_label = Label(photo_frame, background='white')
        self.image_label.pack(fill=BOTH)

        #  **************************************** Button Frame  **************************************** #
        button_frame = Frame(upper_frame, bd=2, relief=RIDGE, bg='white')
        button_frame.place(x=window_width - 200, y=8, width=70, height=150)

        button_add = Button(button_frame, bd=2, relief=RAISED, command=self.add_data, text='ADD',
                            font=('times new roman', 10, 'bold'), bg="#ffce30", fg='#288ba8',
                            width=7)
        button_add.grid(row=0, column=0, padx=5, pady=5)

        button_update = Button(button_frame, bd=2, command=self.update_data, relief=RAISED, text='UPDATE',
                               font=('times new roman', 10, 'bold'), bg="#ffce30", fg='#288ba8',
                               width=7)
        button_update.grid(row=1, column=0, padx=5, pady=5)

        button_delete = Button(button_frame, bd=2, command=self.delete_data, relief=RAISED, text='DELETE',
                               font=('times new roman', 10, 'bold'), bg="#ffce30", fg='#288ba8',
                               width=7)
        button_delete.grid(row=2, column=0, padx=5, pady=5)

        button_clear = Button(button_frame, bd=2, command=self.clear_data, relief=RAISED, text='CLEAR',
                              font=('times new roman', 10, 'bold'), bg="#ffce30", fg='#288ba8',
                              width=7)
        button_clear.grid(row=3, column=0, padx=5, pady=5)

        #  **************************************** Lower Frame  **************************************** #
        lower_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Employee Information Table",
                                 font=('times new roman', 10, 'bold'), bg='white', fg='#C00060')
        lower_frame.place(x=10, y=window_height / 2 - 35, width=window_width - 120,
                          height=window_height / 2 - 60)

        #  **************************************** Search Frame  **************************************** #
        search_frame = LabelFrame(lower_frame, relief=RIDGE, text='Search', bd=3,
                                  font=('times new roman', 10, 'bold'), bg='white', fg='#c00060'
                                  )
        search_frame.place(x=2, y=0, width=window_width - 127, height=50)

        lbl_search_by = Label(search_frame, text="SEARCH BY:", bg="#336b87", fg='#ffffff', width=10,
                              font=('times new roman', 10, 'bold'))
        lbl_search_by.grid(row=0, column=0, padx=5, pady=5)

        combo_search = ttk.Combobox(search_frame, textvariable=self.text_search_by,
                                    width=20, font=('times new roman', 10, 'bold'),
                                    state='readonly')
        combo_search['value'] = ("CompNo", "Rnk", "Name", "Phone", "Unit", 'Bloodgp')
        combo_search.current(0)
        combo_search.grid(row=0, column=1, padx=5)

        self.entry_search = Entry(search_frame, textvariable=self.text_search_text,
                                  relief=RIDGE, font=('times new roman', 9, 'bold'),
                                  width=25, bd=2)
        self.entry_search.grid(row=0, column=2, padx=5)
        self.entry_search.bind('<KeyRelease>', self.search_data)

        lbl_daily_quote = Label(search_frame, text=self.quote_text,
                                font=('times new roman', 12, 'bold italic'), bg='#07575b', fg="white")
        lbl_daily_quote.grid(row=0, column=5, padx=100)

        #  **************************************** Display Frame  **************************************** #
        display_table = Frame(lower_frame, bd=5, relief=RIDGE)
        display_table.place(y=52, width=window_width - 126, height=230)

        scroll_x = ttk.Scrollbar(display_table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(display_table, orient=VERTICAL)
        tree_columns = ('unit', 'CompNo', 'Rnk', 'Name', 'Phone', 'Bloodgp')
        self.phone_details_tree = ttk.Treeview(display_table,
                                               columns=tree_columns,
                                               xscrollcommand=scroll_x.set,
                                               yscrollcommand=scroll_y.set,
                                               height=2)
        count = 0
        for i in tree_columns:
            if count == 0:
                count += 1
                continue
            else:
                self.phone_details_tree.column(i, anchor="w")
        self.phone_details_tree.bind("<<TreeviewSelect>>", self.get_cursor)

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_x.config(command=self.phone_details_tree.xview)
        scroll_y.config(command=self.phone_details_tree.yview)

        self.phone_details_tree.heading('unit', text='Unit', anchor=CENTER)
        self.phone_details_tree.heading('CompNo', text='Comp No', anchor=CENTER)
        self.phone_details_tree.heading('Rnk', text='Rank', anchor=CENTER)
        self.phone_details_tree.heading('Name', text='Name', anchor=CENTER)
        self.phone_details_tree.heading('Phone', text='Phone No', anchor=CENTER)
        self.phone_details_tree.heading('Bloodgp', text='Blood Gp', anchor=CENTER)

        self.phone_details_tree.pack(fill=BOTH, expand=1)
        # self.phone_details_tree.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

        self.phone_details_tree['show'] = 'headings'

        self.phone_details_tree.column("unit", width=80)
        self.phone_details_tree.column("CompNo", width=52)
        self.phone_details_tree.column("Rnk", width=40)
        self.phone_details_tree.column("Name", width=110)
        self.phone_details_tree.column("Phone", width=70)
        self.phone_details_tree.column("Bloodgp", width=60)
        self.window.mainloop()

    # **************************************** Close Button ********************************* #
    def close_app(self):
        self.window.destroy()
        self.parent_window.destroy()

    # **************************************** Minimize Button ********************************* #
    def minimize_app(self):
        self.window.iconify()
        self.parent_window.withdraw()

    #  **************************************** Connecting to Database  **************************************** #
    def connect_database(self):
        my_db = CMySQLConnection()
        try:
            my_db = mysql.connector.connect(
                host='localhost',
                user='root',
                port='3306',
                password='12Bibek!@',
                database='bibekdb'
            )
        except Exception as ex:
            messagebox.showerror('Error: ', f'{str(ex)}', parent=self.window)
        return my_db

    # **************************************** Fetch All Data  **************************************** #
    def fetch_data(self):
        my_conn = self.connect_database()
        my_cursor = my_conn.cursor()
        my_cursor.execute('select * from phone_details')
        datas = my_cursor.fetchall()
        if len(datas) != 0:
            self.phone_details_tree.delete(*self.phone_details_tree.get_children())
            for data in datas:
                self.phone_details_tree.insert("", END, values=data)
            # my_conn.commit()
        my_conn.close()

    # **************************************** Get Data ****************************************
    def get_cursor(self, event=''):
        cursor_row = self.phone_details_tree.focus()
        content = self.phone_details_tree.item(cursor_row)
        data = content['values']
        my_conn = self.connect_database()
        my_cursor = my_conn.cursor()
        sql_query_to_get_binary_data = 'select * from phone_details where CompNo=%s'
        if data != '':
            value = (data[1],)
            self.text_unit.set(data[0])
            self.text_comp_no.set(data[1])
            self.text_name.set(data[3])
            self.text_phone.set(data[4])
            self.text_email.set(data[5])
            self.text_rank.set(data[2])
            self.text_temp_add.set(data[6])
            self.text_perm_add.set(data[7])
            self.text_dob.set(data[8])
            self.text_recent_leave.set(data[9])
            self.text_sex.set(data[10])
            self.text_mar_status.set(data[11])
            self.text_bloodgp.set(data[12])
            my_cursor.execute(sql_query_to_get_binary_data, value)
            self.binary_data_profile_pic = my_cursor.fetchone()[13]
            self.set_profile_pic(self.binary_data_profile_pic)
            Button()

    # **************************************** Set Profile Pic **********************************
    def set_profile_pic(self, binary_data_image):
        if binary_data_image != b'':
            image = Image.open(io.BytesIO(binary_data_image))
            image = ImageTk.PhotoImage(image)
            self.image_label.config(image=image)
            self.image_label.image = image
            self.image_label.pack(fill=BOTH)
        else:
            self.image_label.forget()
            return

    # **************************************** Adding a data to the database **********************************
    def add_data(self):
        if self.text_unit.get() == '' or self.text_comp_no.get() == '' \
                or self.text_name.get() == '' or self.text_phone.get() == '':
            messagebox.showerror('Error ', ' Please enter the values in the fields')
        else:
            try:
                my_conn = self.connect_database()
                my_cursor = my_conn.cursor()
                query = 'insert into phone_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                values = (self.text_unit.get(),
                          self.text_comp_no.get(),
                          self.text_rank.get(),
                          self.text_name.get(),
                          self.text_phone.get(),
                          self.text_email.get(),
                          self.text_temp_add.get(),
                          self.text_perm_add.get(),
                          self.text_dob.get(),
                          self.text_recent_leave.get(),
                          self.text_sex.get(),
                          self.text_mar_status.get(),
                          self.text_bloodgp.get(),
                          self.binary_data_profile_pic)
                my_cursor.execute(query, values)
                my_conn.commit()
                my_conn.close()
                self.fetch_data()
                messagebox.showinfo('SUCCESS', 'User Added Successfully')
            except mysql.connector.errors.IntegrityError:
                messagebox.showerror("Error", "Comp Number repeated!")

            self.clear_data()

    # ************************************* Add Profile Pic and Set binary value ************* #
    def upload_pp(self):
        from tkinter import filedialog
        filetype = [("Image Files", "*.jpg"), ("Portable ", "*.png")]
        file = filedialog.askopenfilename(filetypes=filetype)
        try:
            img_reader = Image.open(file)
            img_file = img_reader.resize((130, 130))
            img_binary = io.BytesIO()
            img_file.save(img_binary, 'PNG')
            self.binary_data_profile_pic = img_binary.getvalue()
        except Exception:
            pass
        finally:
            if self.binary_data_profile_pic != b'':
                img = ImageTk.PhotoImage(img_file)
                self.image_label.config(image=img)
                self.image_label.image = img
                self.image_label.pack(fill=BOTH)
            else:
                self.image_label.forget()
                return

    # ************************************* Update Data ********************************* #
    def update_data(self):
        if self.text_unit.get() == '' or self.text_comp_no.get() == '' \
                or self.text_name.get() == '' or self.text_phone.get() == '':
            messagebox.showerror('Error ', ' Please enter the values in the fields')
        else:
            try:
                update_query = messagebox.askyesno('UPDATE', 'Are you sure, you want to update data?')
                if update_query > 0:
                    my_conn = self.connect_database()
                    my_cursor = my_conn.cursor()

                    query = 'update phone_details set '
                    values_name = 'Unit=%s,Rnk=%s,Name=%s,Phone=%s,Email=%s,TempAdd=%s,PermAdd=%s,DOB=%s,DOJ=%s,' \
                                  'Sex=%s,MaritalStatus=%s,Bloodgp=%s,Photo=%s where CompNo=%s'
                    values = (self.text_unit.get(),
                              self.text_rank.get(),
                              self.text_name.get(),
                              self.text_phone.get(),
                              self.text_email.get(),
                              self.text_temp_add.get(),
                              self.text_perm_add.get(),
                              self.text_dob.get(),
                              self.text_recent_leave.get(),
                              self.text_sex.get(),
                              self.text_mar_status.get(),
                              self.text_bloodgp.get(),
                              self.binary_data_profile_pic,
                              self.text_comp_no.get())
                    my_cursor.execute(query + values_name, values)
                else:
                    return
                my_conn.commit()
                my_conn.close()
                self.fetch_data()
                messagebox.showinfo('UPDATE SUCCESSFUL', 'User has been updated successfully', parent=self.window)
            except Exception as ex:
                messagebox.showerror('Couldn\'t Update', f'{str(ex)}', parent=self.window)
            self.clear_data()

    # ************************************* Delete Data ********************************* #
    def delete_data(self):
        if self.text_comp_no.get() == '':
            messagebox.showerror('Error ', ' Please enter the values in the fields')
        else:
            try:
                delete_query = messagebox.askyesno('Delete', 'Are you sure, you want to delete data?')
                if delete_query > 0:
                    my_conn = self.connect_database()
                    my_cursor = my_conn.cursor()
                    delete_command = 'delete from phone_details where CompNo=%s'
                    value = (self.text_comp_no.get(),)
                    my_cursor.execute(delete_command, value)
                else:
                    return
                my_conn.commit()
                self.fetch_data()
                my_conn.close()
                self.clear_data()
                messagebox.showinfo('DELETE SUCCESSFUL', 'User has been deleted successfully', parent=self.window)

            except Exception as ex:
                messagebox.showerror('Couldn\'t Delete', f'{str(ex)}', parent=self.window)

    # *************************************** Clear Data ***************************************** #
    def clear_data(self):
        self.text_unit.set('')
        self.text_comp_no.set('')
        self.text_rank.set('')
        self.text_name.set('')
        self.text_phone.set('')
        self.text_email.set('')
        self.text_temp_add.set('')
        self.text_perm_add.set('')
        self.text_sex.set('')
        self.text_mar_status.set('')
        # self.lbl_display_age.config(text='')
        self.text_bloodgp.set('')
        import datetime
        today = datetime.date.today()
        self.text_dob.set('{}-{}-{}'.format(today.year, today.month, today.day))
        self.text_recent_leave.set('{}-{}-{}'.format(today.year, today.month, today.day))
        self.image_label.forget()
        self.binary_data_profile_pic = b''

    # **************************************** Search Data *************************************** #
    def search_data(self, event):
        try:
            my_conn = self.connect_database()
            my_cursor = my_conn.cursor()
            my_cursor.execute('select * from phone_details where ' + str(self.text_search_by.get()) + " LIKE '%" +
                              str(self.text_search_text.get()) + "%'")
            obtained_rows = my_cursor.fetchall()
            if len(obtained_rows) != 0:
                self.phone_details_tree.delete(*self.phone_details_tree.get_children())
                for row in obtained_rows:
                    self.phone_details_tree.insert("", END, values=row)
                self.phone_details_tree.focus_set()
                children = self.phone_details_tree.get_children()
                self.phone_details_tree.selection_set(children[0])
                self.entry_search.focus_set()
            else:
                for item in self.phone_details_tree.get_children():
                    self.phone_details_tree.delete(item)
            my_conn.close()
        except Exception as ex:
            pass
            messagebox.showerror('Error', f'{str(ex)}', parent=self.window)

