from utils.collection_splitter import splitter
import os
from model.track_collection import TrackCollection


track_collection = TrackCollection()
track_collection.load(os.path.join('data', 'track_collection_y.json'))

newCollections = splitter(track_collection, 5, 0.01)

for c in newCollections:
  print(c)