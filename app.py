import streamlit as st
import pandas as pd
import DeezerHandler as dh
import SpotifyHandler as sh

# first ask user ID :
# TODO: ask user app_id, app_secret, access_token infos
deezer_handler = dh.DeezerHandler()

try:
    user_id = st.text_input("Put your Deezer user ID", "example : 87654")
    st.write("The current movie title is", deezer_handler.get_user_name(user_id))
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
        edited_df = st.data_editor(df)