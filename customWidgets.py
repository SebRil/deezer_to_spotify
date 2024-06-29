from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton, QMessageBox, QSizePolicy


class Song(QtWidgets.QWidget):

    on_btn_clicked = QtCore.pyqtSignal(QtWidgets.QWidget)
    on_btn_main_associated_song_clicked = QtCore.pyqtSignal(QtWidgets.QWidget)

    def __init__(self, name, artist, album, spotify_URI="", *args, **kwargs):
        super(Song, self).__init__(*args, **kwargs)
        self.name = name
        self.artist = artist
        self.album = album
        self.nameOk = False
        self.artistOk = False
        self.albumOk = False
        self.globalStateOk = False
        self.sptfy_songs = []
        self.sptfy_URI = spotify_URI
        self.widget_name = QtWidgets.QLabel(name)
        self.widget_artist = QtWidgets.QLabel(artist)
        self.widget_album = QtWidgets.QLabel(album)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.widget_name.setFont(font)
        # self.widget_name.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed))
        self.truncate_fields()
        self.set_min_max_size()
        grid_layout_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(grid_layout_widget)
        # self.layout.setContentsMargins(100,0,100,0)
        self.layout.setSpacing(5)
        # self.layout.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed))
        self.layout.addWidget(self.widget_name, 0, 1, 2, 1)
        self.layout.addWidget(self.widget_artist, 0, 2)
        self.layout.addWidget(self.widget_album, 1, 2)
        self.setLayout(self.layout)
        self.associated_sptfy_songs = []
        self.btn_associated_songs = QPushButton("Pistes Spotify")
        self.btn_associated_songs.clicked.connect(self.return_associated_songs)
        self.box_main_song = QtWidgets.QRadioButton()
        self.is_main_associated_song = False
        self.box_main_song.clicked.connect(self.btn_main_associated_song_clicked)
        self.parent_song = None

    def set_name_ok(self):
        self.nameOk = True
        self.compute_global_state()
        self.widget_name.setStyleSheet("background-color:green")

    def set_artist_ok(self):
        self.artistOk = True
        self.compute_global_state()
        self.widget_artist.setStyleSheet("background-color:green")

    def set_album_ok(self):
        self.albumOk = True
        self.compute_global_state()
        self.widget_album.setStyleSheet("background-color:green")

    def set_name_ko(self):
        self.nameOk = False
        self.compute_global_state()
        self.widget_name.setStyleSheet("background-color:red")

    def set_artist_ko(self):
        self.artistOk = False
        self.compute_global_state()
        self.widget_artist.setStyleSheet("background-color:red")

    def set_album_ko(self):
        self.albumOk = False
        self.compute_global_state()
        self.widget_album.setStyleSheet("background-color:red")

    def compute_global_state(self):
        if self.nameOk and self.artistOk and self.albumOk :
            self.globalStateOk = True
        else :
            self.globalStateOk = False

    def truncate_fields(self):
        if self.widget_name.sizeHint().width() > 250 :
            self.widget_name.setToolTip(self.name)
            self.widget_name.setText(self.name[:35]+"...")
        if self.widget_artist.sizeHint().width() > 250 :
            self.widget_artist.setToolTip(self.artist)
            self.widget_artist.setText(self.artist[:35]+"...")
        if self.widget_album.sizeHint().width() > 250 :
            self.widget_album.setToolTip(self.album)
            self.widget_album.setText(self.album[:35]+"...")

    def set_min_max_size(self):
        self.widget_name.setMinimumSize(QSize(250,16))
        self.widget_name.setMaximumSize(QSize(250,16))
        self.widget_artist.setMinimumSize(QSize(250,16))
        self.widget_artist.setMaximumSize(QSize(250,16))
        self.widget_album.setMinimumSize(QSize(250,16))
        self.widget_album.setMaximumSize(QSize(250,16))

    def add_associated_sptfy_song(self, sptfy_song):
        #Format d'une sptfy_song : [URI, nom, artiste, album]
        associated_song = Song(sptfy_song[1], sptfy_song[2], sptfy_song[3], sptfy_song[0])
        associated_song.add_main_song_box()
        associated_song.parent_song = self
        if associated_song.name.lower() == self.name.lower():
            print("Nom égal")
            associated_song.set_name_ok()
        else:
            print("Nom différent")
            associated_song.set_name_ko()
        if associated_song.artist.lower() == self.artist.lower():
            print("Artiste égal")
            associated_song.set_artist_ok()
        else:
            print("Artiste différent")
            associated_song.set_artist_ko()
        if associated_song.album.lower() == self.album.lower():
            print("Album égal")
            associated_song.set_album_ok()
        else:
            print("Album différent")
            associated_song.set_album_ok()
        self.associated_sptfy_songs.append(associated_song)
        return associated_song


    def add_associated_songs_button(self):
        if not self.associated_sptfy_songs :
            self.layout.addWidget(self.btn_associated_songs, 0, 3, 2, 1)

    def add_main_song_box(self):
        self.layout.addWidget(self.box_main_song, 0, 0, 2, 1)

    def return_associated_songs(self):
        self.on_btn_clicked.emit(self)

    def btn_main_associated_song_clicked(self):
        self.on_btn_main_associated_song_clicked.emit(self)

    def set_main_associated_song(self, main_bool):
        self.box_main_song.setChecked(main_bool)
        self.is_main_associated_song = main_bool

