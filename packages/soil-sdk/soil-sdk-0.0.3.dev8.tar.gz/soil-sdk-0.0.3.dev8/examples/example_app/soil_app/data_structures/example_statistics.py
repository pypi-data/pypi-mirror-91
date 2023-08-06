import json
from soil.data_structures.data_structure import DataStructure


class Statistics(DataStructure):
    @staticmethod
    def unserialize(str_lines, metadata, db_object=None):
        return Statistics(json.loads(next(str_lines)), metadata)

    def serialize(self):
        return json.dumps(self.data)

    def get_data(self, **args):
        return self.data
