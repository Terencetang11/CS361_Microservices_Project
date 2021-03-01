# Author: Terence Tang
# Project: Life Generator
# Assignment: Sprint 4
# Date: 2/28/2021
# Description:  GUI Application for building out the graphical user interface portion of the life generator application
#

from tkinter import *
from tkinter import ttk
import Life_Generator.Data_Query as data
import Life_Generator.csv_manager as csv


class GUI:
    """
    GUI Application for the Life-Generator app.  Provides a gui window with instructions and fields to provide inputs
    for toy categories and # of desired search results.
    """
    def __init__(self, root, process, request_queue, receive_queue):
        self.root = root
        self.mainframe = Frame(self.root)
        self.root.title("Life Generator")

        self.toy_data = data.Data()

        self.p1 = process
        self.request_queue = request_queue
        self.receive_queue = receive_queue

        # define frame parameters and sizing
        self.mainframe = ttk.Frame(root, padding="50 30 50 30")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # display instructions for life generator
        welcome = "Welcome to the Life Generator app!"
        instructions = "Instructions: Please enter a toy category and the desired number of results, and " \
                       "we'll display the top toys for your selection."

        ttk.Label(self.mainframe, text=welcome).grid(column=2, row=0, columnspan=3, sticky=W)
        ttk.Label(self.mainframe, text=instructions).grid(column=2, row=1, columnspan=3, sticky=W)

        # define toy categories drop-down
        self.toy_categories = self.toy_data.get_toy_categories()

        self.cat_input = StringVar(self.mainframe)
        self.cat_input.set(self.toy_categories[1]) # default value

        self.cat_dropdown = OptionMenu(self.mainframe, self.cat_input, *self.toy_categories)
        self.cat_dropdown.grid(column=3, row=2, sticky=(W, E))
        ttk.Label(self.mainframe, text="Enter a Toy Category").grid(column=2, row=2, sticky=E)

        # define integer input for # of desired records returned
        self.rows = IntVar()
        self.rows_entry = ttk.Entry(self.mainframe, width=10, textvariable=self.rows)
        self.rows_entry.grid(column=3, row=3, sticky=(W, E))
        ttk.Label(self.mainframe, text="Enter # of Results Desired").grid(column=2, row=3, sticky=E)

        # define search button and it's call to the earch function
        ttk.Button(self.mainframe, text="Search", command=self.search).grid(column=4, row=3, sticky=W)

        # define output display area and builds table using tkinter treeview object
        self.headers = self.toy_data.get_data_headers()

        self.data_display = ttk.Treeview(self.mainframe, selectmode="browse", columns=self.headers, show='headings')
        for i in range(len(self.headers)):
            self.data_display.heading(self.headers[i], text=self.headers[i])
            self.data_display.column(i, anchor="center", width=40, minwidth=100)

        self.data_display.grid(row=4, rowspan=10, column=2, columnspan=3, padx=10, pady=3, sticky=NSEW)

        # define scrollbars for the data display widget
        self.vsb = ttk.Scrollbar(self.mainframe, orient="vertical", command=self.data_display.yview)
        self.vsb.grid(row=4, column=4, sticky=NE)

        self.hsb = ttk.Scrollbar(self.mainframe, orient="horizontal", command=self.data_display.xview)
        self.hsb.grid(row=14, column=2, sticky=SW)

        self.data_display.configure(yscrollcommand=self.vsb.set)
        self.data_display.configure(xscrollcommand=self.hsb.set)

        # general padding of widgets in mainframe
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=10, pady=5)

        # sets keyboard focus and allows for use of <Return> key
        self.cat_dropdown.focus()
        self.root.bind("<Return>", self.search)

    def search(self, *args):
        try:
            self.data_display.delete(*self.data_display.get_children())
            input_rows = int(self.rows.get())
            input_cat = str(self.cat_input.get())

            self.request_queue.put(self.get_input_content(input_cat))           # sends data to content-gen microservice
            content = self.receive_queue.get()                                  # receives input from content-generator
            results = self.toy_data.generate_results(input_cat, input_rows)     # toy results from Life Generator

            # writes data to data display widget of GUI
            for row in range(len(results)):
                self.data_display.insert("", "end", values=results[row])

            # readies results to get written in output csv format
            query = [[input_cat, input_rows, content], results]
            csv.write_csv_output([query])

        except ValueError:  # error handling for input csv files, does not break program if invalid inputs provided
            pass

    def get_input_content(self, string):
        string = string.replace(',', '')
        string = string.replace('&', '')
        string = string.split()[:2]
        if len(string) == 1:
            string.append(string[0])
        return string


def main():
    root = Tk()
    app = GUI(root)
    root.mainloop()


if __name__ == "__main__":  main()  # allows for normal run procedure if file ran as script.
