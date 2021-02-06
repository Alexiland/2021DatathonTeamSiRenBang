import datetime

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
        """
        :param id: int
        :param agency: string
        :param vendor: string
        :param date: string, in format '10/11/2019 12:00PM' '%b %d %Y %I:%M%p'
        :param amount: double
        :param descrip: String
        """
        self.objectid = id
        self.agency = agency
        self.vendor = vendor
        # should be a datetime object
        self.date = datetime.datetime.strptime(date, '%b %d %Y %I:%M%p')
        self.transac_amount = amount
        self.mcc_descrip = descrip

    def month(self):
        return self.date.month

