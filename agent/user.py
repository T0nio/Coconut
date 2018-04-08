import random
import pandas as pd
import numpy as np
import math

class User(object):
    def __init__(self, id=None, df=None, nextNode=None):
        self.__id = id
        self.__df =  df.astype("float")
        self.__nextNode = nextNode
        self.__similarity_matrix = None
        self.__average_rating = float(self.__df[self.__df["rating_score"] > 0.].mean())

    def __repr__(self):
        return "User Object, ID: {}\n".format(self.__id)


    def compute_average(self, track_id):
        """ Compute the average rating score for a given track
                It's working with the user network.
                Generating a huge number, then adding its own rating (if has any), and then give it to the next node
                Each node will add its own rating (if has any), and then returning to the first node that will compute the average

        Arguments:
            track_id {int} -- The id of the track for which we need to work

        Returns:
            float -- The average rating of the track
        """

        init_val = random.randint(5000, 10000)
        track = self.__df.iloc[track_id]
        score = track['rating_score']
        r = self.__nextNode.executeSum('average', {
            'origin': self.id,
            'value': init_val + (0 if math.isnan(score) else score),
            'n': 0 if math.isnan(score) else 1,
            'i': track_id
        })
        if(r[1] == 0):
            return 0
        else:
            return float(r[0] - init_val) / r[1]

    def compute_norma(self, track_id):
        """ Compute the norma of a given track
                It's working with the user network.
                Generating a huge number, then adding its own square rating (if has any), and then give it to the next node
                Each node will add its own square rating (if has any), and then returning to the first node that will compute the sqrt

        Arguments:
            track_id {int} -- The id of the track for which we need to work

        Returns:
            float -- The norma of the track
        """


        init_val = random.randint(50000, 100000)
        track = float(self.__normalized_vector.iloc[track_id])
        r = self.__nextNode.executeSum('norma', {
            'origin': self.id,
            'value': init_val + (0 if math.isnan(track) else track**2),
            'n': 0 if math.isnan(track) else 1,
            'i': track_id
        })
        if(r[1] == 0):
            return math.nan
        return math.sqrt(r[0]-init_val)

    def compute_scalar(self, i, j):
        """ Compute the scalar product between two tracks
                It's working with the user network.
                Generating a huge number, then adding its own track multiplication (if has any), and then give it to the next node
                Each node will add its own track multiplication (if has any), and then returning to the first node that will compute the sqrt

        Arguments:
            i {int} -- The first track
            j {int} -- The second track

        Returns:
            float -- The scalar product between the two tracks
        """

        init_val = random.randint(5000, 10000)
        scoreI = float(self.__normalized_vector.iloc[i])
        scoreJ = float(self.__normalized_vector.iloc[j])
        add = 0 if math.isnan(scoreI) or math.isnan(scoreJ) else scoreI * scoreJ
        r = self.__nextNode.executeSum('scalar', {
            'origin': self.id,
            'value': init_val + add,
            'i': i,
            'j': j
        })
        return r - init_val

    def executeSum(self, sum_type, params=None):
        """ Compute sum with the network of nodes.

        Arguments:
            sum_type {string} -- The type of sum. Used as a switch( is that linear, square, ..)

        Keyword Arguments:
            params {dict} -- Will depend of the sum_type. But basically the infos needed to compute the sum (default: {None})

        Returns:
            tuple -- Will depends of the sum_type. But are the values needed for the master node to cumpute it's calculus
        """
        if params['origin'] == self.id:
            if sum_type == 'average':
                return (params['value'], params['n'])
            elif sum_type == 'norma':
                return (params['value'], params['n'])
            elif sum_type == 'scalar':
                return (params['value'])
        else:
            if sum_type == 'average':
                newParams = params
                score = float(self.__df.iloc[params['i']]['rating_score'])
                if(score != 0):
                    newParams['n'] += 0 if math.isnan(score) else 1
                    newParams['value'] += 0 if math.isnan(score) else score
                return self.__nextNode.executeSum(sum_type, newParams)
            elif sum_type == 'norma':
                newParams = params
                score = float(self.__normalized_vector.iloc[params['i']])
                newParams['value'] += 0 if math.isnan(score) else score**2
                newParams['n'] += 0 if math.isnan(score) else 1
                return self.__nextNode.executeSum(sum_type, newParams)
            elif sum_type == 'scalar':
                newParams = params
                scoreI = float(self.__normalized_vector.iloc[params['i']])
                scoreJ = float(self.__normalized_vector.iloc[params['j']])
                newParams['value'] += 0 if math.isnan(scoreI) or math.isnan(scoreJ) else scoreI*scoreJ
                return self.__nextNode.executeSum(sum_type, newParams)

    def compute_normalized_vector(self):
        """ Compute the normalized vecor of rates for the current user
        """
        rates = self.__df.rename(columns={'rating_score':'normalized_score'}).normalized_score.apply(float)
        av = self.__averages.rename(columns={'av':'normalized_score'}).normalized_score.apply(float)
        self.__normalized_vector =  rates - av


    def save_averages(self, averages):
        self.__averages = averages

    def save_similarity_matrix(self, matrix):
        self.__similarity_matrix = matrix

    def predict_rating(self, element_index):
        """ Predicting a rating for a given element

        Arguments:
            element_index {int} -- The ID of the element to predict

        Returns:
            float -- The predicted score for the element
        """

        upper_sum = 0
        lower_sum = 0
        for index, el in enumerate(self.__similarity_matrix.iloc[:, element_index]):
            if (not math.isnan(el)) and not math.isnan(self.__df.iloc[index]) and  el >= 0 and el <= 0.99:
                upper_sum += el * float(self.__df.iloc[index])
                lower_sum += el

        #print("UpSum: %f, loSum: %f" % (upper_sum, lower_sum))
        ret = self.__averages.iloc[element_index]
        if lower_sum != 0:
            return upper_sum / lower_sum
        else:
            return - math.inf

    def willILikeIt(self, element_index):
        """ Does this user will like a song ?
                We'll decide if we recomand it to him

        Arguments:
            element_index {int} -- Index of the element to predict

        Returns:
            bool -- Do we recommand the user this song ?
        """

        return self.predict_rating(element_index) >= self.__average_rating

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def average_rating(self):
        return self.__average_rating

    @property
    def nextNode(self):
        return self.__nextNode

    @nextNode.setter
    def nextNode(self, node):
        self.__nextNode = node

    @property
    def similarity_matrix(self):
        return self.__similarity_matrix
