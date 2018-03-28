import json


class TrackCollection(object):
    def __init__(self, filepath=None):
        self.__collection = {}
        if filepath:
            self.load(filepath)

    def __getitem__(self, key):
        return self.__collection[key]

    def __setitem__(self, key, value):
        self.__collection[key] = value

    def values(self):
        return self.__collection.values()

    def __len__(self):
        return len(self.__collection)

    def save(self, filepath):
        with open(filepath, 'w') as collection_file:
            for value in self.__collection.values():
                line = value.toJSON()
                collection_file.write(line)
                collection_file.write('\n')

    def load(self, filepath):
        with open(filepath, 'r') as collection_file:
            self.__collection = json.load(collection_file)
