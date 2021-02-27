# Author: Terence Tang
# Project: Life Generator
# Assignment: Sprint 3
# Date: 2/18/2021
# Description:  Methods for managing the reading and writing of CSV files for the Life-Generator application



import sys
import GUI_App as gui
import csv_manager as csv
import multiprocessing
import test     # update to content generator


def main():
    request_list = multiprocessing.Queue()
    receive_list = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=test.test_send, args=(request_list, receive_list))      # needs fx name update!
    p1.start()

    try:
        # check if input csv file provided
        input = sys.argv[1]
        csv.read_file_input(input)

    except IndexError:
        # if no input provided, launch GUI application
        root = gui.Tk()
        app = gui.GUI(root, p1, request_list, receive_list)
        root.mainloop()
        p1.terminate()


if __name__ == "__main__":  main()                          # allows for normal run procedure if file ran as script.
