import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
from math import ceil
import base64
import datetime
from urllib.parse import urlencode
import requests
import spotipy.util as util



class SpotifyHandler:

    def __init__(self, client_id, client_secret, redirect_uri):
        print('Creation d\'un client spotify')
        os.environ['SPOTIPY_CLIENT_ID'] = client_id
        os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
        os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri
        
        scope = "user-library-read playlist-modify-private playlist-modify-public"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        #print('test')
        #token = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        #cache_token = token.get_access_token()
        #print(cache_token)
        #self.sp = spotipy.Spotify(cache_token)

        #self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),scope=scope)
        
        #username = 'serilba@laposte.net'
        #scope = "user-library-read playlist-modify-private playlist-modify-public"
        #token = util.prompt_for_user_token(username, scope)
        #self.sp = spotipy.Spotify(auth=token)
        #results = sp.current_user_saved_tracks()

        #access_token = None
        #token_url = "https://accounts.spotify.com/api/token"
        #if client_secret == None or client_id == None:
          #raise Exception("You must set client_id and client_secret")
        #client_creds = f"{client_id}:{client_secret}"
        #client_creds_b64 = base64.b64encode(client_creds.encode())
        #print(client_creds)
        #print(client_creds_b64)
        #token_headers = {"Authorization": f"Basic {client_creds_b64}"}
        #token_data = {"grant_type": "client_credentials"}
        #r = requests.post(token_url, data=token_data, headers=token_headers)
        #print(r)
        #print(r.status_code)
        #if r.status_code not in range(200, 299): 
            #print("Could not authenticate client")
        #print('yolo')
        #data = r.json()
        #print(data)
        #access_token = data['access_token']
        #print(access_token)
        #self.sp = spotipy.Spotify(auth=access_token)

        try :
            self.user_id = self.sp.current_user()['id']
        except :
            print("Erreur d'authentification Spotify : suppression du cache et re-tentative")
            os.remove(".cache")
            self.user_id = self.sp.current_user()['id']

    def find_tracks_in_playlists(self, input_playlist_dict):
        sptfy_playlist_dict = {}
        # Dictionnaire de la forme : { <NomPlaylist> : liste d'IDs de morceaux à ajouter à la playlist}

        for input_playlist in input_playlist_dict:
            # if input_playlist == 'Epica': #AFAC
            sptfy_track_list = []
            print('INFO : Recherche des morceaux équivalents pour la playlist : ' + input_playlist)

            for input_track in input_playlist_dict[input_playlist]:
                track_name, track_artist, track_album = input_track[0], input_track[1], input_track[2]
                print('INFO : Recherche du morceau : ' + track_name)
                sptfy_track_result_list = self.find_track(track_name, track_artist, track_album)
                # if sptfy_track_result_list:
                # On ajoute le résultat même si c'est une chaîne vide afin d'avoir autant d'élément qu'au départ
                sptfy_track_list.append(sptfy_track_result_list)

            if sptfy_track_list :
                sptfy_playlist_dict[input_playlist] = sptfy_track_list
            else :
                print('ERREUR : Aucun résultat pour les morceaux de la playlist ' + input_playlist + '. La playlist ne sera pas créée.')

        print(sptfy_playlist_dict)
        return sptfy_playlist_dict

    # Recherche un morceau sur Spotify puis vérifie si l'artiste et l'album correspondent
    # Si oui, renvoie une liste d'un seul élément (liste) contenant l'id du morceau, son artiste et son album
    # Si non, renvoie une liste de jusqu'à 5 éléments (listes), chacune contenant l'id d'un morceaux, son artiste et son album
    # Exemple de renvoi : [[id, nom, artiste, album], [id2, nom2, artiste2, album2]], False
    def find_track(self, track_name, track_artist=None, track_album=None):
        if len(track_name)>100 :
            track_name = track_name[:99]
        query_result = self.sp.search(track_name, limit=5, type='track')['tracks']['items']
        exact_track_found = False
        result = []
        if not query_result :
            print("ERREUR : Aucun résultat")
        else :
            result_tracks_list = []
            # On parcourt les résultats (5 max)
            for elem in query_result:
                result_track_uri = elem['id']
                current_track = self.sp.track(result_track_uri)
                # On stocke les infos de du résultat courant dans une liste formatée plus simplement
                current_track_data = [result_track_uri, current_track['name'], current_track['artists'][0]['name'], current_track['album']['name']]
                # On ajoute ce résultat à la liste des résultats potentiels
                result_tracks_list.append(current_track_data)
                # Si le résultat courant correspond exactement au morceau cherché, on ne renvoie que celui-là ; sinon on continue de parcourir en ajoutant les morceaux aux résultat potentiels
                if current_track_data[1] == track_name and current_track_data[2] == track_artist and current_track_data[3] == track_album:
                    result_tracks_list = current_track_data
                    result = result_tracks_list
                    exact_track_found = True
                    print('INFO : Morceau exact trouvé')
                    break
            # Si aucun résultat exact n'a été trouvé, on renvoie le premier résultat
            if not exact_track_found :
                print('AVERTISSEMENT : le morceau exact n\'a pas été trouvé')
                result = result_tracks_list[0]
        return result

    def create_playlist(self, playlist_name, playlist_description):
        playlist_already_exists, playlist_id = self.find_playlist_by_name(playlist_name)
        if not playlist_already_exists:
            created_playlist = self.sp.user_playlist_create(self.user_id, playlist_name, False, False, playlist_description)
            playlist_id = created_playlist['id']
        print("Playlist id = " + playlist_id)
        return playlist_id

    def find_playlist_by_name(self, playlist_name):
        user_playlists = self.sp.user_playlists(self.user_id)
        for playlist in user_playlists['items']:
            print("Playlist courante : " + playlist['name'])
            if playlist_name == playlist['name']:
                print('Une playlist existe déjà avec ce nom')
                return True, playlist['id']
        return False, None

    # Ajoute des morceaux à une playlist
    # Format de tracks_list : liste d'URI
    def add_tracks_to_playlist(self, playlist_id, tracks_list):
        # On découpe en paquets de 99 tracks car c'est la limite de l'API
        API_limit = 99
        nb_tracks = len(tracks_list)
        nb_packets = ceil(nb_tracks / API_limit)
        last_packet_length = nb_tracks % API_limit
        j = 0
        for i in range(nb_packets - 1):
            self.sp.playlist_add_items(playlist_id, tracks_list[j:(j + API_limit)])
            j += API_limit
        if last_packet_length > 0:
            self.sp.playlist_add_items(playlist_id, tracks_list[j:(j + last_packet_length)])
    
    # Récupère les playlists
    def get_playlists(self):
        playlists = self.sp.current_user_playlists()
        playlists_dict = {}
        for playlist in playlists['items']:
            playlists_dict[playlist['name']] = {}
            playlists_dict[playlist['name']]['id'] = playlist['id']
            playlists_dict[playlist['name']]['tracks'] = ['TODO']
            # TODO: add list of tracks in this playlist!
        return playlists_dict

    # Récupère les morceaux d'une playlist
    def get_playlist_tracks(self,playlist_id):
        tracks = self.sp.playlist(playlist_id,additional_types=('track'))
        print('##########################')
        print(tracks['items'])