class Playlist(QtWidgets.QWidget):

    mouse_clicked_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, QtWidgets.QWidget)

    def __init__(self, name, *args, **kwargs):
        super(Playlist, self).__init__(*args, **kwargs)
        self.name = name
        self.songs_list = []
        self.selected = False
        self.global_state_ok = False
        self.spotify_checked = False
        self.widget_name = QtWidgets.QLabel(name)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.widget_name.setFont(font)
        grid_layout_widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(grid_layout_widget)
        # layout.setContentsMargins(10, 10, 10, 10)
        # layout.setSpacing(2)
        layout.addWidget(self.widget_name, 0, 0, 1, 1)
        self.setLayout(layout)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        #Création d'un event sur le clic (voir méthode eventFilter)
        self.installEventFilter(self)

    def add_song(self, name, artist, album):
        new_song = Song(name, artist, album)
        self.songs_list.append(new_song)

    # Renvoie un event lorsque l'objet Playlist est cliqué gauche
    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.mouse_clicked_signal.emit(event, watched)
        return super(Playlist, self).eventFilter(watched, event)

    def toggle_selected(self):
        if self.selected :
            self.set_unselected()
        else :
            self.set_selected()

    def set_unselected(self):
        self.selected = False
        self.setStyleSheet("")

    def set_selected(self):
        self.selected = True
        self.setStyleSheet("background-color:gray")

    def compute_global_state(self):
        for song in self.songs_list :
            if not song.globalStateOk :
                self.set_global_state_ko()
                break

    def set_global_state_ok(self):
        self.global_state_ok = True
        self.setStyleSheet("background-color:green")

    def set_global_state_ko(self):
        self.global_state_ok = False
        self.setStyleSheet("background-color:red")

    def find_song_by_name(self, track_name):
        print("Recherche de la chanson " + track_name)
        for song in self.songs_list :
            if song.name == track_name :
                return song
        else :
            return None

