import pandas as pd 
import os 

path = os.getcwd()
ratings_df = pd.read_csv(os.path.join(path,'ratings.csv'))


def check_user(user_id):
    movie_ids_user = ratings_df.loc[ratings_df["userId"] == user_id, "movieId"]
    return len(movie_ids_user)

