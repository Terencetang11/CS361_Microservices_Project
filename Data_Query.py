# Author: Terence Tang
# Project: Life Generator
# Assignment: Sprint 3
# Date: 2/18/2021
# Description:  Methods for managing the data query and sorting/filtering algorithm for the life generator application.
#


import csv
from operator import itemgetter


"""Returns a list of the distinct toy categories available for search"""
def get_toy_categories():
    with open("amazon_co-ecommerce_sample.csv", 'r', encoding="utf8") as csv_data_file:  # Opens data input csv file and parses out the inputs
        csv_reader = csv.reader(csv_data_file)
        headers = next(csv_reader)
        category_index = headers.index("amazon_category_and_sub_category")
        categories = []

        # scans and notes each distinct toy category in the dataset
        for row in csv_reader:
            category = row[8].split(" >")
            if category[0] not in categories:
                categories.append(category[0])

        # sorts the categories for alpha numeric display
        categories.sort()

    csv_data_file.close()
    return categories


"""Returns the headers for the toy dataset"""
def get_data_headers():
    with open("amazon_co-ecommerce_sample.csv", 'r', encoding="utf8") as csv_data_file:  # Opens data input csv file and parses out the inputs
        csv_reader = csv.reader(csv_data_file)
        headers = next(csv_reader)
    csv_data_file.close()
    return headers


"""Returns the results from querying the toy dataset given a category input and # of results desired"""
def generate_results(input_cat, input_rows):
    with open("amazon_co-ecommerce_sample.csv", 'r', encoding="utf8") as csv_data_file:  # Opens data input csv file and parses out the inputs
        csv_reader = csv.reader(csv_data_file)
        headers = next(csv_reader)

        id_index = headers.index("uniq_id")
        reviews_index = headers.index("number_of_reviews")
        ratings_index = headers.index("average_review_rating")
        category_index = headers.index("amazon_category_and_sub_category")

        results = []

        # generates an array holding all records that match the right toy category
        for row in csv_reader:
            toy_category = row[8].split(" >")
            if toy_category[0] == input_cat:
                if row[reviews_index] == '':
                    row[reviews_index] = '0'

                row[reviews_index] = row[reviews_index].replace(',', '')

                row[reviews_index] = int(row[reviews_index])
                results.append(row)

        # sorts by UID and then by # of reviews
        results.sort(key=itemgetter(id_index))
        results.sort(key=itemgetter(reviews_index), reverse=True)

        # takes a subset of overall results
        if len(results) > input_rows * 10:
            results = results[:input_rows * 10]

        # sorts again by UID and then by review ratings
        results.sort(key=itemgetter(id_index))
        results.sort(key=itemgetter(ratings_index), reverse=True)

        # generates the desired number of results
        results = results[:input_rows]

    csv_data_file.close()
    return results


def my_compare(lhs, rhs, index=5):
    # compare by reviews or ratings first
    if lhs[index] < rhs[index]:
        return 1
    elif lhs[index] > rhs[index]:
        return -1

    # if tied, then compare by uid
    elif lhs[index] == rhs[index] and lhs[0] > rhs[0]:
        return 1
    elif lhs[index] == rhs[index] and lhs[0] < rhs[0]:
        return -1
    else:
        return 0


def main():
    # testing data query methods
    # results = get_toy_categories()                                      # runs insertion sort and scans for input file
    # for category in results:
    #     print(category)
    # results = generate_results("Games", 3)
    # for item in results:
    #     print(item)
    # return results
    pass


if __name__ == "__main__":  main()                          # allows for normal run procedure if file ran as script.
