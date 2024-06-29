import deezer
from math import ceil

class DeezerHandler:

	def __init__(self, app_id=None, app_secret=None, access_token=None):
		self.private_client = None
		self.client = None
		self.public_client = None
		if app_id and app_secret and access_token :
			print("Création d'un client Deezer privé (avec application)")
			self.private_client = deezer.Client(app_id, app_secret, access_token)
			self.client = self.private_client
			self.public_client = deezer.Client()
		else:
			print("Création d'un client Deezer publique (sans application)")
			self.public_client = deezer.Client()
			print("Client Deezer créé")
			self.client = self.public_client

	def get_user_name(self, user_id=None):
		if user_id :
			user = self.client.get_user(user_id)
		else :
			user = self.client.get_user()
		return user.name

	def get_playlists_from_user(self, user_id=None):
		print("Getting playlists")
		if self.private_client:
			print("Getting playlists private client")
			private_user = self.private_client.get_user() #2328033 pour daph
			user_id = private_user.id
		print("Getting public user")
		public_user = self.public_client.get_user(user_id)  # 2328033 pour daph

		if self.private_client:
			private_playlists = private_user.get_playlists()
		print("Getting public playlists")
		public_playlists = public_user.get_playlists()

		# print(playlists)

		dzr_playlist_dict={}
		# Dictionnaire de la forme : { <NomPlaylist> : liste de [TitreMorceau, ArtisteDuMorceau, AlbumDuMorceau]}

		if self.private_client:
			dzr_playlist_dict = self.get_loved_tracks_as_dir(private_user)
			dzr_playlist_dict = self.get_playlist_as_dir(private_playlists, dzr_playlist_dict)
		print("Setting playlist dict")
		dzr_playlist_dict = self.get_playlist_as_dir(public_playlists, dzr_playlist_dict)
		print("Printing playlist dict")
		print(dzr_playlist_dict)
		return dzr_playlist_dict

	def get_playlist_as_dir(self, input_playlists, output_dict):
		print("Setting playlist dict 2")
		max = 75
		current = 0
		for playlist in input_playlists:
			print(playlist)
			track_list = []
			# L'API renvoie uniquement 25 morceaux par 25 morceaux, donc on les parcourt en incrémentant à chaque fois l'index de départ de 25
			for i in range(ceil(playlist.nb_tracks/25)):
				try:
					print("Getting playlist tracks...")
					playlists_tracks = playlist.get_tracks(index=i*25)
				except:
					print("API error?")
					return output_dict
				for track in playlists_tracks:
					print("ajout de: " + track.title)
					track_list.append([track.title, track.artist.name, track.album.title])
					print("Ajouté!")
					current += 1
					if current >= max:
						print("Reaching too many songs in a variable, stopping here")
						break
				if current >= max:
					break
			print("Adding playlist to dict")
			output_dict[playlist.title] = track_list
		print("Returning playlist dict")
		return output_dict

	def get_loved_tracks_as_dir(self, private_user):
		output_dict = {}
		tmp = private_user.get_tracks()
		print(tmp)
		result = [[track.title, track.artist.name, track.album.title] for track in tmp]
		i = 25
		while len(tmp)==25 :
			tmp = private_user.get_tracks(index=i)
			print(tmp)
			for track in tmp :
				result.append([track.title, track.artist.name, track.album.title])
			i+=25
		output_dict['Coups de coeur'] = result
		return output_dict