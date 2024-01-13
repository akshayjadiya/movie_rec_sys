import pandas as pd 
import os 
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

def filter_for_genre(df , genre):
    filter_df = df[master_df['genres'] == genre][['original_title','runtime','cast','popularity']].\
                    sort_values(by='popularity' , ascending=False).\
                    drop_duplicates()
    
    return filter_df[:20]

def concat_dfs(df_list):
    concat_df = pd.concat(df_list)
    concat_df = concat_df.drop_duplicates()
    return concat_df

def return_random_movies(df , num_rec = 5):
    if(len(df) < num_rec):
        num_rec = len(df)

    return df.sample(num_rec)

def prettify_df(df):
    df = df.rename(columns = {'original_title' : 'Title' , 'runtime' : 'Runtime' , 'cast' : 'Cast'})
    return df[['Title' , 'Runtime' ,  'Cast']]

def _show_popular_recommendations(df , genres):
    all_dfs = []
    for genre in genres:
        filter_df = filter_for_genre(df , genre)
        all_dfs.append(filter_df)

    concat_df = concat_dfs(all_dfs)

    concat_df = return_random_movies(concat_df)

    concat_df = prettify_df(concat_df)

    return concat_df

def show_popular_recommendations(genres):
    
    return _show_popular_recommendations(master_df , genres)