import datetime
import statistics


def getstocknames(data):
    stocks = [row[0] for row in data]
    unique_stocks = list(dict.fromkeys(stocks))
    return unique_stocks


def getstockfiltereddata(stock_nm, data):
    stock_filter_data = [row for row in data if stock_nm == row[0]]
    if len(listduplicatedates(stock_filter_data)) > 0:
        print("Multiple Data for same date found, CSV Integrity Lost, Please try with a different CSV")
        exit()
    return stock_filter_data


def listduplicatedates(seq):
    seen = set()
    seen_add = seen.add
    seen_twice = set(x[1] for x in seq if x[1] in seen or seen_add(x[1]))
    return list(seen_twice)


def getdatefiltereddata(start_date_str, end_date_str, data):
    start_filter_data = [row for row in data if
                         datetime.datetime.strptime(start_date_str, "%d-%m-%Y") <= datetime.datetime.strptime(row[1],
                                                                                                              "%d-%b-%Y")]
    stock_filter_data = [row for row in start_filter_data if
                         datetime.datetime.strptime(end_date_str, "%d-%m-%Y") >= datetime.datetime.strptime(row[1],
                                                                                                            "%d-%b-%Y")]
    return stock_filter_data


def sortdataondate(data):
    sorted_data = sorted(data, key=lambda x: datetime.datetime.strptime(x[1], '%d-%b-%Y'))
    return sorted_data


def fillintermediatedata(sorted_data, start_date_day, start_date_month, start_date_year, end_date_day, end_date_month,
                         end_date_year, stock_filtered_data):
    focused_data = []
    start_date = datetime.date(start_date_year, start_date_month, start_date_day)
    end_date = datetime.date(end_date_year, end_date_month, end_date_day)
    for single_date in daterange(start_date, end_date):
        day_price = getpricefordate(single_date, sorted_data, stock_filtered_data, start_date)
        single_focused_data_row = [single_date.strftime("%d-%m-%Y"), day_price]
        focused_data.append(single_focused_data_row)
    return focused_data


def getpricefordate(date, sorted_data, stock_filtered_data, start_date):
    data_before_date = [row for row in sorted_data if
                        datetime.datetime.strptime(row[1], "%d-%b-%Y") <= datetime.datetime.strptime(
                            date.strftime("%d-%m-%Y"), "%d-%m-%Y")]
    if len(data_before_date) == 0:
        return getlastpriceoutoffocus(stock_filtered_data, start_date)
    last_record = max(data_before_date, key=lambda x: datetime.datetime.strptime(x[1], '%d-%b-%Y'))
    last_price = float(last_record[2])
    return last_price


def getlastpriceoutoffocus(stock_filtered_data, start_date):
    last_date = [row for row in stock_filtered_data if
                 datetime.datetime.strptime(row[1], "%d-%b-%Y") <= datetime.datetime.strptime(
                     start_date.strftime("%d-%m-%Y"), "%d-%m-%Y")]
    if len(last_date) == 0:
        print("Logical Error, the data does not exist, please try again with a broader CSV or narrower Focus Range")
        exit()
    last_record = max(last_date, key=lambda x: datetime.datetime.strptime(x[1], '%d-%b-%Y'))
    last_price = float(last_record[2])
    return last_price


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + datetime.timedelta(n)


def getmean(data):
    prices = [float(i[1]) for i in data]
    mean = statistics.mean(prices)
    return mean


def getstdeviation(data):
    prices = [float(i[1]) for i in data]
    stdev = statistics.stdev(prices)
    return stdev


def getprofittrade(data):
    pair1_sell_date, pair2_buy_date = getmaxminpricedates(data)
    pair1_buy_date = getminbeforedate(data, pair1_sell_date)
    pair2_sell_date = getmaxafterdate(data, pair2_buy_date)
    pair1_profit = getunitprofit(data, pair1_buy_date, pair1_sell_date)
    pair2_profit = getunitprofit(data, pair2_buy_date, pair2_sell_date)

    if pair1_profit > pair2_profit:
        return pair1_buy_date, pair1_sell_date, pair1_profit
    return pair2_buy_date, pair2_sell_date, pair2_profit


def getmaxminpricedates(data):
    min_record = min(data[:-1], key=lambda x: float(x[1]))
    data.reverse()
    max_record = max(data[:-1], key=lambda x: float(x[1]))
    max_date = max_record[0]
    min_date = min_record[0]
    return max_date, min_date


def getmaxafterdate(data, date):
    after_date_data = [row for row in data if
                         datetime.datetime.strptime(date, "%d-%m-%Y") < datetime.datetime.strptime(row[0], "%d-%m-%Y")]
    after_date_data.reverse()
    max_price_date = max(after_date_data, key=lambda x: float(x[1]))[0]
    return max_price_date

def getminbeforedate(data, date):
    before_date_data = [row for row in data if
                       datetime.datetime.strptime(date, "%d-%m-%Y") > datetime.datetime.strptime(row[0], "%d-%m-%Y")]
    min_price_date = min(before_date_data, key=lambda x: float(x[1]))[0]
    return min_price_date

def getunitprofit(data, buy_date, sell_date):
    date_arr = [row[0] for row in data]
    buy_index = date_arr.index(buy_date)
    sell_index = date_arr.index(sell_date)
    buy_price = float(data[buy_index][1])
    sell_price = float(data[sell_index][1])
    unit_profit = sell_price - buy_price
    return unit_profit