import datetime
import sys
import csv
import os
import tabCompleter
import readline
import difflib


# CSV FilePath Input Logic Start

def getcsvfileinput(firstexecution=False):
    if (len(sys.argv)) >= 2 and firstexecution:
        if (len(sys.argv)) > 2:
            print("Additional Arguments passed will be ignored.")
        file_path = sys.argv[1]
    else:
        print("Enter the FilePath for CSV of Stocks")
        file_path = str(input())
    return file_path


def iscsvfilevalid(file_path):
    if not os.path.isfile(file_path):
        return False
    with open(file_path) as csvfile:
        try:
            lines = csv.reader(csvfile)
            for row in lines:
                reduced_row = [i for i in row if i]
                if len(row) != 3 or len(reduced_row) != 3:
                    return False
            return True
        except:
            return False

    return True


def getcsvfilepath():
    file_path = getcsvfileinput(True)
    while True:
        if not file_path:
            print('This is a required field, Please try again')
            file_path = getcsvfileinput()
        elif not iscsvfilevalid(file_path):
            print('The given FilePath or CSV File Structure is not Valid, Please try again')
            file_path = getcsvfileinput()
        else:
            break
    return file_path


# CSV FilePath Input Logic End

# Search Stock Name Input Logic Start

def getsearchstocknameinput(available_stocks):
    t = tabCompleter.tabCompleter()
    t.createListCompleter(available_stocks)

    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")

    readline.set_completer(t.listCompleter)
    print("Enter the Stock to Search: (Hint: Use Tab for Autocomplete)")
    search_stock = input()
    return search_stock


def getsearchstockname(available_stocks):
    search_stock = getsearchstocknameinput(available_stocks)
    while True:
        if not search_stock in available_stocks:
            closest_diff_match = difflib.get_close_matches(search_stock, available_stocks, 1)
            if closest_diff_match:
                print("Do you mean " + str(closest_diff_match[0]) + "? (y/n)")
                use_closest_choice = input()
                if use_closest_choice == 'y':
                    search_stock = closest_diff_match[0]
                else:
                    print("Invalid Input, Please try again")
                    search_stock = getsearchstocknameinput(available_stocks)
            else:
                print("Invalid Stock Name Entered, Please try again")
                search_stock = getsearchstocknameinput(available_stocks)
        else:
            break

    return search_stock


# Search Stock Name Input Logic End

# Start Date Input Logic Start

def getstartdateinput():
    print('Enter the Start date in DD-MM-YYYY format')
    date_entry = input()
    try:
        day, month, year = map(int, date_entry.split('-'))
        _ = datetime.date(day=day, month=month, year=year)
        return day, month, year
    except:
        return False, False, False


def getstartdate():
    day, month, year = getstartdateinput()
    while True:
        if not day or not month or not year:
            print("Invalid Input, Please try again")
            day, month, year = getstartdateinput()
        elif datetime.date(day=day, month=month, year=year) >= datetime.date.today():
            print("Search Start Date cannot be of future")
            day, month, year = getstartdateinput()
        else:
            break
    return day, month, year


# Start Date Input Logic End

# End Date Input Logic Start

def getendtdateinput():
    print('Enter the End date in DD-MM-YYYY format')
    date_entry = input()
    try:
        day, month, year = map(int, date_entry.split('-'))
        _ = datetime.date(day=day, month=month, year=year)
        return day, month, year
    except:
        return False, False, False


def getenddate(start_day, start_month, start_year):
    day, month, year = getendtdateinput()
    while True:
        if not day or not month or not year:
            print("Invalid Input, Please try again")
            day, month, year = getendtdateinput()
        elif datetime.date(day=day, month=month, year=year) <= datetime.date(day=start_day, month=start_month,
                                                                             year=start_year):
            print("End Date should be atleast one day more than the Start date")
            day, month, year = getendtdateinput()
        elif datetime.date(day=day, month=month, year=year) > datetime.date.today():
            print("End Date cannot be in future")
            day, month, year = getendtdateinput()
        else:
            start_date = datetime.date(start_year, start_month, start_day)
            end_date = datetime.date(year, month, day)
            delta = end_date - start_date
            if delta.days > 30:
                print("Note: This is just a hacked version of the program, it is not memory optimized, it might not "
                      "run properly depending on the Machine.")
            break
    return day, month, year

# End Date Input Logic End
