from __future__ import division

import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        rows = 100
        columns = 3
        tk.Tk.__init__(self)
        # draw Frame above the table which contains the button
        frame = tk.Frame(self)
        frame.pack(side='top', pady=(0, 5))
        button1 = tk.Button(frame, text='New Window', width=25, command=lambda: self.btnTwoWayAnova_Click())
        button1.pack()


    def btnTwoWayAnova_Click(self):
        placeholder = 1
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)


class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()

