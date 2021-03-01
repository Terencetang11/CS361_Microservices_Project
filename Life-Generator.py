# Author: Terence Tang
# Project: Life Generator
# Assignment: Sprint 3
# Date: 2/18/2021
# Description:  Methods for managing the reading and writing of CSV files for the Life-Generator application


import sys
import GUI_App as gui
import csv_manager as csv
import Data_Query as data
import multiprocessing
import content_generator_microservice as cg
import random


def life_generator_microservice(request, receive):
    """For calls made to the Life Generator microservice, provides a tuple of single word strings of toy categories"""
    categories = data.get_toy_categories()
    formatted_categories = generate_output_for_content_generator(categories)

    # while there are requests in the request queue, provide a random toy category
    while True:
        requested_results = request.get()
        for i in range(requested_results):
            num = random.randrange(1, len(formatted_categories))
            receive.put(formatted_categories[num])
    return


def generate_output_for_content_generator(categories):
    """Cleans up toy category data into a tuple of single words representing toy categories"""
    category_list = []

    # removes all ',' and '&' chars from list of toy categories
    for cat in categories:
        results = cat
        results = results.replace(",", "")
        results = results.replace("&", "")
        results = results.split()[:2]
        if len(results) == 1:
            results.append(results[0])
        category_list.append(results)

    return category_list


def main():
    request_list = multiprocessing.Queue()
    receive_list = multiprocessing.Queue()
    content_generator = multiprocessing.Process(target=cg.CG, args=(request_list, receive_list))
    content_generator.start()

    try:
        # check if input csv file provided
        input = sys.argv[1]
        csv.read_file_input(input)

    except IndexError:
        # if no input provided, launch GUI application
        root = gui.Tk()
        app = gui.GUI(root, content_generator, request_list, receive_list)
        root.mainloop()

    content_generator.terminate()


if __name__ == "__main__":  main()
