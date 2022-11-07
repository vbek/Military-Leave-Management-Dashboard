import tkinter
from tkinter import Tk, Label, Frame, Entry, ttk, Button


class DisplayUser:
    def __init__(self, window, user):
        self.search_key = ""
        self.parent_window = window
        self.search_window = tkinter.Toplevel(self.parent_window)
        self.user = user
        self.set_window()

    def set_window(self):
        screen_width = self.search_window.winfo_screenwidth()
        screen_height = self.search_window.winfo_screenheight()
        window_width = int(screen_width / 5)
        window_height = int(screen_height / 5)
        self.search_window.geometry('{}x{}'.format(window_width, window_height))
        self.search_window.resizable(False, False)
        self.search_window.config(bg='white')
        self.search_window.title("FIND USER")

        # ************************************ SEARCH BY LABEL ****************************************
        lbl_search_by = Label(self.search_window, text="SEARCH BY:", fg='teal', bg='orange', anchor='w')
        lbl_search_by.place(x=0, y=0)

        # ************************************ FRAME QUERY ********************************************
        frame_query = Frame(self.search_window, bg='white')
        frame_query.place(x=0, y=30, width=window_width, height=window_height)

        # ************************************ SEARCH COMBO BOX ***************************************
        search_key_tuple = ("CompNo", "Rnk", "Name", "Phone", "Unit", 'Bloodgp')
        search_text_tuple = ("Comp No", 'Rank', 'Name', 'Phone No', 'Unit', 'Blood Gp')
        text_query = tkinter.StringVar()
        combo_search = ttk.Combobox(self.search_window, textvariable=text_query, state='readonly', width=10)
        combo_search['values'] = search_text_tuple
        combo_search.place(x=80, y=0)
        combo_search.current(0)
        lbl_query_text = combo_search.get()
        lbl_query = Label(frame_query, text=lbl_query_text + ": ", fg='teal', bg='WHITE', anchor='w')
        lbl_query.place(x=0)
        self.search_key = search_key_tuple[0]

        def searchQuery(e):
            entry_query.delete(0, "end")
            text = combo_search.get()
            lbl_query.config(text=text + ": ")
            entry_query.focus_set()
            self.search_key = search_key_tuple[combo_search.current()]

        combo_search.bind("<<ComboboxSelected>>", searchQuery)

        # *********************************** ENTRY SEARCH QUERY *************************************
        frame_underline = Frame(frame_query, height=2, background='black')
        frame_underline.place(x=lbl_query.winfo_reqwidth() + 18, y=18, width=170)
        entry_query = Entry(frame_query, width=16, border=0)
        entry_query.place(x=80, y=0)
        entry_query.focus_set()

        # *********************************** SEARCH BUTTON ******************************************
        def main_dashboard(e):
            self.search_window.destroy()
            from Employee import Employee
            Employee(self.parent_window, self.user)

        btn_search = Button(frame_query, width=10, bg='teal', text="SEARCH", fg='white')
        btn_search.place(x=int(window_width - btn_search.winfo_reqwidth()), y=25)

        btn_add_user = Button(frame_query, width=10, bg='orange', text="ADD USER")
        btn_add_user.place(x=int(window_width - btn_search.winfo_reqwidth()), y=80)
        btn_add_user.bind('<ButtonRelease-1>', main_dashboard)
        self.search_window.mainloop()

