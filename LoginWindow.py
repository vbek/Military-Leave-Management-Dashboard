import os
from tkinter import Tk, Entry, Label, Frame, PhotoImage, Button, messagebox, TclError, Toplevel, RAISED


class Layout(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.top_frame = Frame()
        self.lbl_title = Label()
        self.username_entry = Entry()
        self.password_entry = Entry()
        self.desired_location_x = int((self.winfo_screenwidth() - 300) / 2)
        self.create_base_widget()

    def create_base_widget(self):
        desired_width = 300
        desired_height = 500
        self.geometry('300x500+{}+{}'.format(self.desired_location_x, 0))
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

        font = ('Microsoft YaHei UI Light', 23)

        main_frame = Frame(self, bg='white')
        main_frame.place(x=0, y=0)

        self.top_frame = Frame(self, bg='white')
        self.top_frame.place(x=0, y=0, width=desired_width, height=desired_height)

        self.lbl_title = Label(self.top_frame, text="TITLE", font=font, bg="White",
                               fg='#2596be')
        self.lbl_title.place(x=0, y=0, width=desired_width, height=70)

        self.username_entry = Entry(self.top_frame, foreground='grey', bg="white", border=0)
        self.username_entry.place(x=25, y=100, width=desired_width - 50, height=20)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind('<FocusIn>', self.__clear_username_focus_in)
        self.username_entry.bind('<FocusOut>', self.__refill_username_focus_out)

        Frame(self.top_frame, background='black').place(x=25, y=120, width=desired_width - 50, height=1)

        self.password_entry = Entry(self.top_frame, foreground='grey', bg="white", border=0)
        self.password_entry.place(x=25, y=150, width=desired_width - 50, height=20)
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', self.__clear_password_focus_in)
        self.password_entry.bind('<FocusOut>', self.__refill_password_focus_out)

        Frame(self.top_frame, background='black').place(x=25, y=170, width=desired_width - 50, height=1)

    def __clear_username_focus_in(self, event):
        username_text = self.username_entry.get()
        if username_text == '' or username_text.capitalize() == 'Username':
            self.username_entry.delete(0, "end")
            self.username_entry.config(fg='black')

    def __refill_username_focus_out(self, event):
        username_text = self.username_entry.get()
        if username_text == '':
            self.username_entry.config(fg='grey')
            self.username_entry.insert(0, 'Username')
        elif username_text.capitalize() == 'Username':
            messagebox.showwarning('Warning', 'Please enter another Username')
            self.username_entry.config(fg='grey')
            self.username_entry.delete(0, "end")
            self.username_entry.insert(0, 'Username')

    def __clear_password_focus_in(self, event):
        password_text = self.password_entry.get()
        if password_text == '' or password_text.capitalize() == 'Password':
            self.password_entry.delete(0, "end")
            self.password_entry.config(show='*')
            self.password_entry.config(fg='black')

    def __refill_password_focus_out(self, event):
        password_text = self.password_entry.get()
        if password_text == '':
            self.password_entry.insert(0, 'Password')
            self.password_entry.config(fg='grey')
            self.password_entry.config(show='')
        elif password_text.capitalize() == 'Password':
            messagebox.showwarning('Warning', 'Please enter strong password')
            self.password_entry.delete(0, 'end')
            self.password_entry.insert(0, 'Password')
            self.password_entry.config(fg='grey')
            self.password_entry.config(show='')


class LoginPage(Layout):
    def __init__(self):
        Layout.__init__(self)
        self.bind('<Return>', self.sign_in_attempt)
        self.modify_widget_content()
        self.create_login_page_widget()
        self.focus_force()
        self.mainloop()

    def modify_widget_content(self):
        self.title("LOGIN PAGE")
        self.lbl_title.configure(text="LOGIN")

    def create_login_page_widget(self):
        self.username_entry.focus_set()
        filepath = os.path.join(os.path.dirname(__file__), "res", "loginlogo.png")
        icon_photo_button = PhotoImage(file=filepath)
        icon_photo_button = icon_photo_button.subsample(4, 4)
        btn_login = Button(self.top_frame, background="white",
                           image=icon_photo_button, border=0, command=self.sign_in_attempt)
        btn_login.image = icon_photo_button
        btn_login.place(x=300 / 2 - 75, y=190)

        Label(self.top_frame, text="Don't have an account?", font=('Microsoft YaHei UI Light', 9),
              fg="black", bg='white').place(x=25, y=290)
        redirect_sign_up_button = Button(self.top_frame, text="Sign Up",
                                         font=('Microsoft YaHei UI Light', 9),
                                         border=0, bg='white', command=self.sign_up_attempt,
                                         fg='#2596be', cursor='hand2', width=6)
        redirect_sign_up_button.place(x=170, y=290)

        Label(self.top_frame, text="Change User Password?", font=('Microsoft YaHei UI Light', 9),
              fg="black", bg='white').place(x=25, y=270)

        btn_change_password = Button(self.top_frame, text="Change",
                                     font=('Microsoft YaHei UI Light', 9),
                                     border=0, bg='white', command=self.change_password,
                                     fg='#2596be', cursor='hand2', width=10, anchor='w')
        btn_change_password.place(x=170, y=270)
    #
    #     btn_create_connection = Button(self.top_frame, text='Test Connection', command=self.check_connection)
    #     btn_create_connection.place(x=90, y=350)
    #
    # def check_connection(self):
    #     from CreateConnection import CreateConnection
    #     db = CreateConnection('bibekdb')
    #     conn = db.create_connection()
    #     lbl_test_connection = Label(self.top_frame,
    #                                 fg='red', font=('Times', 10, 'bold'), bg='white')
    #     lbl_test_connection.place(x=80, y=390)
    #     if conn:
    #         lbl_test_connection.configure(text='Connection Successful', fg='GREEN')
    #     else:
    #         lbl_test_connection.configure(text='Couldn\'t Connect to database', fg='red')

    def change_password(self):
        window = Toplevel(self)
        window.title("Change Password")
        window.configure(bg='light blue')
        window.focus_set()
        window.geometry("250x120+{}+{}".format(int(self.winfo_screenwidth() / 2 - 150), 0))
        font = ('Microsoft YaHei UI Light', 10, 'bold')
        lbl_username = Label(window, text="Username: ", width=12, font=font, bg='light blue')
        lbl_username.grid(row=0, column=0, padx=5)

        entry_username = Entry(window, relief='solid', width=15)
        entry_username.grid(row=0, column=1, padx=5)

        lbl_old_password = Label(window, text="Old Password: ", width=12, font=font, bg='light blue')
        lbl_old_password.grid(row=1, column=0, padx=5)

        entry_old_password = Entry(window, relief='solid', width=15)
        entry_old_password.grid(row=1, column=1, padx=5)

        lbl_new_password = Label(window, text="New Password: ", width=12, font=font, bg='light blue')
        lbl_new_password.grid(row=2, column=0, padx=5)

        entry_new_password = Entry(window, relief='solid', width=15)
        entry_new_password.grid(row=2, column=1, padx=5)

        def authenticate(event):
            text_username = entry_username.get().upper()
            text_old_password = entry_old_password.get()
            text_new_password = entry_new_password.get()
            lbl_error = Label(window, text='', font=('Times', 8, 'bold'), fg='RED', anchor='w', bg='light blue')
            lbl_error.grid(row=3, column=1)

            if text_username == '' or text_old_password == '' or text_new_password == '':
                lbl_error.configure(text="Enter All Data")
            else:
                lbl_error.configure(text='')
                from CreateConnection import CreateConnection
                db = CreateConnection('bibekdb')
                conn = db.create_connection()
                cur = conn.cursor()
                query_username_exists = '''Select * from login_details where username=%s'''
                value_username_exists = (text_username,)
                cur.execute(query_username_exists, value_username_exists)
                data = cur.fetchone()
                if data:
                    if data[1] == text_old_password:
                        query_to_update_password = '''UPDATE login_details 
                                                        SET
                                                        password=%s
                                                        WHERE username = %s;'''

                        values_to_update_password = (text_new_password, text_username,)
                        cur.execute(query_to_update_password, values_to_update_password)
                        conn.commit()
                        messagebox.showinfo("Success", "Password updated")
                        window.destroy()
                        cur.close()
                        conn.close()
                    else:
                        lbl_error.configure(text="Old Password \n Wrong")
                else:
                    messagebox.showwarning("Warning", "User doesn\'t exists!!!\n Please Create User")

        btn_confirm_change = Button(window, text='Confirm', width=12, font=font)
        btn_confirm_change.grid(row=3, column=0, padx=5, pady=5)
        btn_confirm_change.bind('<ButtonRelease>', authenticate)
        window.bind('<Return>', authenticate)

    def sign_in_attempt(self, event=None):
        from CreateConnection import CreateConnection
        conn = CreateConnection(database_name='bibekdb')
        data_dict = dict(conn.get_data_from_table('login_details'))
        user_input_username = self.username_entry.get()
        user_input_password = self.password_entry.get()
        if user_input_username.upper() in data_dict.keys():
            if user_input_password == '':
                messagebox.showwarning('Warning', 'Please type in password')
            else:
                if user_input_password in data_dict.values():
                    Label(self, text="Loading.....", font=('Helvetica', 16, "bold"),
                          bg='WHITE', fg='#F2AA4C').place(x=90, y=370)
                    self.update()
                    self.show_success()
                else:
                    messagebox.showerror("Error", "Username/Password incorrect")
        else:
            messagebox.showerror("Error", "Username/Password incorrect")

    def show_success(self):
        try:
            from BaseWindow import Employee
            # self.parent_window.deiconify()
            Employee(self, self.username_entry.get())


        except TclError as tcl:
            messagebox.showerror("Error", tcl)

    def sign_up_attempt(self):
        admin_authentication_window_width = 200
        admin_authentication_window_height = 100
        admin_authentication_window = Toplevel(self)
        admin_authentication_window.title("AUTH")
        admin_authentication_window.configure(bg='light blue')
        admin_authentication_window.geometry('{}x{}+{}+{}'.format(admin_authentication_window_width,
                                                                  admin_authentication_window_height,
                                                                  self.desired_location_x, 0))
        Label(admin_authentication_window, text="Enter admin Password",
              font=('Microsoft YaHei UI Light', 10), anchor='w', bg='light blue').place(x=30, y=5)
        entry_password = Entry(admin_authentication_window, width=15, show='*')
        entry_password.place(x=50, y=55, anchor="w")
        entry_password.focus_set()

        from CreateConnection import CreateConnection
        conn = CreateConnection(database_name='bibekdb')
        data_dict = dict(conn.get_data_from_table('login_details'))
        if 'ADMIN' in data_dict.keys():
            admin_password = data_dict['ADMIN']
        else:
            admin_password = 'admin'

        def authorize_administration(event):
            if entry_password.get() == admin_password:
                admin_authentication_window.destroy()
                self.destroy()
                Signup()

            else:
                Label(admin_authentication_window,
                      text='Incorrect', font=('Microsoft YaHei UI Light', 10),
                      fg='RED', bg='light blue').place(x=115, y=70)

        btn_auth = Button(admin_authentication_window, relief=RAISED, text='Ok')
        btn_auth.place(x=85, y=70)
        btn_auth.bind('<ButtonRelease-1>', authorize_administration)
        admin_authentication_window.bind('<Return>', authorize_administration)


class Signup(Layout):
    def __init__(self):
        Layout.__init__(self)
        self.title('SIGN UP PAGE')
        self.confirm_password_entry = Entry()
        self.lbl_title.configure(text='SIGN UP')
        self.bind('<Return>', self.create_user)
        self.create_sign_up_widget()
        self.mainloop()

    def create_sign_up_widget(self):
        self.username_entry.focus_force()

        def clear_confirm_password_focus_in(event):
            confirm_password_text = self.confirm_password_entry.get()
            if confirm_password_text == '' or confirm_password_text.capitalize() == 'Confirm password':
                self.confirm_password_entry.delete(0, "end")
                self.confirm_password_entry.config(show='*')
                self.confirm_password_entry.config(fg='black')

        def refill_confirm_password_focus_out(event):
            confirm_password_text = self.confirm_password_entry.get()
            if confirm_password_text == '':
                self.confirm_password_entry.insert(0, 'Confirm Password')
                self.confirm_password_entry.config(fg='grey')
                self.confirm_password_entry.config(show='')
            elif confirm_password_text.capitalize() == 'Confirm Password':
                self.confirm_password_entry.delete(0, 'end')
                self.confirm_password_entry.insert(0, 'Confirm Password')
                self.confirm_password_entry.config(fg='grey')
                self.confirm_password_entry.config(show='')

        self.confirm_password_entry = Entry(self.top_frame, foreground='grey', bg='white', border=0)
        self.confirm_password_entry.place(x=25, y=200, width=300 - 50, height=20)
        self.confirm_password_entry.insert(0, 'Confirm Password')
        self.confirm_password_entry.bind('<FocusIn>', clear_confirm_password_focus_in)
        self.confirm_password_entry.bind('<FocusOut>', refill_confirm_password_focus_out)

        Frame(self.top_frame, background='black').place(x=25, y=220, width=300 - 50, height=1)
        filepathSignUp = os.path.join(os.path.dirname(__file__), "res", "signup.png")
        icon_photo_button = PhotoImage(file=filepathSignUp)
        icon_photo_button = icon_photo_button.subsample(5, 5)
        btn_sign_up = Button(self.top_frame, text="Sign Up", background="white",
                             command=self.create_user,
                             image=icon_photo_button, border=0)
        btn_sign_up.image = icon_photo_button
        btn_sign_up.place(x=300 / 2 - 65, y=250)

        Label(self.top_frame, text="Already have an account?", font=('Microsoft YaHei UI Light', 9),
              fg="black", bg='white').place(x=25, y=330)
        btn_login = Button(self.top_frame, text="Log In", font=('Microsoft YaHei UI Light', 9),
                           command=self.redirect_login_page, border=0, bg='white', fg='#2596be',
                           cursor='hand2', width=6)
        btn_login.place(x=170, y=330)

    def redirect_login_page(self):
        self.destroy()
        LoginPage()

    def create_user(self, event=None):
        from CreateConnection import CreateConnection
        sign_up_conn = CreateConnection(database_name='bibekdb')
        my_conn = sign_up_conn.create_connection()
        my_cursor = my_conn.cursor()
        insert_user_query = 'insert into login_details values(%s, %s)'
        get_column_query = 'select username from login_details'
        username_text = self.username_entry.get().upper()
        password_text = self.password_entry.get()
        confirm_password_text = self.confirm_password_entry.get()
        if username_text.lower() == 'admin':
            messagebox.showwarning("Warning", "Can\'t create Admin account")
        elif username_text == 'Username' or password_text == 'Password' or confirm_password_text == "Confirm Password":
            messagebox.showwarning("Warning", "Please enter Username/Password")
        elif password_text != confirm_password_text:
            messagebox.showerror("Could\'t Create Account", 'Password doesn\'t match')
        else:
            my_cursor.execute(get_column_query)
            usernames = my_cursor.fetchall()
            if (username_text,) in usernames:
                messagebox.showwarning("Error", "User Exists. Login instead!!!")
            else:
                values = (username_text.upper(), password_text)
                my_cursor.execute(insert_user_query, values)
                my_conn.commit()
                my_conn.close()
                messagebox.showinfo('SUCCESS', 'User Added Successfully')
                self.redirect_login_page()
