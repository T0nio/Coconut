import random
import pandas as pd
import numpy as np

class User(object):
  def __init__(self, id=None, df=None, nextNode=None):
    self.__id = id
    self.__df = df
    self.__nextNode = nextNode
    self.__similarity_matrix = []

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
    r = self.__nextNode.executeSum('average', {
      'origin': self.id,
      'value': init_val + float(track['rating_score']),
      'n': 0 if track['rating_score'] == 0 else 1,
      'i': track_id
    })
    if(r[1] == 0): 
      return 0
    else:
      return float(r[0] - init_val) / r[1]


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
    else:
      if sum_type == 'average':
        newParams = params
        score = float(self.__df.iloc[params['i']]['rating_score'])
        if(score != 0):
          newParams['n'] += 1
          newParams['value'] += score
        return self.__nextNode.executeSum(sum_type, newParams)

  def compute_normalized_vector(self):


  def save_averages(self, averages):
    self.__averages = averages

  def save_similarity_matrix(self, matrix):
    self.__similarity_matrix = matrix

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, id):
    self.__id = id

  @property
  def nextNode(self):
    return self.__nextNode

  @nextNode.setter
  def nextNode(self, node):
    self.__nextNode = node