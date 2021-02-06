import operator

import numpy as np
import pandas as pd
import sys
import os
import pickle
from collections import defaultdict, OrderedDict
from datetime import datetime
def load_bill_data():
    # print(os.getcwd())
    path = os.getcwd()+"/project/Purchase_Card_Transactions.csv"
    return pd.read_csv(path)


bill = load_bill_data()

def agg_mcc():
    smalldf = bill['MCC_DESCRIPTION']
    print(bill)
    mcc_agg = dict(smalldf.value_counts())
    return mcc_agg


def add_month_year():
    date_format = "%Y/%m/%d"
    min_date = datetime.strptime('2000/01/01', date_format)

    day_col = []
    month_col = []
    year_col = []

    for orig in bill["TRANSACTION_DATE"]:
        date = datetime.strptime(orig, '%Y/%m/%d %I:%M:00+00')
        month = str(date.year) + '/' + str(date.month - min_date.month)
        month_col.append(month)
        year = date.year
        year_col.append(year)

    bill_full = bill.copy()
    bill_full['MONTH'] = month_col
    bill_full['YEAR'] = year_col
    return bill_full


bill_full = add_month_year()


def getseries():
    newdf = bill_full[['AGENCY', 'YEAR', 'TRANSACTION_AMOUNT']]
    rsltdict = defaultdict(dict)
    for index, row in newdf.iterrows():
        if (row['YEAR'] > 2008):
            #             print('bang')
            key = row['YEAR'] - (row['YEAR'] - 2009) % 3
            if row['AGENCY'] not in rsltdict[key].keys():
                rsltdict[key][row['AGENCY']] = [row['TRANSACTION_AMOUNT'], 1]
            else:
                rsltdict[key][row['AGENCY']][0] += row['TRANSACTION_AMOUNT']
                rsltdict[key][row['AGENCY']][1] += 1

    return rsltdict


def calculate_index(raw_dict, alpha, beta):
    """
    calculate index value for each agency (business)
    :param alpha: coefficient for transaction amount
    :param beta: coefficient for transaction incidents
    :return: a dict with agency as keys and index as value
    """
    return_dict = OrderedDict()
    for key, value in raw_dict.items():
        return_dict[key] = alpha * value[0] + beta * value[1]

    return return_dict

def ranking(input_dict):
    """
    rank the current snapshot year interval with index value
    :param input_dict: input dictionary
    :return: sorted list of tuple
    """
    sorted_tuples = sorted(input_dict.items(), key=operator.itemgetter(1), reverse=True)
    return(sorted_tuples)

def specific_ranking(agency, sorted_list):
    for i in range(1, len(sorted_list)+1):
        if agency == sorted_list[i-1][0]:
            return i

