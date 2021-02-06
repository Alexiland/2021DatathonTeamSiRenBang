import datetime
import json
import uuid

import common.data_obj as data_obj


class Json_data(data_obj.Data):
    """JSON object representation"""
    def __init__(self, json_file=None):
        if json_file is not None:
            self.load(json_file)
        else:
            self.json = None
        self.uuid = uuid.uuid4()
        self.creation_time = datetime.datetime.now()

    def __str__(self):
        return json.dumps(self.json, indent=1)

    def load(self, json_file):
        self.json = json.load(json_file)

    def json_keys(self):
        return self.json.keys()

class To_front(data_obj.Data):
    """
    To the front end data
    """
    def __init__(self, matrix):
        """
        Init
        :param matrix: has form of list of [month, transaction amount, average amount, transaction time] or
        [location, transaction amount]
        """
        self.data = matrix

    def to_dict(self):
        dict_new = dict()
        for i in range(len(self.data)):
            dict_new[i] = self.data[i]
        return dict_new
