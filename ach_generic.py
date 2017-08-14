from decimal import *
from tkinter import *
import os


def convert_to_3places(float_):
    str_ = str(float_)
    return round(Decimal(str_), 3)

# print(convert_to_3places(2.0091750200663202e-08))
# print(convert_to_3places(2.675))


class Dialog(Toplevel):
    def __init__(self, parent, settings=None, title = None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.in_settings = settings  # ach: optional argument for settings input

        if title:
            self.title(title)

        self.parent = parent
        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()
        self.grab_set()  # makes parent inactive

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()
        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override


class LoadWizard(Dialog):  # extends Dialog
    def body(self, master):
        self.settings = []

        # ~~~ 1st group ~~~
        group1 = LabelFrame(master, text='Are variable names included at the top of your file?', padx=5, pady=5)
        group1.pack(padx=10, pady=10)
        radio_title = StringVar()
        self.settings.append(radio_title)
        radio_title.set('Yes')  # initializing the choice ('True')
        Radiobutton(group1, text='Yes', variable=radio_title, value='Yes').pack(anchor='w')
        Radiobutton(group1, text='No', variable=radio_title, value='No').pack(anchor='w')

        # ~~~ 2nd group ~~~
        group2 = LabelFrame(master, text='Which delimiters appear between your variables?', padx=5, pady=5)
        group2.pack(padx=10, pady=10, fill='x')
        delimiters = StringVar()
        self.settings.append(delimiters)
        delimiters.set(',')
        Radiobutton(group2, text='Tab', variable=delimiters, value='\t').pack(anchor='w')
        Radiobutton(group2, text='Space', variable=delimiters, value=' ').pack(anchor='w')
        Radiobutton(group2, text='Comma', variable=delimiters, value=',').pack(anchor='w')
        Radiobutton(group2, text='Semicolon', variable=delimiters, value=';').pack(anchor='w')

        # ~~~ 3rd group ~~~
        group3 = LabelFrame(master, text='What is the text qualifier?', padx=5, pady=5)
        group3.pack(padx=10, pady=10, fill='x')
        qualifier = StringVar()
        self.settings.append(qualifier)
        qualifier.set('\"')
        # Radiobutton(group3, text='None', variable=qualifier, value='None').pack(anchor='w')
        Radiobutton(group3, text='Single quote \t \' ', variable=qualifier, value='\'').pack(anchor='w')
        Radiobutton(group3, text='Double quote \t \" ', variable=qualifier, value='\"').pack(anchor='w')
        Radiobutton(group3, text='Vertical bar \t | ', variable=qualifier, value='|').pack(anchor='w')

        if self.in_settings == None:
            # ~~~ Use the default settings ~~~
            pass
        elif not isinstance(self.settings, list):
            print('Debug: the input must be a list')
        else:
            self.settings[0].set(self.in_settings[0])
            self.settings[1].set(self.in_settings[1])
            self.settings[2].set(self.in_settings[2])

    def apply(self):
        self.result = [x.get() for x in self.settings]

# root = Tk()
# wiz = Wizard(root)
# string_list_temp = [x.get() for x in wiz.settings]
# print(string_list_temp)
# wiz = Wizard(root, settings=string_list_temp)
# print([x.get() for x in wiz.settings])
# root.mainloop()

