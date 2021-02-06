import numpy as np
import pandas as pd
from utils.data_obj import *
from collections import defaultdict
import sys
import os
import pickle

def load_bill_data():
    print(os.getcwd())
    path = os.getcwd()+"/project/Purchase_Card_Transactions.csv"
    return pd.read_csv(path)

bill = load_bill_data()

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

def getinfo_by_vendor(vendorname):
    
    newdf = bill_full[bill_full['VENDOR_NAME']==vendorname]
    rsltdf = newdf[['MONTH','TRANSACTION_AMOUNT']]
    rsltdict = defaultdict(list)
    rsltlist = []
    for index, row in rsltdf.iterrows():
        rsltdict[row['MONTH']].append(row['TRANSACTION_AMOUNT'])
    
    for key, value in rsltdict.items():
        num = len(value)
        total = sum(value)
        avg = total / num
        rsltlist.append([key, total, num, avg])
        
    return rsltlist

def getinfo_by_agency(agencyname):
    newdf = bill_full[bill_full['AGENCY']==vendorname]
    rsltdf = newdf[['MONTH','TRANSACTION_AMOUNT']]
    rsltdict = defaultdict(list)
    rsltlist = []
    for index, row in rsltdf.iterrows():
        rsltdict[row['MONTH']].append(row['TRANSACTION_AMOUNT'])
    
    for key, value in rsltdict.items():
        num = len(value)
        total = sum(value)
        avg = total / num
        rsltlist.append([key, total, num, avg])
        
    return rsltlist

def agg_agent_dict(df):
    
    agg_dict = defaultdict(list)
    vend_dict = defaultdict(list)
    vendor_list = set()
    agency_list = set()

    for index, row in df.iterrows():
        if index %1000 == 0:
            print(index)
        vend = Vendor(str(row['VENDOR_NAME']), str(row['VENDOR_STATE_PROVINCE']))
        vendor_list.add(vend)
        agen = Agency(str(row['AGENCY']))
        agency_list.append(agen)
        dat = str(row['TRANSACTION_DATE'])
        trans = Transaction(row['OBJECTID'], agen, vend, dat, row['TRANSACTION_AMOUNT'], str(row['MCC_DESCRIPTION']))

        agg_dict[agen.name].append(trans)
        vend_dict[vend.name].append(trans)
    return agg_dict, vend_dict

def save_data():
    with open('agency.pickle', 'wb') as handle:
        pickle.dump(agg_agent_dict(bill)[0], handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('vendor.pickle', 'wb') as handle:
        pickle.dump(agg_agent_dict(bill)[1], handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("save complete")

def read_data():
    with open('agency.pickle', 'rb') as handle:
        agency = pickle.load(handle)

    with open('vendor.pickle', 'rb') as handle:
        vendor = pickle.load(handle)

    return agency, vendor


