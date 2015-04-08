from __future__ import unicode_literals

import logging

from wimpy import Session

logger = logging.getLogger(__name__)

class WimpySession(object):
	
	def __init__(self):
		
		super(WimpySession, self).__init__()
		logger.info(u'Mopidy uses Wimp')
		self.api = Session()
		
		
	def login(self, username, password):
		self.api.login(username, password)
		
	def logout(self):
		pass
		
	def get_media_url(self, track_id):
		logger.info(u'Getting stream url')
		if self.api.check_login() == True:
			logger.debug(u'Logged in')
			url = self.api.get_media_url(track_id)
		else:
			logger(u'Logging in again')
			self.login(self.backend.config['wimpy']['username'], self.backend.config['wimpy']['password'])
			url = self.api.get_media_url(track_id)
		if not url.startswith('http://') and not url.startswith('https://'):
			host, app, playpath = url.split('/', 3)
			url = 'rtmp://%s app=%s playpath=%s' % (host, app, playpath)
		return url
		
	def get_all_playlists(self):
		logger.info(u'Wimpy trying to get playlists')
		return self.api.get_user_playlists(self.api.user.id)
	
	def get_all_tracks(self):
		tracks = []
		logger.info(u'Not tested yet')
		for playlist in self.api.get_user_playlists(self.api.user.id):
			for track in self.api.get_playlist_tracks(playlist.id):
				tracks.append(track)
				logger.debug(u'Fetched %s tracks so far' % len(tracks))
		logger.debug(u'Fetched %s tracks from wimp. And now i am done' % len(tracks))
		
		'''for track in self.api.get_playlist_tracks('ccba4c72-6aaf-43db-a46f-7f0cc579362d'):
			tracks.append(track)
		for track in self.api.get_playlist_tracks('0c84fe6a-4cf1-425a-9598-f09eb377738b'):
			tracks.append(track)
		for track in self.api.get_playlist_tracks('5d5b6916-3201-4293-ac8d-e204852c90f8'):
			tracks.append(track)
		for track in self.api.get_playlist_tracks('14cb2e61-bd41-4aab-a03a-33b2d9a65181'):
			tracks.append(track)
		for track in self.api.get_playlist_tracks('895a801a-eb62-4466-b811-6043c148fb98'):
			tracks.append(track)'''
		#return self.api.get_playlist_tracks('ccba4c72-6aaf-43db-a46f-7f0cc579362d')
		return tracks
	
	def get_album(self, album_id):
		if self.api.check_login() == True:
			logger.debug(u'Logged in')
			try:
				album = self.api.get_album(album_id)
				logger.debug(u'Got Album %s' % album)
			except:
				logger.debug(u'Error')
				return []
			return album
		else:
			logger(u'Logging in again')
			self.login(self.backend.config['wimpy']['username'], self.backend.config['wimpy']['password'])
			return self.api.get_album(album_id)
	def get_playlist(self, playlist_id):
		logger.debug(u'Getting playlist %s' % playlist_id)
		return self.api.get_playlist(playlist_id)
	
	def get_album_tracks(self, album_id):
		logger.debug(u'Getting tracks for album %s' % album_id)
		return self.api.get_album_tracks(album_id)
	
	def get_artist_top_tracks(self, artist):
		logger.debug(u'Getting top track of artist %s' % artist)
		return self.api.get_artist_top_tracks(artist)
	
	def get_featured(self):
		return self.api.get_featured()
	
	def get_featured_items(self, type, group):
		return self.api.get_featured_items(type, group)	
	
	def search(self, field, value):
		logger.debud(u'searching for %s in %s' % value, field)
		return self.api.search(field, value)
	
	def get_playlist_tracks(self, playlist_id):
		logger.info(u'Getting tracks for playlist %s' % playlist_id)
		return self.api.get_playlist_tracks(playlist_id)
		
	def get_favorite_tracks(self):
		logger.info(u'Wimpy getting favorite tracks')
		return self.api.get_favorite_tracks(self.api.user.id)
	
