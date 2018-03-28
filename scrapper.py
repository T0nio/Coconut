import os
import re
import mutagen
from model.track_collection import TrackCollection
from model.track import Track

ROOT_DIR_PATH = os.path.join(os.sep, 'media', 'DATA', 'Musique')
AUTHORIZED_ZIK_EXTENSIONS = ('mp3', 'flac', 'ogg')

if __name__ == "__main__":
    ext = re.compile('/\.[0-9a-z]+$/i')
    track_collection = TrackCollection()
    id = 0
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR_PATH):
        for file_name in filenames:
            if id % 100 == 0:
                print(id)
            print(dirpath, file_name)
            if file_name.lower().endswith(AUTHORIZED_ZIK_EXTENSIONS):
                # print(file_name)
                file = mutagen.File(os.path.join(dirpath, file_name))
                print(file.keys())
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
                print(id, title, playcount, rating)
                track_collection[id] = Track(
                    id,
                    title,
                    playcount,
                    rating)
                id += 1
    print(track_collection)
    track_collection.save(os.path.join('data', 'track_collection.json'))
