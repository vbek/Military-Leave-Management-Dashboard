import mysql.connector
from tkinter import Entry, Tk, Label, Frame, PhotoImage, Button, messagebox, TclError, Toplevel, RAISED


class LoginPage:
    def __init__(self, window):
        self.parent_window = window
        self.parent_window.withdraw()
        self.login_window = Toplevel(self.parent_window)
        self.login_window.resizable(False, False)
        self.login_window.protocol("WM_DELETE_WINDOW", lambda: self.parent_window.destroy())
        self.desired_location_y = int()
        self.desired_location_x = int()
        self.desired_height = int()
        self.desired_width = int()
        self.host = 'localhost'
        self.user = 'root'
        self.database = 'bibekdb'
        self.port = '3306'
        self.password = '12Bibek!@'
        self.admin_password = ''
        self.login_frame = Frame(self.login_window, bg='white')
        self.t_frame = Frame(self.login_frame, bg='white')
        self.username_entry = Entry(self.t_frame, foreground='grey', bg="white", border=0)
        self.password_entry = Entry(self.t_frame, foreground='grey', bg="white", border=0)
        self.set_window()

    def data_connection(self):
        my_con = mysql.connector.connect(host=self.host, user=self.user, database=self.database,
                                         port=self.port, password=self.password)
        return my_con

    def read_data(self):
        login_data_conn = self.data_connection()
        my_cursor = login_data_conn.cursor()
        my_cursor.execute("""select * from login_details""")
        datas = my_cursor.fetchall()
        login_data_conn.close()

        data_dict = dict(datas)
        return data_dict

    def sign_in_attempt(self):
        data_dict = self.read_data()
        user_input_username = self.username_entry.get()
        user_input_password = self.password_entry.get()
        if user_input_username.lower() in data_dict:
            if user_input_password == '':
                messagebox.showwarning('Warning', 'Please type in password')
            else:
                if user_input_password in data_dict[user_input_username.lower()]:
                    self.show_success()


                else:
                    messagebox.showerror("Error", "Username/Password incorrect")
        else:
            messagebox.showerror("Error", "Username/Password incorrect")

    def show_success(self):
        time_to_wait = 100  # in milliseconds

        try:
            self.login_window.after(time_to_wait, self.login_window.destroy)
            from search_user_data import DisplayUser
            DisplayUser(self.parent_window, self.username_entry.get())
        except TclError:
            pass

    def sign_up_attempt(self):
        admin_authentication_window_width = 200
        admin_authentication_window_height = 100
        admin_authentication_window = Toplevel(self.login_window)
        admin_authentication_window.title("AUTH")
        admin_authentication_window.geometry('{}x{}+{}+{}'.format(admin_authentication_window_width,
                                                                  admin_authentication_window_height,
                                                                  int(self.desired_location_x) + int(
                                                                      (self.desired_width - 200) / 2),
                                                                  int(self.desired_location_y) + int(
                                                                      (self.desired_height - 200) / 2)))
        Label(admin_authentication_window, text="Enter admin Password",
              font=('Microsoft YaHei UI Light', 10), anchor='w').place(x=30, y=5)
        entry_password = Entry(admin_authentication_window, width=15, show='*')
        entry_password.place(x=50, y=55, anchor="w")
        entry_password.focus_set()

        data_dict = self.read_data()
        if 'admin' in data_dict:
            self.admin_password = data_dict['admin']
        else:
            self.admin_password = 'admin'

        def authorize_administration(event):
            if entry_password.get() == self.admin_password:
                admin_authentication_window.destroy()
                self.login_window.destroy()
                SignUp(self.parent_window)

            else:
                Label(admin_authentication_window,
                      text='Incorrect', font=('Microsoft YaHei UI Light', 10), fg='RED').place(x=115, y=70)

        btn_auth = Button(admin_authentication_window, relief=RAISED, text='Ok')
        btn_auth.place(x=85, y=70)
        btn_auth.bind('<ButtonRelease-1>', authorize_administration)

    def set_window(self):
        self.login_window.title("LOGIN PAGE")
        self.login_window.config(background='white')
        screen_width = self.parent_window.winfo_screenwidth()
        screen_height = self.parent_window.winfo_screenheight()
        self.desired_width = 300
        self.desired_height = 500
        self.desired_location_x = int(screen_width / 2 - self.desired_width / 2)
        self.desired_location_y = int(screen_height / 2 - self.desired_height / 2 - 50)

        self.login_window.geometry(
            "{}x{}+{}+{}".format(self.desired_width, self.desired_height, self.desired_location_x,
                                 self.desired_location_y))
        self.login_frame.config(width=self.desired_width, height=self.desired_height)
        self.login_frame.place(x=0, y=0)

        # ************************************** Title Frame ********************************************
        self.t_frame.place(x=0, y=0, width=self.desired_width, height=self.desired_height)
        Label(self.t_frame, text="LOG IN", font=('Microsoft YaHei UI Light', 23), bg="White",
              fg='#2596be').place(x=0, y=0, width=self.desired_width, height=70)

        # ***************************** Username ****************************************
        def clear_username_on_focus(event):
            username_text = self.username_entry.get()
            if username_text == '' or username_text.capitalize() == 'Username':
                self.username_entry.delete(0, "end")
                self.username_entry.config(fg='black')

        def refill_username_if_no_entry_focus_out(event):
            username_text = self.username_entry.get()
            if username_text == '':
                self.username_entry.config(fg='grey')
                self.username_entry.insert(0, 'Username')
            elif username_text.capitalize() == 'Username':
                messagebox.showwarning('Warning', 'Please enter another Username')
                self.username_entry.config(fg='grey')
                self.username_entry.delete(0, "end")
                self.username_entry.insert(0, 'Username')
            else:
                pass
        self.username_entry.focus_set()
        self.username_entry.place(x=25, y=100, width=self.desired_width - 50, height=20)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind('<FocusIn>', clear_username_on_focus)
        self.username_entry.bind('<FocusOut>', refill_username_if_no_entry_focus_out)
        Frame(self.t_frame, background='black').place(x=25, y=120, width=self.desired_width - 50, height=1)

        # ***************************** Password ****************************************

        def clear_password_focus_in(event):
            password_text = self.password_entry.get()
            if password_text == '' or password_text.capitalize() == 'Password':
                self.password_entry.delete(0, "end")
                self.password_entry.config(show='*')
                self.password_entry.config(fg='black')

        def refill_password_focus_out(event):
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
            else:
                pass

        self.password_entry.place(x=25, y=150, width=self.desired_width - 50, height=20)
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', clear_password_focus_in)
        for entry in [self.password_entry]:
            self.password_entry.bind('<FocusOut>', refill_password_focus_out)
        Frame(self.t_frame, background='black').place(x=25, y=170, width=self.desired_width - 50, height=1)

        # ********************************** Login Button ****************************

        icon_photo_button = PhotoImage(file="res/loginlogo.png")
        icon_photo_button = icon_photo_button.subsample(4, 4)
        btn_login = Button(self.t_frame, text="Login", background="white", command=self.sign_in_attempt,
                           image=icon_photo_button, border=0)
        btn_login.image = icon_photo_button
        btn_login.place(x=self.desired_width / 2 - 75, y=190)

        Label(self.t_frame, text="Don't have an account?", font=('Microsoft YaHei UI Light', 9), fg="black",
              bg='white').place(x=25, y=270)
        sign_up_button = Button(self.t_frame, text="Sign Up", font=('Microsoft YaHei UI Light', 9),
                                border=0, bg='white', command=self.sign_up_attempt, fg='#2596be', cursor='hand2',
                                width=6)
        sign_up_button.place(x=170, y=270)

        self.login_window.mainloop()


