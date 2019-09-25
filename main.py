import inputHelper
import csvHelper
import dataUtils

file_path = inputHelper.getcsvfilepath()
data = csvHelper.getcsvdata(file_path)
stocks = dataUtils.getstocknames(data)

should_continue = csvHelper.analyzecsvdata(data)
if not should_continue:
    print("There are errors in the CSV File, Cannot Proceed")
    take_input = False
else:
    take_input = True

while take_input:
    search_stock_nm = inputHelper.getsearchstockname(stocks)
    filtered_stock_data = dataUtils.getstockfiltereddata(search_stock_nm, data)

    start_day, start_month, start_year = inputHelper.getstartdate()
    end_day, end_month, end_year = inputHelper.getenddate(start_day, start_month, start_year)

    start_date_str = str(start_day) + "-" + str(start_month) + "-" + str(start_year)
    end_date_str = str(end_day) + "-" + str(end_month) + "-" + str(end_year)
    date_filtered_stock_data = dataUtils.getdatefiltereddata(start_date_str, end_date_str, filtered_stock_data)

    if len(date_filtered_stock_data) == 0:
        print("No Data found for the searched Parameters.")
    else:
        sorted_data = dataUtils.sortdataondate(date_filtered_stock_data)
        focused_data = dataUtils.fillintermediatedata(sorted_data=sorted_data, start_date_day=start_day,
                                                      start_date_month=start_month, start_date_year=start_year,
                                                      end_date_day=end_day, end_date_month=end_month,
                                                      end_date_year=end_year, stock_filtered_data=filtered_stock_data)
        mean_price = dataUtils.getmean(focused_data)
        stdev_price = dataUtils.getstdeviation(focused_data)
        buy_date, sell_date, unit_profit = dataUtils.getprofittrade(focused_data)
        total_profit = unit_profit*100
        print('\n')
        print("Mean Price of the Stock: " + str(mean_price))
        print("Standard Deviation of the Stock: " + str(stdev_price))
        print("For Maximum Profit...")
        print("Buy on: " + buy_date)
        print("Sell on: " + sell_date)
        print("Profit will be " + str(unit_profit) + " Per Unit or total of " + str(total_profit) + " for 100 units")
        print('\n')

    print("Do you want to Perform another Search? (y/n)")
    try_again_input = input()
    if try_again_input != 'y':
        take_input = False
