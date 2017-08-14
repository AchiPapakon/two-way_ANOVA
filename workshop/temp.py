import tkinter as tk
import tkinter.ttk as ttk

class App:
    def __init__(self, parent):
        self.parent = parent
        self.value_of_combo = 'X'
        self.combo()

    def newselection(self, event):
        self.value_of_combo = self.box.get()
        print(self.value_of_combo)

    def combo(self):
        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value, state='readonly')
        self.box.bind("<<ComboboxSelected>>", self.newselection)
        self.box['values'] = ('X', 'Y', 'Z')
        self.box.current(0)
        self.box.grid(column=0, row=0)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()