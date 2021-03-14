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
        instructions = "Instructions: \n" \
                       "Please select a toy category and enter the desired number of results, and " \
                       "we'll display the top toys for your selection.\n" \
                       "For more instructions, please click on the additional details button!"

        ttk.Label(self.mainframe, text=welcome).grid(column=2, row=0, columnspan=3, sticky=W)
        ttk.Label(self.mainframe, text=instructions, wraplength=750).grid(column=2, row=1, columnspan=3, sticky=W)
        self.more_info_label = ttk.Label(self.mainframe, wraplength=750)
        self.more_info_label.grid(column=2, row=2, columnspan=3, sticky=W)

        # define more info button and it's call to the more info function
        self.info_btn = ttk.Button(self.mainframe, text="Additional Details", command=self.generate_details)
        self.info_btn.grid(column=2, row=2, sticky=W)

        # define toy categories drop-down
        self.toy_categories = self.toy_data.get_toy_categories()

        self.cat_input = StringVar(self.mainframe)
        self.cat_input.set(self.toy_categories[1]) # default value

        self.cat_dropdown = OptionMenu(self.mainframe, self.cat_input, *self.toy_categories)
        self.cat_dropdown.grid(column=3, row=4, sticky=(W, E))
        ttk.Label(self.mainframe, text="Enter a Toy Category").grid(column=2, row=4, sticky=E)

        # define integer input for # of desired records returned
        self.rows = IntVar()
        self.rows_entry = ttk.Entry(self.mainframe, width=10, textvariable=self.rows)
        self.rows_entry.grid(column=3, row=5, sticky=(W, E))
        ttk.Label(self.mainframe, text="Enter # of Results Desired").grid(column=2, row=5, sticky=E)

        # define search button and it's call to the search function
        ttk.Button(self.mainframe, text="Search", command=self.search).grid(column=4, row=5, sticky=W)

        # define output display area and builds table using tkinter treeview object
        self.headers = self.toy_data.get_data_headers()

        self.data_display = ttk.Treeview(self.mainframe, selectmode="browse", columns=self.headers, show='headings')
        for i in range(len(self.headers)):
            self.data_display.heading(self.headers[i], text=self.headers[i])
            self.data_display.column(i, anchor="center", width=40, minwidth=100)

        self.data_display.grid(row=6, rowspan=10, column=2, columnspan=3, padx=10, pady=3, sticky=NSEW)

        # define scrollbars for the data display widget
        self.vsb = ttk.Scrollbar(self.mainframe, orient="vertical", command=self.data_display.yview)
        self.vsb.grid(row=6, column=4, sticky=NE)

        self.hsb = ttk.Scrollbar(self.mainframe, orient="horizontal", command=self.data_display.xview)
        self.hsb.grid(row=16, column=2, sticky=SW)

        self.data_display.configure(yscrollcommand=self.vsb.set)
        self.data_display.configure(xscrollcommand=self.hsb.set)

        # define content generator display area for query results
        cg_title = "*NEW* Content Generator Results - Get an informational paragraph on your search topic:"
        ttk.Label(self.mainframe, text=cg_title).grid(row=18, column=2, columnspan=3, sticky=W)
        self.cg_results = ttk.Label(self.mainframe, text='Start a search to get results...')
        self.cg_results.grid(row=19, column=2, columnspan=3, sticky=W)

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

            content_request = self.get_input_content(input_cat)
            print("Requesting data from Content-Generator with the following input: " + str(content_request))
            self.request_queue.put(self.get_input_content(input_cat))           # sends data to content-gen microservice
            content = self.receive_queue.get()                                  # receives input from content-generator
            print("Content Generated: " + str(content))
            results = self.toy_data.generate_results(input_cat, input_rows)     # toy results from Life Generator

            # writes data to data display widget of GUI
            for row in range(len(results)):
                self.data_display.insert("", "end", values=results[row])

            # destroys and rewrites content generator content to display
            self.cg_results.destroy()
            self.cg_results = ttk.Label(self.mainframe, text=content, wraplength=750)
            self.cg_results.grid(row=19, column=2, columnspan=3, sticky=W)

            # readies results to get written in output csv format
            query = [[input_cat, input_rows, content], results]
            csv.write_csv_output([query])

        except ValueError:  # error handling for input csv files, does not break program if invalid inputs provided
            pass

    def generate_details(self):
        """ Updates additional_details button to function as a hide_details button and displays details text """
        self.info_btn.config(text="Hide Details", command=self.hide_details)
        self.info_btn.grid(column=2, row=3, sticky=W)
        more_info = "Each search will generate results which will be displayed in the table below as well as " \
                    "updating a CSV formatted output file named output.csv in this program's local directory.\n\n" \
                    "This program also provides the advanced ability to enter multiple search inputs at once via " \
                    "a provided input file during program run-time.  Use of this feature requires knowledge of how" \
                    " to run python programs via a console or terminal and a formatted input.csv file. \n" \
                    "Required format for input.csv (with header): input_item_type, input_item_category," \
                    "input_number_to_generate, where input_item_type=toys." \
                    "\n"
        self.more_info_label.config(text=more_info)

    def hide_details(self):
        """ Updates hide_details button to function as show additional_details button and hides details text """
        self.info_btn.config(text="Additional Details", command=self.generate_details)
        self.info_btn.grid(column=2, row=2, sticky=W)
        self.more_info_label.config(text='')

    def get_input_content(self, string):
        """ Formats string of toy categories to be sent to the content generator microservice."""
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
