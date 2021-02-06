

class Data:
    """Data super class"""
    def __str__(self):
        pass

class Vendor(Data):
    """Vendor data object"""
    def __init__(self, name, loc):
        self.name = name
        self.state_location = loc

    def __str__(self):
        return self.name


class Agency(Data):
    """Agency data object"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Transaction(Data):
    """Transaction data object"""
    def __init__(self, id, agency, vendor, date, amount, descrip):
        self.objectid = id
        self.agency = agency
        self.vendor = vendor
        self.date = date
        self.transac_amount = amount
        self.mcc_descrip = descrip

