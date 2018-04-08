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
        """ Will run all what we need to be able to predict.
                    * Will compute the averages for each track
                    * Will spread this vector to all users
                    * Will Compute the similarity matrix
                    * Will spread the matrix to all users
        """

        self.__compute_averages()
        self.__spread_averages()
        self.__compute_similarity_matrix()
        self.__spread_similarity_matrix()

    def __compute_averages(self):
        """ Compute the average score for all the tracks
                We pick a random user to start the calculus each time, it's to avoid giving too much power to one user
        """
        for index,track in self.track_list.iterrows():
            user = random.choice(self.__users)
            self.__averages.iloc[index] = user.compute_average(index)
        
    def __spread_averages(self):
        """ Send the cumputed average to all nodes
        """
        for user in self.__users:
            user.save_averages(self.__averages)

    def __compute_similarity_matrix(self):
        """ Create the similarity matrix. 
                    * First of all, we need to ask all user to compute their normalized vector
                    * Then we need to calculate the norme of all the tracks
                    * Then we can calculate the similarity, using a scalare computation

                Note: it could be optimized by the fact that the similarity matrix is symetrical. So we can reduce the number of calculus by 2
        """

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
                if math.isnan(norma.iloc[indexI].item()) or math.isnan(norma.iloc[indexJ].item() ):
                    similarity_matrix[indexI, indexJ] = - math.inf
                elif norma.iloc[indexI].item() == 0. or norma.iloc[indexJ].item() == 0.:
                    similarity_matrix[indexI, indexJ] = 0
                else:
                    similarity_matrix[indexI, indexJ] = user.compute_scalar(indexI, indexJ) / (norma.iloc[indexI] * norma.iloc[indexJ])

        self.__similarity_matrix = pd.DataFrame(similarity_matrix)
        

    def __spread_similarity_matrix(self):
        """ Send the similarity matrix to all nodes
        """
        for user in self.__users:
            self.__users[user.id].save_similarity_matrix(self.__similarity_matrix)

