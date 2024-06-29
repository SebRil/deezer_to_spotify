# -*- coding: utf-8 -*-
import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QScrollArea, QSizePolicy, QMainWindow

from SpotifyHandler import SpotifyHandler
from customWidgets import Playlist, SpotifyLogger, SpotifyAssociatedSongs, DeezerLogger
from DeezerHandler import DeezerHandler


class Ui_Dialog(QMainWindow):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.resize(1100, 600)
        self.setWindowTitle("Deezer To Spotify Playlists Migrator")
        self.Titre = QtWidgets.QLabel()
        # self.Titre.setGeometry(QtCore.QRect(10, 0, 160, 40))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Titre.setFont(font)
        # self.Titre.setTextFormat(QtCore.Qt.AutoText)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1100, 600))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        # self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.lb_Deezer_UserID = QtWidgets.QLabel()
        self.deezerUserId = QtWidgets.QLineEdit()
        self.deezerUserId.setText("1411619") #Daph : 2328033 ou 1071240304
        # self.setGridRowStretching([1, 1, 2, 2])
        self.setGridColStretching([1, 1, 5, 5, 2])
        self.Titre.setText("Deezer To Spotify")
        self.lb_Deezer_UserID.setText("Deezer User ID")
        self.lb_usr_connection = QtWidgets.QLabel("Connexion via ID d'utilisateur (playlists publiques uniquement)")
        self.lb_app_connection = QtWidgets.QLabel("Connexion via ID application Deezer dédiée (toutes les playlists)")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_app_connection.setFont(font)
        self.lb_usr_connection.setFont(font)
        self.btn_dzr_uid = QtWidgets.QPushButton()
        self.btn_dzr_app = QtWidgets.QPushButton()
        self.btn_dzr_uid.setText("Connexion publique")
        self.btn_dzr_app.setText("Connexion privée")
        self.gridLayout.addWidget(self.Titre, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.lb_usr_connection, 1, 1, 1, 3)
        self.gridLayout.addWidget(self.lb_app_connection, 5, 1, 1, 3)

        self.gridLayout.addWidget(self.lb_Deezer_UserID, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.deezerUserId, 2, 3, 1, 1)

        self.gridLayout.addWidget(self.btn_dzr_uid, 3, 2, 2, 2)
        self.gridLayout.addWidget(self.btn_dzr_app, 6, 2, 2, 2)

        # Autres éléments globaux non utilisés à l'initialisation
        self.spotify_handler = None
        self.playlists_list = []
        self.songs_layout = None
        self.deezer_logger = None
        # self.progress_bar = None

        # Connexions
        self.btn_dzr_app.clicked.connect(self.show_deezer_logger)
        self.btn_dzr_uid.clicked.connect(lambda x: self.connect_to_deezer(self.deezerUserId.text()))


    # Charge les playlists de l'utilisateur Deezer via son ID puis fait appel à la méthode showPlaylistPanel pour
    # afficher ces playlists
    def connect_to_deezer(self, dzr_uid, dzr_app_id=None, dzr_app_uri=None, dzr_app_secret=None):
        if self.deezer_logger:
            self.deezer_logger.close()
        self.empty_layout()
        # print(self.gridLayout.rowCount())
        # print(self.gridLayout.columnCount())
        self.setGridRowStretching([1])
        self.setGridColStretching([1])
        waiting_msg = QtWidgets.QLabel("Connexion en cours ...")
        font = QtGui.QFont()
        font.setPointSize(20)
        waiting_msg.setFont(font)
        self.gridLayout.addWidget(waiting_msg, 1, 1)
        # DeezerHandler
        if dzr_app_id and dzr_app_uri and dzr_app_secret :
            deezer_handler = DeezerHandler(dzr_app_id, dzr_app_uri, dzr_app_secret)
        else :
            deezer_handler = DeezerHandler()
        print("Récupération du username")
        dzr_username = deezer_handler.get_user_name(dzr_uid)
        print("Récupération des playlists publiques")
        dzr_playlists = deezer_handler.get_playlists_from_user(dzr_uid)
        print("Affichage des playlists")
        self.showPlaylistPanel(dzr_username, dzr_playlists)

    # Modifie l'IHM pour afficher 2 tableaux (playlists + morceaux de la playlist sélectionnée) et 2 boutons
    # (connexion à Spotify et recherche des playlists sur Spotify)
    def showPlaylistPanel(self, dzr_username, dzr_playlists):
        print("Affichage des playlists 2")
        self.empty_layout()
        self.setGridRowStretching([1, 2, 1, 20])
        self.setGridColStretching([5, 5, 5])

        # Ajout d'un texte de bienvenue
        welcome_msg = QtWidgets.QLabel("Bienvenue, " + dzr_username)
        font = QtGui.QFont()
        font.setPointSize(20)
        welcome_msg.setFont(font)
        self.gridLayout.addWidget(welcome_msg, 1, 0, 1, 4)
        welcome_msg = QtWidgets.QLabel("Vos playlists :")
        self.gridLayout.addWidget(welcome_msg, 2, 0)

        # Ajout d'un bouton de connexion à Spotify et d'un bouton de check des playlists
        connect_sptfy_button = QtWidgets.QPushButton("Connecter Spotify")
        check_playlist_button = QtWidgets.QPushButton("Rechercher les playlists sur Spotify")
        connect_sptfy_button.clicked.connect(self.show_spotify_logger)
        check_playlist_button.clicked.connect(lambda x: self.check_playlists_on_spotify(dzr_playlists))
        self.gridLayout.addWidget(connect_sptfy_button, 1, 1, 1, 1)
        self.gridLayout.addWidget(check_playlist_button, 1, 2, 1, 1)
        # self.add_progress_bar()

        # Création de la zone de parcours des playlists
        playlists_scroll_area = self.create_playlists_list(dzr_playlists)

        # Création de la zone de parcours des chansons
        songs_scroll_area = self.create_songs_list()

        self.gridLayout.addWidget(playlists_scroll_area, 3, 0, 1, 1)
        self.gridLayout.addWidget(songs_scroll_area, 3, 1, 1, 4)

    # Crée un widget de type QScrollArea contenant chaque playlist
    def create_playlists_list(self, dzr_playlists):
        # Ajout de la liste des playlist
        playlist_scroll_area = QScrollArea()
        playlist_layout = QVBoxLayout()
        playlist_widget = QtWidgets.QWidget()

        for i, playlist in enumerate(dzr_playlists):
            current_playlist = self.create_playlist(playlist, dzr_playlists[playlist])
            current_playlist.mouse_clicked_signal.connect(self.select_playlist)
            self.playlists_list.append(current_playlist)
            playlist_layout.addWidget(current_playlist)

        playlist_widget.setLayout(playlist_layout)
        # Scroll Area Properties
        playlist_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        playlist_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        playlist_scroll_area.setWidgetResizable(True)
        playlist_scroll_area.setWidget(playlist_widget)
        return playlist_scroll_area

    # Crée une playlist avec toutes ses chansons
    def create_playlist(self, playlist, songs_list):
        new_playlist = Playlist(playlist)
        # print(songs_list)
        for song in songs_list:
            new_playlist.add_song(song[0], song[1], song[2])
        return new_playlist

    # Sélectionne une playlist
    def select_playlist(self, event, playlist):
        for current_playlist in self.playlists_list:
            if not (playlist is current_playlist):
                current_playlist.set_unselected()
        playlist.toggle_selected()
        if playlist.selected:
            self.update_songs_list(playlist.songs_list, playlist.spotify_checked)
        else:
            self.update_songs_list()

    # Initialise la liste des chansons d'une playlist
    def create_songs_list(self):
        # Ajout de la liste des chansons
        songs_scroll_area = QScrollArea()
        self.songs_layout = QtWidgets.QGridLayout()
        songs_widget = QtWidgets.QWidget()
        songs_widget.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        songs_widget.setLayout(self.songs_layout)
        # Scroll Area Properties
        songs_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        songs_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        songs_scroll_area.setWidgetResizable(True)
        songs_scroll_area.setWidget(songs_widget)
        return songs_scroll_area

    # Met à jour la liste des chansons associées à la playlist courante
    def update_songs_list(self, songs_list=None, spotify_checked=False):
        self.empty_songs_layout()
        if songs_list:
            for i, song in enumerate(songs_list):
                if spotify_checked : # Si la chanson a été checkée sur Spotify, on connecte son bouton
                    song.on_btn_clicked.connect(self.show_associated_songs)
                self.songs_layout.addWidget(song, i, 0)
                self.songs_layout.setColumnStretch(0, 5)
                self.songs_layout.setColumnStretch(1, 1)

    def empty_songs_layout(self):
        for i in reversed(range(self.songs_layout.count())):
            self.songs_layout.itemAt(i).widget().setParent(None)

    def empty_layout(self):
        for i in reversed(range(self.gridLayout.count())):
            if not (self.gridLayout.itemAt(i).widget() == self.Titre) :
                self.gridLayout.itemAt(i).widget().deleteLater()

    # Définit le ratio d'affichage de chaque ligne (en facteur d'étendue)
    # rowStretchList : liste d'étendues de lignes [etendueLigne1, etendueLigne2, etc]
    def setGridRowStretching(self, rowStretchList):
        for i in range(len(rowStretchList)):
            self.gridLayout.setRowStretch(i, rowStretchList[i])

    # Définit le ratio d'affichage de chaque ligne (en facteur d'étendue)
    def setGridColStretching(self, colStretchList):
        for j in range(len(colStretchList)):
            self.gridLayout.setColumnStretch(j, colStretchList[j])

    # Ouvre le pop-up d'authentification à l'app Spotify permettant de gérer les playlists d'un user Spotify
    def show_spotify_logger(self):
        self.spotify_logger = SpotifyLogger()
        self.spotify_logger.show()
        self.spotify_logger.btn_connection.clicked.connect(
            lambda x: self.connect_to_spotify(self.spotify_logger.sptfy_client_id.text(),
                                              self.spotify_logger.sptfy_client_secret.text(),
                                              self.spotify_logger.sptfy_redirect_uri.text()))

    # A partir du dictionnaire de playlists Deezer, recherche chaque morceau de ces playlists sur Spotify
    # Pour chaque Song de chaque Playlist, lui attribue une liste de chansons associées trouvées sur Spotify (max 5)
    def check_playlists_on_spotify(self, dzr_playlists):
        if not self.spotify_handler :
            print("ERREUR : Pas de SpotifyHandler")
            return
        spotify_playlist_dict = self.spotify_handler.find_tracks_in_playlists(dzr_playlists)
        # self.set_progress_bar()
        # Exemple de résultat :
        # {'Rammstein':  [
        #                   [
        #                       ['5aNH8inF5BsbThDeOLs7zs', 'Feuer frei!', 'Rammstein', 'Mutter'],
        #                   ],
        #                   [
        #                       ['5awDvzxWfd53SSrsRZ8pXO', 'Du hast', 'Rammstein', 'Sehnsucht'],
        #                       ['277PM4ZassDkFkrzBwwkh0', 'Du Hast', 'Thy Art Is Murder', 'The Depression Sessions'],
        #                       ['4ltpEffX5XJa8kqH8bqWna', 'Du hast den schönsten Arsch der Welt', 'Alex C.', 'Euphorie'],
        #                   ]
        #                ]}

        for playlist in self.playlists_list:
            print(playlist.name)
            # self.progress_bar.setValue(int(self.progress_bar.value)+1)
            if playlist.name in spotify_playlist_dict:
                i = 0
                if len(spotify_playlist_dict[playlist.name]) != len(playlist.songs_list):
                    print("ERREUR : il n'y a pas autant de morceaux dans la liste provenant de Deezer (" + \
                          str(len(spotify_playlist_dict[playlist.name])) + ") et celle provenant de Spotify (" + \
                          str(len(playlist.songs_list)) + ")")
                    return
                for track_possibilities in spotify_playlist_dict[playlist.name]:
                    if not track_possibilities :
                        print('ERREUR : La liste des pistes associées trouvées sur Spotify était vide')
                        playlist.songs_list[i].set_album_ko()
                        playlist.songs_list[i].set_artist_ko()
                        playlist.songs_list[i].set_name_ko()
                        playlist.songs_list[i].add_associated_songs_button() #On ajoute le bouton quand même
                    elif len(track_possibilities) > 1:
                        print("Plus d'un résultat pour la chanson " + playlist.songs_list[i].name)
                        for j, track_possibility in enumerate(track_possibilities):
                            playlist.songs_list[i].add_associated_songs_button()
                            associated_song = playlist.songs_list[i].add_associated_sptfy_song(track_possibility)
                            # Si c'est la première chanson trouvée par Spotify, on considère que c'est la plus proche
                            # Donc on compare la chanson Deezer par rapport à celle-ci et pas aux autres
                            if j == 0:
                                associated_song.set_main_associated_song(True)
                                self.compute_song_state(playlist.songs_list[i], track_possibility)
                    else:
                        print("Une seule possibilité")
                        playlist.songs_list[i].add_associated_songs_button()
                        associated_song = playlist.songs_list[i].add_associated_sptfy_song(track_possibilities[0])
                        associated_song.set_main_associated_song(True)
                        playlist.songs_list[i].set_album_ok()
                        playlist.songs_list[i].set_artist_ok()
                        playlist.songs_list[i].set_name_ok()
                    i += 1
                    # self.progress_bar.setValue(int(self.progress_bar.value)+1)
                playlist.spotify_checked = True
        create_playlists_button = QtWidgets.QPushButton("Migrer les playlists sur Spotify")
        create_playlists_button.clicked.connect(self.create_sptfy_playlists)
        self.gridLayout.addWidget(create_playlists_button, 1, 3, 1, 1)

    def compute_song_state(self, main_song, track_possibility):
        if track_possibility[1].lower() == main_song.name.lower():
            main_song.set_name_ok()
        else:
            main_song.set_name_ko()
        if track_possibility[2].lower() == main_song.artist.lower():
            main_song.set_artist_ok()
        else:
            main_song.set_artist_ko()
        if track_possibility[3].lower() == main_song.album.lower():
            main_song.set_album_ok()
        else:
            main_song.set_album_ok()

    # Crée un SPotifyHandler avec les paramètres entrés par l'utilisateur
    def connect_to_spotify(self, client_id, client_secret, redirect_uri):
        print(client_id, client_secret, redirect_uri)
        self.spotify_handler = SpotifyHandler(client_id, client_secret, redirect_uri)
        print(self.spotify_handler.user_id)
        self.spotify_logger.close()

    # Ouvre le pop-up des chansons associées
    def show_associated_songs(self, song):
        self.sptfy_associated_songs_popup = SpotifyAssociatedSongs(song)
        for associated_song in self.sptfy_associated_songs_popup.songs_list :
            associated_song.on_btn_main_associated_song_clicked.connect(self.toggle_main_associated_song)
        self.sptfy_associated_songs_popup.show()

    # Gère les radio buttons permettant de définir quelle est la chanson associée principale
    def toggle_main_associated_song(self, song):
        for s in self.sptfy_associated_songs_popup.songs_list :
            s.set_main_associated_song(False)
        if song.is_main_associated_song :
            song.set_main_associated_song(False)
        else :
            song.set_main_associated_song(True)
            self.compute_song_state(song.parent_song, ["osef", song.name, song.artist, song.album])

    def create_sptfy_playlists(self):
        print("Création des playlists")
        for pl in self.playlists_list :
            print(pl.name)
            # if pl.name == 'Epica' :
            if pl.songs_list :
                songs_list_to_add = []
                # Création de la playlist (vide)
                playlist_id = self.spotify_handler.create_playlist(pl.name, "Playlist "+pl.name)
                for song in pl.songs_list :
                    for associated_song in song.associated_sptfy_songs :
                        if associated_song.is_main_associated_song :
                            # print(associated_song.name, associated_song.sptfy_URI)
                            songs_list_to_add.append(associated_song.sptfy_URI)
                # Ajout des morceaux à la playlist
                print(playlist_id)
                print(songs_list_to_add)
                self.spotify_handler.add_tracks_to_playlist(playlist_id, songs_list_to_add)
            else :
                print(pl.name, "vide")

    # Affiche la fenêtre de login à Deezer
    # Pour rappel, pour s'authentifier :
    # 		- Créer une app deezer (qui aura du coup un ID + un secret)
    # 		- Utiliser l'URL https://connect.deezer.com/oauth/auth.php?app_id=YOUR_APP_ID&redirect_uri=YOUR_REDIRECT_URI&perms=offline_access,email
    # 		- Cela redirige vers une URL possédant un "code=XXX", récupérer ce XXX
    # 		- Utiliser le code dans https://connect.deezer.com/oauth/access_token.php?app_id=YOU_APP_ID&secret=YOU_APP_SECRET&code=THE_CODE_FROM_ABOVE
    # 		- Cela fournit (dans le body de la page retournée) un access token
    # 		- Access token à passer en paramètre access_token
    def show_deezer_logger(self):
        self.deezer_logger = DeezerLogger()
        self.deezer_logger.show()
        # Connexion du bouton pour obtenir un code
        self.deezer_logger.btn_code.clicked.connect(
            lambda x: self.dzr_get_code(self.deezer_logger.dzr_app_id_wdgt.text(),
                                              self.deezer_logger.dzr_app_uri_wdgt.text()))

        # Connexion du bouton pour obtenir un access token
        self.deezer_logger.btn_access_token.clicked.connect(
            lambda x: self.dzr_get_access_token(self.deezer_logger.dzr_app_id_wdgt.text(),
                                                self.deezer_logger.dzr_app_secret_wdgt.text(),
                                                self.deezer_logger.dzr_code_wgdt.text()))

        # # Connexion du bouton pour générer un client deezer privé
        self.deezer_logger.btn_connection.clicked.connect(
            lambda x: self.connect_to_deezer(None,
                                             self.deezer_logger.dzr_app_id_wdgt.text(),
                                             self.deezer_logger.dzr_app_secret_wdgt.text(),
                                             self.deezer_logger.dzr_access_token_wdgt.text()))

    # Ouvre une page web permettant d'obtenir un code pour générer un access token (directement dans l'URL)
    def dzr_get_code(self, app_id, app_uri):
        print("Obtention d'un code pour l'authentification Deezer")
        base_url = "https://connect.deezer.com/oauth/auth.php"
        params = {}
        params["app_id"] = app_id
        params["redirect_uri"] = app_uri
        params["perms"] = "offline_access,email"
        try:
            webbrowser.open(base_url +"?app_id="+params["app_id"]+"&redirect_uri="+params["redirect_uri"]+"&perms="+params["perms"], new=2)
        except :
            print("Erreur d'accès à l'URL")

    # Ouvre une page web permettant d'obtenir un access token (directement dans le body de la page web)
    def dzr_get_access_token(self, app_id, app_secret, code):
        print("Obtention d'un access token pour l'authentification Deezer")
        base_url = "https://connect.deezer.com/oauth/access_token.php"
        params = {}
        params["app_id"] = app_id
        params["secret"] = app_secret
        params["code"] = code
        try:
            webbrowser.open(base_url+"?app_id="+params["app_id"]+"&secret="+params["secret"]+"&code="+params["code"], new=2)
        except :
            print("Erreur d'accès à l'URL")
