import os
from collections import OrderedDict
from datetime import datetime
from tkinter import Toplevel, Canvas, Frame, Label, ttk, END, Button, messagebox, PhotoImage

from PIL import ImageFilter, Image


class AlphaHajirWindow(Toplevel):
    def __init__(self, window, dict_data_attachment):
        self.btn_save_image = Button()
        self.window = window

        self.total_attachment = dict_data_attachment['total']
        self.attachment_on_leave = dict_data_attachment['leave']
        self.attachment_on_post = dict_data_attachment['post']
        self.attachment_absent = dict_data_attachment['absent']

        self.window_width = self.window.master.master.winfo_width()
        self.window_height = self.window.master.master.winfo_height()
        Toplevel.__init__(self, self.window)
        heading_text_horizontal = "Lt Col,Major,Captain,Tech Captain,Lt/2nd Lt,Acc Lt,Chief WO3,WO2,Crl WO2," \
                                  "Acc WO2,Brh WO1,WO1,Acc WO1,Crl WO1,Adj Sgt,Lgs Sgt,Sgt,Crl Sgt,L.Cpl,Crl L.Cpl," \
                                  "L.Cpl,Sappers,Soldier,Fol Sgt,Fol,Cleaner,Broomer," \
                                  "Barber,Sweeper,Welder,Total,Attach,Gross Total"

        self.headings_horizontal = heading_text_horizontal.split(',')

        self.headings_vertical = ['Rqd Appont', 'Present', 'Less By', 'More With', 'UN MSN',
                                  'Trg', 'Tmp Posting', 'Out of Bn', 'Other', 'Total out', 'Inside Bn', 'In Leave',
                                  'Suspended', 'Post Duty', 'AWOL', 'Total', 'Total Present']
        self.rank_count_req = OrderedDict({'Lt Col': 1, 'Major': 7, 'Capt': 7, 'T/Capt': 1, 'Lt': 6,
                                           'Acc Lt': 1, 'Sub Major': 1, 'Sub': 4, 'Sub Ka': 1, 'Acc Sub': 1,
                                           'Pandit Jam': 1, 'Jam': 14, 'Acc Jam': 0, 'Jama Ka': 1,
                                           'Sgt Major': 4, 'Q/Sgt': 4, 'Sgt': 45, 'Hu Ka': 2, 'Cpl': 62, 'A Ka': 2,
                                           'L/Cpl': 82, 'Sapper': 167, 'Sainya': 0, 'Fol Sgt': 1, 'Ba Kaa Si': 10,
                                           'Charma Karmi': 2, 'Su Chi Kar': 2, 'Barber': 2, 'Safaai Karmi': 3,
                                           'Loha Kaar': 2,
                                           'Total': 0, 'Attach': 0, 'Grand Total': 0})
        self.rank_count_req['Total'] = sum(self.rank_count_req.values())
        self.rank_count_req['Grand Total'] = self.rank_count_req['Total']
        self.tree_data = ttk.Treeview()
        self.set_window()
        self.mainloop()

    def set_window(self):
        self.geometry(f'{self.window_width}x{self.window_height}+0+0')
        self.title('\'A\' Hajir')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.focus_set()
        self.overrideredirect(True)
        self.configure(background='White')

        def on_key_release(event):
            if event.keysym == 'Escape':
                self.destroy()

        self.bind("<KeyRelease>", on_key_release)

        font = ('Haveltica', 8)

        height_of_horizontal_canvas = 80
        width_of_horizontal_canvas = self.window_width - 120
        height_of_vertical_canvas = self.window_height - 304
        width_of_vertical_canvas = 80
        x_of_horizontal_canvas = 120
        y_of_horizontal_canvas = 1
        x_of_vertical_canvas = 40
        y_of_vertical_canvas = 90

        frame_heading = Frame(self, width=self.window_width - 20, height=50, bg='White')
        frame_heading.place(x=0, y=0)

        lbl_title = Label(frame_heading, text='Kalidal Bn(E) Personnel Details', bg='White',
                          font=('Haveltica', 14, 'underline', 'bold'))
        lbl_title.place(x=int((self.window_width - lbl_title.winfo_reqwidth()) / 2))

        lbl_date = Label(self, font=('Haveltica', 9, 'bold'), bg='White',
                         text='Date: ' + str(datetime.now().date()))
        lbl_date.place(x=self.window_width - lbl_date.winfo_reqwidth() - 28,
                       y=40)

        hajir_frame = Frame(self, width=width_of_horizontal_canvas + width_of_vertical_canvas + 5,
                            height=height_of_horizontal_canvas + height_of_vertical_canvas + 5,
                            bg='White')
        hajir_frame.place(x=5, y=60)

        frame_for_horizontal_canvas = Frame(hajir_frame)
        frame_for_horizontal_canvas.place(x=x_of_horizontal_canvas - 10, y=y_of_horizontal_canvas,
                                          width=width_of_horizontal_canvas, height=height_of_horizontal_canvas)

        canvas_horizontal = Canvas(frame_for_horizontal_canvas, height=height_of_horizontal_canvas,
                                   width=width_of_horizontal_canvas)
        canvas_horizontal.place(x=0, y=0)
        canvas_horizontal.create_rectangle(4, 4, width_of_horizontal_canvas - 30, height_of_horizontal_canvas - 3,
                                           width=2)

        frame_left_column_for_canvas = Frame(hajir_frame)
        frame_left_column_for_canvas.place(x=x_of_vertical_canvas, y=y_of_vertical_canvas - 10,
                                           width=width_of_vertical_canvas, height=height_of_vertical_canvas)

        canvas_vertical = Canvas(frame_left_column_for_canvas, height=height_of_vertical_canvas,
                                 width=width_of_vertical_canvas)
        canvas_vertical.place(x=0, y=0)
        canvas_vertical.create_rectangle(4, 4, width_of_vertical_canvas - 4, height_of_vertical_canvas - 2,
                                         width=2)

        frame_asami = Frame(hajir_frame, relief='solid', bd=2)
        frame_asami.place(x=x_of_vertical_canvas + 3, y=y_of_horizontal_canvas + 3,
                          width=width_of_vertical_canvas - 5, height=height_of_horizontal_canvas - 5)
        Label(frame_asami, text='Details', font=font).pack(fill='both', expand=True)

        column_width = 34
        column_height = 24
        x = 6
        for i, heading in enumerate(self.headings_horizontal):
            canvas_horizontal.create_line(x, 4, x, height_of_horizontal_canvas - 4, fill="black", width=2)
            # noinspection PyArgumentList
            canvas_horizontal.create_text(x + 16, int(height_of_horizontal_canvas / 2), text=heading, anchor='center',
                                          angle=90, tags='heading', font=font)
            if i == 30:
                Frame(frame_for_horizontal_canvas, bd=2,
                      relief='solid').place(x=x - 1, y=4, width=4,
                                            height=height_of_horizontal_canvas - 6)

            x += column_width
        y = 20
        for i, heading in enumerate(self.headings_vertical):
            canvas_vertical.create_text(int(width_of_vertical_canvas / 2), y - 3, text=heading,
                                        font=font, tags='heading', anchor='center')
            canvas_vertical.create_line(4, y + 10, width_of_vertical_canvas - 4, y + 10,
                                        fill='black', tags='line', width=2)
            if i == 3 or i == 9 or i == 15 or i == 10 or i == 14:
                Frame(frame_left_column_for_canvas, bd=2,
                      relief='solid').place(x=4, y=y + 9, height=4,
                                            width=width_of_vertical_canvas - 8)
            y += column_height
        font = ('Haveltica', 10, 'bold', 'underline')
        Label(self, text='Arrival Report:', bg='White',
              font=font).place(x=x_of_vertical_canvas,
                               y=hajir_frame.winfo_reqheight() + frame_heading.winfo_reqheight() + 5)

        Label(self, text='Internal Password:', bg='White',
              font=font, justify='left').place(x=x_of_vertical_canvas + int(self.window_width / 5.5) - 10,
                                               y=hajir_frame.winfo_reqheight() + frame_heading.winfo_reqheight() + 5)
        Label(self, text='Check in Question:\nCheck in Password:\nCheck in Number:', bg='White',
              font=('Haveltica', 10, 'bold'), justify='left'
              ).place(x=x_of_vertical_canvas + int(self.window_width / 5.8),
                      y=hajir_frame.winfo_reqheight() + frame_heading.winfo_reqheight() + 28)

        Label(self, text='External Password:', bg='White',
              font=font).place(x=x_of_vertical_canvas + int(self.window_width / 3) + 30,
                               y=hajir_frame.winfo_reqheight() + frame_heading.winfo_reqheight() + 5)

        Label(self, text='Question:\nPassword:', bg='White',
              font=('Haveltica', 10, 'bold'), justify='left'
              ).place(x=x_of_vertical_canvas + int(self.window_width / 3) + 30,
                      y=hajir_frame.winfo_reqheight() + frame_heading.winfo_reqheight() + 28)

        Label(self, text='Chronic Sick Leave:', bg='White',
              font=font).place(x=x_of_vertical_canvas + int(self.window_width / 2) + 20,
                               y=hajir_frame.winfo_reqheight() + frame_heading.winfo_reqheight() + 5)

        Label(self, text='Departure Report:', bg='White',
              font=font).place(x=x_of_vertical_canvas + int(self.window_width / 1.3),
                               y=hajir_frame.winfo_reqheight() + frame_heading.winfo_reqheight() + 5)

        Label(self, text='.........................\nAdj Sgt Sign', justify='left', bg='White',
              font=('Haveltica', 9)).place(x=x_of_vertical_canvas,
                                          y=self.window_height - 45)
        Label(self, text='...........................\nAdj WO Sign', justify='left', bg='White',
              font=('Haveltica', 9)).place(x=x_of_vertical_canvas + int(self.window_width / 4) + 10,
                                          y=self.window_height - 45)
        Label(self, text='...........................\nAdj Officer Sign', justify='left', bg='White',
              font=('Haveltica', 9)).place(x=x_of_vertical_canvas + int(self.window_width / 1.5),
                                          y=self.window_height - 45)
        Label(self, text='............................\nBattalion Cdr Sign', justify='left', bg='White',
              font=('Haveltica', 9)).place(x=x_of_vertical_canvas + int(self.window_width / 1.2),
                                          y=self.window_height - 45)

        filepath = os.path.join(os.path.dirname(__file__), "res", "printer.png")
        icon_printer = PhotoImage(file=filepath)
        icon_printer = icon_printer.subsample(15, 10)
        btn_save = Button(self, background="orange",
                           image=icon_printer, border=1)
        btn_save.image = icon_printer
        btn_save.place(x=self.window_width - 20, y=20, width=20, height=20)
        btn_save.bind('<ButtonRelease-1>', self.save_image)

        self.display_record()

    def display_record(self):
        frame_tree_record = Frame(self, width=self.window_width - 151,
                                  height=self.window_height - 308, relief='solid', bd=2)
        frame_tree_record.place(x=118, y=143)
        self.tree_data = ttk.Treeview(frame_tree_record, columns=list(self.rank_count_req.keys()), show="")
        self.tree_data.place(x=0, y=0, height=self.window_height - 256, width=self.window_width - 154)
        self.tree_data.tag_configure("font", font=('Haveltica', 8))
        x = 34

        for i, column_id in enumerate(self.rank_count_req.keys()):
            self.tree_data.heading(column_id, anchor='center')
            self.tree_data.column(column_id, width=34, anchor='w')
            Frame(frame_tree_record, bd=1, relief='solid').place(x=x, y=0, width=2,
                                                                 height=self.window_height - 310)
            if i == 29:
                Frame(frame_tree_record, bd=2, relief='solid').place(x=x, y=0, width=4,
                                                                     height=self.window_height - 310)
            if i <= 30:
                x += 34
        y = 24
        for i in range(17):
            Frame(frame_tree_record, bd=1, relief='solid').place(x=0, y=y, height=2,
                                                                 width=self.window_width - 140)
            if i == 3 or i == 9 or i == 15 or i == 10 or i == 14:
                Frame(frame_tree_record, bd=2, relief='solid').place(x=0, y=y, height=4,
                                                                     width=self.window_width - 140)
            y += 24
        self.display_table()

    def display_table(self):
        from CreateConnection import CreateConnection
        db = CreateConnection(database_name='bibekdb')
        conn = db.create_connection()
        cursor = conn.cursor()

        # ****************** Displaying required rank count and available rank count********************#
        cursor.execute("""SELECT Rnk, COUNT(Rnk)
                            FROM kalidal_bn
                            GROUP BY Rnk;""")
        rows = cursor.fetchall()
        available_ranks_count = {}
        for (rank, count) in rows:
            available_ranks_count[rank] = count
        self.tree_data.tag_configure('red', background='red')
        self.tree_data.tag_configure('white', background='white')
        available_ranks_count_ordered = OrderedDict()
        for key in self.rank_count_req.keys():
            if key not in available_ranks_count:
                available_ranks_count_ordered[key] = 0
            else:
                available_ranks_count_ordered[key] = available_ranks_count.get(key)
        _ = {key: '' if value == 0 else value for key, value in self.rank_count_req.items()}
        self.tree_data.insert("", END, values=list(_.values()), tags="font")

        data = available_ranks_count_ordered
        data['Total'] = sum(data.values())
        data['Attach'] = self.total_attachment
        data['Grand Total'] = data['Total'] + data['Attach']
        _ = {key: '' if value == 0 else value for key, value in data.items()}
        self.tree_data.insert("", END, values=list(_.values()), tags="font")

        # ********************** Displaying less and more rows ********************************** #
        less_rows = {}
        more_rows = {}
        for key, value in self.rank_count_req.items():
            if value < available_ranks_count_ordered[key]:
                less_rows[key] = 0
                more_rows[key] = available_ranks_count_ordered[key] - value
            elif value > available_ranks_count_ordered[key]:
                less_rows[key] = value - available_ranks_count_ordered[key]
                more_rows[key] = 0
            else:
                less_rows[key] = 0
                more_rows[key] = 0

        for row in [less_rows, more_rows]:
            row['Total'] = sum(value for key, value in row.items() if key not in ['Total', 'Attach', 'Grand Total'])
            row['Grand Total'] = row['Total'] + row['Attach']
            _ = {key: '' if value == 0 else value for key, value in row.items()}
            self.tree_data.insert("", END, values=list(_.values()), tags="font")

        cursor.execute("""SELECT Rnk, Loc, COUNT(*)
                            FROM kalidal_bn
                            GROUP BY Loc, Rnk;""")
        loc_count = cursor.fetchall()
        mission_rows = OrderedDict()
        talim_rows = OrderedDict()
        kaaj_rows = OrderedDict()
        out_of_hq = OrderedDict()
        other_rows = OrderedDict()
        hq_rows = OrderedDict()
        inside_hq = OrderedDict()
        leave_rows = OrderedDict()
        suspended_rows = OrderedDict()
        post_duty = OrderedDict()
        absent_rows = OrderedDict()
        total_present_rows = OrderedDict()

        ordered_keys = list(self.rank_count_req.keys())
        total_rank_out_of_hq_count = OrderedDict()
        total_rank_on_out = OrderedDict()

        for keys in ordered_keys:
            mission_rows[keys] = 0
            talim_rows[keys] = 0
            kaaj_rows[keys] = 0
            out_of_hq[keys] = 0
            hq_rows[keys] = 0
            other_rows[keys] = 0
            total_rank_out_of_hq_count[keys] = 0
            inside_hq[keys] = 0
            leave_rows[keys] = 0
            suspended_rows[keys] = 0
            post_duty[keys] = 0
            absent_rows[keys] = 0
            total_rank_on_out[keys] = 0
            total_present_rows[keys] = 0

        for data in loc_count:
            if data[1] == 'Mission':
                mission_rows[data[0]] = data[2]
            elif data[1] == 'Training':
                talim_rows[data[0]] = data[2]
            elif data[1] == 'Kaaj':
                kaaj_rows[data[0]] = data[2]
            elif data[1] == 'Out of HQ':
                out_of_hq[data[0]] = data[2]
            elif data[1] == 'HQ':
                hq_rows[data[0]] = data[2]
            elif data[1] == 'Post':
                post_duty[data[0]] = data[2]
            else:
                other_rows[data[0]] = data[2]

        for rows in [mission_rows, talim_rows, kaaj_rows, out_of_hq, other_rows]:
            _ = OrderedDict()
            for key in ordered_keys:
                if key not in rows.keys():
                    _[key] = 0
                else:
                    _[key] = rows.get(key)
                total_rank_out_of_hq_count[key] += rows[key]
            _['Total'] = sum(_.values())
            _['Grand Total'] = _['Total']
            _ = {key: '' if value == 0 else value for key, value in _.items()}
            self.tree_data.insert("", END, values=list(_.values()), tags="font")

        total_rank_out_of_hq_count['Total'] = sum(total_rank_out_of_hq_count.values())
        total_rank_out_of_hq_count['Grand Total'] = total_rank_out_of_hq_count['Total']
        out_count = {key: '' if value == 0 else value for key, value in total_rank_out_of_hq_count.items()}
        self.tree_data.insert("", END, values=list(out_count.values()), tags="font")

        for keys in ordered_keys:
            inside_hq[keys] = available_ranks_count_ordered[keys] - total_rank_out_of_hq_count[keys]
        _ = {key: '' if value == 0 else value for key, value in inside_hq.items()}
        self.tree_data.insert("", END, values=list(_.values()), tags="font")

        query_to_get_person_on_leave = """Select Rnk, count(*) from kalidal_bn where CompNo in 
                                          (SELECT  CompNo 
                                          from leave_record_kalidal_bn
                                          where ReturnDate>now()) group by Rnk;"""
        cursor.execute(query_to_get_person_on_leave)
        count_rank_on_leave = cursor.fetchall()

        for key, value in count_rank_on_leave:
            leave_rows[key] = value

        leave_rows['Total'] = sum(leave_rows.values())
        leave_rows['Attach'] = self.attachment_on_leave
        leave_rows['Grand Total'] = leave_rows['Total'] + leave_rows['Attach']
        _ = {key: '' if value == 0 else value for key, value in leave_rows.items()}
        self.tree_data.insert("", END, values=list(_.values()), tags="font")

        query_to_get_person_suspended = """Select Rnk, count(*) from kalidal_bn 
                                           where Remarks like '%suspended%'
                                           group by Rnk;"""
        cursor.execute(query_to_get_person_suspended)
        count_suspended = cursor.fetchall()

        for key, value in count_suspended:
            suspended_rows[key] = value

        suspended_rows['Total'] = sum(suspended_rows.values())
        suspended_rows['Grand Total'] = suspended_rows['Total']
        _ = {key: '' if value == 0 else value for key, value in suspended_rows.items()}
        self.tree_data.insert("", END, values=list(_.values()), tags="font")

        query_to_get_person_on_post = """Select Rnk, count(*) from kalidal_bn 
                                        where Loc='Post'
                                        group by Rnk;"""
        cursor.execute(query_to_get_person_on_post)
        count_post = cursor.fetchall()

        for key, value in count_post:
            post_duty[key] = value

        post_duty['Total'] = sum(post_duty.values())
        post_duty['Attach'] = self.attachment_on_post
        post_duty['Grand Total'] = post_duty['Total'] + self.attachment_on_post
        _ = {key: '' if value == 0 else value for key, value in post_duty.items()}
        self.tree_data.insert("", END, values=list(_.values()), tags="font")

        query_to_get_person_absent = """Select Rnk, count(*) from kalidal_bn where Remarks like '%absent%'
                                                    group by Rnk;"""
        cursor.execute(query_to_get_person_absent)
        count_absent = cursor.fetchall()

        for key, value in count_absent:
            absent_rows[key] = value

        absent_rows['Total'] = sum(absent_rows.values())
        absent_rows['Attach'] = self.attachment_absent
        absent_rows['Grand Total'] = absent_rows['Total'] + self.attachment_absent
        _ = {key: '' if value == 0 else value for key, value in absent_rows.items()}
        self.tree_data.insert("", END, values=list(_.values()), tags="font")

        for keys in ordered_keys:
            total_rank_on_out[keys] = leave_rows[keys] + suspended_rows[keys] + post_duty[keys] + absent_rows[keys]
            total_present_rows[keys] = inside_hq[keys] - total_rank_on_out[keys]

        _ = {key: '' if value == 0 else value for key, value in total_rank_on_out.items()}
        self.tree_data.insert("", END, values=list(_.values()), tags="font")

        _ = {key: '' if value == 0 else value for key, value in total_present_rows.items()}
        self.tree_data.insert("", END, values=list(_.values()), tags="font")

        number_of_items = len(self.tree_data.get_children())
        for i in range(0, number_of_items, 2):
            self.tree_data.item(self.tree_data.get_children()[i], tags=("gray", "font"))
        for i in range(1, number_of_items, 2):
            self.tree_data.item(self.tree_data.get_children()[i], tags=("white", "font"))

        self.tree_data.tag_configure("gray", background="#cccccc")
        self.tree_data.tag_configure("white", background="#FCF6F5")

        query_people_coming_today = """Select Rnk, Name from kalidal_bn where CompNo in (Select CompNo from leave_record_kalidal_bn
                                        where ReturnDate=curdate());"""
        cursor.execute(query_people_coming_today)
        data_coming = cursor.fetchall()
        row_height = 0

        for i, datum in enumerate(data_coming):
            if i <= 4:
                Label(self, text=datum[0] + ' ' + datum[1], fg='black', bg='White',
                      font=('Halvetica', 9, 'bold')).place(x=20,
                                                   y=self.window_height - 140 + row_height, height=15)
                row_height += 15

        query_people_going_today = """Select Rnk, Name from kalidal_bn where CompNo in (Select CompNo from leave_record_kalidal_bn
                                        where LeaveDate=curdate());"""
        cursor.execute(query_people_going_today)
        data_going = cursor.fetchall()

        row_height = 0
        for i, datum in enumerate(data_going):
            if i <= 4:
                Label(self, text=datum[0] + ' ' + datum[1], fg='black', bg='White',
                      font=('Halvetica', 9, 'bold')).place(x=self.window_width - 260,
                                                   y=self.window_height - 140 + row_height, height=15)
                row_height += 15

    def save_image(self, event):
        from PIL import ImageGrab
        import os
        image = ImageGrab.grab(bbox=(0, 0, int(self.window_width * 1.5) - 30, int(self.window_height * 1.5)))
        image.info['dpi'] = (300, 300)
        i = 1

        filename = "A Hajir " + str(datetime.today().date())
        desktop_path = os.path.expanduser("~\\Desktop")
        file_path = os.path.join(desktop_path, filename + '.png')
        while os.path.exists(file_path):
            file_path = file_path[:-4] + f'({i})' + file_path[-4:]
            i += 1
        else:
            ratio = 2  # Increase the resolution by a factor of 2
            new_width = int(image.width * ratio)
            new_height = int(image.height * ratio)
            for i in range(5):
                image = image.resize((new_width, new_height), resample=Image.LANCZOS)

            # apply the EDGE_ENHANCE filter
            im_edge_enhance = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

            # Save the image
            im_edge_enhance.save(file_path)
            messagebox.showinfo("Saved", 'Image Saved on Desktop')

