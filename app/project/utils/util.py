from utils.run import *
from utils.network_graphing import *
import pickle

VENDORS = []
AGENCIES = []

def is_valid_vendor(vendor_name):
    if not vendor_name == "":
        return True
    else:
        return False


def is_valid_agency(agency_name):
    if not agency_name == "":
        return True
    else:
        return False

def lookup_vendor_info(vendor_name):
    lst = read_vendor_by_month()
    return lst[vendor_name]


def lookup_agency_info(agency_name):
    lst = read_agency_by_month()
    return lst[agency_name]

def rank(agency_name):
    with open('ranking2009.pickle', 'rb') as handle:
        first = pickle.load(handle)
    with open('ranking2012.pickle', 'rb') as handle:
        second = pickle.load(handle)
    with open('ranking2015.pickle', 'rb') as handle:
        third = pickle.load(handle)
    with open('ranking2018.pickle', 'rb') as handle:
        fourth = pickle.load(handle)

    lst = []
    lst.append(specific_ranking(agency_name, first))

    lst.append(specific_ranking(agency_name, second))

    lst.append(specific_ranking(agency_name, third))

    lst.append(specific_ranking(agency_name, fourth))

    return lst

def success_factor(agency_name):
    with open('index_2009.pickle', 'rb') as handle:
        first = pickle.load(handle)
    with open('index_2012.pickle', 'rb') as handle:
        second = pickle.load(handle)
    with open('index_2015.pickle', 'rb') as handle:
        third = pickle.load(handle)
    with open('index_2018.pickle', 'rb') as handle:
        fourth = pickle.load(handle)

    lst = []
    for key, values in first.items():
        if key == agency_name:
            lst.append(values)
            break

    for key, values in second.items():
        if key == agency_name:
            lst.append(values)
            break

    for key, values in third.items():
        if key == agency_name:
            lst.append(values)
            break

    for key, values in fourth.items():
        if key == agency_name:
            lst.append(values)
            break

    return lst

