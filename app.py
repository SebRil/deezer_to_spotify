import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import DeezerHandler as dh
import SpotifyHandler as sh

def initialize_dzr_inputs(migrate_from_dzr):
    st.sidebar.title('Deezer')
    if migrate_from_dzr:
        deezer_element_choice = st.sidebar.selectbox(
            'What element would you like to retrieve from Deezer?',
            ('One public playlist', 'A user\'s public playlists', 'All playlists from a user')
        )
    else:
        deezer_element_choice='All playlists from a user'

    # Deezer Inputs can be either:
    # - Playlist ID
    # - User ID (public playlists)
    # - User application (private playlists)
    dzr_playlist_id = ''
    dzr_user_id = ''
    dzr_app_id,dzr_app_secret,dzr_access_token='','',''
    default_value = 'example: 12345678'
    if deezer_element_choice == 'One public playlist':
        dzr_playlist_id = st.sidebar.text_input("Playlist ID", default_value)
    elif deezer_element_choice == 'A user\'s public playlists':
        st.title('Feature not yet implemented, please wait! 😊⏱️')
        dzr_user_id = st.sidebar.text_input("Deezer user ID", default_value)
    elif deezer_element_choice == 'All playlists from a user':
        st.title('Feature not yet implemented, please wait! 😊⏱️')
        dzr_app_id = st.sidebar.text_input("Deezer Application ID", "")
        dzr_app_secret = st.sidebar.text_input("Deezer Application Secret", "")
        dzr_access_token = st.sidebar.text_input("Deezer Redirect URI", "")

    if dzr_playlist_id != '' and dzr_playlist_id != default_value:
        return {'input':dzr_playlist_id,'type':'playlist'}
    if dzr_user_id != '' and dzr_user_id != default_value:
        return {'input':dzr_user_id,'type':'user'}
    if dzr_app_id != '' and dzr_app_secret != '' and dzr_access_token != '':
        return {'input':(dzr_app_id,dzr_app_secret,dzr_access_token),'type':'app'}


def initialize_sptfy_inputs():
    st.sidebar.title('Spotify')
    spfy_app_id = st.sidebar.text_input("Spotify Application ID", "")
    spfy_app_secret = st.sidebar.text_input("Spotify Application Secret", "")
    spfy_access_token= st.sidebar.text_input("Spotify Redirect URI", "")
    global sptfy_handler
    if spfy_app_id != '' and spfy_app_secret != '' and spfy_access_token != '':
        try:
            sptfy_handler = sh.SpotifyHandler(spfy_app_id,spfy_app_secret,spfy_access_token)
            st.sidebar.write("Successfully connected to Spotify! 😊")
        except Exception as e:
            st.sidebar.write("Couldn't connect to this Spotify App 🫣")
            sptfy_handler = None


def search_sptfy_songs(dzr_songs):
    results=[]
    for index,dzr_song in dzr_songs.iterrows():
        matching_track = sptfy_handler.find_track(track_name=dzr_song['Title'],track_artist=dzr_song['Artist'],track_album=dzr_song['Album'])
        if matching_track is not None:
            results.append(matching_track)
    return results

def handle_deezer_input_playlist(playlist_id):
    try:
        deezer_handler = dh.DeezerHandler()
        playlist = deezer_handler.get_public_playlist(playlist_id)
        st.title(playlist.title)
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
            column_config={
                "Select": st.column_config.CheckboxColumn(
                    "Select",
                    help="Migrate this song",
                    default=False,
                )
            },
            disabled=["Title","Artist","Album"],
            hide_index=True,
        )
        selected_rows = dzr_track_array[dzr_track_array.Select]

        sptfy_playlist_name = st.text_input("Target Spotify Playlist Name",playlist.title)
        sptfy_playlist_desc= st.text_input("Target Spotify Playlist Description",'')

        sptfy_matches = None
        if st.button('Migrate to Spotify'):
            sptfy_matches = search_sptfy_songs(selected_rows)
            if sptfy_matches is not None:
                # Create the new playlist
                sptfy_playlist_id = sptfy_handler.create_playlist(sptfy_playlist_name,sptfy_playlist_desc)
                if sptfy_playlist_id is not None:
                    # Keep only URI to add to the playlist
                    tracks_uri = [elem[0] for elem in sptfy_matches]
                    # Add tracks to the playlist
                    sptfy_handler.add_tracks_to_playlist(sptfy_playlist_id,tracks_uri)
                    # Display recap
                    st.title('Migration recap')
                    st.write('The following tracks were added to the new playlist:')
                    sptfy_df = pd.DataFrame.from_records(sptfy_matches, columns=["Id","Title", "Artist", "Album"])
                    sptfy_track_array = st.data_editor(
                        sptfy_df,
                        disabled=["Id","Title","Artist","Album"],
                        column_order=("Title", "Artist", "Album")
                    )
                else:
                    st.write('A playlist already exists with this name 🫣')


def handle_deezer_input_user(dzr_user_id):
    try:
        deezer_handler = dh.DeezerHandler()
        st.title("{0}'s playlists".format(deezer_handler.get_user_name(dzr_user_id)))
    except Exception as e:
        st.sidebar.write("Wrong user ID 🫣")
        dzr_user_id = None

    #TODO: implement feature

    if dzr_user_id is not None:
        deezer_playlists = deezer_handler.get_playlists_from_user(dzr_user_id)

        selected_playlists = st.multiselect(
            "Select playlists you want to migrate",
            list(deezer_playlists.keys()),
            [])

        for playlist in selected_playlists:
            st.title('Migrate playlist %s' % playlist)
            df = pd.DataFrame(deezer_playlists[playlist], columns=["Title", "Artist", "Album"])
            df_spotify = pd.DataFrame([["Test1", "Test1", "Test1"],["Test2", "Test2", "Test2"]],columns=["Title", "Artist", "Album"])
            #edited_df = st.data_editor(df)
            edited_df = st.table(df)
            #col1, col2 = st.columns(2)
            #col1.data_editor(df)
            #col2.data_editor(df_spotify)
            #tabs
            #tab1, tab2 = st.tabs(["Data", "Chart"])
            #with tab1:
            #    st.table(df)


def handle_deezer_input_app(app_input):
    app_id, app_secret, app_token = app_input
    #TODO: implement feature


print('################################## RUN ################################## ')
toggle_label = (
    'Migrate from Deezer'
    if st.session_state.get('my_toggle', False)
    else "Migrate from Spotify"
)
toggle_value = st.session_state.get("my_toggle", False)
is_toggle = st.sidebar.toggle(toggle_label, value=toggle_value, key="my_toggle")

if toggle_value:
    dzr_inputs = initialize_dzr_inputs(True)

initialize_sptfy_inputs()

if not toggle_value:
    dzr_inputs= initialize_dzr_inputs(False)

if dzr_inputs is not None:
    if dzr_inputs['type'] == 'playlist':
        handle_deezer_input_playlist(dzr_inputs['input'])
    #elif dzr_inputs['type'] == 'user':
        #handle_deezer_input_user(dzr_inputs['input'])
    #elif dzr_inputs['type'] == 'user':
        #handle_deezer_input_app(dzr_inputs['input'])
