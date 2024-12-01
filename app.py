import streamlit as st
import pandas as pd
import DeezerHandler as dh
import SpotifyHandler as sh

# Deezer Inputs can be either:
# - Playlist ID
# - User ID (public playlists)
# - User application (private playlists)

st.set_page_config(page_title='Deezer To Spotify Migration by Seb!', layout='wide')

def reset_session(caller):
    print("Reset cache initiated by " + caller)
    st.session_state.search_songs = False
    st.session_state.sptfy_matches = []
    st.session_state.playlist_created_success = ''
    if('caller' == 'sptf_inputs'):
        st.session_state.spotify_handler = None

# Left menu
# Deezer elements
global deezer_handler
deezer_handler=None
#st.sidebar.text('Deezer')
st.sidebar.title('Deezer')
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
    st.write("This feature has not been implemented! 🥵")
elif deezer_element_choice == 'All playlists from a user':
    dzr_app_id = st.sidebar.text_input("Deezer Application ID", "")
    dzr_app_secret = st.sidebar.text_input("Deezer Application Secret", "")
    dzr_access_token = st.sidebar.text_input("Deezer Application Redirect URI", "")
    st.write("This feature has not been implemented! 🥵")

# Spotify elements
#global sptfy_handler
#sptfy_handler=None
st.sidebar.title('Spotify')
spfy_app_id = st.sidebar.text_input("Spotify Application ID", "",on_change=reset_session, args=('sptf_inputs',))
spfy_app_secret = st.sidebar.text_input("Spotify Application Secret", "",on_change=reset_session, args=('sptf_inputs',))
spfy_access_token = st.sidebar.text_input("Spotify Application Redirect URI", "",on_change=reset_session, args=('sptf_inputs',))

# Initiate session variables
if 'search_songs' not in st.session_state:
    st.session_state.search_songs = False

# Methods
def search_sptfy_songs(dzr_songs, sptfy_handler):
    results=[]
    for index,dzr_song in dzr_songs.iterrows():
        matching_track = sptfy_handler.find_track(track_name=dzr_song['Title'],track_artist=dzr_song['Artist'],track_album=dzr_song['Album'])
        print(matching_track)
        if matching_track is not None:
            results.append(matching_track)
    return results

def create_sptfy_playlist(sptfy_playlist_name, sptfy_playlist_desc, sptfy_matches,sptfy_handler):
    # Create the new playlist
    sptfy_playlist_id = sptfy_handler.create_playlist(sptfy_playlist_name,sptfy_playlist_desc)
    if sptfy_playlist_id is not None:
        # Keep only URI to add to the playlist
        tracks_uri = [elem[0] for elem in sptfy_matches]
        print(tracks_uri)
        # Add tracks to the playlist
        try:
            sptfy_handler.add_tracks_to_playlist(sptfy_playlist_id,tracks_uri)
            st.session_state.playlist_created_success = 'OK'
        except:
            st.session_state.playlist_created_success = 'TracksKO'
    else:
        st.session_state.playlist_created_success = 'PlaylistKO'
        st.write('A playlist already exists with this name 🫣')

def button_search_songs_clicked():
    st.session_state.search_songs = True

