import json


class Track(object):
    def __init__(self, id=None, title="", playcount=0, rating_score=0,
                 artist="", genre="", album="", year=None, json=None):
        self.__id = id
        self.__title = title
        self.__playcount = playcount
        self.__rating_score = rating_score
        self.__artist = artist
        self.__genre = genre
        self.__album = album
        self.__year = year
        if json:
            self.fromJSON(json)

    def toJSON(self):
        return json.dumps({
            "id": self.__id,
            "title": self.__title,
            "playcount": self.__playcount,
            "rating_score": self.__rating_score,
            "artist": self.__artist,
            "genre": self.__genre,
            "album": self.__album,
            "year": self.__year,
        })

    def fromJSON(self, json_line):
        entry = json.loads(json_line)
        self.__id = entry['id']
        self.__title = entry['title']
        self.__playcount = entry['playcount']
        self.__rating_score = entry['rating_score']
        self.__artist = entry['artist']
        self.__genre = entry['genre']
        self.__album = entry['album']
        self.__year = entry['year']

    def __repr__(self):
        return "ID: {}, TITLE: {}, PLAYCOUNT: {}, RATING: {}\n".format(
            self.__id,
            self.__title[:20],
            self.__playcount,
            self.__rating_score)

    @property
    def id(self):
        return self.__id
