from __future__ import division   # proper division 5/2 = 2.5

from ach_multiple_comparisons import multiple_comparisons_with_bonferroni
import ach_generic
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import os
import re
import pandas as pd
# import numpy as np
# from scipy.stats import ttest_ind
import csv
from statsmodels.graphics.factorplots import interaction_plot
import matplotlib.pyplot as plt
# from scipy import stats
# import operator
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm
# from statsmodels.sandbox.stats.multicomp import multipletests


# Change App -> self.verbose = True for debugging.

class App(tk.Tk):
    def __init__(self):
        rows = 200
        columns = 3
        self.settings_string_list = None
        self.verbose = False
        tk.Tk.__init__(self)
        # draw Frame above the table which contains the button
        frame = tk.Frame(self)
        frame.pack(side='top', pady=(0, 5))
        # draw Buttons
        btnTwoWayAnova = tk.Button(frame, text="Two way ANOVA\nwith Bonferroni's correction", takefocus=False,
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
        if dataframe.empty:
            return
        # print(dataframe.dtypes)

        # ~~~ The Wizard saves settings between first and subsequent dialogs ~~~
        # wiz = ach_generic.LoadWizard(self, self.settings_string_list)
        # self.settings_string_list = wiz.result
        # if self.settings_string_list is None:
        #     return
        #
        # wiz_settings = {'title': self.settings_string_list[0],
        #                 'delimiter': self.settings_string_list[1],
        #                 'qualifier': self.settings_string_list[2]}

        # ~~~ saveFileDialog ~~~
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fpath = tkinter.filedialog.asksaveasfilename(title='Select a dataset file...', initialdir=dir_path,
                                                     initialfile='dataset1.csv',
                                                     filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
        if fpath == '':
            return

        dataframe.index += 1
        # dataframe.to_csv(fpath, sep=wiz_settings['delimiter'], quotechar=wiz_settings['qualifier'],
        #                  header=['a', 'b', 'c'], quoting=csv.QUOTE_NONNUMERIC)
        dataframe.to_csv(fpath, sep=',', quotechar='\"', header=True, quoting=csv.QUOTE_NONNUMERIC)

    def convert_to_float(self, m_list):
        if m_list is []:
            return m_list
        new_list = m_list
        try:
            i = 0
            for x in new_list:
                new_list[i] = float(x)
                i += 1

            if self.verbose:
                print('Successfully converted \"%s\" to float' % (str(m_list[0])))
        except ValueError:
            new_list = m_list
            if self.verbose:
                print('Cannot convert \"%s\" to float; keeping string' % (str(m_list[0])))
        return new_list

    def create_pandas_DataFrame(self, m_widget):
        data = self.extract_data(m_widget)
        if data == -1:
            return pd.DataFrame()
        else:
            column1_name = m_widget._widgets[0][1]['text']
            column2_name = m_widget._widgets[0][2]['text']
            column3_name = m_widget._widgets[0][3]['text']
            column1 = data[column1_name]
            column2 = data[column2_name]
            column3 = data[column3_name]
            column1 = self.convert_to_float(column1)
            column2 = self.convert_to_float(column2)
            column3 = self.convert_to_float(column3)
            dataSet = list(zip(column1, column2, column3))
            dataframe = pd.DataFrame(data=dataSet, columns=[column1_name, column2_name, column3_name])
            return dataframe

    # ~~~~~~~~~~~~~~~~~~~~~ openFileDialog ~~~~~~~~~~~~~~~~~~~~~~~~
    def openFile(self):
        ''' Called when startButton is clicked or via menu '''
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return tkinter.filedialog.askopenfilename(title='Select a dataset file...', initialdir=dir_path,
                                                  filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])

    def onLoad(self, m_widget, m_rows):
        # Popup dialog in order to select a file:
        fpath = self.openFile()
        # If the filepath is empty, then do nothing
        if fpath == '':
            return

        # ~~~ The Wizard saves settings between first and subsequent dialogs ~~~
        wiz = ach_generic.LoadWizard(self, self.settings_string_list)
        self.settings_string_list = wiz.result
        if self.settings_string_list is None:
            return

        wiz_settings = {'title': self.settings_string_list[0],
                        'delimiter': self.settings_string_list[1],
                        'qualifier': self.settings_string_list[2]}

        try:
            # In Linux, maybe I need to open as 'rb', where b stands for binary. (Appending 'b' is useful even on
            # systems that don’t treat binary and text files differently, where it serves as documentation.)
            # https://docs.python.org/2/library/functions.html#open data = pd.read_csv('ToothGrowth.csv') print(data)
            with open(fpath, 'r') as csvfile:
                datareader = csv.reader(csvfile,
                                        delimiter=wiz_settings['delimiter'], quotechar=wiz_settings['qualifier'])
                i = 0
                for row in datareader:
                    # print(', '.join(row))
                    # name the labels above the table:
                    if i == 0:
                        # ~~~ Fill in the labels (column names) ~~~
                        if wiz_settings['title'] == 'Yes':
                            for j in range(1, 4):
                                m_widget._widgets[0][j].config(text=row[j])
                        else:
                            i += 1
                            for j in range(1, 4):
                                m_widget._widgets[0][j].config(text='column_' + str(j))
                                m_widget._widgets[i][j].delete(0, 'end')
                                m_widget._widgets[i][j].insert(0, row[j])
                    else:
                        # populate the table:
                        for j in range(1, 4):
                            m_widget._widgets[i][j].delete(0, 'end')
                            m_widget._widgets[i][j].insert(0, row[j])
                    i += 1
                    if self.verbose:
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
            self.settings_string_list = None
            info = 'Invalid file!\n'
            info += 'The file must have three columns:\n'
            info += '* the first column is the dependent variable\n' \
                    '* the second column is one categorical variable\n' \
                    '* the third column is the other categorical variable'
            tkinter.messagebox.showerror('Statistics', info)

    def invalid_row(self, strList):
        # ~~~ ''.join(strList) concatenates all the list values ~~~
        if ''.join(strList) == '':
            # ~~~ if all the list values are empty ~~~
            return -1
        elif '' in strList:
            # ~~~ if the list contains an empty string ~~~
            return 1
        else:
            return 0

    def extract_data(self, m_widget):
        # Scan each row:
        column1 = m_widget._widgets[0][1]['text']
        column2 = m_widget._widgets[0][2]['text']
        column3 = m_widget._widgets[0][3]['text']
        table = {column1: [], column2: [], column3: []}
        for i in range(1, len(m_widget._widgets)):  # range(1, rows)
            row = [m_widget._widgets[i][1].get(), m_widget._widgets[i][2].get(), m_widget._widgets[i][3].get()]
            invalid_row = self.invalid_row(row)
            # if invalid_row == -2:
            #     info = 'Please check your data.\n'
            #     info += 'Ensure that your decimal values have a comma as a decimal mark.'
            #     tkinter.messagebox.showerror('Statistics', info)
            #     return -1
            if invalid_row == 1:
                tkinter.messagebox.showinfo('Statistics', 'You can\'t have both empty and non-empty values in a row!')
                return -1
            elif invalid_row == -1:
                if i == 1:  # if the first row is empty:
                    return -1
                break
            else:
                table[column1].append(row[0])
                table[column2].append(row[1])
                table[column3].append(row[2])
        if self.verbose:
            print(table)
        return table

    def create_bonferroni_dataframe(self, m_p_values, m_corresponding_groups):
        pretty_cor_grps = []  # just changing the output string
        for x in m_corresponding_groups:
            str_ = '%s and %s' % (str(x[0]), str(x[1]))
            pretty_cor_grps.append(str_)
        pretty_p_v_cor = []  # just changing the output string
        for x in m_p_values:
            rounded = round(x, 3)
            if rounded < 0.001:
                pretty_p_v_cor.append('< 0.001')
            else:
                pretty_p_v_cor.append(str(rounded))
        dataset_bon = list(zip(pretty_cor_grps, pretty_p_v_cor))
        row_names = [''] * len(m_corresponding_groups)
        return pd.DataFrame(data=dataset_bon, columns=['Groups', 'p-value'], index=row_names)

    def btnTwoWayAnova_Click(self, m_widget):
        # Create a pandas DataFrame from the GUI table:
        dataframe = self.create_pandas_DataFrame(m_widget)
        if dataframe.empty:
            return
        # print(dataframe)
        # The table must have at least 3 rows:
        if len(dataframe) < 3:  # number of rows = len(dataframe)
            tkinter.messagebox.showinfo('Two-way ANOVA', 'You must have at least 3 values for each group.')
            return

        # I will use "dependent" for the dependent variable, "twoplus" for the group that has at least 2 variables
        # and "threeplus" for the group that has at least 3 variables

        # print(dataframe.ix[:, 0])  # First column
        column_names = list(dataframe)  # unsorted
        # ~~~ Each column name must start with a letter! ~~~
        pattern = re.compile(r'^[a-z]')
        try:
            for x in column_names:
                m = re.search(pattern, x)
                # ~~~ If m doesn't exist, it's because a variable name doesn't begin with a-z or A-Z, thus the assertion
                # fails.
                assert m
        except:
            dataframe.columns = ['column_1', 'column_2', 'column_3']
            column_names = list(dataframe)

        # ~~~ Launch the two-way ANOVA wizard ~~~
        wiz = ach_generic.TwoWayAnovaWizard(self, settings=tuple(x for x in column_names))
        if wiz.result is None:  # The user presses Cancel
            return
        dependent_var = wiz.result[0]  # just the column name
        posthoc_var = wiz.result[1]  # just the column name
        # ~~~ Get the other two variables from the column_names list ~~~
        temp_list = [str(x) for x in column_names if not str(x) == dependent_var]
        second_var = temp_list[0]
        third_var = temp_list[1]
        if not dataframe.dtypes[dependent_var] == float:
            tk.messagebox.showerror('Statistics', 'The dependent variable must be continuous')
            return

        # statmodels uses R-like model notation.
        # Two-way ANOVA with interactions: formula = 'len ~ C(supp) + C(dose) + C(supp):C(dose)'
        # Two-way ANOVA without interactions: formula = 'len ~ C(supp) + C(dose)'
        formula = '%s ~ C(%s) + C(%s)' % (dependent_var, second_var, third_var)
        # print(formula)
        model = ols(formula, dataframe).fit()
        aov_table1 = anova_lm(model, typ=2)
        # print('\n~~~ Two-way ANOVA without interactions ~~~')
        # print(aov_table1)
        results_string = ''
        results_string += '\n~~~ Two-way ANOVA without interactions ~~~\n'
        results_string += formula + '\n'
        results_string += aov_table1.to_string()
        results_string += '\n'

        # ~~~ Bonferroni's correction ~~~
        if not posthoc_var == '':
            # ~~~ 1st variable: dependent_var, 2nd variable: c2_var, 3rd variable: posthoc_var ~~~
            c2_var = [x for x in column_names if not x in [dependent_var, posthoc_var]][0]
            second_var = c2_var
            third_var = posthoc_var
            c1 = dataframe[dependent_var]
            c2 = dataframe[second_var]
            c3 = dataframe[third_var]
            # assert column c3 had at least 3 unique values
            if len(c3.unique()) < 3:
                info = 'Post hoc test \'Bonferroni\' should have at least 3 values in column \'%s\'' % posthoc_var
                tk.messagebox.showerror('Statistics', info)
            else:
                row_names = [''] * len(c3.unique())
                p_v_cor, corresponding_groups = multiple_comparisons_with_bonferroni(c1, c3)
                dataframe_bon = self.create_bonferroni_dataframe(p_v_cor, corresponding_groups)
                # print('\n~~~ Post hoc test: Multiple comparisons with Bonferroni correction ~~~')
                # print(dataframe_bon)
                results_string += '\n~~~ Post hoc test: Multiple comparisons with Bonferroni correction ~~~\n'
                results_string += dataframe_bon.to_string()
        else:
            c1 = dataframe[dependent_var]
            c2 = dataframe[second_var]
            c3 = dataframe[third_var]



        # Plots:
        plt.close('all')
        # fig1 = interaction_plot(threeplus, twoplus, dependent, colors=['red', 'blue'], markers=['D', '^'], ms=10)
        # fig2 = sm.qqplot(model.resid, line='s')

        # ~~~ plotting fails when posthoc_var is 'supp' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # fig, axx = plt.subplots(nrows=2)  # create two subplots, one in each row
        # interaction_plot(c3, c2, c1, colors=['red', 'blue'], markers=['D', '^'], ms=10, ax=axx[0])
        # sm.qqplot(model.resid, line='s', ax=axx[1])
        plots = []
        try:
            plot1 = interaction_plot(c3, c2, c1, colors=['red', 'blue'], markers=['D', '^'], ms=10)
            plots.append(plot1)
        except Exception as e:
            print('Error in plot1:', str(e))

        # plt.show()

        # Scatter plot
        # plt.figure()
        # if c3.dtypes == float:
        #     plt.scatter(c3, c1, color='red')
        # else:
        #     # Convert categorical variables to numbers
        #     from sklearn.preprocessing import LabelEncoder
        #     labelencoder = LabelEncoder()
        #     c3_encoded = labelencoder.fit_transform(c3)
        #     plt.scatter(c3_encoded, c1, color='red')
        # plt.title('Outliers')

        # Boxplot
        try:
            fig_boxplot = plt.figure()
            temp = []
            for i in range(len(c3.unique())):
                temp2 = c1[c3 == c3.unique()[i]]
                temp.append(temp2)
            plt.boxplot(temp)
            plt.title('Outlier detection', figure=fig_boxplot)
            plt.xlabel(third_var, figure=fig_boxplot)
            plt.ylabel(dependent_var, figure=fig_boxplot)
            plots.append(fig_boxplot)
        except Exception as e:
            print('Error in Boxplot:', str(e))

        results_popup = ach_generic.ResultsPopup(self, settings=results_string, plots=plots)
        # plt.show()


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
                entry.bind('<Shift-Return>', self.onUp)
                # entry.bind('<FocusOut>', self.lost_focus)
            self._widgets.append(current_row)

        self._widgets[0][1]['text'] = 'column_1'
        self._widgets[0][2]['text'] = 'column_2'
        self._widgets[0][3]['text'] = 'column_3'

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


def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