def handle_deezer_input_playlist(playlist_id):
    try:
        deezer_handler = dh.DeezerHandler()
        playlist = deezer_handler.get_public_playlist(playlist_id)
        st.write("The playlist title is", playlist.title)
    except Exception as e:
        st.sidebar.write("Wrong playlist ID 🫣")
        playlist = None

    if playlist is not None:
        select_all = st.checkbox('Select all')
        tracks = {}
        tracks = deezer_handler.get_playlist_as_dir([playlist],tracks)
        list_for_df = ((elem + [select_all]) for elem in tracks[playlist.title])
        dzr_df = pd.DataFrame(list_for_df, columns=["Title", "Artist", "Album","Select"])
        dzr_track_array = st.data_editor(
            dzr_df,
            use_container_width=True,
            column_config={
                "Select": st.column_config.CheckboxColumn(
                    "Select",
                    help="Migrate this song",
                    default=False,
                )
            },
            disabled=["Title","Artist","Album"],
            hide_index=True,
            on_change=reset_session,
            args=('Deezer table',)
        )
        selected_rows = dzr_track_array[dzr_track_array.Select]

        # Search for matching songs in Spotify
        sptfy_matches = None
        st.button('Search songs in Spotify', on_click=button_search_songs_clicked)
        if st.session_state.search_songs:
            print("Searching Spotify songs")
            if 'spotify_handler' in st.session_state:
                sptfy_handler = st.session_state.spotify_handler
            else:
                sptfy_handler=None
            if sptfy_handler is None:
                st.write('Please connect to your Spotify API application to search for songs 🫣')
            else:
                if len(selected_rows) == 0:
                    st.write('Please select some songs to migrate 🫣')
                else:
                    if st.session_state.sptfy_matches:
                        print('Retrieving matching songs from cache')
                        sptfy_matches = st.session_state.sptfy_matches
                    else:
                        print('Searching for songs in Spotify')
                        sptfy_matches = search_sptfy_songs(selected_rows, sptfy_handler)
                    print(sptfy_matches)
                    if sptfy_matches is not None:
                        st.session_state.sptfy_matches = sptfy_matches
                        # Display recap
                        st.title('Spotify search results')
                        st.write('The following tracks will be added to the new playlist:')
                        sptfy_df = pd.DataFrame.from_records(sptfy_matches, columns=["Id","Title", "Artist", "Album"])
                        sptfy_track_array = st.data_editor(
                            sptfy_df,
                            use_container_width=True,
                            disabled=["Id","Title","Artist","Album"],
                            column_order=("Title", "Artist", "Album")
                        )

                        # Add inputs for the new playlist
                        sptfy_playlist_name = st.text_input("Target Spotify Playlist Name",playlist.title)
                        sptfy_playlist_desc= st.text_input("Target Spotify Playlist Description",'')
                        if st.button('Create the playlist!', on_click=create_sptfy_playlist, args=(sptfy_playlist_name, sptfy_playlist_desc, sptfy_matches, sptfy_handler)):
                            if st.session_state.playlist_created_success == 'OK':
                                st.write('The playlist has been created! 🥳')
                            elif st.session_state.playlist_created_success == 'TracksKO':
                                st.write('Something went wrong when adding the tracks to the new playlist 🫣')
                            elif st.session_state.playlist_created_success == 'PlaylistKO':
                                st.write('The playlist could not be created (maybe this name is already taken?) 🫣')
                    else:
                        st.write('The corresponding songs in Spotify were not found 🫣')

def handle_deezer_input_user(dzr_user_id):
    try:
        deezer_handler = dh.DeezerHandler()
        st.write("The user is", deezer_handler.get_user_name(dzr_user_id))
    except Exception as e:
        st.sidebar.write("Wrong user ID 🫣")
        dzr_user_id = None

    st.write("This feature has not been implemented! 🥵")
    #if dzr_user_id is not None:
    #    deezer_playlists = deezer_handler.get_playlists_from_user(dzr_user_id)

    #    selected_playlists = st.multiselect(
    #        "Select playlists you want to migrate",
    #        list(deezer_playlists.keys()),
    #        [])

    #    for playlist in selected_playlists:
    #        st.title('Migrate playlist %s' % playlist)
    #        df = pd.DataFrame(deezer_playlists[playlist], columns=["Title", "Author", "Album"])
    #        df_spotify = pd.DataFrame([["Test1", "Test1", "Test1"],["Test2", "Test2", "Test2"]],columns=["Title", "Author", "Album"])
            #edited_df = st.data_editor(df)
    #        edited_df = st.table(df)
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
#if dzr_user_id != '' and dzr_user_id != default_value:
#    handle_deezer_input_user(dzr_user_id)

if spfy_app_id != '' and spfy_app_secret != '' and spfy_access_token != '':
    # Check if a spotify handler already exists in cache
    create_spotify_handler = True
    if 'spotify_handler' in st.session_state:
        if st.session_state.spotify_handler is not None:
            print('Récupération du spotify_handler depuis le cache')
            spotify_handler = st.session_state.spotify_handler
            create_spotify_handler = False
    # Create the spotify handler if needed
    if create_spotify_handler:
        print('Création du spotify_handler from scratch')
        try:
            spotify_handler = sh.SpotifyHandler(spfy_app_id,spfy_app_secret,spfy_access_token)
        except Exception as e:
            st.sidebar.write("Couldn't connect to this Spotify App 🫣")
            spotify_handler = None
        st.session_state.spotify_handler = spotify_handler
    if spotify_handler is not None:
        st.sidebar.write("Successfully connected to Spotify! 😊")
else:
    spotify_handler = None
