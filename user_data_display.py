from datetime import datetime
from tkinter import Frame, Label, messagebox, RIDGE, W, SUNKEN, ttk, VERTICAL, END, RIGHT, Y
from tkinter import Toplevel, BOTH
from PIL import Image, ImageTk
import io


class UserDataWindow:
    def __init__(self, container, comp_no, unit_table):
        self.frame_leave_details = Frame()
        self.window = container
        self.comp_no = comp_no
        self.unit_name = unit_table
        self.set_basic_data_window()

    def set_basic_data_window(self):
        if self.comp_no:
            self.comp_no = int(float(self.comp_no))
            window_width = self.window.winfo_screenwidth()
            window_height = self.window.winfo_screenheight()
            from CreateConnection import CreateConnection
            db = CreateConnection(database_name='bibekdb')
            con = db.create_connection()
            cursor = con.cursor()

            leave_table = 'leave_record_' + self.unit_name
            query_to_get_data = f"select * from {self.unit_name} where CompNo={self.comp_no}"
            cursor.execute(query_to_get_data)

            req_basic_data = cursor.fetchone()

            user_unit = req_basic_data[0]
            user_comp_no = req_basic_data[1]
            user_rnk = req_basic_data[2]
            user_name = req_basic_data[3]
            user_phone = req_basic_data[4]
            user_mail = req_basic_data[5]
            user_trade = req_basic_data[6]
            user_address = req_basic_data[7]
            user_dob = req_basic_data[8]
            user_sex = req_basic_data[9]
            user_remarks = req_basic_data[11]
            user_blood_gp = req_basic_data[10]
            user_photo = req_basic_data[12]

            user_data_window = Toplevel(self.window)
            user_data_window.grab_set()
            user_data_window.focus_set()
            user_data_window.title('DATA')
            user_data_window.geometry("{}x{}+{}+{}".format(window_width - 10, window_height - 50, 0, 0))
            user_data_window.resizable(False, False)
            user_data_window.configure(bg='#296E85')
            title_frame = Frame(user_data_window)
            title_frame.place(x=0, y=0, width=800, height=20)
            font_title = ('Times New Roman', 13, 'bold')
            font_data = ('Times New Roman', 12, 'bold')
            bg_title = '#296E85'
            fg_title = 'WHITE'
            fg_data = 'YELLOW'
            font_bg_title = {'font': font_title, 'bg': bg_title, 'fg': fg_title}
            font_bg_data = {'font': font_data, 'bg': bg_title, 'fg': fg_data}

            Label(user_data_window, text=str(user_comp_no) + ', ' + user_rnk.upper() + ' ' + user_name.upper(),
                  bg='orange',
                  font=('Segoe UI', 10, 'bold'), relief=RIDGE,
                  borderwidth=5).place(x=0, y=0, width=window_width - 10, height=30)

            frame_user_data_column = Frame(user_data_window, bg='#296E85', borderwidth=3, relief=RIDGE)
            frame_user_data_column.place(x=5, y=65, width=int(window_width / 2), height=int(window_height / 2))
            Label(user_data_window, text='BIODATA',
                  bg='orange', font=('Segoe UI', 10, 'bold'), relief=RIDGE,
                  borderwidth=5).place(x=5, y=33, width=int(window_width / 2), height=30)

            Label(frame_user_data_column, font_bg_title, text='Unit: ').grid(row=0, column=0, sticky=W, pady=5)
            Label(frame_user_data_column, font_bg_data, text=user_unit).grid(row=0, column=1, sticky=W)

            Label(frame_user_data_column, font_bg_title, text='Phone No: ').grid(row=1, column=0, sticky=W, pady=5)
            Label(frame_user_data_column, font_bg_data, text=user_phone).grid(row=1, column=1, sticky=W)

            Label(frame_user_data_column, font_bg_title, text='Loc: ').grid(row=2, column=0, sticky=W, pady=5)
            Label(frame_user_data_column, font_bg_data, text=user_mail, ).grid(row=2, column=1, sticky=W)

            Label(frame_user_data_column, font_bg_title, text='Trade: ').grid(row=3, column=0, sticky=W, pady=5)
            Label(frame_user_data_column, font_bg_data, text=user_trade).grid(row=3, column=1, sticky=W)

            Label(frame_user_data_column, font_bg_title, text='Address: ').grid(row=4, column=0, sticky=W, pady=5)
            Label(frame_user_data_column, font_bg_data, text=user_address, ).grid(row=4, column=1, sticky=W)

            Label(frame_user_data_column, font_bg_title, text='Date of Birth: ', ).grid(row=5, column=0, sticky=W,
                                                                                        pady=5)
            Label(frame_user_data_column, font_bg_data, text=user_dob, ).grid(row=5, column=1, sticky=W)

            Label(frame_user_data_column, font_bg_title, text='Sex: ', ).grid(row=6, column=0, sticky=W, pady=5)
            Label(frame_user_data_column, font_bg_data, text=user_sex, ).grid(row=6, column=1, sticky=W)

            Label(frame_user_data_column, font_bg_title, text='Remarks: ', ).grid(row=8, column=0, sticky=W, pady=5)
            Label(frame_user_data_column, font_bg_data, text=user_remarks, ).grid(row=8, column=1, sticky=W)

            Label(frame_user_data_column, font_bg_title, text='Blood Group: ', ).grid(row=7, column=0, sticky=W, pady=5)
            Label(frame_user_data_column, font_bg_data, text=user_blood_gp, ).grid(row=7, column=1, sticky=W)

            Label(user_data_window, text='LEAVE DETAILS',
                  bg='orange', font=('Segoe UI', 10, 'bold'), relief=RIDGE,
                  borderwidth=5).place(x=5, y=int(window_height / 2 + 70), width=int(window_width / 2),
                                       height=30)

            self.frame_leave_details = Frame(user_data_window, bg='#296E85', borderwidth=3, relief=RIDGE,)
            self.frame_leave_details.place(x=5, y=int(window_height / 2) + 105, width=int(window_width / 2), height=200)

            frame_partition = Frame(user_data_window, borderwidth=3, relief=SUNKEN)
            frame_partition.place(x=int(window_width / 2) + 10, y=30, width=2, height=window_height)

            Frame(frame_user_data_column, borderwidth=3, relief=SUNKEN,
                  bg='light blue').place(x=int(window_width / 2 - 160), y=10, width=150, height=150)

            frame_photo = Frame(frame_user_data_column, relief=RIDGE, borderwidth=3, bg='grey')
            frame_photo.place(x=int(window_width / 2 - 148), y=20, width=130, height=130)

            profile_photo = Label(frame_photo)
            if user_photo:
                image = Image.open(io.BytesIO(user_photo))
                image = ImageTk.PhotoImage(image)
                profile_photo.config(image=image)
                profile_photo.image = image
                profile_photo.pack(fill=BOTH)

            try:
                query_to_get_leave_data = f'select * from {leave_table} where CompNo={self.comp_no}'
                cursor.execute(query_to_get_leave_data)
                leave_data = cursor.fetchall()
            except Exception as ex:
                leave_data = []
                messagebox.showerror("ERROR", ex)
            cursor.close()
            con.close()
            self.set_leave_data_window(leave_data)
        else:
            messagebox.showwarning("Warning!!!", "Select Row")

    def set_leave_data_window(self, leave_data):

        scroll_y = ttk.Scrollbar(self.frame_leave_details, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        columns = ('Leave Date', 'Return Date', 'No of Days')
        leave_display_treeview = ttk.Treeview(self.frame_leave_details,
                                              columns=columns)
        leave_display_treeview.pack(fill=BOTH, expand=True)
        leave_display_treeview.tag_configure("Treeview", background="light blue")
        leave_display_treeview['show'] = 'headings'
        leave_display_treeview.column('Leave Date', width=20, anchor='c')
        leave_display_treeview.column('Return Date', width=20, anchor='c')
        leave_display_treeview.column('No of Days', width=20, anchor='c')
        leave_display_treeview.heading('Leave Date', text='Leave Date', anchor='c')
        leave_display_treeview.heading('Return Date', text='Return Date', anchor='c')
        leave_display_treeview.heading('No of Days', text='No of Days', anchor='c')

        scroll_y.config(command=leave_display_treeview.yview)

        for data in leave_data:
            leave_date = datetime.strptime(str(data[1]), "%Y-%m-%d")
            returning_day = datetime.strptime(str(data[2]), "%Y-%m-%d")
            days_in_date = returning_day - leave_date
            total_days = str(days_in_date.days + 1)
            leave_display_treeview.insert('', END, values=(data[1], data[2], total_days,))
