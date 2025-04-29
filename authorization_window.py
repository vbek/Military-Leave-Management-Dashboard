from tkinter import Toplevel, Label, Entry, Button, RAISED


class AuthorizeWindow:
    def __init__(self, window):
        self.window = window

    def authorize_user(self, user, function_to_call):
        user = user if user.upper() == 'ADMIN' or user.upper() == "SUPER USER" else 'ADMIN'
        admin_authentication_window_width = 200
        admin_authentication_window_height = 100
        admin_authentication_window = Toplevel(self.window)
        admin_authentication_window.title("AUTH")
        admin_authentication_window.configure(bg='light blue')
        admin_authentication_window.geometry('{}x{}+{}+{}'.format(admin_authentication_window_width,
                                                                  admin_authentication_window_height,
                                                                  int(self.window.winfo_screenwidth() / 2), 0))
        Label(admin_authentication_window, text="Enter admin Password",
              font=('Microsoft YaHei UI Light', 10), anchor='w', bg='light blue').place(x=30, y=5)
        entry_password = Entry(admin_authentication_window, width=15, show='*')
        entry_password.place(x=50, y=55, anchor="w")
        entry_password.focus_set()

        from CreateConnection import CreateConnection
        conn = CreateConnection(database_name='bibekdb')
        data_dict = dict(conn.get_data_from_table('login_details'))
        if user.upper() in data_dict.keys():
            user_acc_password = data_dict[user.upper()]
        else:
            user_acc_password = ''

        def authorize_administration(event):
            if entry_password.get() == user_acc_password:
                admin_authentication_window.destroy()
                function_to_call()

            else:
                Label(admin_authentication_window,
                      text='Incorrect', font=('Microsoft YaHei UI Light', 10), fg='RED',
                      bg='light blue').place(x=115, y=70)

        btn_auth = Button(admin_authentication_window, relief=RAISED, text='Ok')
        btn_auth.place(x=85, y=70)
        btn_auth.bind('<ButtonRelease-1>', authorize_administration)
        admin_authentication_window.bind('<Return>', authorize_administration)
