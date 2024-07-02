import streamlit as st
import pandas as pd
import DeezerHandler as dh
import SpotifyHandler as sh

# Deezer Inputs can be either:
# - Playlist ID
# - User ID (public playlists)
# - User application (private playlists)
# TODO: ask user app_id, app_secret, access_token infos
deezer_handler = dh.DeezerHandler()

# Left menu
deezer_element_choice = st.sidebar.selectbox(
    'What element would you like to retrieve from Deezer?',
    ('One public playlist', 'A user\'s public playlists', 'All playlists from a user')
)
playlist_id = ''
user_id = ''
app_id,app_secret,access_token='','',''
default_value = 'example: 12345678'
if deezer_element_choice == 'One public playlist':
    playlist_id = st.sidebar.text_input("Playlist ID", default_value)
elif deezer_element_choice == 'A user\'s public playlists':
    user_id = st.sidebar.text_input("Deezer user ID", default_value)
elif deezer_element_choice == 'All playlists from a user':
    app_id = st.sidebar.text_input("Application ID", "")
    app_secret = st.sidebar.text_input("Application Secret", "")
    access_token = st.sidebar.text_input("Access Token", "")

if playlist_id != '' and playlist_id != default_value:
    #TODO
    pass
if user_id != '' and user_id != default_value:
    try:
        st.sidebar.write("The user is", deezer_handler.get_user_name(user_id))
    except Exception as e:
        st.sidebar.write("Wrong user ID 🫣")
        user_id = None

    if user_id is not None:
        deezer_playlists = deezer_handler.get_playlists_from_user(user_id)

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

