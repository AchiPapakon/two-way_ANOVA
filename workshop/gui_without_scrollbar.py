from __future__ import division

import tkinter as tk
import tkinter.messagebox
import re
import numpy
from scipy.stats import ttest_ind


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # topFrame = tk.Frame(self)
        # draw Buttons
        btnPrintArrays = tk.Button(self, text="Print Arrays", command=lambda:self.btnPrintArrays_Click(t))
        btnPrintArrays.pack(side='top')
        # draw Table
        t = SimpleTable(self, 100, 2)
        t.pack(side="top") # don't fill x
        # menu
        menu = tk.Menu(self)
        self.config(menu=menu)
        submenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Data', menu=submenu)
        submenu.add_command(label='Load', command=lambda: self.onLoad(t))
        submenu.add_command(label='Save', command=lambda: self.onSave(t))

    def onSave(self, m_widget):
        data = self.extract_data(m_widget)
        fpOut = open('data.csv', 'w')
        for i in range(0, len(data['leftColumn'])):
            outStr = '%g;%g\n' % (data['leftColumn'][i], data['rightColumn'][i])
            fpOut.write(outStr)
        fpOut.close()

    def onLoad(self, m_widget):
        fpIn = open('data.csv', 'r')
        i = 1
        for line in fpIn: # Can I get fpIn's lines (length)?
            lineArray = line.split(';')
            j = 1
            for element in lineArray:
                m_widget._widgets[i][j].delete(0, 'end')
                m_widget._widgets[i][j].insert(0, element.strip()) # remove the '\n' character
                j = j + 1
            i = i + 1
        fpIn.close()

    def extract_data(self, m_widget):
        data = {'leftColumn': [], 'rightColumn': [], 'subgroup1': [], 'subgroup2': []}
        for i in range(1, len(m_widget._widgets)):
            leftColumn_value = float(m_widget._widgets[i][1].get())
            data['leftColumn'].append(leftColumn_value)
            for j in range(2, len(m_widget._widgets[i])):
                rightColumn_value = float(m_widget._widgets[i][j].get())
                data['rightColumn'].append(rightColumn_value)
                if leftColumn_value == 1:
                    data['subgroup1'].append(rightColumn_value)
                elif leftColumn_value == 2:
                    data['subgroup2'].append(rightColumn_value)
        print(data)
        return data

    def btnPrintArrays_Click(self, m_widget):
        data = self.extract_data(m_widget)
        # at least 2x2
        print(len(data['subgroup1']))
        if (len(data['subgroup1']) < 2) | (len(data['subgroup2']) < 2):
            tkinter.messagebox.showinfo('t-test for independent samples', 'You must have at least 2 values for each group.')
        else:
            t, p = ttest_ind(data['subgroup1'], data['subgroup2'], equal_var=True) # True: equal variances assumed
            print("ttest_ind:   t = %g  p = %g" % (t, p))


class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to
        # form grid lines
        tk.Frame.__init__(self, parent, background="lightblue", padx=1, pady=1)
        self._widgets = []
        vcmd = (self.register(self.onValidate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        for row in range(rows + 1):
            current_row = []
            for column in range(columns + 1):
                if (row == 0) | (column == 0):
                    labelText = row | column
                    if labelText == 0:
                        labelText = ''
                    label = tk.Label(self, borderwidth=0, width=5, text=labelText)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)
                    continue
                entry = tk.Entry(self, borderwidth=0, width=22, validate='key',
                                 validatecommand=vcmd)
                entry.insert(0, "%s.%s" % (row, column))  # default Entry text
                entry.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(entry)
                entry.bind('<Return>', self.onEnter)
                entry.bind('<Down>', self.onEnter)
                entry.bind('<Up>', self.onUp)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def onValidate(self, action, index, value_if_allowed,
                   prior_value, text, validation_type, trigger_type, widget_name):
        # print ('###')
        # print ('action:', action)
        # print ('index:', index)
        # print ('value_if_allowed', value_if_allowed)
        # print('prior_value:', prior_value)
        # print('text:', text)
        # print('validation_type:', validation_type)
        # print('trigger_type:', trigger_type)
        # print('widget_name:', widget_name, '\n')
        m = re.search('(\d{1,10}\.\d{0,10})|(\d{1,10})|(?![\s])', value_if_allowed)
        if m:
            # print (m.group(0))
            if m.group(0) == value_if_allowed:
                return True
            else:
                # print(m.group(0))
                self.bell()
                return False
        else:
            self.bell()
            return False

    def onEnter(self, event):
        nextWidget = event.widget.tk_focusNext().tk_focusNext()
        # print(nextWidget.winfo_class())
        if nextWidget.winfo_class() == 'Button':
            nextWidget = self._widgets[1][2]
        nextWidget.focus()
        nextWidget.select_range(0, 'end')

    def onUp(self, event):
        # fix-minor: Stacks in 1, 2 position
        previousWidget = event.widget.tk_focusPrev().tk_focusPrev()
        # print(previousWidget.winfo_class())
        if previousWidget.winfo_class() != 'Button':
            previousWidget.focus()
            previousWidget.select_range(0, 'end')

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        # widget.configure(text=value)


if __name__ == "__main__":
    app = App()
    app.mainloop()
