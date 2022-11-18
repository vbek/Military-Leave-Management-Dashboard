from tkinter import Tk, ttk, Frame, RIDGE, HORIZONTAL, VERTICAL, Y, X, BOTTOM, RIGHT, CENTER, BOTH, Button

from Employee import Employee


class UserProfile:
    def __init__(self):
        self.window = Tk()
        self.set_window()

    def set_window(self):
        window_width = self.window.winfo_screenwidth()
        window_height = self.window.winfo_screenheight()
        self.window.attributes('-fullscreen', True)
        self.window.geometry('{}x{}'.format(window_width, window_height))

        main_frame = Frame(self.window, bd=2, relief=RIDGE, bg='WHITE')
        main_frame.place(x=100, y=70, width=window_width - 101, height=window_height - 90)

        btn_close = Button(self.window, text='X', command=lambda: self.window.destroy())
        btn_close.place(x=window_width - 15)
        btn_minimize = Button(self.window, text='-', command=lambda: Employee(self.window, "bibek"))
        btn_minimize.place(x=window_width - 35)
        display_frame = Frame(main_frame, bd=5, relief=RIDGE)
        display_frame.place(width=window_width - 126, height=window_height - 90)
        scroll_x = ttk.Scrollbar(display_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(display_frame, orient=VERTICAL)
        tree_columns = ('unit', 'CompNo', 'Rnk', 'Name', 'Phone', 'Bloodgp')
        phone_details_tree = ttk.Treeview(display_frame,
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
                phone_details_tree.column(i, anchor="w")
        # phone_details_tree.bind("<<TreeviewSelect>>", self.get_cursor)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_x.config(command=phone_details_tree.xview)
        scroll_y.config(command=phone_details_tree.yview)

        phone_details_tree.heading('unit', text='Unit', anchor=CENTER)
        phone_details_tree.heading('CompNo', text='Comp No', anchor=CENTER)
        phone_details_tree.heading('Rnk', text='Rank', anchor=CENTER)
        phone_details_tree.heading('Name', text='Name', anchor=CENTER)
        phone_details_tree.heading('Phone', text='Phone No', anchor=CENTER)
        phone_details_tree.heading('Bloodgp', text='Blood Gp', anchor=CENTER)

        phone_details_tree.pack(fill=BOTH, expand=1)
        # phone_details_tree.bind("<ButtonRelease>", self.get_cursor)
        phone_details_tree['show'] = 'headings'
        phone_details_tree.column("unit", width=80)
        phone_details_tree.column("CompNo", width=52)
        phone_details_tree.column("Rnk", width=40)
        phone_details_tree.column("Name", width=110)
        phone_details_tree.column("Phone", width=70)
        phone_details_tree.column("Bloodgp", width=60)
        self.window.mainloop()


UserProfile()
