import tkinter as tk
import tkinter.filedialog as fd
import PIL.Image
import PIL.ImageTk
from tkinter import messagebox as msg
from crypto_handler import Crypt
from ctypes import windll
import password_manager


windll.shcore.SetProcessDpiAwareness(1)


class DeEnc(tk.Tk):
    def __init__(self):
        super().__init__()
        self.file = None
        self.key = None
        self.encryptionObj = Crypt()
        self.decryptionObj = None
        photo = tk.PhotoImage(file="Untitled-1.png")
        self.iconphoto(True, photo)

        self.geometry('1000x768')
        self.resizable(False, False)
        self.title('HashX')



        hashx_logo = PIL.Image.open('hashx_logo.png')
        hashx_logo = hashx_logo.resize((300, 100), PIL.Image.ANTIALIAS)
        hashx_logo_obj = PIL.ImageTk.PhotoImage(hashx_logo)
        logo = tk.Label(self, image = hashx_logo_obj)
        logo.image = hashx_logo_obj
        logo.pack()

        mainFrame = tk.Frame(self)
        mainFrame.pack(fill = tk.BOTH, expand = 1)

        wrapperFrame = tk.Frame(mainFrame)
        wrapperFrame.pack(expand = 1)

        leftFrame = tk.Frame(wrapperFrame)
        leftFrame.grid(row = 0, column = 0, padx = 20)

        rightFrame = tk.Frame(wrapperFrame)
        rightFrame.grid(row = 0, column = 1)


        fileFrame = tk.Frame(leftFrame)
        fileFrame.pack(pady = 10)

        file_img = PIL.Image.open('file_logo.png')
        file_img = file_img.resize((30, 30), PIL.Image.ANTIALIAS)
        file_img_obj = PIL.ImageTk.PhotoImage(file_img)
        fileBtn = tk.Label(fileFrame, image = file_img_obj, cursor = 'circle')
        fileBtn.image = file_img_obj
        fileBtn.grid(row = 0, column = 0)
        fileBtn.bind('<Button-1>', self.openFile)

        self.fileLabel = tk.Label(fileFrame, text = 'File Selected: None')
        self.fileLabel.grid(row=0, column=1, padx = '15px')

        encr_decr_frame = tk.Frame(leftFrame)
        encr_decr_frame.pack()

        self.encrypt_decrypt = tk.IntVar()
        self.edrb1 = tk.Radiobutton(encr_decr_frame, text = 'Encrypt', value = 1, tristatevalue = 10,
                       variable = self.encrypt_decrypt, state = tk.DISABLED,
                       command = self.encrypt_formalities)
        self.edrb1.grid(row = 0, column = 0)

        self.edrb2 = tk.Radiobutton(encr_decr_frame, text = 'Decrypt', value = 2, tristatevalue = 10,
                       variable = self.encrypt_decrypt, state = tk.DISABLED,
                       command = self.key_entry)
        self.edrb2.grid(row = 0, column = 1)


        self.go_button = tk.Button(encr_decr_frame, text='Go!', width = '15', state = tk.DISABLED,
                                   command = self.doTheJob)
        self.go_button.grid(row=2, column=0, columnspan = 2, pady = 10)



        contentFrame = tk.Frame(rightFrame)
        contentFrame.pack()

        self.contents = tk.Text(contentFrame, padx = 10, pady = 10)
        self.contents.pack()

        switchLbl = tk.Label(self, text = '⦼', font = ('Arial', 20), cursor = 'hand2')
        switchLbl.place(x = 5, y = 5)

        switchLbl.bind('<Button-1>', self.switch_mode)




    def write_to_screen(self, stuff):
        self.contents.delete('1.0', tk.END)
        self.contents.insert('1.0', stuff)


    def openFile(self, event):
        self.file = fd.askopenfile(mode ='r')
        # self.fileLabel.config(text = f'File Selected: {file.name}')
        if self.file is not None:
            self.fileLabel.config(text = f'File Selected: {self.file.name.split("/")[-1]}')
            self.edrb1.config(state = tk.NORMAL)
            self.edrb2.config(state = tk.NORMAL)

            # self.contents.delete('1.0', tk.END)
            # self.encryptionObj = Crypt()
            # self.encryptionObj.content = self.file
            # self.contents.insert('1.0', self.file.read())
            # self.file.close()

            self.encryptionObj = Crypt()
            self.write_to_screen(self.file.read())
            self.encryptionObj.content = (None, self.file)
            self.file.close()



    def key_entry(self):
        popUp = tk.Toplevel(self, pady = 20, padx = 30)
        popUp.title('Key')
        popUp.grab_set()
        popUp.geometry('500x200')
        popUp.resizable(False, False)

        tk.Label(popUp, text = 'Enter Key').pack()
        self.keyEntry = tk.Entry(popUp, width = 250)
        self.keyEntry.pack(pady = 10)

        tk.Button(popUp, text = 'Okay', command = self.save_key, width = 15).pack(pady = 5)


    def save_key(self):
        self.key = self.keyEntry.get()
        if self.key == '':
            msg.showerror('Empty Key', 'Please enter a valid key!')
            return
        # print(self.key)
        self.keyEntry.master.destroy()
        self.go_button.config(state = tk.NORMAL)


    def encrypt_formalities(self):
        self.go_button.config(state = tk.NORMAL)


    def doTheJob(self):

        modifiedContents, key = None, None

        if msg.askyesno('Confirmation', 'Old contents will be overwritten. Proceed?'):
            try:
                if self.encrypt_decrypt.get() == 1:
                    self.encryptionObj.content = (self.contents.get('1.0', tk.END), self.file)
                    modifiedContents, key = self.encryptionObj.encrypt()
                elif self.encrypt_decrypt.get() == 2:
                    modifiedContents, key = self.encryptionObj.decrypt(self.key)
                else:
                    msg.showerror('>:(', 'Select an option first!')
                    return



            except Exception as e:
                msg.showerror('Error', 'Wrong key')
                print(e)
                self.encrypt_decrypt.set(69)


            else:
                self.write_to_screen(modifiedContents)
                self.encryptionObj.write_to_file()

                if key is not None:
                    ok = msg.showinfo('Key', 'Key will be copied to the clipboard once you press OK.'
                                             ' Paste it somewhere before closing the application'
                                             ' and keep it safe, as it will be required during decryption')
                    if ok == 'ok':
                        self.clipboard_clear()
                        self.clipboard_append(key)
                        self.update()
        else:
            return


    def switch_mode(self, event):
        self.destroy()
        self.quit()

        pw_man = password_manager.PwManager()
        pw_man.mainloop()




if __name__ == '__main__':
    def main():
        deenc = DeEnc()
        deenc.mainloop()

    main()





