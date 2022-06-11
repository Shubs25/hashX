import tkinter as tk
from tkinter import ttk
import db_handlers as db
from tkinter import messagebox as msg
from ctypes import windll
import encryptor_decryptor



windll.shcore.SetProcessDpiAwareness(1)


class PwManager(tk.Tk):

    def __init__(self):
        super(PwManager, self).__init__()

        self.geometry('900x620')
        self.title('HashX')
        self.resizable(False, False)

        db.create_table()

        mainFrame = tk.Frame(self)
        mainFrame.pack(expand = 1)

        topFrame = tk.Frame(mainFrame)
        topFrame.pack(side = tk.TOP, fill = tk.BOTH, expand = 1, padx = 10, pady = 10)

        table_frame = tk.Frame(topFrame)
        tree_scroll = tk.Scrollbar(table_frame)
        tree_scroll.pack(side='right', fill='y')
        self.data_tree = ttk.Treeview(table_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        tree_scroll.config(command=self.data_tree.yview)

        self.data_tree['columns'] = ('S.No', 'Website', 'Username', 'Password')
        self.data_tree.column('#0', width=0, stretch='no')
        self.data_tree.column('S.No', anchor='w', width=0)
        self.data_tree.column('Website', anchor='center', width=30)
        self.data_tree.column('Username', anchor='center', width=30)
        self.data_tree.column('Password', anchor='center', width=30)

        self.data_tree.heading('#0', text='Label', anchor='w')
        self.data_tree.heading('S.No', text='S. No', anchor='w')
        self.data_tree.heading('Website', text='Website', anchor='center')
        self.data_tree.heading('Username', text='Username', anchor='center')
        self.data_tree.heading('Password', text='Password', anchor='center')

        self.data_tree.bind('<<TreeviewSelect>>', self.show_selected)

        # data_tree.insert('', tk.END, values = ('dfsd', 'asdds', 'asdad'))
        self.data_tree.pack(fill='both', expand='True')
        table_frame.pack(fill='both', expand='True', padx = 10)



        bottomFrame = tk.Frame(mainFrame, padx = 20, pady = 20)
        bottomFrame.pack(side = tk.BOTTOM, anchor = tk.CENTER)

        tk.Label(bottomFrame, text='Website').grid(row=0, column=0)
        self.wsEntry = tk.Entry(bottomFrame, width=25)
        self.wsEntry.grid(row=1, column=0, padx=10, ipady=5)

        tk.Label(bottomFrame, text = 'Username').grid(row = 0, column = 1)
        self.unameEntry = tk.Entry(bottomFrame, width = 25)
        self.unameEntry.grid(row = 1, column = 1, padx = 10, ipady = 5)

        tk.Label(bottomFrame, text='Password').grid(row=0, column=2)
        self.pwEntry = tk.Entry(bottomFrame, width = 25, show = '*')
        self.pwEntry.grid(row=1, column=2, padx = 10, ipady = 5)


        button_frame = tk.Frame(bottomFrame)
        button_frame.grid(row = 2, column = 0, columnspan = 3)


        tk.Button(button_frame, text = 'Add/Update', command = self.add_to_db)\
            .grid(row = 0, column = 0, pady = 10, padx = 10)

        tk.Button(button_frame, text = 'Delete', command = self.remove_from_db)\
            .grid(row = 0, column = 1, pady = 10, padx = 10)

        tk.Button(button_frame, text = 'Check', command = self.check_pw)\
            .grid(row = 0, column = 2, pady = 10, padx = 10)

        self.showBtn = tk.Button(button_frame, text = 'Show', command = self.show_pw)
        self.showBtn.grid(row = 0, column = 3, pady = 10, padx = 10)

        self.refresh_table()

        switchLbl = tk.Label(self, text='💱', font=('Arial', 20), cursor='hand2')
        switchLbl.place(x=5, y=5)

        switchLbl.bind('<Button-1>', self.switch_mode)


    def add_to_db(self):
        # data = ()

        website, username, password = self.wsEntry.get(), self.unameEntry.get(), self.pwEntry.get()
        if not (website and username and password):
            msg.showerror('Empty', 'Kindly fill all the details!')
        else:
            db.add_or_update(website, username, password)
            self.refresh_table()
            self.clear_all()



    def remove_from_db(self):
        # items = self.data_tree.item(self.data_tree.focus(), 'values')
        # items = (self.wsEntry.get(), self.unameEntry.get(), self.pwEntry.get())
        website, username, password = self.wsEntry.get(), self.unameEntry.get(), self.pwEntry.get()
        if not (website and username and password):
            msg.showerror('Empty', 'Kindly fill all the details!')
        else:
            try:
                db.remove_entry(website, username, password)
            except Exception as e:
                msg.showerror('Huh?', e)
            self.refresh_table()



    def check_pw(self):
        website, uname, password = self.wsEntry.get(), self.unameEntry.get(), self.pwEntry.get()

        if not (website and uname and password):
            msg.showerror('Empty', 'Kindly fill all the details!')
        else:
            matched = False
            try:
                matched = db.check(website, uname, password)
            except Exception as e:
                msg.showerror('What?', e)
            else:
                if matched:
                    msg.showinfo('Matched!', 'The username-password combination is valid')
                else:
                    msg.showerror('Not Matched', 'The username-password combination is not valid')



    def show_pw(self):
        website, uname = self.wsEntry.get(), self.unameEntry.get()
        if not (website and uname):
            msg.showerror('Empty', 'Kindly fill all the details!')
        else:
            response = None
            if self.showBtn['text'] == 'Show':
                try:
                    response = db.reveal_password(website, uname)
                except Exception as e:
                    msg.showerror('Oh no', e)
                else:
                    self.pwEntry.delete(0, tk.END)
                    self.pwEntry.insert(0, response)
                    self.pwEntry.config(show='')
                    self.showBtn.config(text='Hide')
            else:
                self.pwEntry.config(show='*')
                self.showBtn.config(text='Show')


    def refresh_table(self):
        self.data_tree.delete(*self.data_tree.get_children())
        rows = db.get_content()

        for sno, row in enumerate(rows, 1):
            self.data_tree.insert('', tk.END, values = (sno,) + row + ('[ENCRYPTED]',))

    def clear_all(self):
        self.wsEntry.delete(0, tk.END)
        self.unameEntry.delete(0, tk.END)
        self.pwEntry.delete(0, tk.END)



    def show_selected(self, event):
        items = self.data_tree.item(self.data_tree.focus(), 'values')
        # print(items, type(items))
        self.showBtn.config(text = 'Show')
        self.clear_all()

        try:
            self.wsEntry.insert(0, items[1])
            self.unameEntry.insert(0, items[2])
            self.pwEntry.insert(0, items[3])
        except IndexError:
            pass


    def switch_mode(self, event):
        self.destroy()
        self.quit()

        enc_dec = encryptor_decryptor.DeEnc()
        enc_dec.mainloop()



if __name__ == '__main__':
    def main():
        password_manager = PwManager()
        password_manager.mainloop()


    main()


