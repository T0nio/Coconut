import pandas as pd
import numpy as np
from model.track import Track


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

    def __repr__(self):
        return self.__collection.__repr__

    def __str__(self):
        return str(self.__collection)

    def save(self, filepath):
        with open(filepath, 'w') as collection_file:
            for value in self.__collection.values():
                line = value.toJSON()
                collection_file.write(line)
                collection_file.write('\n')

    def load(self, filepath):
        with open(filepath, 'r') as collection_file:
            line = collection_file.readline()
            while len(line) > 1:  # EOF
                track = Track(json=line)
                self[track.id] = track
                line = collection_file.readline()

    def to_dataframe(self):
        columns = np.array(['id', 'title', 'rating_score', 'playcount',
                            'artist', 'album', 'genre', 'year'])
        df = np.empty((0, 8))
        for item in self.__collection.values():
            row = np.array([[item.id, item.title, item.rating_score,
                             item.playcount, item.artist, item.album,
                             item.genre, item.year]])
            df = np.append(df, row, axis=0)
        return pd.DataFrame(df, columns=columns)
