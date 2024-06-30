import streamlit as st
import pandas as pd
import DeezerHandler as dh
import SpotifyHandler as sh

# first ask user ID :
# TODO: ask user app_id, app_secret, access_token infos
deezer_handler = dh.DeezerHandler()

try:
    user_id = st.text_input("Put your Deezer user ID", "example : 87654")
    st.write("The user is", deezer_handler.get_user_name(user_id))
except Exception as e:
    st.write("Wrong user ID 🫣")
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
        edited_df = st.data_editor(df)
        #col1, col2 = st.columns(2)
        #col1.data_editor(df)
        #col2.data_editor(df_spotify)
        #tabs
        #tab1, tab2 = st.tabs(["Data", "Chart"])
        #with tab1:
        #    st.table(df)

