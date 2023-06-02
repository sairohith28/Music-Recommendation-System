import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import streamlit as st
from packages.search_song import search_song
from packages.run_recommender import get_feature_vector, show_similar_songs
# load data
dat = pd.read_csv('data/processed/dat_for_recommender.csv')

song_features_normalized = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness']
song_features_not_normalized = ['duration_ms', 'key', 'loudness', 'mode', 'tempo']

all_features = song_features_normalized + song_features_not_normalized + ['decade', 'popularity']

# set app layout
# st.set_page_config(layout="wide")

# set a good looking font
st.markdown(
    """
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



def main():
    st.markdown("# Your Customized Music Recommender")
    st.markdown("Welcome to this music recommender! \
                \n You can search for a song and get recommendations based on the song you searched for. \
                \n You can also customize the recommendations by selecting the features you care about. Enjoy!")

    # add selectbox for selecting the features
    st.sidebar.markdown("### Select Features")
    features = st.sidebar.multiselect('Select the features you care about', all_features, default=all_features)
    # add a slider for selecting the number of recommendations
    st.sidebar.markdown("### Number of Recommendations")
    num_recommendations = st.sidebar.slider('Select the number of recommendations', 10, 50, 10)

    # add a search box for searching the song by giving capital letters and year
    st.markdown("### Ready to get recommendations based on my song?")
    song_name = st.text_input('Enter the name of the song')
    if song_name != '':
        song_name = song_name.upper()
    year = st.text_input('Enter the year of the song (e.g. 2019). \
                         \nIf you are not sure if the song is in the database or not sure about the year, \
                         please leave the year blank and click the button below to search for the song.')
    if year != '':
        year = int(year)

    # exmaples of song name and year:
    # song_name = 'YOUR HAND IN MINE'
    # year = 2003

    # add a button for searching the song if the user does not know the year
    if st.button('Search for my song'):
        found_flag, found_song = search_song(song_name, dat)
        if found_flag:
            st.markdown("Perfect, this song is in the dataset:")
            st.markdown(found_song)
        else:
            st.markdown("Sorry, this song is not in the dataset. Please try another song!")

    # add a button for getting recommendations

# ...

    if st.button('Get Recommendations'):

        if song_name == '':
            st.markdown("Please enter the name of the song!")
        elif year == '':
            st.markdown("Please enter the year of the song!")
        else:
        # Get the most similar songs
            similar_songs = show_similar_songs(song_name, year, dat, features, top_n=num_recommendations)

            if len(similar_songs) > 0:
            # Display the recommendations in a table
                st.markdown(f"### Great! Here are your recommendations for {song_name} ({year})!")
                # st.table(similar_songs)
                st.table(similar_songs[['name', 'artists', 'year', 'Similarity']])
                fig_bar = plt.figure(figsize=(7, 5))
                similar_songs['name+year'] = similar_songs['name'] + ' (' + similar_songs['year'].astype(str) + ')'
        # create a dictionary of song and their similarity
                song_similarity = dict(zip(similar_songs['name+year'], similar_songs['Similarity']))
        # sort the dictionary by value
                song_similarity = sorted(song_similarity.items(), key=lambda x: x[1], reverse=True)
        # plot the text of the most similar songs and year in order, like a stacked bar chart
                plt.barh(range(len(song_similarity)), [val[1] for val in song_similarity], 
                 align='center', color=sns.color_palette('pastel', len(song_similarity)))
                plt.yticks(range(len(song_similarity)), [val[0] for val in song_similarity])
                plt.gca().invert_yaxis()
                plt.title(f'{num_recommendations} most similar songs to: {song_name} ({year})', fontsize=16)
                min_similarity = min(similar_songs['Similarity'])
                max_similarity = max(similar_songs['Similarity'])
        # add song name on the top of each bar
                for i, v in enumerate([val[0] for val in song_similarity]):
                    plt.text(min_similarity*0.955, i, v, color='black', fontsize=8)
        # plt.xlabel('Similarity', fontsize=15)
        # plt.ylabel('Song', fontsize=15)
                plt.xlim(min_similarity*0.95, max_similarity)
        # not show figure frame and ticks
                plt.box(False)
                plt.tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False, left=False, right=False, labelleft=False)
                st.pyplot(fig_bar)
            else:
                st.markdown("No recommendations found for the given song and year.")
if __name__ == "__main__":
    main()

    
    


