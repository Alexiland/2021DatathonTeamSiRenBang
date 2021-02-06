from utils.run import *

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