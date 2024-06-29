# _*_ coding:utf-8 _*_
from DeezerHandler import DeezerHandler
from SpotifyHandler import SpotifyHandler

deezerHandler = DeezerHandler()
dzr_playlist_dict = deezerHandler.get_playlists_from_user(1411619) # ID de Kafiolet : 1411619

spotifyHandler = SpotifyHandler('29f0d515bedc41a9922e0bdb002d3156', '25acc9c6e17b4b1dac8fb29bd58dae32', 'http://localhost')
spotify_playlist_dict = spotifyHandler.find_tracks_in_playlists(dzr_playlist_dict)
for playlist in spotify_playlist_dict:
    playlist_id = spotifyHandler.create_playlist("RammsteinTest", "Playlist de Rammstein de test")
    print(spotify_playlist_dict[playlist])
    spotifyHandler.add_tracks_to_playlist(playlist_id, spotify_playlist_dict[playlist])
