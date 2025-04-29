import tkinter
from datetime import datetime
from tkinter import Frame, Label, LabelFrame, Button, ttk, messagebox, StringVar, RIDGE, DISABLED, LEFT, filedialog
from tkinter import RIGHT, Toplevel, BOTTOM, VERTICAL, HORIZONTAL, CENTER, END, X, Y, GROOVE, NORMAL, BOTH, Entry

import mysql.connector
from tkcalendar import DateEntry


class HomeWindow(Frame):
    def __init__(self, container_frame, dict_data):
        Frame.__init__(self, container_frame)

        self.current_sort_order = 'ascending'
        self.display_tree = ttk.Treeview()
        self.dict_data = dict_data
        self.user = self.dict_data['user']
        self.sorted_unit_name = self.dict_data['sorted_unit_name']
        self.unit_name = StringVar()
        self.text_combo_search = StringVar()
        self.text_search_input = StringVar()
        self.unit_data_frame = LabelFrame()
        self.window_width = self.dict_data['window_width']
        self.window_height = self.dict_data['window_height']
        self._database = 'bibekdb'
        self.set_window()

    def select_unit_info(self, event=None):
        self.unit_data_frame.configure(text=self.unit_name.get())
        self.display_data()

    def search_data(self, event=None):
        search_value = self.text_search_input.get()
        for item in self.display_tree.get_children():
            item_text = self.display_tree.item(item, 'values')
            if self.text_combo_search.get() == 'CompNo':
                if search_value.lower() in item_text[1].lower():
                    self.display_tree.selection_set(item)
                    self.display_tree.yview_moveto(0.5)
                    self.display_tree.see(item)
                    break
                else:
                    self.display_tree.selection_clear()
            else:
                if search_value.lower() in item_text[3].lower():
                    self.display_tree.selection_set(item)
                    self.display_tree.yview_moveto(0.5)
                    self.display_tree.see(item)

                    break
                else:
                    self.display_tree.selection_clear()

    def set_window(self):
        padding = 10
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="white", foreground="black")
        style.theme_use("clam")
        style.configure("Treeview", background='light green',
                        fieldbackground="light blue", foreground="BLACK", rowheight=24)
        style.configure("TCombobox", background='light blue', foreground='Black')

        top_frame = LabelFrame(self, bd=2, relief=RIDGE, text="Unit Leave Information",
                               font=('times new roman', 10, 'bold'), bg='white', fg='#C00060')
        top_frame.place(width=self.window_width - 115, height=self.window_height - 100)

        #  **************************************** UNIT DATA Frame  **************************************** #
        self.unit_data_frame = LabelFrame(top_frame, relief=RIDGE, text="Unit", bd=3,
                                          font=('times new roman', 10, 'bold'), bg='white', fg='#c00060'
                                          )
        self.unit_data_frame.place(x=0, y=0, width=self.window_width - 120, height=50)

        lbl_unit_data = Label(self.unit_data_frame, text="SELECT UNIT:", bg="#336b87", fg='#ffffff',
                              font=('times new roman', 10, 'bold'))
        lbl_unit_data.pack(side=LEFT, pady=5, padx=5)

        combo_unit = ttk.Combobox(self.unit_data_frame, textvariable=self.unit_name,
                                  width=20, font=('times new roman', 10, 'bold'), state='readonly')

        combo_unit['value'] = self.sorted_unit_name
        combo_unit.current(0)
        combo_unit.pack(side=LEFT, after=lbl_unit_data, padx=5, pady=5)
        combo_unit.bind("<<ComboboxSelected>>", self.select_unit_info)

        combo_search = ttk.Combobox(self.unit_data_frame, textvariable=self.text_combo_search,
                                    width=20, font=('times new roman', 10, 'bold'), state='readonly')
        combo_search['value'] = ['CompNo', 'Name']
        combo_search.pack(side=LEFT, after=combo_unit, padx=5, pady=5)
        combo_search.current(0)

        entry_search = tkinter.Entry(self.unit_data_frame, textvariable=self.text_search_input,
                                     width=20, font=('times new roman', 10, 'bold'), bg='white')
        entry_search.pack(side=LEFT, after=combo_search, padx=5, pady=5)
        entry_search.bind('<KeyRelease>', self.search_data)
        entry_search.focus_force()
        display_frame = Frame(self, bd=5, relief=RIDGE)
        display_frame.place(x=125, y=75, width=self.window_width - 245, height=self.window_height - 200)

        # ***************************************************** Leave Start Date Frame *************************

        btn_leave_frame = Frame(self, bd=5, relief=GROOVE, bg='Teal')
        btn_leave_frame.place(x=2, y=80, width=125, height=230)

        row_size = 27
        font_text = ('Segoe UI', 8, 'bold')
        # ***************************************************** Leave Start Date Label *************************
        lbl_start_date = Label(btn_leave_frame, font=font_text, text="Leave Start Date", fg='white', bg='teal',
                               anchor='w')

        lbl_start_date.place(x=0+padding, y=0+padding)

        LabelFrame(btn_leave_frame, borderwidth=1, relief='solid').place(x=0, y=20+padding, width=110, height=2)

        # ***************************************************** Leave Start Date Entry *************************
        leave_start_date = DateEntry(btn_leave_frame, width=11, date_pattern='mm/dd/y')
        leave_start_date.place(x=0+padding, y=row_size * 1+padding+10)
        leave_start_date.configure(state=DISABLED)

        days = list(range(1, 36))
        scroll_no_of_days = ttk.Combobox(btn_leave_frame, width=2, state='readonly')
        scroll_no_of_days['values'] = days
        scroll_no_of_days.current(0)
        scroll_no_of_days.place(x=0+padding, y=row_size * 2+padding+20)

        scroll_no_of_days.configure(state=DISABLED)

        Label(btn_leave_frame, text='Days', font=font_text, anchor='w', fg='white', bg='teal',
              width=4).place(x=40, y=row_size * 2+padding+20)

        LabelFrame(btn_leave_frame, borderwidth=1, relief='solid').place(x=0, y=78+padding+25, width=110, height=2)

        # ***************************************************** Leave End Date Label *************************

        lbl_end_date = Label(btn_leave_frame, text="Return Date", font=font_text, fg='white', bg='teal',
                             anchor='w')
        lbl_end_date.place(x=0+padding, y=row_size * 3 + padding + 30)
        LabelFrame(btn_leave_frame, borderwidth=1, relief='solid').place(x=0, y=105+padding+25, width=110, height=2)

        return_date = DateEntry(btn_leave_frame, width=11, date_pattern='mm/dd/y')
        return_date.place(x=0+padding, y=row_size * 4+padding+30)
        return_date.configure(state=DISABLED)

        def set_return_date(event):
            no_of_days = int(scroll_no_of_days.get())
            going_date = leave_start_date.get_date()
            from datetime import timedelta
            date_1 = datetime.strptime(str(going_date), "%Y-%m-%d")
            returning_date = date_1 + timedelta(days=(no_of_days - 1))
            return_date.set_date(returning_date)

        scroll_no_of_days.bind("<<ComboboxSelected>>", set_return_date)

        btn_record_leave = Button(btn_leave_frame, fg='teal', font=font_text, text='Record Leave', anchor='e')
        btn_record_leave.place(x=0+padding, y=row_size * 5+padding+35)
        btn_record_leave.configure(state=DISABLED)

        bmi_frame = Frame(self, relief='groove', borderwidth=5, bg='TEAL')
        bmi_frame.place(x=2, y=310, width=125, height=180)

        age = list(range(18, 63))
        Label(bmi_frame, text='BMI', width=15, fg='white', bg='teal', font=font_text, anchor='center').place(x=0, y=0)

        LabelFrame(bmi_frame, borderwidth=1, relief='solid').place(x=0, y=25, width=110, height=2)

        Label(bmi_frame, text='Age', fg='white', font=font_text, bg='teal', anchor='w').place(x=0, y=30)

        age_combobox = ttk.Combobox(bmi_frame, width=2, state='readonly')
        age_combobox['values'] = age
        age_combobox.current(0)
        age_combobox.place(x=25, y=30)

        Label(bmi_frame, text='Sex', fg='white', bg='teal', font=font_text, anchor='w').place(x=59, y=30)

        sex_combobox = ttk.Combobox(bmi_frame, width=2, state='readonly')
        sex_combobox['values'] = ['M', 'F']
        sex_combobox.current(0)
        sex_combobox.place(x=80, y=30)

        height_in_cm = list(range(152, 214))
        height_in_inch = ['5\'0\"', '5\'1\"', '5\'2\"', '5\'3\"', '5\'4\"', '5\'5\"', '5\'6\"',
                          '5\'7\"', '5\'8\"', '5\'9\"', '5\'10\"', '5\'11\"', '5\'12\"'
                                                                              '6\'0\"', '6\'1\"', '6\'2\"', '6\'3\"',
                          '6\'4\"', '6\'5\"',
                          '6\'6\"', '6\'7\"', '6\'8\"', '6\'9\"', '6\'10\"', '6\'11\"', '6\'12\"']
        Label(bmi_frame, text='Ht:', width=12, fg='white', font=font_text, bg='teal', anchor='w').place(x=0, y=60)
        height_combobox = ttk.Combobox(bmi_frame, width=5, state='readonly')
        height_combobox['values'] = height_in_cm
        height_combobox.current(0)
        height_combobox.place(x=19, y=60)

        height_sel_combobox = ttk.Combobox(bmi_frame, width=3, state='readonly')
        height_sel_combobox['values'] = ['cm', 'ft']
        height_sel_combobox.current(0)
        height_sel_combobox.place(x=74, y=60)

        Label(bmi_frame, text='Wt(Kg):', width=12, font=font_text, fg='white', bg='teal', anchor='w').place(x=0, y=90)
        wt_values = list(range(40, 100))
        wt_combobox = ttk.Combobox(bmi_frame, width=2, state='readonly')
        wt_combobox['values'] = wt_values
        wt_combobox.current(0)
        wt_combobox.place(x=50, y=90)

        def set_height(event):
            if height_sel_combobox.get() == 'ft':
                height_combobox.configure(values=height_in_inch)
                height_combobox.current(0)
            else:
                height_combobox.configure(values=height_in_cm)
                height_combobox.current(0)

        height_sel_combobox.bind('<<ComboboxSelected>>', set_height)

        def calculate_bmi(event):
            height_type = height_sel_combobox.get()
            ht = height_combobox.get()
            wt = float(wt_combobox.get())
            if height_type == 'cm':
                ht_in_meter = int(ht) / 100
                bmi = wt / (ht_in_meter * ht_in_meter)
            else:
                import re
                ht_list = list(map(int, re.findall(r'\d+', ht)))
                ht_in_meter = (ht_list[0] + ht_list[1] / 12) / 3.28
                bmi = wt / (ht_in_meter * ht_in_meter)

            age_value = int(age_combobox.get())
            sex = sex_combobox.get()

            if sex.upper() == 'M':
                if 18 <= age_value <= 30:
                    min_bmi = 18.5
                    max_bmi = 25.25
                elif 31 <= age_value <= 35:
                    min_bmi = 18.5
                    max_bmi = 25.5
                elif 36 <= age_value <= 40:
                    min_bmi = 18.5
                    max_bmi = 25.7
                elif 41 <= age_value <= 45:
                    min_bmi = 18.5
                    max_bmi = 26
                elif 46 <= age_value <= 50:
                    min_bmi = 18.5
                    max_bmi = 26.25
                else:
                    min_bmi = 18.5
                    max_bmi = 26.5
            else:
                if 18 <= age_value <= 30:
                    min_bmi = 18.5
                    max_bmi = 25
                elif 31 <= age_value <= 35:
                    min_bmi = 18.5
                    max_bmi = 25.25
                elif 36 <= age_value <= 40:
                    min_bmi = 18.5
                    max_bmi = 25.5
                elif 41 <= age_value <= 45:
                    min_bmi = 18.5
                    max_bmi = 25.75
                elif 46 <= age_value <= 50:
                    min_bmi = 18.5
                    max_bmi = 26
                else:
                    min_bmi = 18.5
                    max_bmi = 26.25

            Label(bmi_frame, text="BMI: " + str(round(bmi, 2)),
                  fg='teal', font=font_text, bg='orange').place(x=0, y=150)


        btn_calculate_bmi = Button(bmi_frame, text='Calculate', font=font_text, fg='teal')
        btn_calculate_bmi.place(x=30, y=120)

        btn_calculate_bmi.bind('<ButtonRelease>', calculate_bmi)

        def view_leave_record_of_a_person(event):
            my_conn = self.connect_database()
            my_cursor = my_conn.cursor()

            unit_table = self.convert_unit_name_into_table_name(self.unit_name.get())
            unit_leave_table = 'leave_record_' + unit_table

            query = f'''select * from {unit_leave_table} where 
                        {unit_leave_table}.CompNo=%s'''
            cur_item = self.display_tree.focus()
            selected_name = self.display_tree.item(cur_item)['values'][3]
            selected_comp_no = int(self.display_tree.item(cur_item)['values'][1])
            selected_rank = self.display_tree.item(cur_item)['values'][2]
            values = (selected_comp_no,)
            my_cursor.execute(query, values)
            all_leave = my_cursor.fetchall()
            my_conn.close()

            leaveRecordWindow = Toplevel(self)
            leaveRecordWindow.geometry('300x300+200+200')
            leaveRecordWindow.title('LEAVE RECORD')
            leaveRecordWindow.resizable(False, False)
            leaveRecordWindow.focus_set()
            Label(leaveRecordWindow, text=str(selected_comp_no) + ', ' + selected_rank.upper() + " " +
                                          selected_name.upper(), bg='orange',
                  font=('Segoe UI', 10, 'bold'), relief='solid',
                  borderwidth=5).place(x=0, y=0, width=300)
            columns = ('Leave Date', 'Return Date', 'No of Days')

            leave_display_treeview = ttk.Treeview(leaveRecordWindow,
                                                  columns=columns)
            leave_display_treeview['show'] = 'headings'
            leave_display_treeview.column('Leave Date', width=20, anchor='c')
            leave_display_treeview.column('Return Date', width=20, anchor='c')
            leave_display_treeview.column('No of Days', width=20, anchor='c')
            leave_display_treeview.heading('Leave Date', text='Leave Date', anchor='c')
            leave_display_treeview.heading('Return Date', text='Return Date', anchor='c')
            leave_display_treeview.heading('No of Days', text='No of Days', anchor='c')
            scrl_y = ttk.Scrollbar(leaveRecordWindow, orient=VERTICAL)
            scrl_y.configure(command=leave_display_treeview.yview)
            scrl_y.place(x=280, y=30, width=20, height=240)
            for data in all_leave:
                leave_date = datetime.strptime(str(data[1]), "%Y-%m-%d")
                returning_day = datetime.strptime(str(data[2]), "%Y-%m-%d")
                days_in_date = returning_day - leave_date
                total_days = str(days_in_date.days + 1)
                leave_display_treeview.insert('', END, values=(data[1], data[2], total_days,))
            leave_display_treeview.place(x=0, y=30, width=280, height=240)

            def delete_leave(event):
                btn_delete_leave['state'] = NORMAL
                btn_delete_leave.configure(bg='ORANGE', fg='TEAL')

                def delete_data(e):
                    try:
                        item = leave_display_treeview.focus()
                        leaving_on = str(leave_display_treeview.item(item)['values'][0])
                        conn = self.connect_database()
                        cur = conn.cursor()
                        query_delete = f'''delete from {unit_leave_table} where
                                       ({unit_leave_table}.CompNo=%s and {unit_leave_table}.LeaveDate=%s)'''
                        cur.execute(query_delete, (selected_comp_no, leaving_on))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('DELETE SUCCESSFUL', 'Record Deleted', parent=self)
                    except Exception as exp:
                        messagebox.showerror('Error: ', f'{str(exp)}', parent=self)

                btn_delete_leave.bind('<ButtonRelease-1>', delete_data)

            btn_delete_leave = Button(leaveRecordWindow, text='Delete', font=font_text)
            btn_delete_leave.place(x=130, y=275)
            btn_delete_leave['state'] = DISABLED

            leave_display_treeview.bind('<<TreeviewSelect>>', delete_leave)

        frame_create_A_hajir = Frame(self, relief=RIDGE, borderwidth=5, bg='white')
        frame_create_A_hajir.place(x=0, y=490, width=127, height=130)

        btn_A_Hajir = Button(frame_create_A_hajir, width=11, fg='white', text='CREATE\n\'ADJ\' RECORD',
                             font=("times", 10, 'bold'), bg='teal', relief='raised',
                             command=self.a_hajir_window)
        btn_A_Hajir.pack(fill=BOTH, expand=True, padx=5, pady=5)

        btn_view_all_leave_record = Button(self.unit_data_frame, text="View All\nLeave Records",
                                           fg='white', font=font_text, anchor='center', bg="gray")
        btn_view_all_leave_record.pack(side=RIGHT, ipadx=5, ipady=5)
        btn_view_all_leave_record['state'] = DISABLED

        from authorization_window import AuthorizeWindow
        auth_window = AuthorizeWindow(self)

        btn_update_leave_record = Button(self.unit_data_frame, fg='white', bg='#660033',
                                         command=lambda: auth_window.authorize_user(self.user,
                                                                                    self.update_leave_record),
                                         text="Upload/Update \n Leave Record", font=font_text)
        btn_update_leave_record.pack(side=RIGHT, padx=5, after=btn_view_all_leave_record)

        btn_view_all_leave_record.bind('<ButtonRelease-1>', view_leave_record_of_a_person)

        if not (self.user.upper() == 'ADMIN' or self.user.upper() == 'SUPER USER'):
            btn_update_leave_record.pack_forget()

        scroll_x = ttk.Scrollbar(display_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(display_frame, orient=VERTICAL)
        tree_columns = ('unit', 'CompNo', 'Rnk', 'Name', 'LeaveDate', 'ReturnDate', 'LeaveStatus')
        self.display_tree = ttk.Treeview(display_frame,
                                         columns=tree_columns,
                                         xscrollcommand=scroll_x.set,
                                         yscrollcommand=scroll_y.set,
                                         height=2)

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_x.config(command=self.display_tree.xview)
        scroll_y.config(command=self.display_tree.yview)

        self.display_tree.heading('unit', text='Unit', anchor=CENTER,
                                  command=lambda: self.sort_tree(self.display_tree, "unit", False))
        self.display_tree.heading('CompNo', text='Comp No', anchor=CENTER,
                                  command=lambda: self.sort_tree(self.display_tree, "CompNo", False))
        self.display_tree.heading('Rnk', text='Rank', anchor=CENTER,
                                  command=lambda: self.sort_tree(self.display_tree, "Rnk", False))
        self.display_tree.heading('Name', text='Name', anchor=CENTER,
                                  command=lambda: self.sort_tree(self.display_tree, "Name", False))
        self.display_tree.heading('LeaveDate', text='Leave Date', anchor=CENTER,
                                  command=lambda: self.sort_tree(self.display_tree, "LeaveDate", False))
        self.display_tree.heading('ReturnDate', text='Return Date', anchor=CENTER,
                                  command=lambda: self.sort_tree(self.display_tree, "ReturnDate", False))
        self.display_tree.heading("LeaveStatus", text='Leave Days Status', anchor=CENTER,
                                  command=lambda: self.sort_tree(self.display_tree, "LeaveStatus", False))
        self.display_tree.place(x=0, y=0, width=self.window_width - 270, height=self.window_height - 230)
        # display_tree.bind("<ButtonRelease>", self.get_cursor)
        self.display_tree['show'] = 'headings'
        self.display_tree.column("unit", width=80, anchor='c')
        self.display_tree.column("CompNo", width=52, anchor='c')
        self.display_tree.column("Rnk", width=40, anchor='c')
        self.display_tree.column("Name", width=110, anchor='c')
        self.display_tree.column("LeaveDate", width=70, anchor='c')
        self.display_tree.column("ReturnDate", width=60, anchor='c')
        self.display_tree.column("LeaveStatus", width=60, anchor='c')
        self.display_data()

        def enable_buttons(event):
            scroll_no_of_days.configure(state=NORMAL)
            leave_start_date.configure(state=NORMAL)
            return_date.configure(state=NORMAL)
            btn_record_leave.configure(state=NORMAL)
            btn_view_all_leave_record['state'] = NORMAL
            btn_view_all_leave_record.configure(bg='#660033', fg="white")

        self.display_tree.bind('<<TreeviewSelect>>', enable_buttons)

        def add_data(event):
            cur_item = self.display_tree.focus()
            selected_comp_no = int(self.display_tree.item(cur_item)['values'][1])

            unit_table = self.convert_unit_name_into_table_name(self.unit_name.get())
            unit_leave_table = 'leave_record_' + unit_table

            query_to_add_data = f"""insert into {unit_leave_table}
                                (CompNo, LeaveDate, ReturnDate) VALUES (%s, %s, %s)"""
            values = (selected_comp_no, leave_start_date.get_date(), return_date.get_date(),)
            try:
                my_conn = self.connect_database()
                my_cursor = my_conn.cursor()
                my_cursor.execute(query_to_add_data, values)
                my_conn.commit()
                my_conn.close()
                messagebox.showinfo(title='Success', message='Leave Recorded')
                self.display_data()
            except Exception as ex:
                messagebox.showerror('Error: ', f'{str(ex)}', parent=self)

        btn_record_leave.bind('<ButtonRelease-1>', add_data)

    def update_leave_record(self):
        split_unit = self.unit_name.get().split(' ')
        combined_unit_text = split_unit[0].lower()
        for i in range(1, len(split_unit)):
            combined_unit_text += '_' + split_unit[i].lower()
        parent_unit_table = combined_unit_text
        unit_leave_record_table = 'leave_record_' + combined_unit_text
        import pandas as pd
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        conn = self.connect_database()
        cursor = conn.cursor()
        if file_path:
            df = pd.read_csv(file_path)
            rows_updated = 0
            if all(col in df.columns for col in ['CompNo', 'LeaveDate', 'ReturnDate']):
                # Iterate over DataFrame rows
                for index, row in df.iterrows():
                    # check if the CompNo is present in the parent table
                    comp_no = int(row['CompNo'])
                    date_format = "%Y-%m-%d"

                    try:
                        # leave_date = datetime.date(r)
                        from dateutil.parser import parse
                        leave_date_string = parse(row['LeaveDate'])
                        return_date_string = parse(row['ReturnDate'])
                        leave_date = leave_date_string.strftime(date_format)
                        return_date = return_date_string.strftime(date_format)

                        sql = f'''INSERT INTO {unit_leave_record_table} (CompNo, LeaveDate, ReturnDate)  
                                values ({comp_no}, '{leave_date}','{return_date}');'''
                        cursor.execute(sql)
                        conn.commit()
                        rows_updated += 1
                    except mysql.connector.Error as err:
                        continue
                if rows_updated > 0:
                    messagebox.showinfo("UPDATE SUCCESSFUL", f"{str(rows_updated)} rows have been updated")
                self.select_unit_info()

            else:
                messagebox.showerror("ERROR", "Table Doesn't match columns with CompNo, LeaveDate, ReturnDate")
            if rows_updated <= 0:
                messagebox.showwarning("WARNING", "No data to update")
        conn.close()

    def sort_tree(self, tree, column, descending):
        """sort tree contents when a column header is clicked on"""
        data = [(tree.set(child, column), child) for child in tree.get_children('')]
        # Replacing "Currently On Leave" string with -1 and other values to int
        for i in range(len(data)):
            if data[i][0] == "Currently on Leave":
                data[i] = (-1, data[i][1])
            elif data[i][0].isnumeric():
                data[i] = (int(float(data[i][0])), data[i][1])
        # now sort the data in place
        data.sort(key=lambda x: x[0], reverse=descending)
        for ix, item in enumerate(data):
            if data[ix][0] == -1:
                tree.set(data[ix][1], column, "Currently on Leave")
            else:
                tree.set(data[ix][1], column, str(data[ix][0]))
            tree.move(data[ix][1], '', ix)
        # switch the heading so that it will sort in the opposite direction
        tree.heading(column, command=lambda col=column: self.sort_tree(tree, col, int(not descending)))

    def connect_database(self):
        from CreateConnection import CreateConnection
        conn = CreateConnection(self._database)
        return conn.create_connection()

    def a_hajir_window(self):
        popup = Toplevel(self)
        popup.geometry(f'500x130+{int((self.window_width - 500) / 2)}+0')
        popup.title('ATTACHMENTS')
        popup.configure(bg='light blue')
        popup.resizable(False, False)
        Label(popup, font=('Haveltica', 10, 'bold'), fg='Purple', bg='light blue', width=10,
              text="Total Attach").grid(row=0, column=0, padx=5, pady=5)
        Label(popup, font=('Halvetica', 10, 'bold'), fg='Purple', bg='light blue', width=10,
              text="Leave").grid(row=0, column=1, padx=10, pady=5)
        Label(popup, font=('Halvetica', 10, 'bold'), fg='Purple', bg='light blue', width=10,
              text="Post").grid(row=0, column=2, padx=10, pady=5)
        Label(popup, font=('Halvetica', 10, 'bold'), fg='Purple', bg='light blue', width=10,
              text="AWOL").grid(row=0, column=3, padx=10, pady=5)

        combo_count = ttk.Combobox(popup, width=10, font=('Halvetica', 10), state='readonly')
        combo_count.grid(row=1, column=0, padx=5, pady=5)
        combo_count['values'] = tuple(range(0, 200))
        combo_count.current(0)
        combo_count.focus_set()

        combo_leave = ttk.Combobox(popup, width=10, font=('Halvetica', 10), state='readonly')
        combo_leave.grid(row=1, column=1, padx=5, pady=5)
        combo_leave['values'] = tuple(range(0, 200))
        combo_leave.current(0)

        combo_post = ttk.Combobox(popup, width=10, font=('Halvetica', 10), state='readonly')
        combo_post.grid(row=1, column=2, padx=5, pady=5)
        combo_post['values'] = tuple(range(0, 200))
        combo_post.current(0)

        combo_absent = ttk.Combobox(popup, width=10, font=('Halvetica', 10), state='readonly')
        combo_absent.grid(row=1, column=3, padx=5, pady=5)
        combo_absent['values'] = tuple(range(0, 200))
        combo_absent.current(0)

        def confirm_data():
            from a_hajir import AlphaHajirWindow
            try:
                total_count = combo_count.get()
                total_leave = combo_leave.get()
                total_post = combo_post.get()
                total_absent = combo_absent.get()

                dict_attach_data = {'total': int(total_count), 'leave': int(total_leave),
                                    'post': int(total_post), 'absent': int(total_absent)}
                popup.destroy()
                AlphaHajirWindow(self, dict_attach_data)

            except ValueError:
                Label(popup, font=('Halvetica', 10, 'bold'),
                      text="Incorrect Data", bg='red').pack(fill=X, expand=True, anchor='center')

        btn_confirm = Button(popup, text='Confirm', bg='White', fg='Black',
                             font=('Halvetica', 10, 'bold'), width=10, command=confirm_data)
        btn_confirm.grid(row=2, column=0, padx=5, pady=5)

    @staticmethod
    def convert_unit_name_into_table_name(unit_name):
        split_unit_name = unit_name.split(' ')
        combined_unit_table_name = split_unit_name[0].lower()
        for i in range(1, len(split_unit_name)):
            combined_unit_table_name += '_' + split_unit_name[i].lower()
        return combined_unit_table_name

    def display_data(self):
        my_conn = self.connect_database()
        my_cursor = my_conn.cursor()
        text_unit_name = self.unit_name.get()

        unit_table = self.convert_unit_name_into_table_name(text_unit_name)
        unit_leave_table = 'leave_record_' + unit_table
        my_cursor.execute(f'''select {unit_table}.Unit,
                          {unit_table}.CompNo, {unit_table}.Rnk,
                          {unit_table}.Name, max({unit_leave_table}.LeaveDate),
                          max({unit_leave_table}.ReturnDate) from {unit_leave_table} INNER 
                          Join 
                          {unit_table} on {unit_table}.CompNo={unit_leave_table}.CompNo 
                          group by {unit_leave_table}.CompNo order by 
                          {unit_leave_table}.CompNo'''
                          )
        # Table design
        data_phone_details = my_cursor.fetchall()
        self.display_tree.tag_configure('On Leave', background='#90EE90')
        self.display_tree.tag_configure('Working for long', background='white')
        self.display_tree.tag_configure('Recently Came', background='#fff4c2')

        if len(data_phone_details) != 0:

            self.display_tree.delete(*self.display_tree.get_children())
            # my_cursor.execute(f'''select * from {unit_leave_table} where ''')
            no_of_people_on_leave = 0
            no_of_people_working_for_long = 0
            for data in data_phone_details:
                if type(data[5]) != str:
                    return_date = str(data[5])
                else:
                    return_date = data[5]
                returning_day = datetime.strptime(return_date, '%Y-%m-%d')
                today = datetime.today()
                leave_status = today - returning_day
                leave_status_days = str(leave_status.days)
                if 0 <= int(leave_status_days) < 90:
                    my_tag = 'Recently Came'
                elif int(leave_status_days) >= 90:
                    my_tag = 'Working for long'
                    no_of_people_working_for_long += 1
                elif int(leave_status_days) < 0:
                    my_tag = 'On Leave'
                    no_of_people_on_leave += 1
                    print(leave_status_days)
                if int(leave_status_days) < 0:
                    leave_status_days = 'Currently on Leave'
                self.display_tree.insert("", END, values=(
                    data[0], data[1], data[2], data[3].title(), data[4], data[5], leave_status_days),
                                         tags=(my_tag,))
            per_on_leave = round(no_of_people_on_leave / len(data_phone_details) * 100, 2)
            # text_per_on_leave = 'On Leave: ' + str(no_of_people_on_leave) + \
            #                     '(' + str(per_on_leave) + '%)'

            # label_per_on_leave = Label(self, text=text_per_on_leave, font=('Seoge UI', 10, 'bold'),
            #                            fg='white', bg='#660033', width=18)
            # label_per_on_leave.place(x=self.window_width - 270,
            #                          y=self.window_height - 123)

            # label_long = Label(self, text='More than 3 Months: ' + str(no_of_people_working_for_long),
            #                    font=('Seoge UI', 10, 'bold'), fg='white', bg='#660033', width=20)
            # label_long.place(x=self.window_width - 445,
            #                  y=self.window_height - 123)
            # my_conn.commit()
        my_conn.close()
