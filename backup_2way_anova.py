from __future__ import division

import tkinter as tk
import tkinter.messagebox
import re
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import csv
from statsmodels.graphics.factorplots import interaction_plot
import matplotlib.pyplot as plt


class App(tk.Tk):
    def __init__(self):
        rows = 100
        columns = 3
        tk.Tk.__init__(self)
        # draw Frame above the table which contains the button
        frame = tk.Frame(self)
        frame.pack(side='top', pady=(0, 5))
        # draw Buttons
        btnTwoWayAnova = tk.Button(frame, text="Two way ANOVA\nwith Bonferroni's", takefocus=False,
                                command=lambda: self.btnTwoWayAnova_Click(t))
        btnTwoWayAnova.pack(side='top')
        # draw Table
        t = SimpleTable(self, rows, columns)
        t.pack(side="top")  # don't fill x
        # menu
        menu = tk.Menu(self)
        self.config(menu=menu)
        submenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Data', menu=submenu)
        submenu.add_command(label='Load', command=lambda: self.onLoad(t, rows))
        submenu.add_command(label='Save', command=lambda: self.onSave(t))

    def onSave(self, m_widget):
        dataframe = self.create_pandas_DataFrame(m_widget)
        dataframe.to_csv("test_output.csv", quoting=csv.QUOTE_NONNUMERIC)

    def create_pandas_DataFrame(self, m_widget):
        data = self.extract_data(m_widget)
        column1_name = m_widget._widgets[0][1]['text']
        column2_name = m_widget._widgets[0][2]['text']
        column3_name = m_widget._widgets[0][3]['text']
        column1 = data[column1_name]
        column2 = data[column2_name]
        column3 = data[column3_name]
        print(type(column1[0]))
        dataSet = list(zip(column1, column2, column3))
        dataframe = pd.DataFrame(data=dataSet, columns=[column1_name, column2_name, column3_name])
        dataframe.index += 1
        return dataframe

    def onLoad(self, m_widget, m_rows):
        # In linux, maybe I need to open as 'rb', where b stands for binary
        # (Appending 'b' is useful even on systems that don’t treat binary and text files differently, where it serves as documentation.)
        # https://docs.python.org/2/library/functions.html#open
        # data = pd.read_csv('ToothGrowth.csv')
        # print(data)
        with open('test_output.csv', 'r') as csvfile:
            datareader = csv.reader(csvfile, delimiter=',', quotechar='\"')
            i = 0
            for row in datareader:
                # print(', '.join(row))

                # name the labels above the table:
                if i == 0:
                    for j in range(1, 4):
                        m_widget._widgets[i][j].config(text=row[j])
                else:
                    # populate the table:
                    for j in range(1, 4):
                        m_widget._widgets[i][j].delete(0, 'end')
                        m_widget._widgets[i][j].insert(0, row[j])
                i = i + 1
                print(row)
            # Populate the rest of the table with zeros:
            # # i count is already +1:
            while i < m_rows + 1:
                # if m_widget._widgets[i][1].winfo_exists():
                for j in range(1, 4):  # for (int j = 1; j < 4; j++)
                    m_widget._widgets[i][j].delete(0, 'end')
                    m_widget._widgets[i][j].insert(0, '')
                # else:
                #     break
                i = i + 1

    def invalid_row(self, strList):
        if ''.join(strList) == '':
            return -1
        elif '' in strList:
            return True
        else:
            return False

    def extract_data(self, m_widget):
        # Scan each row:
        column1 = m_widget._widgets[0][1]['text']
        column2 = m_widget._widgets[0][2]['text']
        column3 = m_widget._widgets[0][3]['text']
        table = {column1: [], column2: [], column3: []}
        for i in range(1, len(m_widget._widgets)):  # range(1, rows)
            row = [m_widget._widgets[i][1].get(), m_widget._widgets[i][2].get(), m_widget._widgets[i][3].get()]
            invalid_row = self.invalid_row(row)
            if invalid_row == True:
                tkinter.messagebox.showinfo('Statistics', 'You can\'t have both empty and non-empty values in a row!')
                return False
            elif invalid_row == -1:
                break
            else:
                table[column1].append(row[0])
                table[column2].append(row[1])
                table[column3].append(row[2])
        print(table)
        return table

    def btnTwoWayAnova_Click(self, m_widget):
        # Create a pandas DataFrame from the GUI table:
        dataframe = self.create_pandas_DataFrame(m_widget)
        print(dataframe)
        # The table must have at least 3 rows:
        if len(dataframe) < 2:  # number of rows = len(dataframe)
            tkinter.messagebox.showinfo('Two-way ANOVA', 'You must have at least 2 values for each group.')
        # I HAVE THE CONVERT SOME VALUES TO FLOAT64!!
        fig = interaction_plot(dataframe.dose, dataframe.supp, dataframe.len, colors=['red', 'blue'], markers=['D', '^'], ms=10)
        plt.show()


