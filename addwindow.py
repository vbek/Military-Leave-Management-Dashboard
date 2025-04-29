import io
import os
import tkinter
import tkinter.font
from tkinter import Frame, Label, LabelFrame, Button, ttk, messagebox, StringVar, Entry, RIDGE, W, PhotoImage, DISABLED, \
    TOP
from tkinter import LEFT, RIGHT, Toplevel, BOTH, BOTTOM, VERTICAL, CENTER, END, RAISED, Y

import mysql.connector
from PIL import Image, ImageTk
from tkcalendar import DateEntry


class AddWindow(Frame):
    def __init__(self, container_frame, dict_data):
        Frame.__init__(self, container_frame)
        self.quote_text = ''
        self.dict_data = dict_data
        self.user = self.dict_data['user']
        self.sorted_unit_name = self.dict_data['sorted_unit_name']
        self.window_width = self.dict_data['window_width']
        self.window_height = self.dict_data['window_height']
        self.database = 'bibekdb'
        self.text_unit = StringVar()
        self.text_comp_no = StringVar()
        self.text_name = StringVar()
        self.text_phone = StringVar()
        self.text_loc = StringVar()
        self.text_rank = StringVar()
        self.text_trade = StringVar()
        self.text_perm_add = StringVar()
        self.text_dob = StringVar()
        self.text_sex = StringVar()
        self.text_remarks = StringVar()
        self.text_search_by = StringVar()
        self.text_search_text = StringVar()
        self.text_select_unit = StringVar()
        self.text_bloodgp = StringVar()
        self.binary_data_profile_pic = b''
        self.entry_search = Entry()
        self.image_label = Label()
        self.phone_details_tree = ttk.Treeview()
        self.combo_select_unit = ttk.Combobox()
        self.combo_unit = ttk.Combobox()
        self.entry_dob = DateEntry()
        self.btn_view_data_of_user = Button()
        self.current_sort_order = 'ascending'
        self.set_layout()

    def set_layout(self):

        #  **************************************** Upper Frame  **************************************** #
        upper_frame = LabelFrame(self, bd=2, relief=RIDGE, text="Employee Information",
                                 font=('times new roman', 10, 'bold'), bg='white', fg='red')
        upper_frame.place(x=0, y=0, width=self.window_width - 110, height=self.window_height / 2 - 90)

        #  **************************************** Unit  **************************************** #
        lbl_unit = Label(upper_frame, text='Unit:', font=('times new roman', 11, 'bold'),
                         bg='white', fg='black')
        lbl_unit.grid(row=0, column=0, sticky=W, padx=5)

        self.combo_unit = ttk.Combobox(upper_frame, textvariable=self.text_unit,
                                       font=('times new roman', 10, 'bold'), width=15, state='readonly')
        self.combo_unit['value'] = self.sorted_unit_name
        self.combo_unit.current(0)
        self.combo_unit.grid(row=0, column=1, padx=5, pady=17, sticky=W)
        self.combo_unit.configure(background='light blue')

        #  **************************************** Comp No.  **************************************** #
        lbl_comp_no = Label(upper_frame, text='Comp No:', font=('times new roman', 11, 'bold'),
                            bg='white', fg='black')
        lbl_comp_no.grid(row=0, column=2, sticky=W, padx=5)

        entry_comp_no = Entry(upper_frame, textvariable=self.text_comp_no,
                              font=('times new roman', 9), bg='white', fg='black', width=15)
        entry_comp_no.grid(row=0, column=3, sticky=W, padx=5, pady=17)

        #  **************************************** Rank  **************************************** #
        rank_columns = ['Lt Col', 'Major', 'Capt', 'T/Capt', 'Lt', 'T/Lt', '2nd Lt', 'Acc Lt', 'Sub Major',
                        'Sub', 'Sub Ka', 'Acc Sub', 'Pandit Sub', 'Jam', 'Jama Ka', 'Acc Jam', 'Sgt Major',
                        'Q/Sgt', 'Sgt', 'Hu Ka', 'Cpl', 'A Ka', 'L/Cpl', 'Sappers', 'Sainya', 'Fol Sgt', 'Ba Kaa Si',
                        'Charma Karmi', 'Su Chi Kar', 'Barber', 'Safaai Karmi', 'Loha Kaar']
        lbl_rank = Label(upper_frame, text='Rank:', font=('times new roman', 11, 'bold'),
                         bg='white', fg='black')
        lbl_rank.grid(row=0, column=4, sticky=W, padx=5)

        combo_rank = ttk.Combobox(upper_frame, textvariable=self.text_rank,
                                  font=('times new roman', 9), background='white',
                                  width=15, state='readonly')
        combo_rank['values'] = rank_columns
        combo_rank.grid(row=0, column=5, sticky=W, padx=5, pady=17)

        # entry_rank = Entry(upper_frame, textvariable=self.text_rank,
        #                    font=('times new roman', 9), bg='white',
        #                    width=15)
        #
        # entry_rank.grid(row=0, column=5, sticky=W, padx=2, pady=17)

        #  **************************************** Name  **************************************** #
        lbl_name = Label(upper_frame, text='Name:', font=('times new roman', 11, 'bold'),
                         bg='white', fg='black')
        lbl_name.grid(row=0, column=6, sticky=W, padx=5)

        entry_name = Entry(upper_frame, textvariable=self.text_name,
                           font=('Times New Roman', 9),
                           bg='white', fg='black', width=30)
        entry_name.grid(row=0, column=7, sticky=W, padx=2, pady=17)

        #  **************************************** Trade  **************************************** #
        lbl_trade = Label(upper_frame, text='Trade:', font=('times new roman', 11, 'bold'),
                          bg='white', fg='black')
        lbl_trade.grid(row=1, column=0, sticky=W, padx=5)

        entry_trade = Entry(upper_frame, textvariable=self.text_trade,
                            font=('times new roman', 9),
                            bg='white', fg='black', width=20)
        entry_trade.grid(row=1, column=1, sticky=W, padx=5, pady=17)

        #  **************************************** Loc  **************************************** #
        lbl_loc = Label(upper_frame, text='Loc:', font=('times new roman', 11, 'bold'),
                        bg='white', fg='black')
        lbl_loc.grid(row=1, column=2, sticky=W, padx=5)

        combo_loc = ttk.Combobox(upper_frame, textvariable=self.text_loc,
                                 font=('times new roman', 9),
                                 width=12, state='readonly')
        combo_loc['values'] = ['HQ', 'Mission', 'Training', 'Kaaj', 'Out of HQ', 'Post', 'Other']
        combo_loc.grid(row=1, column=3, sticky=W, padx=5, pady=17)
        combo_loc.current(0)

        #  **************************************** Phone No  **************************************** #
        lbl_phone = Label(upper_frame, text='Phone No:', font=('times new roman', 11, 'bold'),
                          bg='white', fg='black')
        lbl_phone.grid(row=1, column=4, sticky=W, padx=5)

        entry_phone = Entry(upper_frame, textvariable=self.text_phone,
                            font=('times new roman', 9),
                            bg='white', fg='black', width=18)
        entry_phone.grid(row=1, column=5, sticky=W, padx=5, pady=17)

        #  **************************************** Perm Address  **************************************** #
        lbl_perm_add = Label(upper_frame, text='Address:', font=('times new roman', 11, 'bold'),
                             bg='white', fg='black')
        lbl_perm_add.grid(row=1, column=6, sticky=W, padx=5)

        entry_perm_add = Entry(upper_frame, textvariable=self.text_perm_add,
                               font=('times new roman', 9),
                               bg='white', fg='black', width=30)
        entry_perm_add.grid(row=1, column=7, sticky=W, padx=5, pady=17)

        #  **************************************** Date Of Birth  **************************************** #
        lbl_display_age = Label()

        lbl_dob = Label(upper_frame, text='DOB:', font=('times new roman', 11, 'bold'),
                        bg='white', fg='black')
        lbl_dob.grid(row=2, column=0, sticky=W, padx=5)

        self.entry_dob = DateEntry(upper_frame, textvariable=self.text_dob,
                                   date_pattern='y-mm-dd')
        self.entry_dob.grid(row=2, column=1, sticky=W, padx=5, pady=17)

        #  **************************************** Sex  **************************************** #
        lbl_sex = Label(upper_frame, text='Sex:', font=('times new roman', 11, 'bold'),
                        bg='white', fg='black')
        lbl_sex.grid(row=2, column=2, sticky=W, padx=5)

        combo_sex = ttk.Combobox(upper_frame, textvariable=self.text_sex,
                                 font=('times new roman', 10, 'bold'), width=10, state='readonly')
        combo_sex['value'] = ('', 'Male', 'Female')
        combo_sex.current(0)
        combo_sex.grid(row=2, column=3, sticky=W, padx=5, pady=17)

        #  **************************************** Blood Gp  **************************************** #
        lbl_blood_gp = Label(upper_frame, text='Blood GP:', font=('times new roman', 11, 'bold'),
                             bg='white', fg='black')
        lbl_blood_gp.grid(row=2, column=4, sticky=W, padx=5)

        combo_ms = ttk.Combobox(upper_frame, textvariable=self.text_bloodgp,
                                font=('times new roman', 10, 'bold'), width=13, state='readonly')
        combo_ms['value'] = ('', 'A +ve', 'B +ve', 'AB +ve', 'O +ve', 'A -ve', 'B -ve', 'AB -ve', 'O -ve')
        combo_ms.current(0)
        combo_ms.grid(row=2, column=5, sticky=W, padx=5, pady=17)

        #  **************************************** Remarks  **************************************** #
        lbl_remarks = Label(upper_frame, text='Remarks:', font=('times new roman', 11, 'bold'),
                            bg='white', fg='black')
        lbl_remarks.grid(row=2, column=6, sticky=W, padx=5)

        combo_remarks = Entry(upper_frame, textvariable=self.text_remarks,
                              font=('times new roman', 9),
                              bg='white', fg='black', width=30)
        combo_remarks.grid(row=2, column=7, sticky=W, padx=5, pady=17)

        #  **************************************** Photo Frame  **************************************** #
        filepath = os.path.join(os.path.dirname(__file__), "res", "pc.png")
        icon_photo_button = PhotoImage(file=filepath)
        photo_sample = icon_photo_button.subsample(10, 10)
        button_photo = Button(upper_frame, bg='white', command=self.upload_pp, image=photo_sample,
                              compound=LEFT)
        button_photo.image = photo_sample
        # self.label_title = Label(self.upper_frame, image=self.photo_sample)
        photo_lbl = LabelFrame(upper_frame, labelwidget=button_photo, bg='white',
                               font=('times new roman', 9),
                               fg='red')
        photo_lbl.place(x=self.window_width - 360, width=150, height=160)
        photo_frame = Frame(upper_frame, bd=5, relief=RIDGE, bg='white')
        photo_frame.place(x=self.window_width - 350, y=25, width=130, height=130)
        self.image_label = Label(photo_frame, background='white')
        self.image_label.pack(fill=BOTH)

        #  **************************************** Button Frame  **************************************** #
        button_frame = Frame(upper_frame, bd=2, relief=RIDGE, bg='white')
        button_frame.place(x=self.window_width - 200, y=8, width=70, height=150)

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
        lower_frame = LabelFrame(self, bd=2, relief=RIDGE, text="Employee Information Table",
                                 font=('times new roman', 10, 'bold'), bg='white', fg='#C00060')
        lower_frame.place(x=0, y=self.window_height / 2 - 90, width=self.window_width - 110,
                          height=self.window_height / 2 - 30)

        #  **************************************** Unit Selection Frame  **************************************** #
        frame_unit_selection = Frame(lower_frame, bd=5, relief=RIDGE, bg='WHITE')
        frame_unit_selection.place(x=2, y=0, width=self.window_width - 127, height=40)

        lbl_select_unit = Label(frame_unit_selection, text="SELECT UNIT:", bg="WHITE", fg='Teal', width=12,
                                font=('times new roman', 10, 'bold'))
        lbl_select_unit.grid(row=0, column=0, padx=5, pady=5)

        # if self.user == 'Super User'.upper():
        from authorization_window import AuthorizeWindow
        auth_window = AuthorizeWindow(self)
        if self.user.upper() == "SUPER USER":
            btn_drop_table = Button(frame_unit_selection, fg='Teal', bg='orange', font=('Times', 10, 'bold'),
                                    command=lambda: auth_window.authorize_user(self.user, self.drop_table),
                                    text="DROP TABLE")
            btn_drop_table.grid(row=0, column=2, padx=5, pady=5)

        def set_unit_name(event):
            self.fetch_data()

        self.combo_select_unit = ttk.Combobox(frame_unit_selection, textvariable=self.text_select_unit,
                                              width=20, font=('times new roman', 10, 'bold'),
                                              state='readonly')
        self.combo_select_unit['value'] = self.sorted_unit_name
        self.combo_select_unit.current(0)
        self.combo_select_unit.grid(row=0, column=1, padx=5)
        self.combo_select_unit.bind('<<ComboboxSelected>>', set_unit_name)

        #  **************************************** Search Frame  **************************************** #
        search_frame = LabelFrame(lower_frame, relief=RIDGE, text='Search', bd=3,
                                  font=('times new roman', 10, 'bold'), bg='white', fg='#c00060'
                                  )
        search_frame.place(x=2, y=38, width=self.window_width - 127, height=50)

        lbl_search_by = Label(search_frame, text="SEARCH BY:", bg="WHITE", fg='Teal', width=12,
                              font=('times new roman', 10, 'bold'))
        lbl_search_by.grid(row=0, column=0, padx=5, pady=5)

        combo_search = ttk.Combobox(search_frame, textvariable=self.text_search_by,
                                    width=20, font=('times new roman', 10, 'bold'), state='readonly'
                                    )
        combo_search['value'] = ("CompNo", "Rnk", "Name", "Phone", 'bloodgp', 'Loc', 'Remarks')
        combo_search.current(0)
        combo_search.grid(row=0, column=1, padx=5)

        self.entry_search = Entry(search_frame, textvariable=self.text_search_text,
                                  relief=RIDGE, font=('times new roman', 9, 'bold'),
                                  width=25, bd=2)
        self.entry_search.grid(row=0, column=2, padx=5)
        self.entry_search.bind('<KeyRelease>', self.search_data)
        text = self.get_quote()

        lbl_daily_quote = Label(search_frame, text="\"" + text + "\"",
                                font=('times new roman', 12, 'bold italic'), bg='#07575b', fg="white")
        lbl_daily_quote.grid(row=0, column=5, padx=20)

        def change_quote(e):
            change_quote_window_width = 210
            change_quote_window_height = 110
            pos_x = int((self.dict_data['window_width'] - change_quote_window_width) / 2)
            pos_y = int((self.dict_data['window_height'] - change_quote_window_height) / 2)
            change_quote_window = Toplevel(self)
            change_quote_window.title("NEW")
            change_quote_window.geometry('{}x{}+{}+{}'.format(change_quote_window_width,
                                                              change_quote_window_height,
                                                              pos_x, pos_y))
            Label(change_quote_window, text="New Quote",
                  font=('Microsoft YaHei UI Light', 10, 'bold'), anchor='w').place(x=int(change_quote_window_width / 3),
                                                                                   y=10)
            entry_quote = Entry(change_quote_window, width=30)
            entry_quote.place(x=5, y=50, anchor="w")
            entry_quote.focus_set()

            def confirm(e):
                self.quote_text = str(entry_quote.get())
                self.set_quote(self.quote_text)
                change_quote_window.destroy()
                lbl_daily_quote.config(text="" + self.quote_text + "")

            btn_confirm = Button(change_quote_window, text='CONFIRM')
            btn_confirm.place(x=int(change_quote_window_width / 3), y=70)
            btn_confirm.bind('<ButtonRelease>', confirm)

        if self.dict_data['user'].upper() == "ADMIN" or self.dict_data['user'].upper() == "SUPER USER":
            btn_edit_quote = Button(search_frame, text='EDIT QUOTE', bg="#ffce30", fg='#288ba8',
                                    font=('times new roman', 10, 'bold'))
            btn_edit_quote.grid(row=0, column=6, padx=10)
            btn_edit_quote.bind('<ButtonRelease>', change_quote)

            btn_view_all_quotes = Button(search_frame, text='VIEW QUOTES', bg="#ffce30", fg='#288ba8',
                                         font=('times new roman', 10, 'bold'), command=self.view_quotes)
            btn_view_all_quotes.grid(row=0, column=7, padx=10)
        else:
            button_delete.configure(state=DISABLED)
            button_delete.unbind('<ButtonRelease>')

        #  **************************************** Display Frame  **************************************** #

        frame_display_table = Frame(lower_frame, bd=5, relief=RIDGE)
        frame_display_table.place(y=90, width=self.window_width - 126, height=210)

        scroll_y = ttk.Scrollbar(frame_display_table, orient=VERTICAL)
        tree_columns = ('unit', 'CompNo', 'Rnk', 'Name', 'Phone', 'bloodgp', 'Loc', 'Remarks')
        self.phone_details_tree = ttk.Treeview(frame_display_table,
                                               columns=tree_columns,
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

        self.phone_details_tree.heading('unit', text='Unit', anchor=CENTER,
                                        command=lambda: self.sort_tree(self.phone_details_tree, "unit"))
        self.phone_details_tree.heading('CompNo', text='Comp No', anchor=CENTER,
                                        command=lambda: self.sort_tree(self.phone_details_tree, "CompNo"))
        self.phone_details_tree.heading('Rnk', text='Rank', anchor=CENTER,
                                        command=lambda: self.sort_tree(self.phone_details_tree, "Rnk"))
        self.phone_details_tree.heading('Name', text='Name', anchor=CENTER,
                                        command=lambda: self.sort_tree(self.phone_details_tree, "Name"))
        self.phone_details_tree.heading('Phone', text='Phone No', anchor=CENTER,
                                        command=lambda: self.sort_tree(self.phone_details_tree, "Phone"))
        self.phone_details_tree.heading('bloodgp', text='Blood Gp', anchor=CENTER,
                                        command=lambda: self.sort_tree(self.phone_details_tree, "bloodgp"))
        self.phone_details_tree.heading('Loc', text='Loc', anchor=CENTER,
                                        command=lambda: self.sort_tree(self.phone_details_tree, "Loc"))
        self.phone_details_tree.heading('Remarks', text='Remarks', anchor=CENTER,
                                        command=lambda: self.sort_tree(self.phone_details_tree, "Remarks"))

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.phone_details_tree.yview)
        self.phone_details_tree.pack(fill=BOTH, side=BOTTOM, expand=1)
        # self.phone_details_tree.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

        self.phone_details_tree['show'] = 'headings'

        self.phone_details_tree.column("unit", width=80, anchor='c')
        self.phone_details_tree.column("CompNo", width=52, anchor='c')
        self.phone_details_tree.column("Rnk", width=40, anchor='c')
        self.phone_details_tree.column("Name", width=110, anchor='c')
        self.phone_details_tree.column("Phone", width=70, anchor='c')
        self.phone_details_tree.column("bloodgp", width=60, anchor='c')
        self.phone_details_tree.column("Loc", width=60, anchor='c')
        self.phone_details_tree.column("Remarks", width=60, anchor='c')

        self.btn_view_data_of_user = Button(self, text='VIEW DATA', width=10,
                                            fg='TEAL', bg='ORANGE', font=('times new roman', 10, 'bold'))
        self.btn_view_data_of_user.place(x=self.window_width - 190, y=self.window_height - 120)
        self.btn_view_data_of_user.configure(bg='grey', fg='BLACK', state=DISABLED)

    def drop_table(self):
        parent_table = self.convert_unit_name_into_table_name(self.text_select_unit.get())
        leave_table = 'leave_record_' + parent_table
        result = messagebox.askyesno("ALERT", f"You are about to delete {self.text_select_unit.get()}"
                                              f" data,\nClick Yes to Continue")
        if result:

            try:
                from CreateConnection import CreateConnection
                conn_obj = CreateConnection('bibekdb')
                conn = conn_obj.create_connection()
                cursor = conn.cursor()
                query_to_drop_table = f'''drop table {leave_table}, {parent_table}'''
                cursor.execute(query_to_drop_table)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Record Deleted Successfully")
                self.dict_data['sorted_unit_name'].remove(self.combo_select_unit.get())
                self.combo_select_unit.configure(values=self.dict_data['sorted_unit_name'])
                self.combo_unit.configure(values=self.dict_data['sorted_unit_name'])
                self.combo_select_unit.current(0)
                self.combo_unit.current(0)

                self.fetch_data()
            except mysql.connector.Error as err:
                messagebox.showerror("ERROR", err)
        else:
            pass

    def view_quotes(self):
        quotes_display_window = Toplevel(self)
        quotes_display_window.title("ALL QUOTES")
        quotes_display_window.geometry("500x200+500+0")
        quotes_display_window.configure(bg='White')
        quotes_display_window.focus_set()

        db = self.connect_database()
        query_to_get_quote_text = "select * from bibekdb.quote_list_log"
        my_cursor = db.cursor()
        my_cursor.execute(query_to_get_quote_text)
        data = my_cursor.fetchall()
        for i in range(0, len(data)):
            Label(quotes_display_window, text=str(i + 1) + ". " + str(data[i][1]) + ', ' + str(data[i][2]),
                  font=('Times', 10, 'bold'), fg='BLACK', bg='WHITE').pack(side=TOP, anchor='w')
        # quotes = list(enumerate(quotes))
        # messagebox.showinfo(title='QUOTES', message=str(quotes))
        db.close()

    def get_quote(self):
        db = self.connect_database()
        query_to_get_quote_text = "select * from bibekdb.quote_list_log ORDER BY counter DESC LIMIT 1"
        my_cursor = db.cursor()
        my_cursor.execute(query_to_get_quote_text)
        data = my_cursor.fetchone()
        self.quote_text = data[1]
        db.commit()
        db.close()
        return self.quote_text

    def set_quote(self, quote):
        try:
            db = self.connect_database()
            from datetime import datetime
            date_now_str = str(datetime.now().date())

            query_to_get_quote_text = "insert into bibekdb.quote_list_log (quote_text, date_created) values (%s,%s)"
            values = (quote, date_now_str,)
            my_cursor = db.cursor()
            my_cursor.execute(query_to_get_quote_text, values)
            db.commit()
            db.close()
        except Exception as ex:
            pass

    #  **************************************** Connecting to Database  **************************************** #

    def connect_database(self):
        from CreateConnection import CreateConnection
        conn = CreateConnection(self.database)
        return conn.create_connection()

        # **************************************** Fetch All Data  **************************************** #

    def fetch_data(self):
        conn = self.connect_database()
        my_cursor = conn.cursor(dictionary=True)

        unit_table = self.convert_unit_name_into_table_name(self.text_select_unit.get())

        my_cursor.execute(f'select * from {unit_table}')

        data = my_cursor.fetchall()
        if len(data) != 0:
            self.phone_details_tree.delete(*self.phone_details_tree.get_children())
            for datum in data:
                values = [datum['Unit'].title(), datum['CompNo'], datum['Rnk'], datum['Name'],
                          datum['Phone'], datum['bloodgp'], datum['Loc'], datum['Remarks']]
                self.phone_details_tree.insert("", END, values=values)
            # my_conn.commit()
        conn.close()

        # **************************************** Get Data ****************************************

    def get_cursor(self, event=''):
        self.btn_view_data_of_user.configure(fg='TEAL', bg='ORANGE', state=tkinter.NORMAL)
        cursor_row = self.phone_details_tree.focus()
        self.btn_view_data_of_user.configure(command=lambda: self.display_user_data_window(self.phone_details_tree,
                                                                                           cursor_row))
        content = self.phone_details_tree.item(cursor_row)
        row = content['values']
        my_conn = self.connect_database()
        my_cursor = my_conn.cursor()
        unit_table = self.convert_unit_name_into_table_name(self.text_select_unit.get())
        if row != '':
            comp_no = int(float(row[1]))
            get_data_query = f'''select * from bibekdb.{unit_table} where CompNo={comp_no} '''
            my_cursor.execute(get_data_query)
            data = my_cursor.fetchone()
            self.text_unit.set(data[0].upper())
            self.text_comp_no.set(data[1])
            self.text_name.set(data[3])
            self.text_phone.set(data[4])
            self.text_loc.set(data[5])
            self.text_rank.set(data[2])
            self.text_trade.set(data[6])
            self.text_perm_add.set(data[7])
            self.text_dob.set(data[8])
            self.text_sex.set(data[9])
            self.text_bloodgp.set(data[10])
            self.text_remarks.set(data[11])
            self.binary_data_profile_pic = data[12]
            self.set_profile_pic(self.binary_data_profile_pic)

        # **************************************** Set Profile Pic **********************************

    def set_profile_pic(self, binary_data_image):
        if binary_data_image is not None:
            image = Image.open(io.BytesIO(binary_data_image))
            image = ImageTk.PhotoImage(image)
            self.image_label.configure(image=image)
            self.image_label.image = image
            self.image_label.pack(fill=BOTH)
        else:
            self.image_label.forget()
            return

        # **************************************** Adding a data to the database **********************************

    def add_data(self):
        my_conn = self.connect_database()
        cur = my_conn.cursor()
        if self.text_unit.get() == '' or self.text_comp_no.get() == '' \
                or self.text_name.get() == '' or self.text_rank.get() == '':
            messagebox.showerror('Error ', ' Please enter the values in the fields')
        else:
            unit_table = self.convert_unit_name_into_table_name(self.text_unit.get())
            query = f'''insert into {unit_table} values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            values = (self.text_unit.get(),
                      self.text_comp_no.get(),
                      self.text_rank.get(),
                      self.text_name.get(),
                      self.text_phone.get(),
                      self.text_loc.get(),
                      self.text_trade.get(),
                      self.text_perm_add.get(),
                      self.text_dob.get(),
                      self.text_sex.get(),
                      self.text_bloodgp.get(),
                      self.text_remarks.get(),
                      self.binary_data_profile_pic,)
            try:
                cur.execute(query, values)
                my_conn.commit()
                my_conn.close()
                messagebox.showinfo('SUCCESS', 'User Added Successfully')
            except mysql.connector.Error as err:
                messagebox.showerror("Error", err)
            # my_conn.commit()
            # my_conn.close()
        self.fetch_data()
        self.clear_data()

    @staticmethod
    def convert_unit_name_into_table_name(unit_name):
        split_unit_name = unit_name.split(' ')
        combined_unit_table_name = split_unit_name[0].lower()
        for i in range(1, len(split_unit_name)):
            combined_unit_table_name += '_' + split_unit_name[i].lower()
        return combined_unit_table_name

        # ************************************* Add Profile Pic and Set binary value ************* #

    def upload_pp(self):
        from tkinter import filedialog
        filetype = [("Image Files", "*.jpg"), ("Portable ", "*.png")]
        file = filedialog.askopenfilename(filetypes=filetype)
        try:
            if file:
                img_reader = Image.open(file)
                img_file = img_reader.resize((130, 130))
                img_binary = io.BytesIO()
                img_file.save(img_binary, 'PNG')
                self.binary_data_profile_pic = img_binary.getvalue()

                if self.binary_data_profile_pic:
                    img = ImageTk.PhotoImage(img_file)
                    self.image_label.config(image=img)
                    self.image_label.image = img
                    self.image_label.pack(fill=BOTH)
                else:
                    self.image_label.forget()
                    return
        except Exception:
            pass
        # ************************************* Update Data ********************************* #

    def sort_tree(self, tree, col):
        """sort tree contents when a column header is clicked on"""
        descending = self.current_sort_order == "descending"
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        # check if the data to be sorted is numeric and convert to float
        try:
            data = [(float(val), item) for val, item in data]
        except ValueError:
            pass
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the current sort order for next time
        self.current_sort_order = "ascending" if self.current_sort_order == "descending" else "descending"

    def update_data(self):
        if self.text_unit.get() == '' or self.text_comp_no.get() == '' \
                or self.text_name.get() == '' or self.text_rank.get() == '':
            messagebox.showerror('Error ', ' Please enter the values in the fields')
        else:
            try:
                update_query = messagebox.askyesno('UPDATE', 'Are you sure, you want to update data?')
                if update_query > 0:
                    my_conn = self.connect_database()
                    my_cursor = my_conn.cursor()

                    unit_table = self.convert_unit_name_into_table_name(self.text_unit.get())

                    query = f'update {unit_table} set '
                    values_name = 'Unit=%s,Rnk=%s,Name=%s,Phone=%s,Loc=%s,Trade=%s,Address=%s,DOB=%s,' \
                                  'Sex=%s,Remarks=%s,Bloodgp=%s,Photo=%s where CompNo=%s'
                    values = (self.text_unit.get(),
                              self.text_rank.get(),
                              self.text_name.get(),
                              self.text_phone.get(),
                              self.text_loc.get(),
                              self.text_trade.get(),
                              self.text_perm_add.get(),
                              self.text_dob.get(),
                              self.text_sex.get(),
                              self.text_remarks.get(),
                              self.text_bloodgp.get(),
                              self.binary_data_profile_pic,
                              self.text_comp_no.get())
                    my_cursor.execute(query + values_name, values)
                else:
                    return
                my_conn.commit()
                my_conn.close()
                self.fetch_data()
                messagebox.showinfo('UPDATE SUCCESSFUL', 'User has been updated successfully', parent=self)
            except Exception as ex:
                messagebox.showerror('Couldn\'t Update', f'{str(ex)}', parent=self)
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

                    unit_table = self.convert_unit_name_into_table_name(self.text_unit.get())
                    delete_command = f"delete from {unit_table} where CompNo={self.text_comp_no.get()}"

                    my_cursor.execute(delete_command)
                    my_conn.commit()
                    my_conn.close()
                else:
                    return
                self.fetch_data()
                self.clear_data()
                messagebox.showinfo('DELETE SUCCESSFUL', 'User has been deleted successfully', parent=self)

            except Exception as ex:
                messagebox.showerror('Couldn\'t Delete', f'{str(ex)}', parent=self)

        # *************************************** Clear Data ***************************************** #

    def clear_data(self):
        self.text_comp_no.set('')
        self.text_rank.set('')
        self.text_name.set('')
        self.text_phone.set('')
        self.text_loc.set('')
        self.text_trade.set('')
        self.text_perm_add.set('')
        self.text_sex.set('')
        self.text_remarks.set('')
        self.text_bloodgp.set('')
        import datetime
        today = datetime.date.today()
        self.text_dob.set('{}-{}-{}'.format(today.year, today.month, today.day))
        self.image_label.forget()
        self.binary_data_profile_pic = b''

        # **************************************** Search Data *************************************** #

    def search_data(self, event):
        try:
            my_conn = self.connect_database()
            my_cursor = my_conn.cursor(dictionary=True)

            unit_table = self.convert_unit_name_into_table_name(self.text_select_unit.get())

            my_cursor.execute(f'select * from {unit_table} where ' + str(self.text_search_by.get()) + " LIKE '%" +
                              str(self.text_search_text.get()) + "%'")
            obtained_rows = my_cursor.fetchall()
            if len(obtained_rows) != 0:
                self.phone_details_tree.delete(*self.phone_details_tree.get_children())
                for datum in obtained_rows:
                    values = [datum['Unit'], datum['CompNo'], datum['Rnk'], datum['Name'], datum['Phone'],
                              datum['bloodgp'], datum['Loc'], datum['Remarks']]
                    self.phone_details_tree.insert("", END, values=values)
                self.phone_details_tree.focus_set()
                children = self.phone_details_tree.get_children()
                self.phone_details_tree.selection_set(children[0])
                self.phone_details_tree.focus(children[0])
                self.entry_search.focus_set()
            else:
                for item in self.phone_details_tree.get_children():
                    self.phone_details_tree.delete(item)
            my_conn.close()
        except Exception as ex:
            pass
            messagebox.showerror('Error', f'{str(ex)}', parent=self)

    def display_user_data_window(self, tree, item):
        data = tree.item(item)['values'][1]
        converted_unit_name = self.convert_unit_name_into_table_name(self.text_select_unit.get())
        from user_data_display import UserDataWindow

        UserDataWindow(self, data, converted_unit_name)
