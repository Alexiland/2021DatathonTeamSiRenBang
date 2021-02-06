import numpy as np
import pandas as pd
from data_obj import *
from collections import defaultdict

def load_bill_data():
    path = "../data_processing/Purchase_Card_Transactions.csv"
    return pd.read_csv(path)

bill = load_bill_data()

def agg_agent_dict(df):
    
    agg_dict = defaultdict(list)
    vend_dict = defaultdict(list)

    for index, row in df.iterrows():
        if index %1000 == 0:
            print(index)
        vend = Vendor(str(row['VENDOR_NAME']), str(row['VENDOR_STATE_PROVINCE']))
        agen = Agency(str(row['AGENCY']))
        dat = str(row['TRANSACTION_DATE'])
        trans = Transaction(row['OBJECTID'], agen, vend, dat, row['TRANSACTION_AMOUNT'], str(row['MCC_DESCRIPTION']))
        # print (trans.date)
        # print (dat)
        agg_dict[agen].append(trans)
        vend_dict[agen].append(trans)

    print (len(agg_dict.keys()))
    return agg_dict, vend_dict


def read_data():
    return agg_agent_dict(bill)
