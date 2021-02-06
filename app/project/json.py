import json
import common.data_obj as data_obj
import uuid
import datetime

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

