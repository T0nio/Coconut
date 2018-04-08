import numpy as np
import pandas as pd
import os
import math
import copy
from model.track_collection import TrackCollection
from utils.collection_splitter import splitter

if __name__ == "__main__":
    NUMBER_OF_USERS = 5

    # Loading the tracks data; and splitting them into number_of_users collections
    track_collection = TrackCollection()
    track_collection.load(os.path.join('data', 'track_collection_test.json'))
    df_track_collection = track_collection.to_dataframe()
    track_list = df_track_collection[['id']]

    # Here we merge the different users in one
    user_dfs = []
    for i in range(NUMBER_OF_USERS):
        tc = TrackCollection()
        tc.load(os.path.join('data', 'users', str(i + 1) + '.json'))
        ndf = tc.to_dataframe()[['id', 'rating_score']]
        user_matrix = track_list.merge(ndf, on='id', how='left')
        user_dfs.append(user_matrix[['id', 'rating_score']])

    matrix = track_list
    for index, udf in enumerate(user_dfs):
        matrix = matrix.merge(user_dfs[index], on='id', how='left').rename(columns = {'rating_score': 'user_' + str(index)})

    matrix = matrix.drop('id', axis=1)
    matrix = matrix.filter(regex='^user_[0-9]+$')
    matrix = matrix.astype('float')

    def compute_normalize_matrix(df):
        df = copy.copy(df)
        for index, line in df.iterrows():
            sum = 0
            n = 0
            for el in line:
                if not math.isnan(el):
                    sum += el
                    n += 1
            if n != 0:
                line_mean = sum / n
            else:
                line_mean = 0
            for el_idx, el in enumerate(line):
                if not math.isnan(el):
                    line[el_idx] = el - line_mean
            df.loc[index] = line
        return df

    n_matrix = compute_normalize_matrix(matrix)

    def is_nan_vector(vector):
        for el in vector:
            if not math.isnan(el):
                return False
        return True

    def cos_measure(df, index_x, index_y):
        # If some normalized vector is full of NaN components, then no user have ever evaluated that track
        # So it should be ranked at -Infinity
        rx = df.iloc[index_x]
        ry = df.iloc[index_y]
        if is_nan_vector(rx) or is_nan_vector(ry):
            return - math.inf

        rx = rx.fillna(0.0)
        ry = ry.fillna(0.0)
        sc = np.dot(rx, ry)
        if (np.linalg.norm(rx) * np.linalg.norm(ry)) != 0.:
            return sc / (np.linalg.norm(rx) * np.linalg.norm(ry))
        return 0.0  # the norm could be 0.0 since we normalized

    def rating_mean(df, track_index):
        track = df.iloc[track_index].fillna(0)
        if np.count_nonzero(track) == 0:
            return 0
        return np.sum(track) / np.count_nonzero(track)

    height = n_matrix.shape[0]
    n_sim_matrix = np.empty((height, height))
    columns = n_matrix.index.values
    for i in range(height): # for each track
        for j in range(height):
            n_sim_matrix[i][j] = cos_measure(n_matrix, i, j)
    n_sim_matrix = pd.DataFrame(n_sim_matrix, columns=n_matrix.index.values)

    # Predict the weighted average
    def predict(df, sim_matrix, element_index, user_index):
        user_col = df.iloc[:, user_index]

        upper_sum = 0
        lower_sum = 0
        for index, el in enumerate(sim_matrix.iloc[:, element_index]):
            if el >= 0 and el <= 0.99 and not math.isnan(el) and not math.isnan(user_col[index]):
                upper_sum += el * user_col[index]
                lower_sum += el
        if lower_sum == 0:
            return - math.inf
        return upper_sum / lower_sum

    # we compute the predictions
    userToPredict = []
    userToPredict.append([2,3,4,5,6,10,11,14,15,18])
    userToPredict.append([0,2,3,8,12,13,14,18,19])
    userToPredict.append([2,3,4,5,6,7,10,12,13,14,15,17,19])
    userToPredict.append([2,3,7,8,9,10,12,13,14,15,16])
    userToPredict.append([1,2,4,5,6,7,8,9,10])

    for i in range(5):
        for j in range(20):
            if predict(matrix, n_sim_matrix, j, i) > rating_mean(matrix, j) and j in userToPredict[i]:
                print("user_{} should listen music {}".format(i, j))
