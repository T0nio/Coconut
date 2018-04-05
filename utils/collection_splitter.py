from model.track_collection import TrackCollection
from random import shuffle

def splitter(collection, number_of_collections_to_generate, percent_to_use_per_collection):
  collections = []

  artistList = []

  for track in collection.values():
    if track.artist not in artistList:
      artistList.append(track.artist)

  nb_artists = int(float(len(artistList)) * percent_to_use_per_collection)

  for i in range(number_of_collections_to_generate):
    newCollection = TrackCollection()
    shuffle(artistList)
    artistsToGet = artistList[0:nb_artists]

    for track in collection.values():
      if track.artist in artistsToGet:
        newCollection[track.id] = track

    collections.append(newCollection)

  return collections