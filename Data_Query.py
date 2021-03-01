# Author: Terence Tang
# Project: Life Generator
# Assignment: Sprint 3
# Date: 2/18/2021
# Description:  Methods for managing the data query and sorting/filtering algorithm for the life generator application.
#


import csv
from operator import itemgetter


class Data:
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
        with open("amazon_co-ecommerce_sample.csv", 'r', encoding="utf8") as csv_data_file:
            csv_reader = csv.reader(csv_data_file)
            self.headers = next(csv_reader)
            self.category_index = self.headers.index("amazon_category_and_sub_category")

            self.id_index = self.headers.index("uniq_id")
            self.reviews_index = self.headers.index("number_of_reviews")
            self.ratings_index = self.headers.index("average_review_rating")
            self.category_index = self.headers.index("amazon_category_and_sub_category")

            # scans and notes each distinct toy category in the dataset
            for row in csv_reader:
                self.data.append(row)
                category = row[self.category_index].split(" >")
                if category[0] not in self.categories:
                    self.categories.append(category[0])
            self.categories.sort()

    """Returns a list of the distinct toy categories available for search"""
    def get_toy_categories(self):
        return self.categories

    """Returns the headers for the toy dataset"""
    def get_data_headers(self):
        return self.headers

    """Returns the results from querying the toy dataset given a category input and # of results desired"""
    def generate_results(self, input_cat, input_rows):
        results = self.data[:]

        # filters for all rows which match requested toy category
        results = self.filter_for_toy_category(results, input_cat)

        # Sorts and filters results and returns the desired number of items
        results = self.sort_and_filter_results(results, input_rows)

        return results

    def filter_for_toy_category(self, toy_data, input_cat):
        """ generates an array holding all records that match the right toy category """
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
