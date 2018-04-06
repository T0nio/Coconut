import numpy as np
import pandas as pd
import os
from model.track_collection import TrackCollection
from utils.collection_splitter import splitter
from agent.server import Server
from agent.user import User

#### CONFIG 
number_of_users = 10

### Loading the tracks data; and splitting them into number_of_users collections

track_collection = TrackCollection()
track_collection.load(os.path.join('data', 'track_collection_test.json'))
df_track_collection = track_collection.to_dataframe()
track_list = df_track_collection[['id']]
"""
user_collections = splitter(track_collection, number_of_users, 0.3)
user_dfs = []

### Generating the users_dataframes vector with all tracks and their ratings

for user_collection in user_collections:
  ndf = user_collection.to_dataframe()[['id', 'rating_score']]
  user_matrix = track_list.merge(ndf, on='id', how='left').fillna(0)
  user_dfs.append(user_matrix[['rating_score']])
"""


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
