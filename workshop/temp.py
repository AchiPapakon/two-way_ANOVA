from tkinter import *

class MyDialog:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="Value").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        print("value is", self.e.get())

        self.top.destroy()

def ach_new_window():
    MyDialog(root)

root = Tk()
Button(root, text="Hello!", command=ach_new_window).pack()
root.update()

d = MyDialog(root)

root.wait_window(d.top)