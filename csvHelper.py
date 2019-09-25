import csv
import datetime
import re


def validatedateStr(date_text, date_format="%d-%b-%Y"):
    try:
        datetime.datetime.strptime(date_text, date_format)
        return True
    except ValueError:
        return False


def getcsvdata(file_path):
    with open(file_path) as csvfile:
        data = []
        lines = csv.reader(csvfile)
        first_row = True
        for row in lines:
            if first_row:
                first_row = False
                if not re.match(r"^-?\d*.\d*$", row[2]):
                    continue
            data.append(row)
        return data


def analyzecsvdata(data):
    invalid_shape_error = 0
    invalid_date_error = 0
    invalid_price_error = 0
    negative_price_warning = 0
    for row in data:
        reduced_row = [i for i in row if i]
        if len(reduced_row) != 3:
            invalid_shape_error += 1
        if not validatedateStr(row[1]):
            invalid_date_error += 1
        if not re.match(r"^-?\d*.\d*$", row[2]):
            invalid_price_error += 1
        elif float(row[2]) < 0:
            negative_price_warning += 1

    if invalid_shape_error > 0:
        print("The shape of the CSV is not Proper, there is " + str(
            invalid_shape_error) + " row(s) with incorrect number of columns")
    if invalid_date_error > 0:
        print("There is " + str(invalid_date_error) + " row(s) which have the Date in not proper format")
    if invalid_price_error > 0:
        print("There is " + str(invalid_price_error) + " row(s) which have the Price in not proper format")
    if negative_price_warning > 0:
        print("There is " + str(negative_price_warning) + " instance(s) where the Price has reduced below zero, stock "
                                                          "prices should not be in negative")

    total_errors = invalid_shape_error + invalid_date_error + invalid_price_error
    if total_errors == 0:
        return True
    return False
