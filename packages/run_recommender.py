import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette("Set2")
from sklearn.metrics.pairwise import cosine_similarity

def get_feature_vector(song_name, year, dat, features_list):
    print(dat.head())
    # select dat with the song name and year
    dat_song = dat.query('name == @song_name and year == @year')
    song_repeated = 0
    if len(dat_song) == 0:
        raise Exception('The song does not exist in the dataset or the year is wrong! \
                        \n Use search function first if you are not sure.')
    if len(dat_song) > 1:
        song_repeated = dat_song.shape[0]
        print(f'Warning: Multiple ({song_repeated}) songs with the same name and artist, the first one is selected!')
        dat_song = dat_song.head(1)
    feature_vector = dat_song[features_list].values
    return feature_vector, song_repeated

# define a function to get the most similar songs
import pandas as pd
import urllib.parse
import matplotlib.pyplot as plt
import seaborn as sns

def show_similar_songs(song_name, year, dat, features_list, top_n=10):
    """
    A function to get the most similar songs based on the cosine similarity of the features.
    :param song_name: the name of the song (all letters)
    :param year: the year of the song [int]
    :param dat: the dataset
    :param features_list: the list of features to be used for similarity calculation
    :param top_n: the number of similar songs to be returned
    :return: DataFrame containing the most similar songs or an empty DataFrame if no similar songs are found
    """
    feature_vector, song_repeated = get_feature_vector(song_name, year, dat, features_list)
    feature_for_recommendation = dat[features_list].values
    # calculate the cosine similarity
    similarities = cosine_similarity(feature_for_recommendation, feature_vector).flatten()

    # get the index of the top_n similar songs not including itself
    if song_repeated == 0:
        related_song_indices = similarities.argsort()[-(top_n+1):][::-1][1:]
    else:
        related_song_indices = similarities.argsort()[-(top_n+1+song_repeated):][::-1][1+song_repeated:]

    # get the name, artist, and year of the most similar songs
    similar_songs = dat.iloc[related_song_indices][['name', 'artists', 'year']]
    similar_songs['Similarity'] = similarities[related_song_indices]
    # Add the Spotify link column
    # base_url = 'https://open.spotify.com/search/'
    # encoded_songs = similar_songs['name'].apply(lambda x: urllib.parse.quote(x))
    # encoded_artists = similar_songs['artists'].apply(lambda x: urllib.parse.quote(x))
    # spotify_links = base_url + encoded_songs + ' ' + encoded_artists

    # # Create the 'Click' column with clickable links
    # similar_songs['Click'] = spotify_links.apply(lambda x: f"[Click]({x})")

    # Update the column name to 'Click' for all songs
    # similar_songs.rename(columns={'Spotify Link': 'Click'}, inplace=True)

    similar_songs.reset_index(drop=True, inplace=True) 

    
    
    return similar_songs

