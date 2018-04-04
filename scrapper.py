import os
import re
import mutagen
from model.track_collection import TrackCollection
from model.track import Track

ROOT_DIR_PATH = os.path.join(os.sep, 'media', 'DATA', 'Musique')

if __name__ == "__main__":
    ext = re.compile('/\.[0-9a-z]+$/i')
    track_collection = TrackCollection()
    id = 0
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR_PATH):
        for file_name in filenames:
            if id % 100 == 0:
                print(id)
            if file_name.lower().endswith(('flac', 'ogg')):
                file = mutagen.File(os.path.join(dirpath, file_name))
                try:
                    title = file['title'][0]
                except KeyError:
                    title = ""
                try:
                    playcount = int(file['fmps_playcount'][0])
                except KeyError:
                    playcount = None
                try:
                    rating = float(file['fmps_rating_amarok_score'][0])
                except KeyError:
                    rating = None

            elif file_name.lower().endswith(('mp3')):
                file = mutagen.File(os.path.join(dirpath, file_name))
                try:
                    playcount = file.tags.getall("TXXX:FMPS_PlayCount")[0]
                    playcount = float(playcount[0])
                except IndexError:
                    playcount = None
                try:
                    rating = file.tags.getall("TXXX:FMPS_Rating_Amarok_Score")[0]
                    rating = float(rating[0])
                except IndexError:
                    rating = None
                try:
                    title = file.tags.getall("TIT2")[0][0]
                except IndexError:
                    title = ""

            else:
                break  # do not treat that file

            print(id, title, playcount, rating)
            track_collection[id] = Track(
                id,
                title,
                playcount,
                rating)
            id += 1

    print(track_collection)
    track_collection.save(os.path.join('data', 'track_collection.json'))
