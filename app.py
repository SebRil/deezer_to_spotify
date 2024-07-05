import streamlit as st
import pandas as pd
import DeezerHandler as dh
import SpotifyHandler as sh

# Deezer Inputs can be either:
# - Playlist ID
# - User ID (public playlists)
# - User application (private playlists)

# Left menu
# Deezer elements
st.sidebar.text('Deezer')
deezer_element_choice = st.sidebar.selectbox(
    'What element would you like to retrieve from Deezer?',
    ('One public playlist', 'A user\'s public playlists', 'All playlists from a user')
)
dzr_playlist_id = ''
dzr_user_id = ''
dzr_app_id,dzr_app_secret,dzr_access_token='','',''
default_value = 'example: 12345678'
if deezer_element_choice == 'One public playlist':
    dzr_playlist_id = st.sidebar.text_input("Playlist ID", default_value)
elif deezer_element_choice == 'A user\'s public playlists':
    dzr_user_id = st.sidebar.text_input("Deezer user ID", default_value)
elif deezer_element_choice == 'All playlists from a user':
    dzr_app_id = st.sidebar.text_input("Application ID", "")
    dzr_app_secret = st.sidebar.text_input("Application Secret", "")
    dzr_access_token = st.sidebar.text_input("Redirect URI", "")

# Spotify elements
st.sidebar.text('Spotify')
spfy_app_id = st.sidebar.text_input("Application ID", "")
spfy_app_secret = st.sidebar.text_input("Application Secret", "")
spfy_access_token = st.sidebar.text_input("Redirect URI", "")


# Methods
def handle_deezer_input_playlist(playlist_id):
    try:
        deezer_handler = dh.DeezerHandler()
        playlist = deezer_handler.get_public_playlist(playlist_id)
        st.write("The playlist title is", playlist.title)
    except Exception as e:
        st.sidebar.write("Wrong playlist ID 🫣")
        playlist = None

    if playlist is not None:
        tracks = {}
        tracks = deezer_handler.get_playlist_as_dir([playlist],tracks)
        print(tracks)
        #df = pd.DataFrame([tracks[0]], columns=["Title", "Author", "Album"])
        df = pd.DataFrame.from_dict(tracks)#, columns=["Title", "Author", "Album"])
        #df_spotify = pd.DataFrame([["Test1", "Test1", "Test1"],["Test2", "Test2", "Test2"]],columns=["Title", "Author", "Album"])
        #edited_df = st.data_editor(df)
        edited_df = st.table(df)
        #col1, col2 = st.columns(2)
        #col1.data_editor(df)
        #col2.data_editor(df_spotify)
        #tabs
        #tab1, tab2 = st.tabs(["Data", "Chart"])
        #with tab1:
        #    st.table(df)

def handle_deezer_input_user(dzr_user_id):
    try:
        deezer_handler = dh.DeezerHandler()
        st.sidebar.write("The user is", deezer_handler.get_user_name(dzr_user_id))
    except Exception as e:
        st.sidebar.write("Wrong user ID 🫣")
        dzr_user_id = None

    if dzr_user_id is not None:
        deezer_playlists = deezer_handler.get_playlists_from_user(dzr_user_id)

        selected_playlists = st.multiselect(
            "Select playlists you want to migrate",
            list(deezer_playlists.keys()),
            [])

        for playlist in selected_playlists:
            st.title('Migrate playlist %s' % playlist)
            df = pd.DataFrame(deezer_playlists[playlist], columns=["Title", "Author", "Album"])
            df_spotify = pd.DataFrame([["Test1", "Test1", "Test1"],["Test2", "Test2", "Test2"]],columns=["Title", "Author", "Album"])
            #edited_df = st.data_editor(df)
            edited_df = st.table(df)
            #col1, col2 = st.columns(2)
            #col1.data_editor(df)
            #col2.data_editor(df_spotify)
            #tabs
            #tab1, tab2 = st.tabs(["Data", "Chart"])
            #with tab1:
            #    st.table(df)

def handle_deezer_input_app(app_id, app_secret, app_token):
    pass

if dzr_playlist_id != '' and dzr_playlist_id != default_value:
    handle_deezer_input_playlist(dzr_playlist_id)
if dzr_user_id != '' and dzr_user_id != default_value:
    handle_deezer_input_user(dzr_user_id)

if spfy_app_id != '' and spfy_app_secret != '' and spfy_access_token != '':
    try:
        spotify_handler = sh.SpotifyHandler(spfy_app_id,spfy_app_secret,spfy_access_token)
        st.sidebar.write("Successfully connected to Spotify! 😊")
    except Exception as e:
        st.sidebar.write("Couldn't connect to this Spotify App 🫣")
        spotify_handler = None
    
    if spotify_handler is not None:
        spotify_playlists = spotify_handler.get_playlists()

        selected_playlists = st.multiselect(
            "Select playlists you want to browse",
            list(spotify_playlists.keys()),
            [])

        for selected_playlist in selected_playlists :
            print('Getting tracks from playlist ' + selected_playlist + ' id (' + spotify_playlists[selected_playlist]['id'] + ')')
            spotify_handler.get_playlist_tracks(spotify_playlists[selected_playlist]['id'])
