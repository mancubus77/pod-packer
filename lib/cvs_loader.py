import csv
import json
from math import floor


def csv_to_json(csv_path):
    json_ds = []
    with open(csv_path) as csv_file:
        csv_r = csv.DictReader(csv_file)
        for row in csv_r:
            json_ds.append(row)
            # json_ds.append(row)

    return json_ds
#     json_array = []
#
#     # read csv file
#     with open(csvFilePath, encoding="utf-8") as csvf:
#         # load csv file data using csv library's dictionary reader
#         csvReader = csv.DictReader(csvf)
#
#         # convert each csv row into python dict
#         for row in csvReader:
#             # add this python dict to json array
#             jsonArray.append(row)
#
#     # convert python jsonArray to JSON String and write to file
#     with open(jsonFilePath, "w", encoding="utf-8") as jsonf:
#         jsonString = json.dumps(jsonArray, indent=4)
#         jsonf.write(jsonString)
#
#
# csvFilePath = r"data.csv"
# jsonFilePath = r"data.json"
# csv_to_json(csvFilePath, jsonFilePath)
