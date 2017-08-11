from __future__ import division   # proper division 5/2 = 2.5

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import os
# import re
import pandas as pd
# import numpy as np
# from scipy.stats import ttest_ind
import csv
from statsmodels.graphics.factorplots import interaction_plot
import matplotlib.pyplot as plt
# from scipy import stats
import operator
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm
from statsmodels.sandbox.stats.multicomp import multipletests


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
        print(dataframe.dtypes)
        dataframe.index += 1
        dataframe.to_csv("data/test_output.csv", quoting=csv.QUOTE_NONNUMERIC)

    def convert_to_int_or_float(self, lst):
        if lst == []:
            return lst
        new_lst = lst
        try:
            i = 0
            for value in new_lst:
                new_lst[i] = int(value)  # If this line throws exception, then the following line(s) of the try
                # block will not execute.
                i += 1
            print('Successfully converted \"%s\" to integer' % (str(lst[0])))
        except ValueError:
            new_lst = lst
            print('Cannot convert \"%s\" to integer' % (str(lst[0])))
            try:
                i = 0
                for value in new_lst:
                    new_lst[i] = float(value)
                    i += 1
                print('Successfully converted \"%s\" to float' % (str(lst[0])))
            except ValueError:
                new_lst = lst
                print('Cannot convert \"%s\" to float' % (str(lst[0])))
        return new_lst

    def create_pandas_DataFrame(self, m_widget):
        data = self.extract_data(m_widget)
        column1_name = m_widget._widgets[0][1]['text']
        column2_name = m_widget._widgets[0][2]['text']
        column3_name = m_widget._widgets[0][3]['text']
        column1 = data[column1_name]
        column2 = data[column2_name]
        column3 = data[column3_name]
        column1 = self.convert_to_int_or_float(column1)
        column2 = self.convert_to_int_or_float(column2)
        column3 = self.convert_to_int_or_float(column3)
        dataSet = list(zip(column1, column2, column3))
        dataframe = pd.DataFrame(data=dataSet, columns=[column1_name, column2_name, column3_name])
        return dataframe

    # ~~~~~~~~~~~~~~~~~~~~~ openFileDialog ~~~~~~~~~~~~~~~~~~~~~~~~
    def openFile(self):
        '''Called when startButton is clicked or via menu'''
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # FILEOPENOPTIONS = dict(defaultextension='.bin',
        #                        filetypes=[('All files', '*.*'), ('Bin file', '*.bin')])
        return tkinter.filedialog.askopenfilename(title='Select a dataset file...', initialdir=dir_path,
                                                  filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])

    def onLoad(self, m_widget, m_rows):
        # Popup dialog in order to select a file:
        fpath = self.openFile()
        # If the filepath is empty, then do nothing
        if fpath == '':
            return

        try:
            # In Linux, maybe I need to open as 'rb', where b stands for binary. (Appending 'b' is useful even on systems
            # that don’t treat binary and text files differently, where it serves as documentation.)
            # https://docs.python.org/2/library/functions.html#open data = pd.read_csv('ToothGrowth.csv') print(data)
            with open(fpath, 'r') as csvfile:
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
        except:
            info = 'Invalid file!\n'
            info += 'The file must have three columns:\n'
            info += '* the first column is the dependent variable\n' \
                    '* the second column is one categorical variable\n' \
                    '* the third column is the other categorical variable'
            tkinter.messagebox.showerror('Statistics', info)

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

    #~~~ splitting a group which has 3 categories ~~~
    def split_group(self, m_c1, m_c2):
        # ~~~ m_c1 the depending variable
        # ~~~ m_c2 the categorical variable
        categories = []  # List of unique categorical values
        for y in m_c2:
            if not y in categories:
                categories.append(y)

        # ~~~ groups for the dependent variable (eg 3) ~~~
        from itertools import repeat
        groups = [[] for i in repeat(None, len(categories))]

        for x, y in zip(m_c1, m_c2):
            for i in range(0, len(categories)):
                if y == categories[i]:
                    groups[i].append(x)
        print('Splitted groups are', groups)
        return groups

    def btnTwoWayAnova_Click(self, m_widget):
        # Create a pandas DataFrame from the GUI table:
        dataframe = self.create_pandas_DataFrame(m_widget)
        # print(dataframe)
        # The table must have at least 3 rows:
        if len(dataframe) < 2:  # number of rows = len(dataframe)
            tkinter.messagebox.showinfo('Two-way ANOVA', 'You must have at least 2 values for each group.')
            return

        # I will use "dependent" for the dependent variable, "twoplus" for the group that has at least 2 variables
        # and "threeplus" for the group that has at least 3 variables

        # print(dataframe.ix[:, 0])  # First column
        # print(dataframe.ix[:, 1])  # Second column
        # print(dataframe.ix[:, 2])  # Third column
        column_names = list(dataframe)  # unsorted
        # unsorted_dict = {0: [len(dataframe.ix[:, 0].unique()), column_names[0]],
        #                  1: [len(dataframe.ix[:, 1].unique()), column_names[1]],
        #                  2: [len(dataframe.ix[:, 2].unique()), column_names[2]]}
        # sorted_dict_list = sorted(unsorted_dict.items(), key=operator.itemgetter(1, 0))
        # print(sorted_dict_list)  # e.g [(1, [2, 'sup']), (2, [3, 'dose']), (0, [43, 'len'])]
        # dependent = dataframe.ix[:, sorted_dict_list[2][0]]  # The dependent variable (with the most unique values)
        # twoplus = dataframe.ix[:, sorted_dict_list[0][0]]  # The variable with the 2 or more unique values
        # threeplus = dataframe.ix[:, sorted_dict_list[1][0]]  # The variable with the 3 or more unique values, subject
        #  to Bonferroni's adjustment
        c1 = dataframe[column_names[0]]
        c2 = dataframe[column_names[1]]
        c3 = dataframe[column_names[2]]

        print(c3[20])

        # statmodels uses R-like model notation.
        # Two-way ANOVA with interactions: formula = 'len ~ C(supp) + C(dose) + C(supp):C(dose)'
        # Two-way ANOVA without interactions: formula = 'len ~ C(supp) + C(dose)'
        # formula = '%s ~ C(%s) + C(%s)' % (sorted_dict_list[2][1][1], sorted_dict_list[0][1][1], sorted_dict_list[1][1][1])
        formula = '%s ~ C(%s) + C(%s)' % (column_names[0], column_names[1], column_names[2])
        print(formula)
        model = ols(formula, dataframe).fit()
        aov_table1 = anova_lm(model, typ=2)
        print(aov_table1)

        # ~~~ Multiple comparisons ~~~
        self.split_group(c1, c3)

        # ~~~ Bonferroni's correction ~~~
        reject, pvals_corrected, alphacSidak, alphacBonf = multipletests(aov_table1.ix[:, 3], method='b')

        # Plots:
        plt.close('all')
        # fig1 = interaction_plot(threeplus, twoplus, dependent, colors=['red', 'blue'], markers=['D', '^'], ms=10)
        # fig2 = sm.qqplot(model.resid, line='s')

        fig, axx = plt.subplots(nrows=2)  # create two subplots, one in each row
        interaction_plot(c3, c2, c1, colors=['red', 'blue'], markers=['D', '^'], ms=10, ax=axx[0])
        sm.qqplot(model.resid, line='s', ax=axx[1])

        plt.tight_layout()
        plt.show()

        # new Form to display the results:
        # frmResults = tk.Tk()
        #
        # w = self.Canvas['width']  # width
        # h = self.Canvas['height']  # height
        #
        # # get screen width and height
        # ws = frmResults.winfo_screenwidth()  # width of the screen
        # hs = frmResults.winfo_screenheight()  # height of the screen
        #
        # # calculate x and y coordinates for the Tk window
        # x = (ws / 2) - (w / 2)
        # y = (hs / 2) - (h / 2)
        #
        # # set the dimensions of the screen
        # # and where it is placed
        # frmResults.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # frmResults.mainloop()



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
