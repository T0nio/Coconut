import random
import pandas as pd
import numpy as np
import math

class Server(object):
  def __init__(self, users, track_list):
    self.__users = users
    self.track_list = track_list
    self.__averages = pd.DataFrame(0, index=np.arange(len(track_list)), columns=['av'])
    self.__similarity_matrix = None
  
  def run(self):
    self.__compute_averages()
    self.__spread_averages()
    self.__compute_similarity_matrix()
    self.__spread_similarity_matrix()

  def __compute_averages(self):
    for index,track in self.track_list.iterrows():
      user = random.choice(self.__users)
      self.__averages.iloc[index] = user.compute_average(index)
    
  def __spread_averages(self):
    for user in self.__users:
      user.save_averages(self.__averages)

  def __compute_similarity_matrix(self):
    for user in self.__users:
      user.compute_normalized_vector()
    
    norma = pd.DataFrame(0, index=np.arange(len(self.track_list)), columns=['norma'])
    for index,track in self.track_list.iterrows():
      user = random.choice(self.__users)
      norma.iloc[index] = user.compute_norma(index)
    
    similarity_matrix = np.zeros((len(self.track_list),len(self.track_list)))
    for indexI,trackI in self.track_list.iterrows():
      for indexJ,trackJ in self.track_list.iterrows():
        user = random.choice(self.__users)
        if norma.iloc[indexI].item() == 0. or norma.iloc[indexJ].item() == 0.:
          similarity_matrix[indexI, indexJ] = - math.inf
        else:
          similarity_matrix[indexI, indexJ] = user.compute_scalar(indexI, indexJ) / (norma.iloc[indexI] * norma.iloc[indexJ])

    self.__similarity_matrix = pd.DataFrame(similarity_matrix)
    

  def __spread_similarity_matrix(self):
    for user in self.__users:
      self.__users[user.id].save_similarity_matrix(self.__similarity_matrix)

