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
                try:
                    artist = file['artist'][0]
                except KeyError:
                    artist = ""
                try:
                    genre = file['genre'][0]
                except KeyError:
                    genre = ""
                try:
                    album = file['album'][0]
                except KeyError:
                    album = ""
                try:
                    year = int(file['date'][0][:4])
                except KeyError:
                    year = None

            elif file_name.lower().endswith(('mp3')):
                file = mutagen.File(os.path.join(dirpath, file_name))
                try:
                    playcount = float(file.tags.getall("TXXX:FMPS_PlayCount")[0][0])
                except IndexError:
                    playcount = None
                try:
                    rating = float(file.tags.getall("TXXX:FMPS_Rating_Amarok_Score")[0][0])
                except IndexError:
                    rating = None
                try:
                    title = file.tags.getall("TIT2")[0][0]
                except IndexError:
                    title = ""
                try:
                    artist = file.tags.getall("TPE1")[0][0]
                except IndexError:
                    artist = ""
                try:
                    genre = file.tags.getall("TCON")[0][0]
                except IndexError:
                    genre = ""
                try:
                    album = file.tags.getall("TALB")[0][0]
                except IndexError:
                    album = ""
                try:
                    year = file.tags.getall("TDRC")[0][0]
                    year = str(year)
                    year = year[:4]
                    year = int(year)
                except (ValueError, IndexError):
                    year = None

            else:
                break  # do not treat that file

            track_collection[id] = Track(
                id,
                title,
                playcount,
                rating,
                artist,
                genre,
                album,
                year)
            id += 1

    print("Saving track collection to : ", os.path.join('data', 'track_collection.json'))
    track_collection.save(os.path.join('data', 'track_collection.json'))
