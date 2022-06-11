import tkinter as tk
import PIL.Image
import PIL.ImageTk
from ctypes import windll
import encryptor_decryptor


windll.shcore.SetProcessDpiAwareness(1)

class Splash(tk.Tk):
    def __init__(self):
        super(Splash, self).__init__()
        self.overrideredirect(True)

        hashx_logo = PIL.Image.open('splash.png')
        hashx_logo = hashx_logo.resize((800, 430))
        hashx_logo_obj = PIL.ImageTk.PhotoImage(hashx_logo)
        logo = tk.Label(self, image = hashx_logo_obj)
        logo.image = hashx_logo_obj
        logo.pack()


def start(curr):
    curr.destroy()
    curr.quit()
    enc_dec = encryptor_decryptor.DeEnc()
    enc_dec.mainloop()


def main():
    hashx = Splash()
    hashx.after(2500, lambda: start(hashx))
    hashx.mainloop()


if __name__ == '__main__':
    main()