class SpotifyLogger(QtWidgets.QWidget):
    def __init__(self):
        super(SpotifyLogger, self).__init__()
        self.setWindowTitle("Connexion à Spotify")
        self.resize(400, 300)

        grid_layout_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QGridLayout(grid_layout_widget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.title = QtWidgets.QLabel("Connexion à Spotify")
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setMaximumSize(QSize(400, 35))
        font.setPointSize(12)
        self.lb_client_id = QtWidgets.QLabel("Spotify Client ID")
        self.lb_client_id.setFont(font)
        self.lb_client_secret = QtWidgets.QLabel("Spotify Client Secret")
        self.lb_client_secret.setFont(font)
        self.lb_redirect_uri = QtWidgets.QLabel("Spotify Redirect URI")
        self.lb_redirect_uri.setFont(font)
        self.sptfy_client_id = QtWidgets.QLineEdit()
        self.sptfy_client_id.setText("29f0d515bedc41a9922e0bdb002d3156") #DAph : 6faf534ef9a945a0bb2edbfdbd0f3724
        self.sptfy_client_secret = QtWidgets.QLineEdit()
        self.sptfy_client_secret.setText("25acc9c6e17b4b1dac8fb29bd58dae32") #Daph : d4c07ec3e1a546c28934b87d8d30c9a3
        self.sptfy_redirect_uri = QtWidgets.QLineEdit()
        self.sptfy_redirect_uri.setText("http://localhost") #Daph : https://migration.com
        self.btn_connection = QPushButton("Connexion")
        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.clicked.connect(self.close)
        self.layout.addWidget(self.title, 0, 0, 1, 3)
        self.layout.addWidget(self.lb_client_id, 1, 0, 1, 1)
        self.layout.addWidget(self.sptfy_client_id, 1, 1, 1, 1)
        self.layout.addWidget(self.lb_client_secret, 2, 0, 1, 1)
        self.layout.addWidget(self.sptfy_client_secret, 2, 1, 1, 1)
        self.layout.addWidget(self.lb_redirect_uri, 3, 0, 1, 1)
        self.layout.addWidget(self.sptfy_redirect_uri, 3, 1, 1, 1)
        self.layout.addWidget(self.btn_connection, 4, 0, 1, 1)
        self.layout.addWidget(self.btn_cancel, 4, 1, 1, 1)
        self.setLayout(self.layout)

class SpotifyAssociatedSongs(QtWidgets.QWidget):
    def __init__(self, song):
        super(SpotifyAssociatedSongs, self).__init__()
        # self.setParent = parent
        self.setWindowTitle("Chansons trouvées sur Spotify associées à la chanson '" + song.name + "'")
        self.songs_list = song.associated_sptfy_songs
        if self.songs_list:
            height = len(self.songs_list) * 60 + 20
        else :
            height = 50
        self.resize(600, height)

        grid_layout_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QGridLayout(grid_layout_widget)
        if self.songs_list :
            for i, song in enumerate(self.songs_list) :
                self.layout.addWidget(song, i, 0, 1, 1)
        else :
            label = QtWidgets.QLabel("Aucun morceau correspondant n'a été trouvé sur Spotify.")
            self.layout.addWidget(label,0,0,1,1)

class DeezerLogger(QtWidgets.QWidget):
    def __init__(self):
        super(DeezerLogger, self).__init__()
        self.setWindowTitle("Connexion à Deezer")
        self.resize(400, 600)

        grid_layout_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QGridLayout(grid_layout_widget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.title = QtWidgets.QLabel("Connexion à Deezer")
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setMaximumSize(QSize(400, 35))
        font.setPointSize(12)
        self.lb_dzr_app_id = QtWidgets.QLabel("Application ID")
        self.lb_dzr_app_id.setFont(font)
        self.dzr_app_id_wdgt = QtWidgets.QLineEdit()
        self.dzr_app_id_wdgt.setText("536882")  #Daph : 552702
        self.lb_dzr_app_uri = QtWidgets.QLabel("Application URI")
        self.lb_dzr_app_uri.setFont(font)
        self.dzr_app_uri_wdgt = QtWidgets.QLineEdit()
        self.dzr_app_uri_wdgt.setText("http://example.com")
        self.lb_dzr_app_secret = QtWidgets.QLabel("Application Secret")
        self.lb_dzr_app_secret.setFont(font)
        self.dzr_app_secret_wdgt = QtWidgets.QLineEdit()
        self.dzr_app_secret_wdgt.setText("0e7dc879aeb23ab446a91cc3ce6e97dc") #Daph : 010544c06a6d5a04010c5ee73094b74c
        self.btn_code = QPushButton("Obtenir un code")

        self.lb_code = QtWidgets.QLabel("Code (optionnel)")
        self.lb_code.setFont(font)
        self.dzr_code_wgdt = QtWidgets.QLineEdit()
        self.btn_access_token = QPushButton("Obtenir un access token")

        self.lb_access_token = QtWidgets.QLabel("Access token")
        self.lb_access_token.setFont(font)
        self.dzr_access_token_wdgt = QtWidgets.QLineEdit()
        self.dzr_access_token_wdgt.setText("frJj9TDJqsjVhJ4oZ2TodZ0VRzZjjtBe0oZxTwQsgH4tWAClHC") #Daph : frMduRUJ3idoCtqALjDpMpwBCNsFA3OO66F6ArPGjzUztuAQ5q

        self.btn_connection = QPushButton("Se connecter")

        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.clicked.connect(self.close)
        self.layout.addWidget(self.title, 0, 0, 1, 3)
        self.layout.addWidget(self.lb_dzr_app_id, 1, 0, 1, 1)
        self.layout.addWidget(self.dzr_app_id_wdgt, 1, 1, 1, 1)
        self.layout.addWidget(self.lb_dzr_app_uri, 2, 0, 1, 1)
        self.layout.addWidget(self.dzr_app_uri_wdgt, 2, 1, 1, 1)
        self.layout.addWidget(self.lb_dzr_app_secret, 3, 0, 1, 1)
        self.layout.addWidget(self.dzr_app_secret_wdgt, 3, 1, 1, 1)
        self.layout.addWidget(self.btn_code, 4, 1, 1, 1)

        self.layout.addWidget(self.lb_code, 5, 0, 1, 1)
        self.layout.addWidget(self.dzr_code_wgdt, 5, 1, 1, 1)
        self.layout.addWidget(self.btn_access_token, 6, 1, 1, 1)

        self.layout.addWidget(self.lb_access_token, 7, 0, 1, 1)
        self.layout.addWidget(self.dzr_access_token_wdgt, 7, 1, 1, 1)
        self.layout.addWidget(self.btn_connection, 8, 1, 1, 1)

        self.layout.addWidget(self.btn_cancel, 9, 0, 1, 2)
        self.setLayout(self.layout)

class PlaylistsLog(QtWidgets.QWidget):
    def __init__(self):
        super(PlaylistsLog, self).__init__()
        self.setWindowTitle("Suivi des opérations")
        self.resize(400, 600)

        grid_layout_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QGridLayout(grid_layout_widget)