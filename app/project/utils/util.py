from utils.run import *

VENDORS = []
AGENCIES = []

def is_valid_vendor(vendor_name):
    if not vendor_name == "" and vendor_name in VENDORS:
        return True
    else:
        return False


def is_valid_agency(agency_name):
    if not agency_name == "" and agency_name in AGENCIES:
        return True
    else:
        return False

def lookup_vendor_info(vendor_name):
    return read_vendor_by_month()[vendor_name]


def lookup_agency_info(agency_name):
    return read_agency_by_month()[agency_name]