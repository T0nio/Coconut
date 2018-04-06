""" This was a work file trying the usage of the decentralized algorithm on the course example
	It helped us to be sure that the calculus was right.
"""

import numpy as np
import pandas as pd
import os
import math
from model.track_collection import TrackCollection
from utils.collection_splitter import splitter
from agent.server import Server
from agent.user import User


### Loading the tracks data; and splitting them into number_of_users collections
number_of_users = 12
n = math.nan
glob_df = pd.DataFrame(np.array([
		[1, n, 3, n, n, 5, n, n, 5, n, 4, n],
		[n, n, 5, 4, n, n, 4, n, n, 2, 1, 3],
		[2, 4, n, 1, 2, n, 3, n, 4, 3, 5, n],
		[n, 2, 4, n, 5, n, n, 4, n, n, 2, n],
		[n, n, 4, 3, 4, 2, n, n, n, n, 2, 5],
		[1, n, 3, n, 3, n, n, 2, n, n, 4, n],

]), columns=['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10', 'user11', 'user12'], dtype='float')


track_list = pd.DataFrame(np.array([[0], [1], [2], [3], [4], [5]]))

user_dfs = []
for j in range(12):
	i = j+1
	user_df = glob_df[['user'+str(i)]]
	user_df = user_df.rename(columns={'user'+str(i): 'rating_score'})
	user_dfs.append(user_df)

users = []
i = 0
for df in user_dfs:
	users.append(User(i, df))
	i += 1

### Generating the users
for user in users:
	if(user.id < number_of_users-1):
		user.nextNode = users[user.id+1]
	else:
		user.nextNode = users[0]

### Generating the server
server = Server(users, track_list)

### Running the server
server.run()

### Now all the users have the similarity matrix. So we can predict notes for users !

userToPredict = []
userToPredict.append([1,3,4])
userToPredict.append([0,1,4,5])
userToPredict.append([2])
userToPredict.append([0,3,5])
userToPredict.append([0,1])
userToPredict.append([1,2,3,5])
userToPredict.append([0,2,3,4,5])
userToPredict.append([0,1,2,4])
userToPredict.append([1,3,4,5])
userToPredict.append([0,3,4,5])
userToPredict.append([0])
userToPredict.append([0,2,3,5])

for i, uToPredict in enumerate(userToPredict):
    for j in uToPredict:
        if users[i].willILikeIt(j):
            print("User %d will probably like movie %i " % (i,j))
