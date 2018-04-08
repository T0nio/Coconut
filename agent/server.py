import random

class Server(object):
  def __init__(self, users, track_list):
    self.__users = users
    self.track_list = track_list
    self.__averages = pd.DataFrame(0, index=np.arange(len(track_list)), columns=['av'])
    self.__similarity_matrix = []
  
  def run(self):
    self.__compute_averages()
    self.__spread_averages()
    self.__compute_similarity_matrix()
    self.__spread_similarity_matrix()

  def __compute_averages(self):
    for track in self.track_list.iterrows():
      user = random.choice(self.__users)
      self.__averages.iloc[track.id] = user.compute_average(int(track.id))
    
  def __spread_averages(self):
    for user in self.__users:
      user.save_averages(self.__averages)

    
  def __compute_similarity_matrix(self):
    for user in self.__users:
      user.compute_normalized_vector()
    return False

  def __spread_similarity_matrix(self):
    for user_id, user in self.__users:
      self.__users[user_id].save_similarity_matrix(self.__similarity_matrix)


