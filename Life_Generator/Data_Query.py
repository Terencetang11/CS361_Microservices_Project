# Author: Terence Tang
# Project: Life Generator
# Assignment: Sprint 4
# Date: 2/28/2021
# Description:  Methods for managing the data query and sorting/filtering algorithm for the life generator application.
#


import csv
from operator import itemgetter


class Data:
    """
    Data object which represents the toy data input provided.  Has methods for getting toy categories, data headers
    and for searching for top toys given a category input and # of desired toys to return.
    """
    def __init__(self):
        self.categories = []
        self.headers = []
        self.data = []
        self.id_index = None
        self.category_index = None
        self.reviews_index = None
        self.ratings_index = None
        self.read_data_csv_file()

    def read_data_csv_file(self):
        """ Opens and reads the data input csv file and moves info to memory for manipulation """
        with open("Life_Generator/amazon_co-ecommerce_sample.csv", 'r', encoding="utf8") as csv_data_file:
            csv_reader = csv.reader(csv_data_file)
            self.headers = next(csv_reader)
            self.set_data_indexes()

            # scans and notes each distinct toy category in the dataset and appends each row to data
            for row in csv_reader:
                self.data.append(row)
                category = row[self.category_index].split(" >")
                if category[0] not in self.categories:
                    self.categories.append(category[0])
            self.categories.sort()

    def set_data_indexes(self):
        """ Sets indexes for columns used in filtering and sorting """
        self.category_index = self.headers.index("amazon_category_and_sub_category")
        self.id_index = self.headers.index("uniq_id")
        self.reviews_index = self.headers.index("number_of_reviews")
        self.ratings_index = self.headers.index("average_review_rating")
        self.category_index = self.headers.index("amazon_category_and_sub_category")

    def get_toy_categories(self):
        """Returns a list of the distinct toy categories available for search"""
        return self.categories

    def get_data_headers(self):
        """Returns the headers for the toy dataset"""
        return self.headers

    def generate_results(self, input_cat, input_rows):
        """Returns the results from querying the toy dataset given a category input and # of results desired"""
        results = self.data[:]

        # filters for all rows which match requested toy category
        results = self.filter_for_toy_category(results, input_cat)

        # Sorts and filters results and returns the desired number of items
        results = self.sort_and_filter_results(results, input_rows)

        return results

    def filter_for_toy_category(self, toy_data, input_cat):
        """ Generates an array holding all records that match the right toy category """
        results = []
        for row in toy_data:
            toy_category = row[self.category_index].split(" >")
            if toy_category[0] == input_cat:
                if row[self.reviews_index] == '':
                    row[self.reviews_index] = '0'

                row[self.reviews_index] = row[self.reviews_index].replace(',', '')

                row[self.reviews_index] = int(row[self.reviews_index])
                results.append(row)

        return results

    def sort_and_filter_results(self, results, input_rows):
        """ Sorts and filters the results to show top results based on # of reviews and avg rating """
        # sorts by UID and then by # of reviews
        results.sort(key=itemgetter(self.id_index))
        results.sort(key=itemgetter(self.reviews_index), reverse=True)

        # takes a subset of overall results
        if len(results) > input_rows * 10:
            results = results[:input_rows * 10]

        # sorts again by UID and then by review ratings
        results.sort(key=itemgetter(self.id_index))
        results.sort(key=itemgetter(self.ratings_index), reverse=True)

        # generates the desired number of results
        results = results[:input_rows]

        return results


def main():
    pass


if __name__ == "__main__":  main()                          # allows for normal run procedure if file ran as script.
