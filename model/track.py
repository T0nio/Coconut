import json


class Track(object):
    def __init__(self, id, title="", playcount=0, rating_score=0):
        self.__id = id
        self.__title = title
        self.__playcount = playcount
        self.__rating_score = rating_score

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return "ID: {}, TITLE: {}, PLAYCOUNT: {}, RATING: {}".format(
            self.__id,
            self.__title[:20],
            self.__playcount,
            self.__rating_score)
