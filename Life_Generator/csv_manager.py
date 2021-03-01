# Author: Terence Tang
# Project: Life Generator
# Assignment: Sprint 4
# Date: 2/28/2021
# Description:  Methods for managing the reading and writing of CSV files for the Life-Generator application
#


import csv
import Life_Generator.Data_Query as data


def read_file_input(file):
    """Reads CSV File Input and generates desired outputs"""
    with open(file, 'r', encoding="utf8") as csv_data_file:
        csv_reader = csv.reader(csv_data_file)
        headers = next(csv_reader)

        toy_data = data.Data()
        results = []
        for row in csv_reader:                          # scans each row in CSV file
            if row[0] == 'toys':                        # checks if top level is toys input
                input_cat = row[1]                      # gets input category
                input_rows = int(row[2])                # gets # of desired results
                query = [[input_cat, input_rows, ''], toy_data.generate_results(input_cat, input_rows)]
                results.append(query)

    csv_data_file.close()
    write_csv_output(results)


def write_csv_output(results):
    """Writes CSV Output file given results and query inputs"""
    with open('output.csv', 'w') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter=',')

        # generates and writes required headers for csv output
        headers = ['input_item_type', 'input_item_category', 'input_number_to_generate', 'content_generator_details',
                   'output_item_name', 'output_item_rating', 'output_item_num_reviews']
        csvwriter.writerow(headers)

        # parses out results and writes the required fields to the csv file
        for query in results:
            input_cat = query[0][0]
            input_rows = query[0][1]
            content = query[0][2]
            for item in query[1]:
                line = ['toys', input_cat, input_rows, content, item[1], item[7], item[5]]
                csvwriter.writerow(line)
    csv_file.close()


def main():
    pass


if __name__ == "__main__":  main()