class SimpleTable(tk.Canvas):
    def __init__(self, parent, rows=10, columns=2):
        # 'self' means tk.Canvas!
        # use black background so it "peeks through" to
        # form grid lines
        ### canvas begin
        tk.Canvas.__init__(self, parent, height=450, highlightthickness=0)  # a canvas in the parent object
        frame = tk.Frame(self, background="lightblue", padx=1, pady=1)  # a frame in the canvas
        # a scrollbar in the parent
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=self.yview)
        # connect the canvas to the scrollbar
        self.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")  # comment out this line to hide the scrollbar
        self.pack(side="left", fill="both", expand=True)  # pack the canvas
        # make the frame a window in the canvas
        self.create_window((4, 4), window=frame, anchor="nw", tags="frame")
        # bind the frame to the scrollbar
        frame.bind("<Configure>", lambda x: self.configure(scrollregion=self.bbox("all")))
        # parent.bind("<Down>", lambda x: self.yview_scroll(3, 'units'))  # bind "Down" to scroll down
        # parent.bind("<Up>", lambda x: self.yview_scroll(-3, 'units'))  # bind "Up" to scroll up
        # bind the mousewheel to scroll up/down
        parent.bind("<MouseWheel>", lambda x: self.yview_scroll(int(-1 * (x.delta / 40)), "units"))
        ### canvas end
        self._widgets = []

        for row in range(rows + 1):
            current_row = []
            for column in range(columns + 1):
                if (row == 0) | (column == 0):
                    labelText = row | column
                    if labelText == 0:
                        labelText = ''
                    label = tk.Label(frame, borderwidth=0, width=5, text=labelText)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)
                    continue
                entry = tk.Entry(frame, borderwidth=0, width=22)
                # entry.insert(0, "%s.%s" % (row, column))  # default Entry text
                entry.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(entry)
                entry.bind('<Return>', self.onEnter)
                entry.bind('<Down>', self.onEnter)
                entry.bind('<Up>', self.onUp)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)
        # print(frame['padx'])
        # print(self._widgets[1][0]['width'])
        # print(self._widgets[1][1]['width'])
        # print(self._widgets[1][2]['width'])
        self.config(width=450)  # change the width of the canvas

    def onEnter(self, event):
        nextWidget = event.widget.tk_focusNext().tk_focusNext().tk_focusNext()  # 3 focusnext for 3 columns
        # print(nextWidget.winfo_class())
        # if nextWidget.winfo_class() == 'Button':
        #     nextWidget = self._widgets[1][2]
        nextWidget.focus()
        nextWidget.select_range(0, 'end')

    def onUp(self, event):
        # fix-minor: Stacks in 1, 2 position
        previousWidget = event.widget.tk_focusPrev().tk_focusPrev().tk_focusPrev()  # 3 focusPrev for 3 columns
        # print(previousWidget.winfo_class())
        # if previousWidget.winfo_class() != 'Button':
        previousWidget.focus()
        previousWidget.select_range(0, 'end')

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        # widget.configure(text=value)


if __name__ == "__main__":
    app = App()
    app.mainloop()
