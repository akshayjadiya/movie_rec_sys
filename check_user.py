import pandas as pd 
import os 
path = '/Users/akshay/Documents/interviews/adobe_case_study/'
ratings_df = pd.read_csv(os.path.join(path,'data','ratings.csv'))


def check_user(user_id):
    movie_ids_user = ratings_df.loc[ratings_df["userId"] == user_id, "movieId"]
    return len(movie_ids_user)

