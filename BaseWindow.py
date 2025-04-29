import os.path
from tkinter import Tk, Label, Button, PhotoImage, Frame, filedialog, Toplevel, GROOVE, Text, messagebox
import HomeWindow as hW
import addwindow as aw
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from analytics_windows import show_analytics

class Employee(Tk):
    def __init__(self, window, user):
        self.window = window
        self.window.destroy()
        self.cons = 1
        super().__init__()

        self.unit_name_list = self.get_all_tables_name()
        # unit_name = ('Kalidal Bn(E)', 'Kaliprasad Bn(E)')
        self.sorted_unit_name = list(sorted(self.unit_name_list))
        #  **************************************** Window Title  **************************************** #
        self._holding_frame = None
        self.user = user
        self.dict_data = dict()
        self._frame = None
        self.window_width = self.winfo_screenwidth()
        self.window_height = self.winfo_screenheight()

        self.set_main_screen_window()
        self.mainloop()

    def get_all_tables_name(self):
        self.cons = 2
        from CreateConnection import CreateConnection
        obj_cc = CreateConnection(database_name='bibekdb')
        conn = obj_cc.create_connection()
        cursor = conn.cursor()
        cursor.execute('''show tables in bibekdb where Tables_in_bibekdb not IN 
                        ('login_details', 'quote_list_log', 'attached_troops') and
                        Tables_in_bibekdb not Like '%leave_record%';''')
        all_tables = cursor.fetchall()
        final_tables_name = list()
        for table_name in all_tables:
            temp_tables_name = str(table_name[0]).split('_')
            add_string = temp_tables_name[0].upper()
            for i in range(1, len(temp_tables_name)):
                add_string += ' ' + temp_tables_name[i].upper()
            final_tables_name.append(add_string)
        return tuple(final_tables_name)

    def set_main_screen_window(self):
        self.dict_data = {'user': self.user, 'sorted_unit_name': self.sorted_unit_name,
                          'window_width': self.window_width,
                          'window_height': self.window_height}
        # self.dict_data['sorted_unit_name'].remove('KALIDAL BN')

        self.focus_set()
        self.geometry("{}x{}+0+0".format(self.window_width, self.window_height))
        self.title("UNIT MANAGEMENT PORTAL")
        self.resizable(width=False, height=False)
        self.attributes('-fullscreen', True)

        #  **************************************** String Variables  **************************************** #
        lbl_title = Label(self, text="MANAGEMENT DASHBOARD", font=('times new roman', 37, 'bold'), bg='white',
                          fg='darkblue')
        lbl_title.place(x=0, y=0, width=self.window_width, height=50)
        lbl_user = Label(self, text="USER: " + self.user.upper(), font=('times new roman', 10, 'bold'),
                         fg='teal')
        lbl_user.place(x=self.window_width - lbl_user.winfo_reqwidth() - 30, y=50)

        def log_out(event):
            from LoginWindow import LoginPage
            if self is not None:
                self.destroy()

            LoginPage()

        btn_log_out = Button(self, text='LOG OUT', width=10, bg='Teal', fg='WHITE',
                             font=('times', 10, 'bold'))
        btn_log_out.place(x=self.window_width - btn_log_out.winfo_reqwidth(),
                          y=22)
        btn_log_out.bind('<ButtonRelease-1>', log_out)

        def date_time():
            from time import strftime
            string_time = strftime('%H:%M:%S %p')
            lbl_time.config(text=string_time)
            lbl_time.after(1000, date_time)
            date = datetime.now()
            lbl_date.config(text=f"{date:%B %d, %Y}")

        lbl_time = Label(self, font=('calibri', 10, 'bold'),
                         background='gray',
                         foreground='black')
        lbl_date = Label(self, font=('calibri', 10, 'bold'),
                         background='gray',
                         foreground='black')
        lbl_time.place(x=self.window_width - 230, y=0)
        lbl_date.place(x=self.window_width - 150, y=0)
        date_time()

        #  **************************************** Title  **************************************** #
        filepathLogo = os.path.join(os.path.dirname(__file__), "res", "logo.png")
        logo_image = Image.open(filepathLogo)
        photo_logo = ImageTk.PhotoImage(logo_image)
        title_logo = Label(self, image=photo_logo)
        title_logo.image = photo_logo
        title_logo.place(x=0, y=0, width=50, height=50)

        Label(self, text='\u00A9 Bibek Koirala', fg="teal").place(
            x=self.window_width - 90, y=self.window_height - 20)
        close_button = Button(self, width=12, bg='GREY', text="X", command=self.close_app)
        close_button.place(x=self.window_width - 15, y=0, width=15, height=15)

        minimize_button = Button(self, width=12, bg='GREY', text="-", command=self.minimize_app)
        minimize_button.place(x=self.window_width - 30, y=0, width=15, height=15)

        Label(self, text="WINDOWS", font=('times', '9', 'bold')).place(x=18, y=50)

        # btn_help = Button(self, image='res\help_icon.png', bg='light blue')
        # btn_help.place(x=100, y=50)
        #  **************************************** Army Logo Frame  **************************************** #
        filepathHelpIcon = os.path.join(os.path.dirname(__file__), "res", "help_icon.png")
        icon_help = PhotoImage(file=filepathHelpIcon)
        photo_sample = icon_help.subsample(7, 7)
        button_help = Button(self, bg='black', image=photo_sample, relief=GROOVE, command=self.show_help)
        button_help.image = photo_sample
        # self.label_title = Label(self.upper_frame, image=self.photo_sample)
        button_help.place(x=self.window_width - 25, y=47)

        #  **************************************** Army Logo Frame  **************************************** #
        filepathNepalArmy = os.path.join(os.path.dirname(__file__), "res", "nepal army.png")
        army_logo = PhotoImage(file=filepathNepalArmy)
        army_logo = army_logo.subsample(3, 3)
        army_logo_label = Label(self, image=army_logo, width=96)
        army_logo_label.image = army_logo
        army_logo_label.place(x=0, y=self.window_height - 102)

        # ***************************************** Left Menu Button Frame *********************************** #
        button_size = 60

        left_frame = Frame(self, bd=2, relief='solid', bg='white', borderwidth=2)
        left_frame.place(x=5, y=70, width=90, height=button_size * 4 + 5)

        # ***************************************** HOME WINDOW BUTTON ******************************

        home_user_window_button = Button(left_frame, width=11, fg='TEAL', text='HOME',
                                         command=lambda: self.switch_window(hW.HomeWindow, left_frame),
                                         font=("times", 10, 'bold'))
        home_user_window_button.place(x=0, y=0, height=60)


        # ***************************************** ADD WINDOW BUTTON ******************************

        add_user_window_button = Button(left_frame, width=11, fg='TEAL', text='USER INFO',
                                        font=("times", 10, 'bold'),
                                        command=lambda: self.switch_window(aw.AddWindow, left_frame))
        add_user_window_button.place(x=0, y=button_size * 1, height=60)

        analytics_button = Button(left_frame, width=11, fg='TEAL', text='ANALYTICS',
                                  font=("times", 10, 'bold'),
                                  command=lambda: show_analytics(self, aw.AddWindow, left_frame))
        analytics_button.place(x=0, y=button_size * 2, height=60)

        # ***************************************** Manage Leave Window BUTTON *****************************
        from authorization_window import AuthorizeWindow
        auth_window = AuthorizeWindow(self)

        add_data_from_table_button = Button(left_frame, width=11, fg='TEAL', text='UPLOAD\nUNIT DATA',
                                            font=("times", 10, 'bold'),
                                            command=lambda: auth_window.authorize_user(self.user, self.upload_data))
        add_data_from_table_button.place(x=0, y=button_size * 3, height=60)

        if not (self.user.upper() == "ADMIN" or self.user.upper() == "SUPER USER"):
            add_data_from_table_button.configure(state='disabled')
            add_data_from_table_button.unbind('<ButtonRelease-1>')

        self._holding_frame = Frame(self, borderwidth=2, relief='solid')
        self._holding_frame.place(x=100, y=70, width=self.window_width - 101, height=self.window_height - 90)
        self.switch_window(hW.HomeWindow, left_frame)

    def show_help(self):
        window = Toplevel(self)
        window.title("HELP WINDOW")
        window.geometry('450x300+{}+{}'.format(self.window_width-500, 0))
        window.resizable(False, False)
        window.focus_set()
        window.configure(bg='light blue')
        text_widget = Text(window)
        text_widget.pack()

        with open('res/help.txt', 'r') as f:
            text = f.read()
            text_widget.tag_config('font', font=("Times", 12), spacing1=2, spacing3=15)
            text_widget.insert('1.0', text, 'font')
            text_widget.configure(state='disabled')

    def upload_data(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if file_path:
            file_name = os.path.basename(file_path).split('.')[0]
            file_split = file_name.split(' ')
            if len(file_split) > 1:
                table_name = file_split[0].lower()
                for i in range(1, len(file_split)):
                    table_name += "_" + file_split[i].lower()
            else:
                table_name = file_name
            import pandas as pd
            file = pd.read_csv(file_path)
            if all(col in file.columns for col in ['Unit', 'CompNo', 'Rnk',
                                                   'Name', 'Phone', 'Loc',
                                                   'Trade', 'Address', 'DOB',
                                                   'Sex', 'bloodgp', 'Remarks']):
                primary_key = file.columns[1]
                from importData import CreateAndInsertDataFromCsvIntoTable
                create_table_obj = CreateAndInsertDataFromCsvIntoTable(file_path, table_name, primary_key)
                create_table_obj.create_table(self.dict_data)

            else:
                messagebox.showwarning("Warning!!!", "Columns Don\'t Match. Please click on Help Button on Right Side")
        else:
            pass


    def switch_window(self, frame_class, frame_buttons):
        if frame_class.__name__ == 'HomeWindow':
            frame_buttons.winfo_children()[0].configure(bg='lightblue')
            for i in [1, 2]:
                frame_buttons.winfo_children()[i].configure(bg='SystemButtonFace')
        elif frame_class.__name__ == 'AddWindow':
            frame_buttons.winfo_children()[1].configure(bg='lightblue')
            for i in [0, 2]:
                frame_buttons.winfo_children()[i].configure(bg='SystemButtonFace')
        new_frame = frame_class(self._holding_frame, self.dict_data)
        if type(self._frame) is type(new_frame):
            return
        elif self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=0, y=0, width=self.window_width - 105, height=self.window_height - 95)
        # self.after(0,self.deiconify)
        # self._frame.config(background='red')

    def close_app(self):

        self.destroy()

    # **************************************** Minimize Button ********************************* #
    def minimize_app(self):
        self.iconify()
