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