class SignUp:
    def __init__(self, login_window):
        self.parent_window = login_window
        self.sign_up_window = Toplevel(login_window)
        self.sign_up_window.resizable(False, False)
        self.sign_up_window.protocol("WM_DELETE_WINDOW", lambda: self.parent_window.destroy())
        self.desired_location_y = int()
        self.desired_location_x = int()
        self.desired_height = int()
        self.desired_width = int()
        self.host = 'localhost'
        self.user = 'root'
        self.database = 'bibekdb'
        self.port = '3306'
        self.password = '12Bibek!@'
        self.admin_password = ''
        self.sign_up_frame = Frame(self.sign_up_window, bg='white')
        self.t_frame = Frame(self.sign_up_frame, bg='white')
        self.username_entry = Entry(self.t_frame, foreground='grey', bg="white", border=0)
        self.password_entry = Entry(self.t_frame, foreground='grey', bg="white", border=0)
        self.confirm_password_entry = Entry(self.t_frame, foreground='grey', bg='white', border=0)
        self.set_window()

    def data_connection(self):
        my_con = mysql.connector.connect(host=self.host, user=self.user, database=self.database,
                                         port=self.port, password=self.password)
        return my_con

    def set_window(self):
        self.sign_up_window.title("SIGN UP PAGE")
        self.sign_up_window.config(background='white')
        screen_width = self.parent_window.winfo_screenwidth()
        screen_height = self.parent_window.winfo_screenheight()
        self.desired_width = 300
        self.desired_height = 500
        self.desired_location_x = int(screen_width / 2 - self.desired_width / 2)
        self.desired_location_y = int(screen_height / 2 - self.desired_height / 2 - 50)
        self.sign_up_window.geometry(
            "{}x{}+{}+{}".format(self.desired_width, self.desired_height, self.desired_location_x,
                                 self.desired_location_y))
        self.sign_up_frame.config(width=self.desired_width, height=self.desired_height)
        self.sign_up_frame.place(x=0, y=0)

        # ************************************** Title Frame ********************************************
        self.t_frame.place(x=0, y=0, width=self.desired_width, height=self.desired_height)
        Label(self.t_frame, text="SIGN UP", font=('Microsoft YaHei UI Light', 23), bg="White",
              fg='#2596be').place(x=0, y=0, width=self.desired_width, height=70)

        # ***************************** Username ****************************************
        def clear_username_on_focus(event):
            username_text = self.username_entry.get()
            if username_text == '' or username_text.capitalize() == 'Username':
                self.username_entry.delete(0, "end")
                self.username_entry.config(fg='black')

        def refill_username_if_no_entry_focus_out(event):
            username_text = self.username_entry.get()
            if username_text == '':
                self.username_entry.config(fg='grey')
                self.username_entry.insert(0, 'Username')
            elif username_text.capitalize() == 'Username':
                messagebox.showwarning('Warning', 'Please enter another Username')
                self.username_entry.config(fg='grey')
                self.username_entry.delete(0, "end")
                self.username_entry.insert(0, 'Username')
            else:
                pass

        self.username_entry.place(x=25, y=100, width=self.desired_width - 50, height=20)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind('<FocusIn>', clear_username_on_focus)
        self.username_entry.bind('<FocusOut>', refill_username_if_no_entry_focus_out)
        Frame(self.t_frame, background='black').place(x=25, y=120, width=self.desired_width - 50, height=1)

        # ***************************** Password ****************************************
        def clear_password_focus_in(event):
            password_text = self.password_entry.get()
            if password_text == '' or password_text.capitalize() == 'Password':
                self.password_entry.delete(0, "end")
                self.password_entry.config(show='*')
                self.password_entry.config(fg='black')

        def refill_password_focus_out(event):
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
            else:
                pass

        self.password_entry.place(x=25, y=170, width=self.desired_width - 50, height=20)
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', clear_password_focus_in)
        self.password_entry.bind('<FocusOut>', refill_password_focus_out)
        Frame(self.t_frame, background='black').place(x=25, y=190, width=self.desired_width - 50, height=1)

        # ************************************* Confirm Password *****************************************

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
            else:
                pass

        self.confirm_password_entry.place(x=25, y=240, width=self.desired_width - 50, height=20)
        self.confirm_password_entry.insert(0, 'Confirm Password')
        self.confirm_password_entry.bind('<FocusIn>', clear_confirm_password_focus_in)
        self.confirm_password_entry.bind('<FocusOut>', refill_confirm_password_focus_out)
        Frame(self.t_frame, background='black').place(x=25, y=260, width=self.desired_width - 50, height=1)

        # ********************************** Sign Up Button ****************************

        icon_photo_button = PhotoImage(file="res/signup.png")
        icon_photo_button = icon_photo_button.subsample(5, 5)
        btn_sign_up = Button(self.t_frame, text="Sign Up", background="white", command=self.create_user,
                             image=icon_photo_button, border=0)
        btn_sign_up.image = icon_photo_button
        btn_sign_up.place(x=self.desired_width / 2 - 65, y=300)

        Label(self.t_frame, text="Already have an account?", font=('Microsoft YaHei UI Light', 9), fg="black",
              bg='white').place(x=25, y=380)
        btn_login = Button(self.t_frame, text="Log In", font=('Microsoft YaHei UI Light', 9), command=self.login_attempt,
                           border=0, bg='white', fg='#2596be', cursor='hand2',
                           width=6)
        btn_login.place(x=170, y=380)
        self.sign_up_window.mainloop()

    def login_attempt(self):
        self.sign_up_window.destroy()
        LoginPage(self.parent_window)


    def create_user(self):
        sign_up_conn = self.data_connection()
        my_cursor = sign_up_conn.cursor()
        insert_user_query = 'insert into login_details values(%s, %s)'
        get_column_query = 'select username from login_details'
        username_text = self.username_entry.get()
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
                values = (username_text.lower(), password_text)
                my_cursor.execute(insert_user_query, values)
                sign_up_conn.commit()
                sign_up_conn.close()
                messagebox.showinfo('SUCCESS', 'User Added Successfully')
                self.login_attempt()



