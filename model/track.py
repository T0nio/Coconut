import json


class Track(object):
    def __init__(self, id=None, title="", playcount=0, rating_score=0, json=None):
        self.__id = id
        self.__title = title
        self.__playcount = playcount
        self.__rating_score = rating_score
        if json:
            self.fromJSON(json)

    def toJSON(self):
        return json.dumps({
            "id": self.__id,
            "title": self.__title,
            "playcount": self.__playcount,
            "rating_score": self.__rating_score
        })

    def fromJSON(self, json_line):
        entry = json.loads(json_line)
        self.__id = entry['id']
        self.__title = entry['title']
        self.__playcount = entry['playcount']
        self.__rating_score = entry['rating_score']

    def __repr__(self):
        return "ID: {}, TITLE: {}, PLAYCOUNT: {}, RATING: {}\n".format(
            self.__id,
            self.__title[:20],
            self.__playcount,
            self.__rating_score)

    @property
    def id(self):
        return self.__id
