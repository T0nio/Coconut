import os
from model.track_collection import TrackCollection

if __name__ == "__main__":
    track_collection = TrackCollection()
    track_collection.load(os.path.join('data', 'track_collection.json'))
