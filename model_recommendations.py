import pandas as pd 
import os 
import numpy as np 
path = '/Users/akshay/Documents/interviews/adobe_case_study/'

ratings_df = pd.read_csv(os.path.join(path,'data','ratings.csv'))

movies_df = pd.read_csv(os.path.join(path,'data','movies.csv'))

tmdb_df = pd.read_csv(os.path.join(path,'data','tmdb_data_combine.csv'))

links_df = pd.read_csv(os.path.join(path,'data','links.csv'))

links_df = links_df.dropna(axis=0)
links_df['tmdbId'] = links_df['tmdbId'].astype('int')
master_df = ratings_df.merge(links_df , how='left' , on='movieId')
master_df = master_df.dropna(axis=0)
master_df['imdbId'] = master_df['imdbId'].astype('int')
master_df['tmdbId'] = master_df['tmdbId'].astype('int')
master_df = master_df.merge(tmdb_df, how='left' , left_on='tmdbId' , right_on='id')
master_df = master_df.dropna(axis=0)
master_df = master_df.merge(movies_df[['movieId','title','genres']].copy() , how='left' , on='movieId')

def get_master_df():
    return master_df

def load_model(model_filename):
    print (">> Loading dump")
    from surprise import dump
    import os
    file_name = os.path.expanduser(model_filename)
    _, loaded_model = dump.load(file_name)
    print (">> Loaded dump")
    return loaded_model


def generate_recommendation_svd(user_id, master_df , n_items=5):
   # Get a list of all movie IDs from dataset
   movie_ids = master_df["movieId"].unique()
 
   # Get a list of all movie IDs that have been watched by user
   movie_ids_user = master_df.loc[master_df["userId"] == user_id, "movieId"]

    # Get a list off all movie IDS that that have not been watched by user
   movie_ids_to_pred = np.setdiff1d(movie_ids, movie_ids_user)
 
   # Apply a rating of 1 to all interactions (only to match the Surprise dataset format)
   test_set = [[user_id, movie_id, 1] for movie_id in movie_ids_to_pred]
 
   # Predict the ratings and generate recommendations
   model = load_model('./model.pickle')
   predictions = model.test(test_set)
   pred_ratings = np.array([pred.est for pred in predictions])
#    print("Top {0} item recommendations for user {1}:".format(n_items, user_id))
   # Rank top-n movies based on the predicted ratings
   index_max = (-pred_ratings).argsort()[:n_items]
   movie_ids_to_pred = movie_ids_to_pred[index_max]
   return master_df[master_df['movieId'].isin(movie_ids_to_pred)][['original_title' , 'runtime' ,  'cast' , 'genres']].drop_duplicates()