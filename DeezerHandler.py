import deezer
from math import ceil

class DeezerHandler:

	def __init__(self, app_id=None, app_secret=None, access_token=None):
		self.private_client = None
		self.client = None
		self.public_client = None
		if app_id and app_secret and access_token :
			self.private_client = deezer.Client(app_id, app_secret, access_token)
			self.client = self.private_client
			self.public_client = deezer.Client()
		else:
			self.public_client = deezer.Client()
			self.client = self.public_client

	def get_user_name(self, user_id=None):
		# TODO: handle exception if user_id wrong
		if user_id :
			user = self.client.get_user(user_id)
		else :
			user = self.client.get_user()
		return user.name

	def get_playlists_from_user(self, user_id=None):
		if self.private_client:
			private_user = self.private_client.get_user()
			user_id = private_user.id
		public_user = self.public_client.get_user(user_id)

		if self.private_client:
			private_playlists = private_user.get_playlists()
		public_playlists = public_user.get_playlists()

		dzr_playlist_dict={}
		# Dictionnaire de la forme : { <NomPlaylist> : liste de [TitreMorceau, ArtisteDuMorceau, AlbumDuMorceau]}

		if self.private_client:
			dzr_playlist_dict = self.get_loved_tracks_as_dir(private_user)
			dzr_playlist_dict = self.get_playlist_as_dir(private_playlists, dzr_playlist_dict)
		dzr_playlist_dict = self.get_playlist_as_dir(public_playlists, dzr_playlist_dict)
		return dzr_playlist_dict

	def get_playlist_as_dir(self, input_playlists, output_dict):
		max = 10000000
		current = 0
		for playlist in input_playlists:
			track_list = []
			# L'API renvoie uniquement 25 morceaux par 25 morceaux, donc on les parcourt en incrémentant à chaque fois l'index de départ de 25
			print("Deezer - Getting playlist tracks...")
			for i in range(ceil(playlist.nb_tracks/25)):
				try:
					playlists_tracks = playlist.get_tracks(index=i*25)
				except:
					print("Deezer - API error?")
					return output_dict
				for track in playlists_tracks:
					track_list.append([track.title, track.artist.name, track.album.title])
					current += 1
					if current >= max:
						print("Deezer - Reaching too many songs in a variable, stopping here")
						break
				if current >= max:
					break
			output_dict[playlist.title] = track_list
		return output_dict

	def get_loved_tracks_as_dir(self, private_user):
		output_dict = {}
		tmp = private_user.get_tracks()
		result = [[track.title, track.artist.name, track.album.title] for track in tmp]
		i = 25
		while len(tmp)==25 :
			tmp = private_user.get_tracks(index=i)
			for track in tmp :
				result.append([track.title, track.artist.name, track.album.title])
			i+=25
		output_dict['Coups de coeur'] = result
		return output_dict
	
	def get_public_playlist(self, playlist_id):
		playlist = None
		try:
			playlist = self.client.get_playlist(playlist_id)
		except Exception as e:
			print('Couldn\'t retrieve playlist with id: ' + playlist_id)
		return playlist